from flask import Flask, jsonify, request 
import requests 
import os 
 
app = Flask(__name__) 
 
FLIGHTSTATS_APP_ID = os.getenv('FLIGHTSTATS_APP_ID') 
FLIGHTSTATS_APP_KEY = os.getenv('FLIGHTSTATS_APP_KEY') 
SOUTHWEST_CARGO_API_KEY = os.getenv('SOUTHWEST_CARGO_API_KEY') 
 
def get_flight_info(flight_number): 
    response = requests.get(flightstats_url) 
    return jsonify(response.json()) 
 
def get_cargo_info(tracking_id): 
    cargo_url = f'https://rapidapi.p.rapidapi.com/cargo/v1/track/{tracking_id}' 
    headers = { 
        'Authorization': f'Bearer {SOUTHWEST_CARGO_API_KEY}', 
        'x-rapidapi-host': 'sw-cargo-tracking.p.rapidapi.com', 
        'x-rapidapi-key': SOUTHWEST_CARGO_API_KEY 
    } 
    response = requests.get(cargo_url, headers=headers) 
    return jsonify(response.json()) 
 
if __name__ == '__main__': 
    app.run(debug=True) 
