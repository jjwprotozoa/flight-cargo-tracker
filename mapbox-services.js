const mbxDirections = require('@mapbox/mapbox-sdk/services/directions');
const mbxOptimization = require('@mapbox/mapbox-sdk/services/optimization');
const axios = require('axios');

const directionsClient = mbxDirections({ accessToken: process.env.MAPBOX_ACCESS_TOKEN });
const optimizationClient = mbxOptimization({ accessToken: process.env.MAPBOX_ACCESS_TOKEN });

async function getDirections(start, end, waypoints = []) {
  try {
    const response = await directionsClient
      .getDirections({
        profile: 'driving',
        waypoints: [
          { coordinates: start },
          ...waypoints.map(wp => ({ coordinates: wp })),
          { coordinates: end }
        ],
        geometries: 'geojson'
      })
      .send();

    return response.body;
  } catch (error) {
    console.error('Error getting directions:', error);
    throw error;
  }
}

async function optimizeRoute(coordinates) {
  try {
    const response = await optimizationClient
      .getOptimization({
        profile: 'driving',
        coordinates: coordinates,
        roundtrip: false
      })
      .send();

    return response.body;
  } catch (error) {
    console.error('Error optimizing route:', error);
    throw error;
  }
}

module.exports = { getDirections, optimizeRoute };