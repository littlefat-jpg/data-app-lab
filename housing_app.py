import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing Data (1990)")

def load_housing_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_housing_data()

st.title("California Housing Data (1990) by FortuiTy Liu")
st.caption("See more filters in the sidebar:")

with st.sidebar:
    st.header("Filter Options")
    
    price_range = st.slider(
        "Minimal Median House Price",
        min_value=0,
        max_value=500001,
        value=200000,
        step=1000
    )
    
    location_types = st.multiselect(
        "Select Location Type",
        options=df["ocean_proximity"].unique(),
        default=df["ocean_proximity"].unique() 
    )
    
    income_level = st.radio(
        "Select Income Level (median_income)",
        options=["Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (>4.5)"],
        index=1
    )

filtered_df = df[df["median_house_value"] >= price_range]

filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(location_types)]

if income_level == "Low (≤2.5)":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
else:
    filtered_df = filtered_df[filtered_df["median_income"] > 4.5]

st.subheader("Housing Distribution Map")
st.map(
    filtered_df,
    latitude="latitude",
    longitude="longitude",
    size=80,  
    use_container_width=True
)

st.subheader("Histogram of Median House Value")
fig, ax = plt.subplots()
ax.hist(filtered_df["median_house_value"], bins=30)
ax.set_xlabel("Median House Value")
ax.set_ylabel("Count")
st.pyplot(fig)