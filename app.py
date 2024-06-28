from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/flight-info/<carrierCode>/<flightNumber>', methods=['GET'])
def get_flight_info(carrierCode, flightNumber):
    app_id = os.getenv('FLIGHTSTATS_APP_ID')
    app_key = os.getenv('FLIGHTSTATS_APP_KEY')
    url = f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrierCode}/{flightNumber}/dep?appId={app_id}&appKey={app_key}"
    
    response = requests.get(url)
    print(f"URL: {url}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
