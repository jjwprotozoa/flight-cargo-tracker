from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime, timezone
import os

class Config:
    TRACKINGMORE_API_KEY = os.environ.get('TRACKINGMORE_API_KEY') or 'fld2md4s-vrr0-5egt-mvbi-3rx546nbx105'
    WEATHERAPI_KEY = os.environ.get('WEATHERAPI_KEY') or 'b9ec000c25f642d0a5c180924242806'
    MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY') or 'pk.eyJ1IjoiZmxkaW52Z3JwIiwiYSI6ImNscjl2cmw4bDA1eGQya3Q2cThhejEyN2kifQ.K0cDZ_0cUwJktVaAQZm1pA'

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('index.html', mapbox_key=app.config['MAPBOX_API_KEY'])

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    flight_number = request.form['flight_number']
    airline_code = request.form['airline_code']
    
    callsign = f"{airline_code}{flight_number}"
    current_time = int(datetime.now(timezone.utc).timestamp())
    url = f"https://opensky-network.org/api/states/all?time={current_time}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        flight_data = next((state for state in data['states'] if state[1] and state[1].strip() == callsign), None)
        
        if flight_data:
            flight_info = {
                "icao24": flight_data[0],
                "callsign": flight_data[1],
                "origin_country": flight_data[2],
                "longitude": flight_data[5],
                "latitude": flight_data[6],
                "altitude": flight_data[7],
                "velocity": flight_data[9],
                "heading": flight_data[10],
                "vertical_rate": flight_data[11]
            }
            return jsonify(flight_info)
        else:
            return jsonify({"error": "Flight not found or not currently tracked"}), 404
    
    except requests.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500

@app.route('/track_cargo', methods=['POST'])
def track_cargo():
    waybill_number = request.form['waybill_number']
    
    tracking_url = "https://api.trackingmore.com/v2/trackings/realtime"
    headers = {
        "Content-Type": "application/json",
        "Trackingmore-Api-Key": app.config['TRACKINGMORE_API_KEY']
    }
    payload = {
        "tracking_number": waybill_number,
        "courier_code": "swacargo"  # Adjust this as needed
    }
    
    try:
        response = requests.post(tracking_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data['meta']['code'] == 200 and data['data']:
            return jsonify(data['data'][0])
        else:
            return jsonify({"error": "Cargo information not found"}), 404
    
    except requests.RequestException as e:
        return jsonify({"error": f"Tracking API request failed: {str(e)}"}), 500

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Orlando')  # Default to Orlando if no city provided
    api_key = app.config['WEATHERAPI_KEY']
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        app.logger.error(f"Weather API request failed: {str(e)}")
        return jsonify({"error": f"Weather API request failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
