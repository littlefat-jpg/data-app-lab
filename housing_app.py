import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置页面配置
st.set_page_config(
    page_title="California Housing Data",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题和说明
st.title("🏠 California Housing Data (1990)")
st.markdown("**Explore housing data with interactive filters**")

# 加载数据
@st.cache_data
def load_data():
    try:
        # 尝试读取真实的 housing.csv 文件
        data = pd.read_csv('housing.csv')
        return data
    except FileNotFoundError:
        # 如果文件不存在，创建示例数据
        st.info("Using sample data. To use real data, please add 'housing.csv' to your project folder.")
        np.random.seed(42)
        n_points = 1000
        
        # 创建更真实的数据
        data = pd.DataFrame({
            'longitude': np.random.uniform(-124.3, -114.3, n_points),
            'latitude': np.random.uniform(32.5, 42.0, n_points),
            'median_house_value': np.random.randint(50000, 500001, n_points),
            'median_income': np.random.uniform(0.5, 15.0, n_points),
            'ocean_proximity': np.random.choice(
                ['INLAND', 'NEAR BAY', 'NEAR OCEAN', '<1H OCEAN', 'ISLAND'], 
                n_points,
                p=[0.5, 0.2, 0.15, 0.14, 0.01]
            ),
            'housing_median_age': np.random.randint(1, 52, n_points),
            'total_rooms': np.random.randint(2, 40000, n_points),
            'total_bedrooms': np.random.randint(1, 6500, n_points),
            'population': np.random.randint(3, 15000, n_points),
            'households': np.random.randint(1, 5000, n_points)
        })
        return data

# 加载数据
housing_data = load_data()

# 侧边栏 - 过滤器
st.sidebar.header("🔧 Filters")

# 价格范围滑块
st.sidebar.subheader("💰 Price Range")
min_price, max_price = st.sidebar.slider(
    "Select price range:",
    min_value=int(housing_data['median_house_value'].min()),
    max_value=int(housing_data['median_house_value'].max()),
    value=(int(housing_data['median_house_value'].min()), 
           int(housing_data['median_house_value'].max())),
    step=10000
)

# 位置类型多选
st.sidebar.subheader("📍 Location Type")
location_types = st.sidebar.multiselect(
    "Select ocean proximity:",
    options=sorted(housing_data['ocean_proximity'].unique()),
    default=sorted(housing_data['ocean_proximity'].unique())
)

# 收入水平单选按钮
st.sidebar.subheader("💵 Income Level")
income_level = st.sidebar.radio(
    "Select income category:",
    options=["All", "Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (≥4.5)"],
    index=0
)

# 房屋年龄筛选
st.sidebar.subheader("🏚️ House Age")
house_age = st.sidebar.slider(
    "Minimum house age:",
    min_value=int(housing_data['housing_median_age'].min()),
    max_value=int(housing_data['housing_median_age'].max()),
    value=int(housing_data['housing_median_age'].min())
)

# 应用过滤器
filtered_data = housing_data.copy()

# 价格筛选
filtered_data = filtered_data[
    (filtered_data['median_house_value'] >= min_price) & 
    (filtered_data['median_house_value'] <= max_price)
]

# 位置类型筛选
if location_types:
    filtered_data = filtered_data[filtered_data['ocean_proximity'].isin(location_types)]

# 收入水平筛选
if income_level == "Low (≤2.5)":
    filtered_data = filtered_data[filtered_data['median_income'] <= 2.5]
elif income_level == "Medium (>2.5 & <4.5)":
    filtered_data = filtered_data[(filtered_data['median_income'] > 2.5) & 
                                 (filtered_data['median_income'] < 4.5)]
elif income_level == "High (≥4.5)":
    filtered_data = filtered_data[filtered_data['median_income'] >= 4.5]

# 房屋年龄筛选
filtered_data = filtered_data[filtered_data['housing_median_age'] >= house_age]

# 主内容区域
# 数据显示
st.header("📊 Data Overview")

# 创建指标卡片
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(filtered_data))
    
with col2:
    st.metric("Average Price", f"${filtered_data['median_house_value'].mean():,.0f}")
    
with col3:
    st.metric("Average Income", f"${filtered_data['median_income'].mean():.2f}")
    
with col4:
    st.metric("Average House Age", f"{filtered_data['housing_median_age'].mean():.1f} years")

st.write(f"**Displaying {len(filtered_data)} out of {len(housing_data)} records**")

# 地图和直方图
st.header("🗺️ Geographic Distribution")

col_map, col_stats = st.columns([2, 1])

with col_map:
    # 显示地图
    if not filtered_data.empty:
        # 添加颜色编码基于房价
        filtered_data['price_color'] = filtered_data['median_house_value'] / filtered_data['median_house_value'].max()
        
        st.map(filtered_data[['latitude', 'longitude']], 
               size=50, 
               color='#FF6B6B')
    else:
        st.warning("No data to display with current filters")

with col_stats:
    st.subheader("📈 Quick Stats")
    if not filtered_data.empty:
        st.write(f"**Price Range:** ${filtered_data['median_house_value'].min():,} - ${filtered_data['median_house_value'].max():,}")
        st.write(f"**Income Range:** ${filtered_data['median_income'].min():.2f} - ${filtered_data['median_income'].max():.2f}")
        st.write(f"**Top Location:** {filtered_data['ocean_proximity'].mode().iloc[0] if not filtered_data['ocean_proximity'].mode().empty else 'N/A'}")

# 直方图部分
st.header("📊 Distribution Analysis")

# 选择要可视化的字段
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("House Value Distribution")
    if not filtered_data.empty:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        ax1.hist(filtered_data['median_house_value'], bins=30, color='#4ECDC4', 
                edgecolor='black', alpha=0.7)
        ax1.set_xlabel('Median House Value ($)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of Median House Values')
        ax1.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig1)
    else:
        st.warning("No data available for histogram")

with chart_col2:
    st.subheader("Income Distribution")
    if not filtered_data.empty:
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.hist(filtered_data['median_income'], bins=30, color='#FF6B6B', 
                edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Median Income')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Median Income')
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig2)

# 原始数据表格
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_data.reset_index(drop=True), use_container_width=True)
    
    # 数据下载按钮
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_california_housing.csv",
        mime="text/csv"
    )

# 页脚
st.markdown("---")
st.markdown("### 🏠 California Housing Data (1990) by [Your Name]")
st.markdown("*Data visualization app built with Streamlit*")

# 侧边栏信息
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    "This app visualizes California housing data from 1990. "
    "Use the filters to explore different segments of the market."
)