const fetch = require('node-fetch');

async function fetchDataFromCSV(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch CSV file from ${url}`);
    }
    const csvData = await response.text();
    return csvData;
  } catch (error) {
    throw new Error(`Error fetching CSV data: ${error.message}`);
  }
}

module.exports = async (req, res) => {
  const { place_name } = req.body;

  try {
    // Fetch data from the three CSV files hosted on GitHub
    const csvUrls = [
      'https://raw.githubusercontent.com/MaleekaA/travel/master/build/mallss.csv',
      'https://raw.githubusercontent.com/MaleekaA/travel/master/build/restaurantss.csv',
      'https://raw.githubusercontent.com/MaleekaA/travel/master/build/placess.csv'
    ];

    const csvDataPromises = csvUrls.map(url => fetchDataFromCSV(url));
    const [mallsData, restaurantsData, placesData] = await Promise.all(csvDataPromises);

    // Process the fetched CSV data
    const addDoubleS = (data) => {
      return data.split('\n').map(line => {
        const columns = line.split(',');
        columns[0] = columns[0].replace(/\b(\w+)\b/g, '$1ss');
        return columns.join(',');
      }).join('\n');
    };

    const processedMallsData = addDoubleS(mallsData);
    const processedRestaurantsData = addDoubleS(restaurantsData);
    const processedPlacesData = addDoubleS(placesData);

    res.status(200).json({ mallsData: processedMallsData, restaurantsData: processedRestaurantsData, placesData: processedPlacesData });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
