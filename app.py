import logging
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

def fetch_flight_info(carrier_code, flight_number):
    # Define the URL for scraping
    url = f"https://www.flightaware.com/live/flight/{carrier_code}{flight_number}/history/20240628/1030Z/KSTL/KMCO"
    app.logger.debug(f"Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting necessary information (example, you might need to adjust selectors based on actual HTML structure)
        flight_data = {
            'carrier': 'Southwest Airlines',
            'flight_number': flight_number,
            'departure_airport': soup.find('span', {'id': 'departureAirport'}).text,
            'arrival_airport': soup.find('span', {'id': 'arrivalAirport'}).text,
            'scheduled_departure': soup.find('span', {'id': 'scheduledDeparture'}).text,
            'scheduled_arrival': soup.find('span', {'id': 'scheduledArrival'}).text,
            'status': soup.find('span', {'id': 'status'}).text,
        }
        return flight_data
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f'HTTP error occurred: {http_err}')
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        app.logger.error(f'An error occurred: {err}')
        return {'error': f'An error occurred: {err}'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flight-info/<carrier_code>/<flight_number>'
