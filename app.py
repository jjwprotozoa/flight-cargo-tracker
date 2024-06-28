from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info/<carrier_code>/<flight_number>')
def flight_info(carrier_code, flight_number):
    carrier_code = carrier_code.upper()  # Ensure carrier code is uppercase
    app_id = os.getenv('FLIGHTSTATS_APP_ID')
    app_key = os.getenv('FLIGHTSTATS_APP_KEY')
    url = f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier_code}/{flight_number}/arr?appId={app_id}&appKey={app_key}"
    app.logger.debug(f"Request URL: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        app.logger.debug(f"API Response: {data}")
        return jsonify(data)
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 404
    except Exception as err:
        app.logger.error(f"An error occurred: {err}")
        return jsonify({'error': f'An error occurred: {err}'}), 500

if __name__ == '__main__':
    app.run()
