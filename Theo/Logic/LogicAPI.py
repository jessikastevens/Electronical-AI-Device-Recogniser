from dotenv import load_dotenv
import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime
import json

appliance_terms = {
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

appliance_tags = {
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

# Load .env variables
load_dotenv()

app = Flask(__name__)

@app.route('/Lai', methods=['POST'])
def ai_route():
    print('StartAI')
    data = request.get_json()
    
    real_power = data.get('Real Power')
    reactive_power = data.get('Reactive Power')
    rms_current = data.get('RMS Current')
    frequency = data.get('Frequency')
    rms_voltage = data.get('RMS Voltage')
    phase_angle = data.get('Phase Angle')
    date = data.get('Date')
    time = data.get('time')

    # Combine date and time
    combined_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')
    combined_datetime_str = combined_datetime.strftime('%Y-%m-%d %H:%M:%S')

    ordered_array = [frequency, phase_angle, real_power, reactive_power, rms_current, rms_voltage]

    data_dict = {
        "features": ordered_array,
        "time": combined_datetime_str
    }

    # Send POST request to AI API
    url = os.getenv('AI_API_URL')

    response = requests.post(url, json=data_dict)
    
    response = response.json()

    predicted_class = response['predicted_class']

    raw_prediction = response['raw_prediction']
    formatted_prediction = {}

    for i in range(len(raw_prediction)):
        appliance_name = appliance_tags[i + 1]
        probability = round(raw_prediction[i], 2)  # Round to 2 decimal places
        formatted_prediction[appliance_name] = probability

    predicted_appliance = appliance_tags[predicted_class + 1]

    return jsonify({
        "predicted_appliance": predicted_appliance,
        "raw_predictions": formatted_prediction
    })

    formatted_prediction = {}

    for i in range(len(raw_prediction)):

        appliance_name = appliance_tags[i + 1]
        probability = raw_prediction[i]
        formatted_prediction[appliance_name] = probability


    predicted_appliance = appliance_tags[predicted_class + 1]

    return jsonify({
        "predicted_appliance": predicted_appliance,
        "raw_predictions": formatted_prediction
    })


@app.route('/Lcsv', methods=['POST'])
def csv_route():
    print('StartCSV')
    data = request.get_json()

    # Send POST request to CSV API
    url = os.getenv('CSV_API_URL')


    Appliance = data.get("Appliance")
    start = data.get("start")
    end = data.get("end")


    payload = json.dumps({
        "Appliance": appliance_terms[Appliance],
        "start": start,
        "end": end
    })


    response = requests.post(url, data=jsonify(payload))






    # return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)