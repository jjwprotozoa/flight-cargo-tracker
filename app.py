from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    flight_number = request.form['flight_number']
    airline_code = request.form['airline_code']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    
    start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timestamp())
    end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timestamp())
    
    url = f"https://opensky-network.org/api/flights/callsign?callsign={airline_code}{flight_number}&begin={start_timestamp}&end={end_timestamp}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "No data found for this flight number"}), 404
    else:
        return jsonify({"error": "Could not retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
