const fetch = require('node-fetch');

module.exports = async (req, res) => {
  const { place_name } = req.body;

  try {
    // Fetch data from the GitHub link
    const response = await fetch('https://github.com/MaleekaA/travel/raw/master/Public');
    
    if (!response.ok) {
      throw new Error('Failed to fetch database file from GitHub');
    }

    const database = await response.json();

    // Process the database to find the relevant data based on place_name
    const malls = database.malls.filter(mall => mall.location.includes(place_name));
    const restaurants = database.restaurants.filter(restaurant => restaurant.location.includes(place_name));

    res.status(200).json({ malls, restaurants });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
