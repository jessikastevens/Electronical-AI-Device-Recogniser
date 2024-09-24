from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

DATA_FILE = 'Theo/CSV/acs-f2-dataset 1.csv'
data = None

def load_data():
    global data
    data = pd.read_csv(DATA_FILE)
    data['time'] = pd.to_datetime(data['time'])

@app.before_first_request
def initialize():
    load_data()

@app.route('/', methods=['POST'])
def api():
    request_data = request.get_json()

    equipment = request_data['Appliance']
    start_date = pd.to_datetime(request_data['start'])
    end_date = pd.to_datetime(request_data['end'])

    filtered_data = data[(data['time'] >= start_date) & 
                         (data['time'] <= end_date) & 
                         (data['equipment'] == equipment)]
    
    columns = list(filtered_data.columns)
    
    response = {
        "columns": columns,
        "data": filtered_data.values.tolist()
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=7000)