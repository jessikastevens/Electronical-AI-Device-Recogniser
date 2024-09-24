from flask import Flask, jsonify, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = pd.read_csv('Theo/CSV/acs-f2-dataset 1.csv')
    data['time'] = pd.to_datetime(data['time'])

    request_data = request.get_json()

    equipment = request_data.get('Appliance')
    start_date = pd.to_datetime(request_data.get('Start_time'))
    end_date = pd.to_datetime(request_data.get('End_time'))

    filtered_data = data[(data['time'] >= start_date) & 
                         (data['time'] <= end_date) & 
                         (data['equipment'] == equipment)]
    
    columns = list(filtered_data.columns)
    filtered_data = filtered_data[columns]

    response = {
        "columns": columns,
        "data": filtered_data.values.tolist() 
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True,port=7000)