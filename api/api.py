from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
CORS(app)

# Load data from CSV files
places_df = pd.read_csv('placess.csv')
malls_df = pd.read_csv('mallss.csv')
restaurants_df = pd.read_csv('restaurantss.csv')

# Function to find nearest shopping malls and restaurants given a place name
def find_nearest_locations(places_df, malls_df, restaurants_df, place_name, n_neighbors=4):
    if place_name not in places_df['place_name'].values:
        raise ValueError(f"Place name '{place_name}' not found in the dataset.")
    
    place_coords = places_df.loc[places_df['place_name'] == place_name, ['longitude', 'latitude']].values[0]
    
    mall_coords = malls_df[['longitude', 'latitude']]
    knn_malls = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
    knn_malls.fit(mall_coords)
    distances_malls, indices_malls = knn_malls.kneighbors([place_coords])
    nearest_malls = malls_df.iloc[indices_malls[0]]
    
    restaurant_coords = restaurants_df[['longitude', 'latitude']]
    knn_restaurants = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
    knn_restaurants.fit(restaurant_coords)
    distances_restaurants, indices_restaurants = knn_restaurants.kneighbors([place_coords])
    nearest_restaurants = restaurants_df.iloc[indices_restaurants[0]]
    
    nearest_malls = nearest_malls[['mall_name', 'longitude', 'latitude']].to_dict(orient='records')
    nearest_restaurants = nearest_restaurants[['restaurant_name', 'longitude', 'latitude']].to_dict(orient='records')
    
    return nearest_malls, nearest_restaurants

@app.route('/api/route', methods=['POST'])
def nearest_locations():
    data = request.get_json()
    place_name = data['place_name']
    try:
        nearest_malls, nearest_restaurants = find_nearest_locations(places_df, malls_df, restaurants_df, place_name)
        return jsonify({'malls': nearest_malls, 'restaurants': nearest_restaurants})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# No need for app.run() here
