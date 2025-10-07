# utils.py
import streamlit as st
from data_loader import ZomatoAnalyzer

@st.cache_resource
def get_analyzer():
    return ZomatoAnalyzer()

def format_currency(amount):
    return f"₹{amount:,.0f}"

def format_percentage(value):
    return f"{value:.1%}"

def get_color_for_rating(rating):
    if rating >= 4.0:
        return '#00B050'  # Green
    elif rating >= 3.5:
        return '#92D050'  # Light Green
    elif rating >= 3.0:
        return '#FFC000'  # Yellow
    elif rating >= 2.5:
        return '#FF6600'  # Orange
    else:
        return '#FF0000'  # Red

def get_quality_badge(rating):
    if rating >= 4.5:
        return "🏆 Excellent"
    elif rating >= 4.0:
        return "⭐ Very Good"
    elif rating >= 3.5:
        return "👍 Good"
    elif rating >= 3.0:
        return "⚡ Average"
    else:
        return "⚠️ Below Average"