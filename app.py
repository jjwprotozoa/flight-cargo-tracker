from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

RAPIDAPI_KEY = "35a4dab26fmshf94d4a957b08192p1c19fcjsn766023171635"
RAPIDAPI_HOST = "rapidapi.com"

@app.route('/flight-info/<flight_number>', methods=['GET'])
def get_flight_info(flight_number):
    url = f"https://{RAPIDAPI_HOST}/flight-status/{flight_number}"
    headers = {
        "X-RapidAPI-Host": RAPIDAPI_HOST,
        "X-RapidAPI-Key": RAPIDAPI_KEY
    }
    response = requests.get(url, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
