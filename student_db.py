import streamlit as st
import sqlite3
import pandas as pd
import hashlib

# --------------------- AUTH FUNCTIONS ---------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    return c.fetchone()

def create_user_table():
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# --------------------- DATABASE CONNECTION ---------------------
conn = sqlite3.connect("sample_data.db", check_same_thread=False)
c = conn.cursor()

# Create necessary tables
create_user_table()
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        year_level INTEGER
    )
''')
conn.commit()

# --------------------- AUTHENTICATION UI ---------------------
st.title("Student Database Management with Login")

auth_menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", auth_menu)

if choice == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account created successfully! Go to Login.")
        else:
            st.error("Username already exists!")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = check_credentials(username, password)
        if user:
            st.success(f"Welcome {username}!")

            # --------------------- MAIN APP ---------------------
            # Input form to add a student
            with st.form("student_form"):
                name = st.text_input("Student Name")
                course = st.text_input("Course")
                year_level = st.number_input("Year Level", min_value=1, max_value=5, step=1)
                submitted = st.form_submit_button("Add Student")

                if submitted:
                    c.execute("INSERT INTO students (name, course, year_level) VALUES (?, ?, ?)",
                              (name, course, year_level))
                    conn.commit()
                    st.success("Student added successfully!")

            # View data
            st.subheader("Student Records")
            students_df = pd.read_sql_query("SELECT * FROM students", conn)
            st.dataframe(students_df)

            # Option to delete student
            delete_student_id = st.selectbox("Select Student ID to Delete", students_df["id"])

            if st.button("Delete Student"):
                if delete_student_id:
                    c.execute("DELETE FROM students WHERE id=?", (delete_student_id,))
                    conn.commit()
                    st.success(f"Student with ID {delete_student_id} deleted successfully!")

        else:
            st.error("Invalid credentials")

# --------------------- CLOSE CONNECTION ---------------------
# (Optional: connection can remain open during session)
# conn.close()
