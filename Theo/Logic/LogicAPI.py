from dotenv import load_dotenv
import os
import requests
from flask import Flask, jsonify, request
from datetime import datetime

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
    url = os.getenv('AI_API_URL')  # Use os.getenv to get environment variable
    if not url:
        return jsonify({"error": "AI_API_URL not set"}), 500

    response = requests.post(url, json=data_dict)

    return jsonify(response.json())

@app.route('/Lcsv', methods=['POST'])
def csv_route():
    print('StartCSV')
    data = request.get_json()

    # Send POST request to CSV API
    url = os.getenv('CSV_API_URL')
    if not url:
        return jsonify({"error": "CSV_API_URL not set"}), 500

    response = requests.post(url, json=data)

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
