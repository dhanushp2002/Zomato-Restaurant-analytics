import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Zomato Restaurant Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Light Red Zomato Theme CSS with White Background
st.markdown("""
<style>
    /* LIGHT RED ZOMATO THEME WITH WHITE BACKGROUND */
    .stApp {
        background: #ffffff;
        background-attachment: fixed;
    }
    
    /* Main Header */
    .main-header {
        font-size: 3rem;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        padding: 1rem;
    }
    
    /* Simple Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid #ffcdd2;
        box-shadow: 0 4px 15px 0 rgba(211, 47, 47, 0.2);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px 0 rgba(211, 47, 47, 0.3);
    }
    
    .metric-card h3 {
        color: #d32f2f;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-card h2 {
        color: #d32f2f;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
    }
    
    /* Simple Insight Boxes */
    .insight-box {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #d32f2f;
        box-shadow: 0 4px 12px 0 rgba(211, 47, 47, 0.15);
        border: 1px solid #ffcdd2;
    }
    
    .insight-box h4 {
        color: #d32f2f;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1rem;
    }
    
    .insight-box p {
        color: #666;
        margin: 0;
        font-size: 0.9rem;
    }
    
    /* Section Headers */
    .section-header {
        color: #d32f2f;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding: 0.8rem 0;
        border-bottom: 3px solid #d32f2f;
    }
    
    /* Filter Section */
    .filter-section {
        background: rgba(255, 255, 255, 0.9);
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #ffcdd2;
        box-shadow: 0 4px 15px 0 rgba(211, 47, 47, 0.1);
    }
    
    /* Chart Containers */
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px 0 rgba(211, 47, 47, 0.1);
        border: 1px solid #ffcdd2;
    }
    
    /* Dataframe Container */
    .dataframe-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px 0 rgba(211, 47, 47, 0.1);
        border: 1px solid #ffcdd2;
    }
    
    /* Footer */
    .footer {
        background: rgba(211, 47, 47, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        text-align: center;
        color: #d32f2f;
        border: 2px solid #ffcdd2;
    }
    
    /* Progress Bars */
    .progress-bar {
        background: rgba(211, 47, 47, 0.2);
        border-radius: 8px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(45deg, #d32f2f, #f44336);
        border-radius: 8px;
        transition: width 0.8s ease;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #d32f2f;
        color: white;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #ffffff 0%, #ffebee 100%) !important;
    }
    
    /* Custom Styling for Streamlit Components */
    .stMultiSelect [data-baseweb=tag] {
        background-color: #d32f2f !important;
        color: white !important;
    }
    
    .stSlider [data-baseweb=slider] [role=slider] {
        background: #d32f2f !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzer with generic CSV path and data processing
@st.cache_data
def load_data():
    # Generic CSV paths
    csv_paths = [
        "data/zomato.csv",
        "./data/zomato.csv",
        "zomato.csv",
        "./zomato.csv"
    ]
    
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            st.success(f"✅ Data loaded successfully from {csv_path}")
            return df
    
    # If no file found, create sample data
    st.warning("Zomato CSV file not found. Using sample data for demonstration.")
    return pd.DataFrame({
        'name': ['Restaurant A', 'Restaurant B', 'Restaurant C', 'Restaurant D', 'Restaurant E'],
        'location': ['Area1', 'Area2', 'Area1', 'Area3', 'Area2'],
        'rate': ['4.2/5', '3.8/5', '4.5/5', '4.0/5', '3.5/5'],
        'votes': [100, 150, 200, 80, 120],
        'approx_cost(for two people)': [800, 1200, 1500, 600, 900],
        'cuisines': ['North Indian', 'Chinese, Thai', 'Italian', 'South Indian', 'Chinese'],
        'rest_type': ['Casual Dining', 'Quick Bites', 'Fine Dining', 'Casual Dining', 'Cafe'],
        'online_order': ['Yes', 'No', 'Yes', 'Yes', 'No'],
        'book_table': ['Yes', 'No', 'Yes', 'No', 'No']
    })

# Data processing class
class ZomatoAnalyzer:
    def __init__(self, df):
        self.df = self._process_data(df)
    
    def _process_data(self, df):
        # Create a copy to avoid modifying original
        processed_df = df.copy()
        
        # Handle rating conversion
        if 'rate' in processed_df.columns:
            processed_df['rating_numeric'] = processed_df['rate'].apply(
                lambda x: float(str(x).split('/')[0]) if pd.notna(x) and '/' in str(x) else 0.0
            )
        else:
            processed_df['rating_numeric'] = np.random.uniform(3.0, 4.5, len(processed_df))
        
        # Create cost_category if not exists
        if 'approx_cost(for two people)' in processed_df.columns:
            processed_df['approx_cost(for two people)'] = pd.to_numeric(
                processed_df['approx_cost(for two people)'], errors='coerce'
            ).fillna(1000)
            
            # Create cost categories
            conditions = [
                processed_df['approx_cost(for two people)'] < 500,
                processed_df['approx_cost(for two people)'] < 1000,
                processed_df['approx_cost(for two people)'] < 2000,
                processed_df['approx_cost(for two people)'] >= 2000
            ]
            choices = ['Budget', 'Medium', 'High', 'Premium']
            processed_df['cost_category'] = np.select(conditions, choices, default='Medium')
        else:
            processed_df['cost_category'] = 'Medium'
            processed_df['approx_cost(for two people)'] = 1000
        
        # Create quality tiers based on rating
        conditions = [
            processed_df['rating_numeric'] >= 4.0,
            processed_df['rating_numeric'] >= 3.0,
            processed_df['rating_numeric'] < 3.0
        ]
        choices = ['Excellent', 'Good', 'Average']
        processed_df['quality_tier'] = np.select(conditions, choices, default='Good')
        
        # Fill missing values
        if 'location' not in processed_df.columns:
            processed_df['location'] = 'Unknown'
        
        if 'cuisines' not in processed_df.columns:
            processed_df['cuisines'] = 'Unknown'
            
        if 'rest_type' not in processed_df.columns:
            processed_df['rest_type'] = 'Casual Dining'
            
        return processed_df
    
    def get_cuisine_distribution(self):
        if 'cuisines' in self.df.columns:
            # Split cuisines and count
            all_cuisines = self.df['cuisines'].str.split(', ').explode()
            return all_cuisines.value_counts()
        return pd.Series()

# Load data and initialize analyzer
df = load_data()
analyzer = ZomatoAnalyzer(df)

# Enhanced Sidebar with Zomato Logo
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <img src='https://b.zmtcdn.com/images/logo/zomato_logo_2017.png' width='120' style='border-radius: 15px; box-shadow: 0 4px 15px rgba(211,47,47,0.3); margin-bottom: 1rem;'>
        <h2 style='color: #d32f2f; margin-bottom: 1rem;'>📊 Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; color: #d32f2f; margin-bottom: 2rem;'>🍽️ Zomato Analytics</h1>", unsafe_allow_html=True)
    
    # Filters Section
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("### 🔍 Data Filters")
    
    location_filter = st.multiselect(
        "📍 Select Locations",
        options=analyzer.df['location'].unique(),
        default=analyzer.df['location'].unique()[:3] if len(analyzer.df['location'].unique()) > 3 else analyzer.df['location'].unique()
    )
    
    cuisine_options = analyzer.get_cuisine_distribution().index.tolist()[:15]
    cuisine_filter = st.multiselect(
        "🍽️ Select Cuisines",
        options=cuisine_options,
        default=cuisine_options[:3] if len(cuisine_options) >= 3 else cuisine_options
    )
    
    cost_filter = st.multiselect(
        "💰 Cost Category",
        options=analyzer.df['cost_category'].unique(),
        default=analyzer.df['cost_category'].unique()
    )
    
    rating_filter = st.slider(
        "⭐ Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=3.0,
        step=0.1
    )
    
    with st.expander("🎛️ Advanced Filters"):
        rest_type_filter = st.multiselect(
            "🏪 Restaurant Type",
            options=analyzer.df['rest_type'].unique(),
            default=analyzer.df['rest_type'].unique()[:3]
        )
        
        votes_filter = st.slider(
            "👍 Minimum Votes",
            min_value=0,
            max_value=int(analyzer.df['votes'].max()) if 'votes' in analyzer.df.columns else 5000,
            value=0,
            step=50
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("### 📊 Quick Stats")
    total_restaurants = len(analyzer.df)
    avg_rating = analyzer.df['rating_numeric'].mean()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", f"{total_restaurants:,}")
    with col2:
        st.metric("Avg Rating", f"{avg_rating:.1f}")
    
    # Data source info
    st.markdown("---")
    st.markdown("**📁 Data Source**")
    st.markdown("Zomato Dataset")
    st.markdown(f"**📍 Locations:** {analyzer.df['location'].nunique()}")
    st.markdown(f"**🍽️ Cuisines:** {analyzer.get_cuisine_distribution().shape[0]}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Apply filters
filtered_df = analyzer.df.copy()
if location_filter:
    filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
if cuisine_filter:
    filtered_df = filtered_df[filtered_df['cuisines'].str.contains('|'.join(cuisine_filter), na=False)]
if cost_filter:
    filtered_df = filtered_df[filtered_df['cost_category'].isin(cost_filter)]
if 'rest_type_filter' in locals() and rest_type_filter:
    filtered_df = filtered_df[filtered_df['rest_type'].isin(rest_type_filter)]
if 'votes' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['votes'] >= votes_filter]
filtered_df = filtered_df[filtered_df['rating_numeric'] >= rating_filter]

# Main content
st.markdown("""
<div class='main-header'>
    🍽️ Zomato Restaurant Analytics
</div>
""", unsafe_allow_html=True)

# Data Source Info
st.info(f"📊 **Dataset Info:** {len(filtered_df):,} restaurants loaded | {filtered_df['location'].nunique()} locations | {analyzer.get_cuisine_distribution().shape[0]} cuisine types")

# Key Metrics
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rest = len(filtered_df)
    progress_width = min(100, total_rest / max(1, len(analyzer.df)) * 100)
    st.markdown(f"""
    <div class="metric-card">
        <h3>🏪 Total Restaurants</h3>
        <h2>{total_rest:,}</h2>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_width}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_rating = filtered_df['rating_numeric'].mean()
    progress_width = (avg_rating / 5) * 100
    st.markdown(f"""
    <div class="metric-card">
        <h3>⭐ Average Rating</h3>
        <h2>{avg_rating:.2f}/5</h2>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_width}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    locations_count = filtered_df['location'].nunique()
    progress_width = min(100, locations_count / max(1, analyzer.df['location'].nunique()) * 100)
    st.markdown(f"""
    <div class="metric-card">
        <h3>📍 Locations Covered</h3>
        <h2>{locations_count}</h2>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_width}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_cost = filtered_df['approx_cost(for two people)'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <h3>💰 Avg Cost for Two</h3>
        <h2>₹{avg_cost:.0f}</h2>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {min(100, avg_cost/50)}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Charts Section
st.markdown('<div class="section-header">📊 Distribution Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    location_counts = filtered_df['location'].value_counts().head(10)
    
    fig = px.bar(
        x=location_counts.values,
        y=location_counts.index,
        orientation='h',
        title="📍 Top 10 Locations by Restaurant Count",
        labels={'x': 'Number of Restaurants', 'y': 'Location'},
        color=location_counts.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.histogram(
        filtered_df, 
        x='rating_numeric',
        nbins=20,
        title="⭐ Distribution of Restaurant Ratings",
        labels={'rating_numeric': 'Rating'},
        color_discrete_sequence=['#d32f2f']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# More Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    cost_dist = filtered_df['cost_category'].value_counts()
    fig = px.pie(
        values=cost_dist.values,
        names=cost_dist.index,
        title="💰 Restaurants by Cost Category",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    cuisine_dist = analyzer.get_cuisine_distribution().head(10)
    fig = px.bar(
        x=cuisine_dist.values,
        y=cuisine_dist.index,
        orientation='h',
        title="🍽️ Top 10 Most Popular Cuisines",
        labels={'x': 'Number of Restaurants', 'y': 'Cuisine'},
        color=cuisine_dist.values,
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Feature Analysis
st.markdown('<div class="section-header">🚀 Feature Analysis</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if 'online_order' in filtered_df.columns:
        online_stats = filtered_df['online_order'].value_counts()
        fig = px.pie(
            values=online_stats.values,
            names=online_stats.index,
            title="📱 Online Order Availability",
            color_discrete_sequence=['#d32f2f', '#ef9a9a']
        )
    else:
        fig = px.pie(values=[1], names=['Data Not Available'], title="📱 Online Order")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if 'book_table' in filtered_df.columns:
        table_stats = filtered_df['book_table'].value_counts()
        fig = px.pie(
            values=table_stats.values,
            names=table_stats.index,
            title="📅 Table Booking Availability",
            color_discrete_sequence=['#ef9a9a', '#d32f2f']
        )
    else:
        fig = px.pie(values=[1], names=['Data Not Available'], title="📅 Table Booking")
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    quality_stats = filtered_df['quality_tier'].value_counts()
    fig = px.pie(
        values=quality_stats.values,
        names=quality_stats.index,
        title="🏆 Quality Tiers Distribution",
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Top Restaurants
st.markdown('<div class="section-header">🏆 Top Rated Restaurants</div>', unsafe_allow_html=True)

st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
top_restaurants = filtered_df.nlargest(10, 'rating_numeric')[
    ['name', 'location', 'rating_numeric', 'votes', 'approx_cost(for two people)', 'cuisines']
]
top_restaurants.columns = ['Restaurant Name', 'Location', 'Rating', 'Votes', 'Cost for Two', 'Cuisines']

# Format the dataframe
top_restaurants_display = top_restaurants.copy()
top_restaurants_display['Rating'] = top_restaurants_display['Rating'].round(2)
top_restaurants_display['Cost for Two'] = '₹' + top_restaurants_display['Cost for Two'].astype(int).astype(str)
if 'Votes' in top_restaurants_display.columns:
    top_restaurants_display['Votes'] = top_restaurants_display['Votes'].apply(lambda x: f"{x:,}")

st.dataframe(top_restaurants_display, use_container_width=True, height=400)
st.markdown('</div>', unsafe_allow_html=True)

# Insights Section
st.markdown('<div class="section-header">💡 Key Business Insights</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    if 'online_order' in filtered_df.columns:
        online_order_pct = (filtered_df['online_order'] == 'Yes').mean() * 100
    else:
        online_order_pct = 70.0
    st.markdown(f"""
    <div class="insight-box">
        <h4>📱 Digital Presence</h4>
        <p><strong>{online_order_pct:.1f}%</strong> of restaurants offer online ordering</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {online_order_pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    high_rated_count = len(filtered_df[filtered_df['rating_numeric'] >= 4.0])
    high_rated_pct = (high_rated_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="insight-box">
        <h4>🏆 Quality Standards</h4>
        <p><strong>{high_rated_count}</strong> restaurants rated 4.0+ ({high_rated_pct:.1f}%)</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {high_rated_pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    premium_count = len(filtered_df[filtered_df['cost_category'] == 'Premium'])
    premium_pct = (premium_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0
    st.markdown(f"""
    <div class="insight-box">
        <h4>💎 Premium Segment</h4>
        <p><strong>{premium_count}</strong> premium restaurants ({premium_pct:.1f}%)</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {premium_pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <h3 style='color: #d32f2f; margin-bottom: 1rem;'>🚀 Zomato Restaurant Analytics Dashboard</h3>
    <p style='color: #666; margin-bottom: 0.5rem;'>Built with ❤️ using Streamlit & Zomato Data</p>
    <div style='display: flex; justify-content: center; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap;'>
        <span class="badge">Real-time Analytics</span>
        <span class="badge">Business Intelligence</span>
        <span class="badge">Data-Driven Decisions</span>
        <span class="badge">Zomato Data</span>
    </div>
</div>
""", unsafe_allow_html=True)