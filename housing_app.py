
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

# Load the dataset
@st.cache
def load_data():
    url = "https://www.notion.so/signed/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F32779d0f-1d01-4d8f-ba13-c4cfe1a44008%2Fhousing.csv.zip?table=block&id=fdc2e585-eae0-4b5a-bb67-7a7aa7d2cb6b&spaceId=a5a7c10a-dc11-4700-a4d1-3b917c278921&userId=223d872b-594c-819b-8646-000218778f88&cache=v2"
    # You should download and unzip the data manually or use the provided URL to load it directly
    data = pd.read_csv('housing.csv')  # Adjust if necessary based on the real file path
    return data

# Create the sidebar widgets
def filter_widgets(data):
    # Multiselect for location
    locations = st.sidebar.multiselect("Select Location Types", options=data['location'].unique())

    # Radio button for income level
    income_level = st.sidebar.radio("Filter by Income Level", options=["Low", "Medium", "High"])

    return locations, income_level

# Price slider widget
def price_slider(data):
    min_price = int(data['median_house_value'].min())
    max_price = int(data['median_house_value'].max())
    price = st.slider("Select Price Range", min_price, max_price, (min_price, max_price))
    return price

def plot_map(data):
    # Use Plotly for the map visualization
    fig = px.scatter_geo(data, lat='latitude', lon='longitude', color='median_house_value', 
                         hover_name="location", size="median_house_value", projection="natural earth")
    st.plotly_chart(fig)

def plot_histogram(data):
    fig, ax = plt.subplots()
    ax.hist(data['median_house_value'], bins=30, color='skyblue', edgecolor='black')
    ax.set_title('Median House Value Distribution')
    ax.set_xlabel('House Value')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def main():
    # Load the data
    data = load_data()

    # Widgets
    locations, income_level = filter_widgets(data)
    price = price_slider(data)

    # Filter the data
    if locations:
        data = data[data['location'].isin(locations)]
    if income_level == "Low":
        data = data[data['income'] <= 2.5]
    elif income_level == "Medium":
        data = data[(data['income'] > 2.5) & (data['income'] < 4.5)]
    else:
        data = data[data['income'] >= 4.5]
    
    # Filter by price
    data = data[(data['median_house_value'] >= price[0]) & (data['median_house_value'] <= price[1])]

    # Display results
    st.title("Housing Data App")
    plot_map(data)
    plot_histogram(data)

if __name__ == "__main__":
    main()
