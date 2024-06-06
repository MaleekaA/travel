const express = require('express');
const bodyParser = require('body-parser');
const app = express();
const port = process.env.PORT || 5000;

// Middlewares
app.use(bodyParser.json()); // For parsing application/json

// Import route handlers
const routeHandler = require('./api/route');

// API routes
app.post('/api/route', routeHandler);

// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
