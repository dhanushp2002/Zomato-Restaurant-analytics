import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_analyzer

st.set_page_config(page_title="Cuisine Analysis", page_icon="🍽️", layout="wide")

analyzer = get_analyzer()
df = analyzer.df

st.title("🍽️ Cuisine Analysis")

# Cuisine distribution
st.subheader("Cuisine Popularity")

# Get top cuisines
cuisine_dist = analyzer.get_cuisine_distribution().head(20)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        x=cuisine_dist.values,
        y=cuisine_dist.index,
        orientation='h',
        title="Top 20 Most Popular Cuisines",
        labels={'x': 'Number of Restaurants', 'y': 'Cuisine'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        values=cuisine_dist.head(10).values,
        names=cuisine_dist.head(10).index,
        title="Top 10 Cuisines Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

# Cuisine Performance by Location
st.subheader("Cuisine Performance by Location")

col1, col2 = st.columns(2)

with col1:
    # Select cuisine to analyze
    selected_cuisine = st.selectbox(
        "Select Cuisine to Analyze",
        options=cuisine_dist.index.tolist()[:15]
    )

with col2:
    # Select metric
    metric = st.selectbox(
        "Select Performance Metric",
        options=['Average Rating', 'Average Cost', 'Restaurant Count']
    )

# Filter restaurants that serve selected cuisine
cuisine_restaurants = df[df['cuisines'].str.contains(selected_cuisine, na=False)]

if metric == 'Average Rating':
    performance_data = cuisine_restaurants.groupby('location')['rating_numeric'].mean().sort_values(ascending=False)
    title = f"Average Rating for {selected_cuisine} Cuisine by Location"
    y_label = 'Average Rating'
elif metric == 'Average Cost':
    performance_data = cuisine_restaurants.groupby('location')['approx_cost(for two people)'].mean().sort_values(ascending=False)
    title = f"Average Cost for {selected_cuisine} Cuisine by Location"
    y_label = 'Average Cost (₹)'
else:
    performance_data = cuisine_restaurants.groupby('location').size().sort_values(ascending=False)
    title = f"Number of {selected_cuisine} Restaurants by Location"
    y_label = 'Number of Restaurants'

fig = px.bar(
    x=performance_data.values,
    y=performance_data.index,
    orientation='h',
    title=title,
    labels={'x': y_label, 'y': 'Location'}
)
st.plotly_chart(fig, use_container_width=True)

# Cuisine Combinations
st.subheader("Popular Cuisine Combinations")

# Analyze cuisine pairs (simplified)
from itertools import combinations

cuisine_pairs = {}
for cuisines in df['cuisines_list']:
    if len(cuisines) >= 2:
        for pair in combinations(cuisines, 2):
            sorted_pair = tuple(sorted(pair))
            cuisine_pairs[sorted_pair] = cuisine_pairs.get(sorted_pair, 0) + 1

# Convert to DataFrame
pairs_df = pd.DataFrame([
    {'Cuisine 1': pair[0], 'Cuisine 2': pair[1], 'Count': count}
    for pair, count in sorted(cuisine_pairs.items(), key=lambda x: x[1], reverse=True)[:20]
])

st.dataframe(pairs_df, use_container_width=True, height=400)

# Cost vs Rating by Cuisine
st.subheader("Cost vs Rating Analysis by Cuisine")

# Get top 8 cuisines for analysis
top_cuisines = cuisine_dist.head(8).index.tolist()

fig = go.Figure()

for cuisine in top_cuisines:
    cuisine_data = df[df['cuisines'].str.contains(cuisine, na=False)]
    fig.add_trace(go.Box(
        y=cuisine_data['rating_numeric'],
        x=[cuisine] * len(cuisine_data),
        name=cuisine,
        boxpoints='outliers'
    ))

fig.update_layout(
    title="Rating Distribution by Cuisine",
    xaxis_title="Cuisine",
    yaxis_title="Rating",
    height=500
)
st.plotly_chart(fig, use_container_width=True)