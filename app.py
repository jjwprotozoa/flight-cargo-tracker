from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    flight_number = request.form['flight_number']
    url = f"https://opensky-network.org/api/states/all?icao24={flight_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        return jsonify({"error": "Could not retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
