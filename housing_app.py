import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.datasets import fetch_california_housing

st.title("California Housing Data (1990) by [你的名字]")

# 加载数据
@st.cache_data
def load_data():
    housing = fetch_california_housing()
    data = pd.DataFrame(housing.data, columns=housing.feature_names)
    data['MedHouseVal'] = housing.target * 100000  # 转换为实际价格
    return data

df = load_data()

# 侧边栏筛选器
st.sidebar.header("筛选条件")

# 价格滑块
min_price = st.sidebar.slider(
    "最低房价",
    min_value=int(df['MedHouseVal'].min()),
    max_value=int(df['MedHouseVal'].max()),
    value=int(df['MedHouseVal'].min())
)

# 收入水平单选按钮
income_level = st.sidebar.radio(
    "收入水平",
    ["全部", "Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (≥4.5)"]
)

# 根据收入水平筛选
filtered_df = df[df['MedHouseVal'] >= min_price]

if income_level == "Low (≤2.5)":
    filtered_df = filtered_df[filtered_df['MedInc'] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_df = filtered_df[(filtered_df['MedInc'] > 2.5) & (filtered_df['MedInc'] < 4.5)]
elif income_level == "High (≥4.5)":
    filtered_df = filtered_df[filtered_df['MedInc'] >= 4.5]

# 显示统计数据
st.write(f"显示 {len(filtered_df)} 条记录")

# 显示地图
st.subheader("住房地理位置分布")
st.map(filtered_df[['Latitude', 'Longitude']])

# 显示直方图 - 使用 Plotly 而不是 matplotlib
st.subheader("房价分布直方图")
fig = px.histogram(filtered_df, x='MedHouseVal', nbins=30, 
                   title="Median House Value Distribution")
st.plotly_chart(fig)

# 显示数据表格
st.subheader("筛选后的数据")
st.dataframe(filtered_df.head())