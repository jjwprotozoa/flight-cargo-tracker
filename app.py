import logging
from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

USE_API = False  # Set this to True if you want to use the API, False for scraping

def fetch_flight_info_api(carrier_code, flight_number):
    app_id = os.getenv('FLIGHTSTATS_APP_ID')
    app_key = os.getenv('FLIGHTSTATS_APP_KEY')
    url = f"https://api.flightstats.com/flex/flightstatus/rest/v2/json/flight/status/{carrier_code}/{flight_number}/arr?appId={app_id}&appKey={app_key}"
    app.logger.debug(f"Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            'carrier': 'Southwest Airlines',
            'flight_number': flight_number,
            'departure_airport': data.get('departureAirport', 'N/A'),
            'arrival_airport': data.get('arrivalAirport', 'N/A'),
            'scheduled_departure': data.get('scheduledDeparture', 'N/A'),
            'scheduled_arrival': data.get('scheduledArrival', 'N/A'),
            'status': data.get('status', 'N/A'),
        }
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f'HTTP error occurred: {http_err}')
        return {'error': f'HTTP error occurred: {http_err}'}
    except Exception as err:
        app.logger.error(f'An error occurred: {err}')
        return {'error': f'An error occurred: {err}'}

def fetch_flight_info_scrape(carrier_code, flight_number):
    url = f"https://www.flightaware.com/live/flight/{carrier_code}{flight_number}/history/20240628/1030Z/KSTL/KMCO"
    app.logger.debug(f"Request URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        flight_data = {
            'carrier': 'Southwest Airlines',
            'flight_number': flight_number,
            'departure_airport': soup.find('span', {'id': 'departureAirport'}).text if soup.find('span', {'id': 'departureAirport'}) else 'N/A',
            'arrival_airport': soup.find('span', {'id': 'arrivalAirport'}).text if soup.find('span', {'id': 'arrivalAirport'}) else 'N/A',
            'scheduled_departure': soup.find('span', {'id': 'scheduledDeparture'}).text if soup.find('span', {'id': 'scheduledDeparture'}) else 'N/A',
            'scheduled_arrival': soup.find('span', {'id': 'scheduledArrival'}).text if soup.find('span', {'id': 'scheduledArrival'}) else 'N/A',
            'status': soup.find('span', {'id': 'status'}).text if soup.find('span', {'id': 'status'}) else 'N/A',
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

@app.route('/flight-info/<carrier_code>/<flight_number>')
def flight_info(carrier_code, flight_number):
    carrier_code = carrier_code.upper()
    app.logger.debug(f"Fetching info for {carrier_code} {flight_number}")
    
    if USE_API:
        flight_data = fetch_flight_info_api(carrier_code, flight_number)
    else:
        flight_data = fetch_flight_info_scrape(carrier_code, flight_number)
    
    app.logger.debug(f"Fetched data: {flight_data}")
    return jsonify(flight_data)

if __name__ == '__main__':
    app.run(debug=True)
