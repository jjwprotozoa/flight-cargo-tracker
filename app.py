import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MAPBOX_KEY = os.getenv('MAPBOX_KEY')
TRACKINGMORE_API_KEY = os.getenv('TRACKINGMORE_API_KEY')
OPENSKY_USERNAME = os.getenv('OPENSKY_USERNAME')
OPENSKY_PASSWORD = os.getenv('OPENSKY_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html', mapbox_key=MAPBOX_KEY)

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    airline_code = request.form.get('airline_code')
    flight_number = request.form.get('flight_number')
    
    # This is a placeholder. You should implement the actual API call to OpenSky or your preferred flight tracking API
    # For now, we'll return mock data
    mock_data = {
        "icao24": "a1b2c3",
        "callsign": f"{airline_code}{flight_number}",
        "origin_country": "United States",
        "longitude": -80.9,
        "latitude": 28.1,
        "altitude": 10000,
        "velocity": 200,
        "heading": 90,
        "vertical_rate": 0
    }
    
    return jsonify(mock_data)

@app.route('/track_air_waybill', methods=['POST'])
def track_air_waybill():
    tracking_number = request.form.get('tracking_number')
    carrier_code = request.form.get('carrier_code')
    
    api_url = "https://api.trackingmore.com/v2/trackings/get"
    
    headers = {
        "Content-Type