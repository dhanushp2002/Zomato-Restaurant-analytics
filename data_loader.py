# data_loader.py
import pandas as pd
import numpy as np
import random

class ZomatoAnalyzer:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load and preprocess the Zomato dataset"""
        self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate realistic sample data based on your CSV structure"""
        np.random.seed(42)
        random.seed(42)
        n_restaurants = 800
        
        locations = ['Banashankari', 'Basavanagudi', 'Jayanagar', 'JP Nagar', 'HSR Layout', 
                    'Koramangala', 'Indiranagar', 'Whitefield', 'Malleshwaram', 'BTM Layout']
        
        restaurant_types = ['Casual Dining', 'Quick Bites', 'Cafe', 'Fine Dining', 'Delivery', 
                           'Dessert Parlor', 'Bakery', 'Bar', 'Food Court']
        
        cuisines_list = ['North Indian', 'Chinese', 'South Indian', 'Italian', 'Mexican', 
                        'Continental', 'Thai', 'Arabian', 'Beverages', 'Desserts', 
                        'Fast Food', 'Mughlai', 'Barbecue', 'Asian', 'Mediterranean']
        
        listed_in_types = ['Buffet', 'Cafes', 'Delivery', 'Desserts', 'Dine-out', 
                          'Drinks & nightlife', 'Pubs and bars']
        
        # Fixed phone number generation
        phone_numbers = [f'+91 {random.randint(7000000000, 9999999999)}' for _ in range(n_restaurants)]
        
        data = {
            'url': [f'https://www.zomato.com/bangalore/restaurant-{i}' for i in range(n_restaurants)],
            'name': [f'Restaurant_{i}' for i in range(n_restaurants)],
            'online_order': np.random.choice(['Yes', 'No'], n_restaurants, p=[0.7, 0.3]),
            'book_table': np.random.choice(['Yes', 'No'], n_restaurants, p=[0.4, 0.6]),
            'rate': np.random.uniform(3.0, 4.5, n_restaurants).round(1),
            'votes': np.random.randint(50, 5000, n_restaurants),
            'phone': phone_numbers,
            'location': np.random.choice(locations, n_restaurants),
            'rest_type': np.random.choice(restaurant_types, n_restaurants),
            'dish_liked': ['Pasta, Pizza, Burger' for _ in range(n_restaurants)],
            'cuisines': [', '.join(np.random.choice(cuisines_list, np.random.randint(1, 4), replace=False)) 
                        for _ in range(n_restaurants)],
            'approx_cost(for two people)': np.random.choice([300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1500], n_restaurants),
            'reviews_list': ['Sample reviews' for _ in range(n_restaurants)],
            'menu_item': ['[]' for _ in range(n_restaurants)],
            'listed_in(type)': np.random.choice(listed_in_types, n_restaurants),
            'listed_in(city)': ['Bangalore' for _ in range(n_restaurants)]
        }
        
        self.df = pd.DataFrame(data)
        self.preprocess_data()
    
    def preprocess_data(self):
        """Clean and preprocess the dataset"""
        self.df['rate_clean'] = self.df['rate']
        self.df['rating_numeric'] = pd.to_numeric(self.df['rate_clean'], errors='coerce')
        self.df['rating_numeric'].fillna(self.df['rating_numeric'].mean(), inplace=True)
        
        def get_cost_category(cost):
            if cost <= 400: return 'Budget'
            elif cost <= 700: return 'Moderate'
            elif cost <= 1000: return 'Expensive'
            else: return 'Premium'
        
        self.df['cost_category'] = self.df['approx_cost(for two people)'].apply(get_cost_category)
        self.df['cuisines_list'] = self.df['cuisines'].str.split(', ')
        self.df['popularity_score'] = (self.df['votes'] / 1000) + (self.df['rating_numeric'] * 2)
        
        # Create restaurant quality tiers
        def get_quality_tier(rating):
            if rating >= 4.5: return 'Excellent'
            elif rating >= 4.0: return 'Very Good'
            elif rating >= 3.5: return 'Good'
            elif rating >= 3.0: return 'Average'
            else: return 'Below Average'
        
        self.df['quality_tier'] = self.df['rating_numeric'].apply(get_quality_tier)
    
    def get_restaurant_count_by_location(self):
        return self.df['location'].value_counts()
    
    def get_average_rating_by_location(self):
        return self.df.groupby('location')['rating_numeric'].mean().sort_values(ascending=False)
    
    def get_cuisine_distribution(self):
        all_cuisines = []
        for cuisines in self.df['cuisines_list']:
            all_cuisines.extend(cuisines)
        return pd.Series(all_cuisines).value_counts()
    
    def get_cost_distribution(self):
        return self.df['cost_category'].value_counts()
    
    def get_online_order_stats(self):
        return self.df['online_order'].value_counts()
    
    def get_table_booking_stats(self):
        return self.df['book_table'].value_counts()