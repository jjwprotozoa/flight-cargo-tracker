import os
import requests
from flask import Flask, render_template, request, jsonify
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

FLIGHTSTATS_APP_ID = app.config['FLIGHTSTATS_APP_ID']
FLIGHTSTATS_APP_KEY = app.config['FLIGHTSTATS_APP_KEY']
MAPBOX_ACCESS_TOKEN = app.config['MAPBOX_ACCESS_TOKEN']

FLIGHT_STATUS_API_ENDPOINT = "https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight_number}/arr/{year}/{month}/{day}"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def fetch_flight_status(carrier, flight_number, year, month, day):
    url = FLIGHT_STATUS_API_ENDPOINT.format(carrier=carrier, flight_number=flight_number, year=year, month=month, day=day)
    params = {
        'appId': FLIGHTSTATS_APP_ID,
        'appKey': FLIGHTSTATS_APP_KEY,
    }
    logger.debug(f'Request URL: {url}')

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        logger.debug(f'API Response: {response.json()}')
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        logger.error(f'Other error occurred: {err}')
        return {'error': f'Other error occurred: {err}'}

@app.route('/')
def index():
    return render_template('index.html', mapbox_access_token=MAPBOX_ACCESS_TOKEN)

@app.route('/flight-info/<carrier>/<flight_number>', methods=['GET'])
def get_flight_info(carrier, flight_number):
    from datetime import datetime
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    flight_data = fetch_flight_status(carrier, flight_number, year, month, day)
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
