from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Flight Cargo Tracker is running!"

@app.route('/flight-info/<flight_number>', methods=['GET'])
def get_flight_info(flight_number):
    # Replace with actual API call to fetch flight information
    response = requests.get(f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{flight_number}?appId=YOUR_FLIGHTSTATS_APP_ID&appKey=YOUR_FLIGHTSTATS_APP_KEY")
    return jsonify(response.json())

@app.route('/cargo-info/<waybill_number>', methods=['GET'])
def get_cargo_info(waybill_number):
    # Replace with actual API call to fetch cargo information
    response = requests.get(f"https://rapidapi.com/developer/authorization/default-application_9293627?trackingId={waybill_number}&apikey=YOUR_SOUTHWEST_CARGO_API_KEY")
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
