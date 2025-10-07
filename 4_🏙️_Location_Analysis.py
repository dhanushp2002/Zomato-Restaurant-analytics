import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_analyzer

st.set_page_config(page_title="Location Analysis", page_icon="🏙️", layout="wide")

analyzer = get_analyzer()
df = analyzer.df

st.title("🏙️ Location-based Analysis")

# Location Overview
st.subheader("Location Overview")

col1, col2, col3 = st.columns(3)

with col1:
    total_locations = df['location'].nunique()
    st.metric("Total Locations", total_locations)

with col2:
    avg_restaurants_per_location = len(df) / total_locations
    st.metric("Avg Restaurants per Location", f"{avg_restaurants_per_location:.1f}")

with col3:
    most_restaurants_location = df['location'].value_counts().index[0]
    st.metric("Most Popular Location", most_restaurants_location)

# Location Performance Metrics
st.subheader("Location Performance Comparison")

# Select locations to compare
selected_locations = st.multiselect(
    "Select Locations to Compare",
    options=df['location'].unique(),
    default=df['location'].value_counts().head(5).index.tolist()
)

if selected_locations:
    comparison_data = []
    
    for location in selected_locations:
        location_data = df[df['location'] == location]
        comparison_data.append({
            'Location': location,
            'Restaurant Count': len(location_data),
            'Average Rating': location_data['rating_numeric'].mean(),
            'Average Cost': location_data['approx_cost(for two people)'].mean(),
            'Online Order %': (location_data['online_order'] == 'Yes').mean() * 100,
            'Table Booking %': (location_data['book_table'] == 'Yes').mean() * 100
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.dataframe(comparison_df, use_container_width=True)
    
    # Visual comparisons
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            comparison_df,
            x='Location',
            y='Average Rating',
            title="Average Rating by Location",
            color='Average Rating',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            comparison_df,
            x='Location',
            y='Average Cost',
            title="Average Cost by Location",
            color='Average Cost',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)

# Location Heatmap
st.subheader("Restaurant Density Heatmap")

# Create a simulated geographical distribution (in real scenario, use actual coordinates)
location_counts = df['location'].value_counts()

# Create a heatmap-like visualization
fig = px.bar(
    x=location_counts.index,
    y=location_counts.values,
    title="Restaurant Count by Location",
    labels={'x': 'Location', 'y': 'Number of Restaurants'}
)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Restaurant Type Distribution by Location
st.subheader("Restaurant Type Distribution by Location")

selected_location_type = st.selectbox(
    "Select Location for Type Analysis",
    options=df['location'].unique()
)

location_type_data = df[df['location'] == selected_location_type]['rest_type'].value_counts()

fig = px.pie(
    values=location_type_data.values,
    names=location_type_data.index,
    title=f"Restaurant Type Distribution in {selected_location_type}"
)
st.plotly_chart(fig, use_container_width=True)

# Cost Analysis by Location
st.subheader("Cost Analysis by Location")

fig = px.box(
    df,
    x='location',
    y='approx_cost(for two people)',
    title="Cost Distribution by Location",
    labels={'location': 'Location', 'approx_cost(for two people)': 'Cost for Two (₹)'}
)
fig.update_xaxes(tickangle=45)
st.plotly_chart(fig, use_container_width=True)

# Top Locations by Different Metrics
st.subheader("Top Locations Ranking")

metric = st.selectbox(
    "Rank by Metric",
    options=['Restaurant Count', 'Average Rating', 'Average Cost', 'Online Order %']
)

if metric == 'Restaurant Count':
    ranking_data = df['location'].value_counts().head(10)
    title = "Top 10 Locations by Restaurant Count"
    y_label = "Number of Restaurants"
elif metric == 'Average Rating':
    ranking_data = df.groupby('location')['rating_numeric'].mean().sort_values(ascending=False).head(10)
    title = "Top 10 Locations by Average Rating"
    y_label = "Average Rating"
elif metric == 'Average Cost':
    ranking_data = df.groupby('location')['approx_cost(for two people)'].mean().sort_values(ascending=False).head(10)
    title = "Top 10 Locations by Average Cost"
    y_label = "Average Cost (₹)"
else:
    ranking_data = (df[df['online_order'] == 'Yes'].groupby('location').size() / 
                   df.groupby('location').size()).sort_values(ascending=False).head(10) * 100
    title = "Top 10 Locations by Online Order Percentage"
    y_label = "Online Order %"

fig = px.bar(
    x=ranking_data.values,
    y=ranking_data.index,
    orientation='h',
    title=title,
    labels={'x': y_label, 'y': 'Location'}
)
st.plotly_chart(fig, use_container_width=True)