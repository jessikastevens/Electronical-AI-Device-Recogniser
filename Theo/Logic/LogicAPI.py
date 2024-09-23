from flask import Flask, jsonify, request
import json
import pandas as pd 
import os
import requests

app = Flask(__name__)

@app.route('/AI', methods=['GET'])
def ai_route():
    if request.method == 'GET':
        print('StartAI')
        data = request.get_json()
        
        real_power = data.get('Real Power')
        reactive_power = data.get('Reactive Power')
        rms_current = data.get('RMS Current')
        frequency = data.get('Frequency')
        rms_voltage = data.get('RMS Voltage')
        phase_angle = data.get('Phase Angle')
        
        ordered_array = [frequency, phase_angle, real_power, reactive_power, rms_current, rms_voltage]
        
        # Convert list to JSON
        data_json = json.dumps(ordered_array)

        # # Send GET request
        # url = os.environ.get('AI_API_URL')
        # response = requests.get(url, json=data_json)

        # Return to front end
        return data_json

@app.route('/CSV', methods=['GET', 'POST'])
def csv_route():
    print('StartCSV')
    if request.method == 'POST':
        print('Post')
    
        data = request.get_json()
    
        appliance_type = data.get('Appliance')
        date_1 = data.get('Begin Date')
        date_2 = data.get('Ending Date')
        
        # Process the data here
        
        return jsonify({"message": "Data received successfully"})
    
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True)