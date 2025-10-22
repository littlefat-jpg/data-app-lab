import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.datasets import fetch_california_housing

# 设置页面标题
st.title("🏠 California Housing Data (1990) by Luyiran]")

# 加载数据
@st.cache_data
def load_data():
    housing = fetch_california_housing()
    data = pd.DataFrame(housing.data, columns=housing.feature_names)
    data['MedHouseVal'] = housing.target * 100000
    data['Latitude'] = housing.data[:, 6]
    data['Longitude'] = housing.data[:, 7]
    return data

df = load_data()

# 侧边栏
st.sidebar.header("🔧 筛选条件")

# 价格滑块
min_price = st.sidebar.slider(
    "💰 最低中位房价",
    min_value=int(df['MedHouseVal'].min()),
    max_value=int(df['MedHouseVal'].max()),
    value=int(df['MedHouseVal'].min()),
    step=10000
)

# 收入水平筛选
income_level = st.sidebar.radio(
    "📊 收入水平",
    ["全部", "低收入 (≤2.5)", "中等收入 (2.5-4.5)", "高收入 (≥4.5)"]
)

# 应用筛选
filtered_df = df[df['MedHouseVal'] >= min_price]

if income_level == "低收入 (≤2.5)":
    filtered_df = filtered_df[filtered_df['MedInc'] <= 2.5]
elif income_level == "中等收入 (2.5-4.5)":
    filtered_df = filtered_df[(filtered_df['MedInc'] > 2.5) & (filtered_df['MedInc'] < 4.5)]
elif income_level == "高收入 (≥4.5)":
    filtered_df = filtered_df[filtered_df['MedInc'] >= 4.5]

# 显示统计信息
st.write(f"📈 显示 {len(filtered_df)} 条记录（总共 {len(df)} 条）")

# 显示地图
st.subheader("🗺️ 住房地理位置分布")
if not filtered_df.empty:
    st.map(filtered_df[['Latitude', 'Longitude']].dropna())
else:
    st.warning("没有数据满足筛选条件")

# 显示直方图
st.subheader("📊 房价分布直方图")
if not filtered_df.empty:
    fig = px.histogram(
        filtered_df, 
        x='MedHouseVal', 
        nbins=30,
        title="中位房价分布",
        labels={'MedHouseVal': '中位房价 ($)'}
    )
    st.plotly_chart(fig)
else:
    st.warning("没有数据可显示直方图")

# 显示数据表格
st.subheader("📋 数据预览")
if not filtered_df.empty:
    st.dataframe(filtered_df.head(10))
else:
    st.info("请调整筛选条件以查看数据")
