from flask import Flask, jsonify, request
import os
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return "Flight Cargo Tracker API"

@app.route('/flight-info/<carrier>/<flight>', methods=['GET'])
def get_flight_info(carrier, flight):
    app_id = os.getenv('FLIGHTSTATS_APP_ID')
    app_key = os.getenv('FLIGHTSTATS_APP_KEY')
    url = f'https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight}/arr?appId={app_id}&appKey={app_key}'
    
    logging.debug(f'Request URL: {url}')
    
    try:
        response = requests.get(url)
        logging.debug(f'API Response: {response.json()}')
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            error_message = response.json().get('error', {}).get('errorMessage', 'Flight not found')
            logging.error(f'Error: {error_message}')
            return jsonify({'error': error_message}), response.status_code
    except Exception as e:
        logging.error(f'Exception: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
