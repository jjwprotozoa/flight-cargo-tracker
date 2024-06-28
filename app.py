import requests
from flask import Flask, render_template, jsonify, request
import os
from urllib.parse import quote as url_quote  # Updated import

app = Flask(__name__)

# OpenSky Network API credentials
USERNAME = os.getenv('OPENSKY_USERNAME', 'your_opensky_username')
PASSWORD = os.getenv('OPENSKY_PASSWORD', 'your_opensky_password')

# Function to fetch flight information using the OpenSky Network API
def fetch_flight_info(flight_number):
    url = f'https://opensky-network.org/api/states/all'
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        data = response.json()
        # Filter the data for the specific flight number
        for flight in data['states']:
            if flight_number in str(flight[1]):  # Assuming flight number matches callsign
                return {
                    'icao24': flight[0],
                    'callsign': flight[1].strip(),
                    'origin_country': flight[2],
                    'time_position': flight[3],
                    'last_contact': flight[4],
                    'longitude': flight[5],
                    'latitude': flight[6],
                    'baro_altitude': flight[7],
                    'on_ground': flight[8],
                    'velocity': flight[9],
                    'true_track': flight[10],
                    'vertical_rate': flight[11],
                    'sensors': flight[12],
                    'geo_altitude': flight[13],
                    'squawk': flight[14],
                    'spi': flight[15],
                    'position_source': flight[16]
                }
        return {'error': 'Flight not found'}
    else:
        return {'error': f'HTTP error occurred: {response.status_code} {response.reason}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info', methods=['POST'])
def flight_info():
    flight_number = request.form['flight_number'].upper()
    app.logger.debug(f'Fetching info for flight number: {flight_number}')
    data = fetch_flight_info(flight_number)
    app.logger.debug(f'Fetched data: {data}')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
