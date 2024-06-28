from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Replace these with your actual FlightStats API credentials
FLIGHTSTATS_APP_ID = "8808bb23"
FLIGHTSTATS_APP_KEY = "b138ee0863859350ffb19c540be19713"

@app.route('/')
def index():
    return "Flight Cargo Tracker is running!"

@app.route('/flight-info/<carrier_code>/<flight_number>', methods=['GET'])
def get_flight_info(carrier_code, flight_number):
    url = f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier_code}/{flight_number}/arr?appId={FLIGHTSTATS_APP_ID}&appKey={FLIGHTSTATS_APP_KEY}"
    response = requests.get(url)

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    if response.status_code == 200:
        try:
            return jsonify(response.json())
        except ValueError as e:
            print(f"JSON decode error: {e}")
            return jsonify({"error": "Error decoding JSON response"}), 500
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
