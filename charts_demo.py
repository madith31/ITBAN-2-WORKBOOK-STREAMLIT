import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

st.title("Sales Data Visualization")

# Sample dataset
data = {
    "Product": ["Laptop", "Tablet", "Phone", "Monitor", "Printer"],
    "Sales_Q1": [150, 200, 300, 100, 80],
    "Sales_Q2": [180, 220, 330, 120, 90]
}

df = pd.DataFrame(data)

# Bar chart using Matplotlib
st.subheader("Bar Chart - Sales Q1")
fig, ax = plt.subplots()
ax.bar(df["Product"], df["Sales_Q1"], color='skyblue')
ax.set_xlabel("Product")
ax.set_ylabel("Units Sold")
st.pyplot(fig)

# Line chart using Altair
st.subheader("Line Chart - Sales Q2")
chart = alt.Chart(df).mark_line(point=True).encode(
    x="Product",
    y="Sales_Q2"
).properties(title="Sales in Q2")
st.altair_chart(chart, use_container_width=True)

# Area chart using Streamlit
st.subheader("Area Chart - Combined Sales")
df["Total_Sales"] = df["Sales_Q1"] + df["Sales_Q2"]
st.area_chart(df.set_index("Product")[["Total_Sales"]])