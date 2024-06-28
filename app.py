from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

FLIGHTSTATS_APP_ID = 'your_flightstats_app_id'
FLIGHTSTATS_APP_KEY = 'your_flightstats_app_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flight-info/<carrier>/<flight_number>')
def flight_info(carrier, flight_number):
    url = f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier}/{flight_number}/arr"
    params = {
        'appId': FLIGHTSTATS_APP_ID,
        'appKey': FLIGHTSTATS_APP_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': f'HTTP error occurred: {response.status_code} {response.reason}'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
