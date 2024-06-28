from flask import Flask, jsonify, request
import os
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Flight Cargo Tracker API"

@app.route('/flight-info/<carrier>/<flight>', methods=['GET'])
def get_flight_info(carrier, flight):
    app_id = os.getenv('FLIGHTSTATS_APP_ID')
    app_key = os.getenv('FLIGHTSTATS_APP_KEY')
    url = f'https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight}?appId={app_id}&appKey={app_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Flight not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
