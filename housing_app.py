import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(page_title="California Housing Data", layout="wide")

# Load the data
@st.cache_data
def load_data():
    # Replace with your actual file path
    df = pd.read_csv('housing.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Location type filter (ocean proximity)
location_types = df['ocean_proximity'].unique()
selected_locations = st.sidebar.multiselect(
    "Select Location Type(s):",
    options=location_types,
    default=location_types
)

# Income level filter
income_level = st.sidebar.radio(
    "Select Income Level:",
    options=["Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (≥4.5)"]
)

# Apply location filter
filtered_df = df[df['ocean_proximity'].isin(selected_locations)]

# Apply income filter
if income_level == "Low (≤2.5)":
    filtered_df = filtered_df[filtered_df['median_income'] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_df = filtered_df[(filtered_df['median_income'] > 2.5) & (filtered_df['median_income'] < 4.5)]
else:  # High
    filtered_df = filtered_df[filtered_df['median_income'] >= 4.5]

# Main content
st.title("California Housing Data (1990) by Your Name")  # Replace with your name

# Price slider
min_price = int(df['median_house_value'].min())
max_price = int(df['median_house_value'].max())

price_range = st.slider(
    "Select Price Range:",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Apply price filter
price_filtered_df = filtered_df[
    (filtered_df['median_house_value'] >= price_range[0]) & 
    (filtered_df['median_house_value'] <= price_range[1])
]

# Display map
st.subheader("Housing Distribution Map")
st.map(price_filtered_df[['latitude', 'longitude']].dropna())

# Display histogram
st.subheader("Median House Value Distribution")
fig, ax = plt.subplots()
ax.hist(price_filtered_df['median_house_value'], bins=30, alpha=0.7, color='skyblue')
ax.set_xlabel('Median House Value')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of Median House Values')
st.pyplot(fig)

# Display dataset info
st.sidebar.header("Dataset Info")
st.sidebar.write(f"Original dataset size: {len(df)}")
st.sidebar.write(f"Filtered dataset size: {len(price_filtered_df)}")

# Show raw data option
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(price_filtered_df)


