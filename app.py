from flask import Flask, render_template, request, jsonify
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    flight_number = request.form['flight_number']
    logging.info(f"Received request for flight number: {flight_number}")
    api_url = f"https://opensky-network.org/api/states/all?icao24={flight_number}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Data received: {data}")
        return jsonify(data)
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return jsonify({'error': f'HTTP error occurred: {http_err}'})
    except Exception as err:
        logging.error(f"An error occurred: {err}")
        return jsonify({'error': f'An error occurred: {err}'})

if __name__ == '__main__':
    app.run(debug=True)
