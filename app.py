from flask import Flask, jsonify, request
import requests  # Import the requests library

app = Flask(__name__)

@app.route('/')
def home():
    return "Flight Cargo Tracker is running!"

@app.route('/flight-info/<flight_number>')
def get_flight_info(flight_number):
    response = requests.get(f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{flight_number}?appId=YOUR_FLIGHTSTATS_APP_ID&appKey=YOUR_FLIGHTSTATS_APP_KEY")
    return jsonify(response.json())

@app.route('/cargo-info/<waybill_number>')
def get_cargo_info(waybill_number):
    response = requests.get(f"https://api.southwestcargo.com/tracking/{waybill_number}?apiKey=YOUR_SOUTHWEST_CARGO_API_KEY")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
