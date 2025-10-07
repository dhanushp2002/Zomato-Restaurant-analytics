import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_analyzer
import numpy as np

st.set_page_config(page_title="Reviews Analysis", page_icon="⭐", layout="wide")

analyzer = get_analyzer()
df = analyzer.df

st.title("⭐ Reviews & Ratings Analysis")

# Rating Distribution Analysis
st.subheader("Rating Distribution")

col1, col2 = st.columns(2)

with col1:
    # Rating distribution histogram
    fig = px.histogram(
        df,
        x='rating_numeric',
        nbins=20,
        title="Distribution of Restaurant Ratings",
        labels={'rating_numeric': 'Rating'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Rating by restaurant type
    fig = px.box(
        df,
        x='rest_type',
        y='rating_numeric',
        title="Rating Distribution by Restaurant Type",
        labels={'rest_type': 'Restaurant Type', 'rating_numeric': 'Rating'}
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

# Votes Analysis
st.subheader("Votes Analysis")

col1, col2 = st.columns(2)

with col1:
    # Votes distribution
    fig = px.histogram(
        df,
        x='votes',
        nbins=20,
        title="Distribution of Votes",
        labels={'votes': 'Number of Votes'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Votes vs Rating scatter plot
    fig = px.scatter(
        df,
        x='votes',
        y='rating_numeric',
        color='rest_type',
        size='approx_cost(for two people)',
        hover_data=['name', 'location'],
        title="Votes vs Rating Relationship",
        labels={'votes': 'Number of Votes', 'rating_numeric': 'Rating'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Rating vs Cost Analysis
st.subheader("Rating vs Cost Analysis")

fig = px.scatter(
    df,
    x='approx_cost(for two people)',
    y='rating_numeric',
    color='cost_category',
    size='votes',
    hover_data=['name', 'location', 'rest_type'],
    title="Rating vs Cost Relationship",
    labels={
        'approx_cost(for two people)': 'Cost for Two (₹)',
        'rating_numeric': 'Rating',
        'cost_category': 'Cost Category'
    }
)
st.plotly_chart(fig, use_container_width=True)

# Online Features Impact on Ratings
st.subheader("Impact of Online Features on Ratings")

col1, col2 = st.columns(2)

with col1:
    # Online order impact
    online_impact = df.groupby('online_order')['rating_numeric'].mean()
    fig = px.bar(
        x=online_impact.index,
        y=online_impact.values,
        title="Average Rating by Online Order Availability",
        labels={'x': 'Online Order', 'y': 'Average Rating'},
        color=online_impact.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Table booking impact
    table_impact = df.groupby('book_table')['rating_numeric'].mean()
    fig = px.bar(
        x=table_impact.index,
        y=table_impact.values,
        title="Average Rating by Table Booking Availability",
        labels={'x': 'Table Booking', 'y': 'Average Rating'},
        color=table_impact.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

# Top Rated Restaurants Analysis
st.subheader("Top Rated Restaurants Analysis")

# Criteria for top-rated
min_votes = st.slider("Minimum Votes for Consideration", 0, 1000, 100)

top_rated = df[df['votes'] >= min_votes].nlargest(15, 'rating_numeric')[
    ['name', 'location', 'rest_type', 'rating_numeric', 'votes', 'approx_cost(for two people)', 'cuisines']
]
top_rated.columns = ['Name', 'Location', 'Type', 'Rating', 'Votes', 'Cost for Two', 'Cuisines']

st.dataframe(top_rated, use_container_width=True, height=400)

# Rating Trends by Cost Category
st.subheader("Rating Trends by Cost Category")

cost_rating_analysis = df.groupby('cost_category').agg({
    'rating_numeric': ['mean', 'std', 'count'],
    'votes': 'mean'
}).round(2)

cost_rating_analysis.columns = ['Average Rating', 'Rating Std', 'Restaurant Count', 'Average Votes']
cost_rating_analysis = cost_rating_analysis.sort_values('Average Rating', ascending=False)

st.dataframe(cost_rating_analysis, use_container_width=True)

# Correlation Analysis
st.subheader("Feature Correlation Analysis")

# Calculate correlations
correlation_data = df[['rating_numeric', 'votes', 'approx_cost(for two people)']].corr()

fig = go.Figure(data=go.Heatmap(
    z=correlation_data.values,
    x=correlation_data.columns,
    y=correlation_data.columns,
    colorscale='RdBu',
    zmin=-1,
    zmax=1,
    text=correlation_data.round(2).values,
    texttemplate='%{text}',
    textfont={"size": 10}
))

fig.update_layout(
    title="Feature Correlation Heatmap",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Insights
st.subheader("📊 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    high_rated_affordable = len(df[(df['rating_numeric'] >= 4.0) & (df['approx_cost(for two people)'] <= 500)])
    st.metric("High Rated & Affordable", high_rated_affordable)

with col2:
    avg_rating_online = df[df['online_order'] == 'Yes']['rating_numeric'].mean()
    avg_rating_no_online = df[df['online_order'] == 'No']['rating_numeric'].mean()
    st.metric("Online vs Offline Rating Diff", f"{(avg_rating_online - avg_rating_no_online):.2f}")

with col3:
    rating_votes_corr = df['rating_numeric'].corr(df['votes'])
    st.metric("Rating-Votes Correlation", f"{rating_votes_corr:.2f}")