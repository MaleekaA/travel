from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.neighbors import NearestNeighbors


app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "https://travel-1-txo3.onrender.com"}})
# Load data from CSV files
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
places_df = pd.read_csv(os.path.join(base_dir,'..','public', 'placess.csv'))
malls_df = pd.read_csv(os.path.join(base_dir, '..','public', 'mallss.csv'))
restaurants_df = pd.read_csv(os.path.join(base_dir,'..', 'public', 'restaurantss.csv'))


# Function to find nearest shopping malls and restaurants given a place name
def find_nearest_locations(places_df, malls_df, restaurants_df, place_name, n_neighbors=4):
    if place_name not in places_df['place_name'].values:
        raise ValueError(f"Place name '{place_name}' not found in the dataset.")
    
    place_coords = places_df.loc[places_df['place_name'] == place_name, ['latitude', 'longitude']].values[0]
    
    mall_coords = malls_df[['latitude', 'longitude']]
    knn_malls = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
    knn_malls.fit(mall_coords)
    distances_malls, indices_malls = knn_malls.kneighbors([place_coords])
    nearest_malls = malls_df.iloc[indices_malls[0]]
    
    restaurant_coords = restaurants_df[['latitude', 'longitude']]
    knn_restaurants = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree')
    knn_restaurants.fit(restaurant_coords)
    distances_restaurants, indices_restaurants = knn_restaurants.kneighbors([place_coords])
    nearest_restaurants = restaurants_df.iloc[indices_restaurants[0]]
    
    nearest_malls = nearest_malls[['mall_name', 'latitude', 'longitude']].to_dict(orient='records')
    nearest_restaurants = nearest_restaurants[['restaurant_name', 'latitude', 'longitude']].to_dict(orient='records')
    
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)
