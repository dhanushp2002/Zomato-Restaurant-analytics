import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_analyzer

st.set_page_config(page_title="Restaurant Analysis", page_icon="📊", layout="wide")

analyzer = get_analyzer()
df = analyzer.df

st.title("📊 Restaurant Performance Analysis")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    location_filter = st.multiselect(
        "Select Locations",
        options=df['location'].unique(),
        default=df['location'].unique()[:3]
    )

with col2:
    rest_type_filter = st.multiselect(
        "Restaurant Type",
        options=df['rest_type'].unique(),
        default=df['rest_type'].unique()[:3]
    )

with col3:
    cost_filter = st.slider(
        "Cost Range (for two people)",
        min_value=int(df['approx_cost(for two people)'].min()),
        max_value=int(df['approx_cost(for two people)'].max()),
        value=(300, 1000)
    )

# Apply filters
filtered_df = df.copy()
if location_filter:
    filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
if rest_type_filter:
    filtered_df = filtered_df[filtered_df['rest_type'].isin(rest_type_filter)]
filtered_df = filtered_df[
    (filtered_df['approx_cost(for two people)'] >= cost_filter[0]) & 
    (filtered_df['approx_cost(for two people)'] <= cost_filter[1])
]

# Performance Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_rating = filtered_df['rating_numeric'].mean()
    st.metric("Average Rating", f"{avg_rating:.2f}/5")

with col2:
    avg_cost = filtered_df['approx_cost(for two people)'].mean()
    st.metric("Average Cost for Two", f"₹{avg_cost:.0f}")

with col3:
    online_order_pct = (filtered_df['online_order'] == 'Yes').mean() * 100
    st.metric("Online Order %", f"{online_order_pct:.1f}%")

with col4:
    table_booking_pct = (filtered_df['book_table'] == 'Yes').mean() * 100
    st.metric("Table Booking %", f"{table_booking_pct:.1f}%")

# Charts
col1, col2 = st.columns(2)

with col1:
    # Rating vs Cost scatter plot
    fig = px.scatter(
        filtered_df,
        x='approx_cost(for two people)',
        y='rating_numeric',
        color='rest_type',
        size='votes',
        hover_data=['name', 'location'],
        title="Rating vs Cost Relationship",
        labels={
            'approx_cost(for two people)': 'Cost for Two (₹)',
            'rating_numeric': 'Rating'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Votes distribution by restaurant type
    fig = px.box(
        filtered_df,
        x='rest_type',
        y='votes',
        title="Votes Distribution by Restaurant Type",
        labels={'rest_type': 'Restaurant Type', 'votes': 'Number of Votes'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# Restaurant Type Analysis
st.subheader("🏪 Restaurant Type Performance")

col1, col2 = st.columns(2)

with col1:
    # Average rating by restaurant type
    rating_by_type = filtered_df.groupby('rest_type')['rating_numeric'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=rating_by_type.values,
        y=rating_by_type.index,
        orientation='h',
        title="Average Rating by Restaurant Type",
        labels={'x': 'Average Rating', 'y': 'Restaurant Type'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Average cost by restaurant type
    cost_by_type = filtered_df.groupby('rest_type')['approx_cost(for two people)'].mean().sort_values(ascending=False)
    fig = px.bar(
        x=cost_by_type.values,
        y=cost_by_type.index,
        orientation='h',
        title="Average Cost by Restaurant Type",
        labels={'x': 'Average Cost for Two (₹)', 'y': 'Restaurant Type'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Top Performing Restaurants
st.subheader("🏆 Top Performing Restaurants")

performance_df = filtered_df.nlargest(15, 'popularity_score')[
    ['name', 'location', 'rest_type', 'rating_numeric', 'votes', 'approx_cost(for two people)', 'cuisines']
]
performance_df.columns = ['Name', 'Location', 'Type', 'Rating', 'Votes', 'Cost for Two', 'Cuisines']

st.dataframe(performance_df, use_container_width=True, height=400)