from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Replace these with your actual RapidAPI key and host
RAPIDAPI_KEY = "59947e53eemsh783374ca03c5bdap101325jsn1face78e2b3f"
RAPIDAPI_HOST = "southwest.p.rapidapi.com"

@app.route('/')
def index():
    return "Flight Cargo Tracker is running!"

@app.route('/flight-info/<flight_number>', methods=['GET'])
def get_flight_info(flight_number):
    url = f"https://{RAPIDAPI_HOST}/flights/{flight_number}"

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    querystring = {"currency": "USD", "adults": "1", "seniors": "0"}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
