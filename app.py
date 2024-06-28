import logging
from flask import Flask, render_template, jsonify, request
import requests
import os
from urllib.parse import quote

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Set environment variables for the API credentials
OPENSKY_USERNAME = os.getenv('OPENSKY_USERNAME', 'your_opensky_username')
OPENSKY_PASSWORD = os.getenv('OPENSKY_PASSWORD', 'your_opensky_password')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info/<icao24>')
def flight_info(icao24):
    url = f"https://opensky-network.org/api/states/all?icao24={quote(icao24)}"
    app.logger.debug(f"Request URL: {url}")
    try:
        response = requests.get(url, auth=(OPENSKY_USERNAME, OPENSKY_PASSWORD))
        response.raise_for_status()
        data = response.json()
        app.logger.debug(f"API Response: {data}")
        return jsonify(data)
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 404
    except Exception as err:
        app.logger.error(f"An error occurred: {err}")
        return jsonify({'error': f'An error occurred: {err}'}), 500

if __name__ == '__main__':
    app.run()
