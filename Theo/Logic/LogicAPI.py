from dotenv import load_dotenv
import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime
import json
import logging

load_dotenv()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APPLIANCE_TERMS = {
    'Coffee machines': 'Coffee_machines',
    'Computer stations': 'Computers_stations_(with_monitors)',
    'Fans': 'Fans',
    'Fridges & Freezers': 'Fridges_and_freezers',
    'Hi-Fi systems (with CD players)': 'Hi-Fi_systems_(with_CD_players)',
    'Kettles': 'Kettles',
    'Compact fluorescent lamps': 'Lamps_(compact_fluorescent)',
    'Incandescent lamps': 'Lamps_(incandescent)',
    'Laptops': 'Laptops_(via_chargers)',
    'Microwaves': 'Microwave_ovens',
    'Mobile phones': 'Mobile_phones_(via_chargers)',
    'Monitors': 'Monitors',
    'Printers': 'Printers',
    'Shavers': 'Shavers_(via_chargers)',
    'TVs': 'Televisions_(LCD_or_LED)'
}

APPLIANCE_TAGS = {
    1: 'Coffee Machine',
    2: 'Computer Station',
    3: 'Fan',
    4: 'Fridge / Freezer',
    5: 'Hi-Fi System',
    6: 'Kettle',
    7: 'CFL Lamp',
    8: 'Incandescent Lamp',
    9: 'Laptop Charger',
    10: 'Microwave',
    11: 'Phone Charger',
    12: 'Monitor',
    13: 'Printer',
    14: 'Shaver Charger',
    15: 'LCD/LED TV'
}


@app.route('/ai', methods=['POST'])
def ai_route():
    try:
        data = request.get_json()
        
        real_power = float(data['Real Power'])
        reactive_power = float(data['Reactive Power'])
        rms_current = float(data['RMS Current'])
        frequency = float(data['Frequency'])
        rms_voltage = float(data['RMS Voltage'])
        phase_angle = float(data['Phase Angle'])
        date = data['Date']
        time = data['time']

        combined_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
        combined_datetime_str = combined_datetime.strftime('%Y-%m-%d %H:%M:%S')

        ordered_array = [frequency, phase_angle, real_power, reactive_power, rms_current, rms_voltage]

        data_dict = {
            "features": ordered_array,
            "time": combined_datetime_str
        }

        ai_api_url = os.getenv('AI_API_URL')
        if not ai_api_url:
            logger.error("AI_API_URL environment variable is not set")
            return jsonify({"error": "AI API URL is not configured"}), 500

        logger.info(f"Attempting to call AI API at URL: {ai_api_url}")
        response = requests.post(ai_api_url, json=data_dict, timeout=30)
        response.raise_for_status()
        ai_response = response.json()

        predicted_class = ai_response['predicted_class']
        raw_prediction = ai_response['raw_prediction']

        formatted_prediction = {
            APPLIANCE_TAGS[i + 1]: round(prob, 2)
            for i, prob in enumerate(raw_prediction)
        }

        predicted_appliance = APPLIANCE_TAGS[predicted_class + 1]

        return jsonify({
            "predicted_appliance": predicted_appliance,
            "raw_predictions": formatted_prediction
        })
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling AI API: {str(e)}")
        return jsonify({"error": "Failed to call AI API"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in AI route: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
'''
# @app.route('/csv', methods=['POST'])
@app.route('/', methods=['POST'])
def csv_route():
    try:
        logger.info('CSV route started')
        data = request.get_json()

        payload = {
            "Appliances": [APPLIANCE_TERMS[appliance] for appliance in data['Appliances']],
            "start": data['start'],
            "end": data['end'],
            "graph_type": data['graph_type'],
            "num_graphs": data['num_graphs']
        }
        logger.info(f"CSV payload: {payload}")

        csv_api_url = os.getenv('CSV_API_URL')
        if not csv_api_url:
            logger.error("CSV_API_URL environment variable is not set")
            return jsonify({"error": "CSV API URL is not configured"}), 500

        logger.info(f"Attempting to call CSV API at URL: {csv_api_url}")
        response = requests.post(csv_api_url, json=payload, timeout=30)
        response.raise_for_status()
        logger.info(f'CSV API response status: {response.status_code}')
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling CSV API: {str(e)}")
        return jsonify({"error": "Failed to call CSV API"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in CSV route: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    app.run(port=port)