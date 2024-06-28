from flask import Flask, jsonify, request
import requests  # Import the requests library

app = Flask(__name__)

FLIGHTSTATS_APP_ID = "8808bb23"  # Replace with your actual FlightStats App ID
FLIGHTSTATS_APP_KEY = "b138ee0863859350ffb19c540be19713"  # Replace with your actual FlightStats App Key
SOUTHWEST_CARGO_API_KEY = "59947e53eemsh783374ca03c5bdap101325jsn1face78e2b3f"  # Replace with your actual Southwest Cargo API Key

@app.route('/')
def home():
    return "Flight Cargo Tracker is running!"

@app.route('/flight-info/<flight_number>')
def get_flight_info(flight_number):
    response = requests.get(f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{flight_number}?appId={FLIGHTSTATS_APP_ID}&appKey={FLIGHTSTATS_APP_KEY}")
    return jsonify(response.json())

@app.route('/cargo-info/<waybill_number>')
def get_cargo_info(waybill_number):
    response = requests.get(f"https://api.southwestcargo.com/tracking/{waybill_number}?apiKey={SOUTHWEST_CARGO_API_KEY}")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
