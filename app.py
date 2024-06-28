import logging
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def scrape_flight_info(carrier_code, flight_number):
    # Replace with the actual URL of the website you want to scrape
    url = f"https://www.example.com/flight-status/{carrier_code}/{flight_number}"
    app.logger.debug(f"Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example of extracting flight information; update selectors as needed
        flight_info = {
            'carrier': soup.find('div', {'id': 'carrier'}).text.strip(),
            'flight_number': soup.find('div', {'id': 'flight_number'}).text.strip(),
            'departure_airport': soup.find('div', {'id': 'departure_airport'}).text.strip(),
            'arrival_airport': soup.find('div', {'id': 'arrival_airport'}).text.strip(),
            'scheduled_departure': soup.find('div', {'id': 'scheduled_departure'}).text.strip(),
            'scheduled_arrival': soup.find('div', {'id': 'scheduled_arrival'}).text.strip(),
            'status': soup.find('div', {'id': 'status'}).text.strip(),
        }

        app.logger.debug(f"Scraped Data: {flight_info}")
        return flight_info

    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        app.logger.error(f"An error occurred: {err}")
        return {'error': f'An error occurred: {err}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info/<carrier_code>/<flight_number>')
def flight_info(carrier_code, flight_number):
    carrier_code = carrier_code.upper()
    flight_data = scrape_flight_info(carrier_code, flight_number)
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
