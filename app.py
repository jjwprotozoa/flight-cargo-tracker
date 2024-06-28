from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_flight_info', methods=['POST'])
def get_flight_info():
    flight_number = request.form['flight_number']
    url = f"https://opensky-network.org/api/states/all"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data and data['states']:
            filtered_data = [state for state in data['states'] if state[0] == flight_number]
            if filtered_data:
                return jsonify(filtered_data)
            else:
                return jsonify({"error": "No data found for this flight number"}), 404
        else:
            return jsonify({"error": "No data available"}), 404
    else:
        return jsonify({"error": "Could not retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
