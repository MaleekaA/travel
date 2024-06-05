import React, { useState } from 'react';

function NearestLocations() {
  const [placeName, setPlaceName] = useState('');
  const [malls, setMalls] = useState([]);
  const [restaurants, setRestaurants] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/route`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ place_name: placeName }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setMalls(data.malls);
      setRestaurants(data.restaurants);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  

  return (
    <div>
      <h1>Find Nearest Locations</h1>
      <input 
        type="text" 
        value={placeName} 
        onChange={(e) => setPlaceName(e.target.value)} 
        placeholder="Enter place name" 
      />
      <button onClick={handleSearch}>Search</button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <h2>Nearest Shopping Malls</h2>
      <ul>
        {malls.map((mall, index) => (
          <li key={index}>
            <strong>{mall.mall_name}</strong><br />
            Latitude: {mall.latitude}, Longitude: {mall.longitude}
          </li>
        ))}
      </ul>

      <h2>Nearest Restaurants</h2>
      <ul>
        {restaurants.map((restaurant, index) => (
          <li key={index}>
            <strong>{restaurant.restaurant_name}</strong><br />
            Latitude: {restaurant.latitude}, Longitude: {restaurant.longitude}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default NearestLocations;
