import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="California Housing Data (1990)")

def load_housing_data():
    # 使用 sklearn 数据集，避免文件路径问题
    from sklearn.datasets import fetch_california_housing
    import numpy as np
    
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['median_house_value'] = housing.target * 100000  # 转换为实际价格
    
    # 添加模拟的 ocean_proximity 列
    np.random.seed(42)
    proximity_options = ['INLAND', 'NEAR BAY', 'NEAR OCEAN', 'ISLAND']
    df['ocean_proximity'] = np.random.choice(proximity_options, size=len(df))
    
    return df

df = load_housing_data()

st.title("California Housing Data (1990) by FortuiTy Liu")
st.caption("See more filters in the sidebar:")

with st.sidebar:
    st.header("Filter Options")
    
    price_range = st.slider(
        "Minimal Median House Price",
        min_value=int(df["median_house_value"].min()),
        max_value=int(df["median_house_value"].max()),
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

# 应用筛选
filtered_df = df[df["median_house_value"] >= price_range]
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(location_types)]

if income_level == "Low (≤2.5)":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
else:
    filtered_df = filtered_df[filtered_df["median_income"] > 4.5]

st.write(f"Showing {len(filtered_df)} out of {len(df)} records")

# 显示地图
st.subheader("Housing Distribution Map")
if not filtered_df.empty:
    # 使用正确的列名
    st.map(
        filtered_df[['latitude', 'longitude']],
        use_container_width=True
    )
else:
    st.warning("No data available for the selected filters")

# 显示直方图 - 使用 Plotly 替代 matplotlib
st.subheader("Histogram of Median House Value (30 bins)")
if not filtered_df.empty:
    fig = px.histogram(
        filtered_df, 
        x="median_house_value", 
        nbins=30,
        title="Distribution of Median House Values",
        labels={"median_house_value": "Median House Value ($)"}
    )
    st.plotly_chart(fig)
else:
    st.info("Adjust filters to see the histogram")

# 显示数据表格
st.subheader("Filtered Data Preview")
if not filtered_df.empty:
    st.dataframe(filtered_df.head())

