from dotenv import load_dotenv
import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__)

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

    response = requests.post(os.getenv('AI_API_URL'), json=data_dict)
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

@app.route('/csv', methods=['POST'])
def csv_route():
    print('CSV START')
    data = request.get_json()

    payload = {
        "Appliance": APPLIANCE_TERMS[data['Appliance']],
        "start": data['start'],
        "end": data['end']
    }
    print(payload)
    response = requests.post(os.getenv('CSV_API_URL'), json=payload)
    print(f'Send {response}')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True , port=5000)