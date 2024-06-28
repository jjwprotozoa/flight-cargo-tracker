import os
import requests
from flask import Flask, jsonify, render_template
import logging
from datetime import datetime

app = Flask(__name__)

# Set environment variables for the API credentials
FLIGHTSTATS_APP_ID = os.getenv('FLIGHTSTATS_APP_ID', 'your_app_id_here')
FLIGHTSTATS_APP_KEY = os.getenv('FLIGHTSTATS_APP_KEY', 'your_app_key_here')

# Define the API endpoint template
FLIGHT_STATUS_API_ENDPOINT = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight_number}/arr/{year}/{month}/{day}"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def fetch_flight_status(carrier, flight_number, year, month, day):
    # Construct the URL with the necessary parameters
    url = FLIGHT_STATUS_API_ENDPOINT.format(carrier=carrier, flight_number=flight_number, year=year, month=month, day=day)
    params = {
        'appId': FLIGHTSTATS_APP_ID,
        'appKey': FLIGHTSTATS_APP_KEY,
    }
    logger.debug(f'Request URL: {url}')

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        logger.debug(f'API Response: {response.json()}')
        remaining_requests = response.headers.get('x-ratelimit-remaining')
        total_requests = response.headers.get('x-ratelimit-limit')
        api_limits = {
            'remaining': remaining_requests,
            'limit': total_requests
        }
        data = response.json()
        data['api_limits'] = api_limits
        return data
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        return {'error': f'Other error occurred: {err}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info/<carrier>/<flight_number>', methods=['GET'])
def get_flight_info(carrier, flight_number):
    # Using current date for simplicity; adjust as needed
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    flight_data = fetch_flight_status(carrier, flight_number, year, month, day)
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
