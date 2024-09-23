from flask import Flask, jsonify, request
import json
import pandas as pd 
import os
import requests
import datetime

app = Flask(__name__)

@app.route('/AI', methods=['POST'])
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
    combined_datetime = datetime.datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M:%S')

    # Convert combined datetime to string in the desired format
    combined_datetime_str = combined_datetime.strftime('%Y-%m-%d %H:%M:%S')

    ordered_array = [frequency, phase_angle, real_power, reactive_power, rms_current, rms_voltage]

    # Create a dictionary with the desired format
    data_dict = {
        "features": ordered_array,
        "time": combined_datetime_str
    }

    # Send POST request
    url = os.environ.get('AI_API_URL', 'http://localhost:6000')
    response = requests.post(url, json=data_dict)

    return jsonify(response.json())

@app.route('/CSV', methods=['POST'])
def csv_route():
    print('StartCSV')
    data = request.get_json()

    appliance_type = data.get('Appliance')
    date_1 = data.get('Begin Date')
    date_2 = data.get('Ending Date')
    
    # TODO: Implement CSV processing logic here
    
    return jsonify({"message": "CSV processing completed", "appliance": appliance_type, "start": date_1, "end": date_2})

if __name__ == '__main__':
    app.run(debug=True, port=5000)