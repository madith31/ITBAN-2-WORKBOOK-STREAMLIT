import streamlit as st

# Title and Headers
st.title("Hello, Streamlit!")
st.header("Welcome to Your First Streamlit App")
st.write("This is a simple Streamlit application to demonstrate the basics.")

# Input fields
name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0)

# Display output
if name:
    st.write(f"Hello, {name}! You are {int(age)} years old.")