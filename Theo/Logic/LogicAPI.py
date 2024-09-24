from dotenv import load_dotenv
import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime

appliance_names = {
    'Fridges_and_freezers': 'Fridges & Freezers',
    'Televisions_(LCD_or_LED)': 'TVs',
    'Hi-Fi_systems_(with_CD_players)': 'Hi-Fi systems (with CD players)',
    'Laptops_(via_chargers)': 'Laptops',
    'Computers_stations_(with_monitors)': 'Computer stations',
    'Lamps_(compact_fluorescent)': 'Compact fluorescent lamps',
    'Microwave_ovens': 'Microwaves',
    'Coffee_machines': 'Coffee machines',
    'Mobile_phones_(via_chargers)': 'Mobile phones',
    'Printers': 'Printers',
    'Fans': 'Fans',
    'Kettles': 'Kettles',
    'Lamps_(incandescent)': 'Incandescent lamps',
    'Monitors': 'TVs',
    'Shavers_(via_chargers)': 'Shavers'
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

    # Transform the dat
    transformed_data = {
        "appliance_type": appliance_names.get(data['Appliance'], data['Appliance']),
        "start": datetime.utcfromtimestamp(data['Start_time']).strftime("%Y-%m-%d %H:%M:%S"),
        "end": datetime.utcfromtimestamp(data['End_time']).strftime("%Y-%m-%d %H:%M:%S")
    }

    url = os.getenv('CSV_API_URL')
    response = requests.post(url, json=transformed_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
