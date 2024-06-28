import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Set environment variables for the API credentials
FLIGHTSTATS_APP_ID = os.getenv('FLIGHTSTATS_APP_ID', 'your_app_id_here')
FLIGHTSTATS_APP_KEY = os.getenv('FLIGHTSTATS_APP_KEY', 'your_app_key_here')

# Define the API endpoint template
FLIGHT_STATUS_API_ENDPOINT = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight_number}/arr"

def fetch_flight_status(carrier, flight_number):
    # Construct the URL with the necessary parameters
    url = FLIGHT_STATUS_API_ENDPOINT.format(carrier=carrier, flight_number=flight_number)
    params = {
        'appId': FLIGHTSTATS_APP_ID,
        'appKey': FLIGHTSTATS_APP_KEY,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f'HTTP error occurred: {http_err}')
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        app.logger.error(f'Other error occurred: {err}')
        return {'error': f'Other error occurred: {err}'}

@app.route('/flight-info/<carrier>/<flight_number>', methods=['GET'])
def get_flight_info(carrier, flight_number):
    flight_data = fetch_flight_status(carrier, flight_number)
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
