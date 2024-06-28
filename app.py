import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"
RAPIDAPI_HOST = "exampleapi.p.rapidapi.com"  # Replace this with the actual host

@app.route('/flight-info/<flight_number>', methods=['GET'])
def get_flight_info(flight_number):
    url = f"https://{RAPIDAPI_HOST}/flight/status/{flight_number}"
    headers = {
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run()
