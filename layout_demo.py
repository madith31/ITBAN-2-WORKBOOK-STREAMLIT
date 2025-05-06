import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page config
st.set_page_config(layout="wide")
st.title("Data Warehousing Dashboard")

# Load the dataset
df = pd.read_csv("boston.csv")

# Sidebar
st.sidebar.header("Filter Options")
dataset_option = st.sidebar.selectbox("Choose a Dataset", ["Sales", "Inventory", "Customers"])
show_details = st.sidebar.checkbox("Show Additional Details")

# Columns layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Column 1: Overview")
    st.write("Boston Housing Dataset Overview")
    st.write(df.describe())

with col2:
    st.subheader("Column 2: Detailed View")
    if show_details:
        st.write("Showing first 10 rows:")
        st.dataframe(df.head(10))
    else:
        st.write("Check 'Show Additional Details' in the sidebar to see more.")

# Expander section
with st.expander("View Summary"):
    st.write("This dataset contains information collected by the U.S Census Service concerning housing in the area of Boston, Massachusetts.")

# Tabs
tab1, tab2 = st.tabs(["Chart View", "Table View"])

with tab1:
    st.write("Average House Price by Number of Rooms")
    fig, ax = plt.subplots()
    df.groupby("RM")["MEDV"].mean().plot(kind="bar", ax=ax)
    ax.set_xlabel("Average Number of Rooms (RM)")
    ax.set_ylabel("Median Value (MEDV)")
    st.pyplot(fig)

with tab2:
    st.write("Complete Dataset")
    st.dataframe(df)