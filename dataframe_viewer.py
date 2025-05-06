import streamlit as st
import pandas as pd
st.title("DataFrame Viewer")

# upload csv
uploaded_file=st.file_uploader("Upload your CSV file", type=["csv"])


if uploaded_file:
    df=pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")

    #checkbox to toggle raw data
    if st.checkbox("Show raw data"): 
        st.dataframe(df)
    
    #Select column filter
    column_to_filter=st.selectbox ("Select a column to filter by", df.columns)

    #get unique from seleted column
    unique_values =df[column_to_filter].unique()
    filter_value=st.selectbox("Select a value", unique_values)

    #filter and show result
    filtered_df=df[df[column_to_filter]==filter_value]
    st.subheader("Filtered Data")
    st.dataframe(filtered_df)

    