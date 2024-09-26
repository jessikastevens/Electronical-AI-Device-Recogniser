from flask import Flask, request, jsonify
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    request_data = request.get_json()

    appliances = request_data.get('Appliances')
    if not appliances:
        return jsonify({"error": "'Appliances' key is missing"}), 400

    start_time = request_data.get('start')
    if not start_time:
        return jsonify({"error": "'start' key is missing"}), 400

    end_time = request_data.get('end')
    if not end_time:
        return jsonify({"error": "'end' key is missing"}), 400

    graph_type = request_data.get('graph_type')
    if not graph_type:
        return jsonify({"error": "'graph_type' key is missing"}), 400

    num_graphs = request_data.get('num_graphs')
    if not num_graphs:
        return jsonify({"error": "'num_graphs' key is missing"}), 400

    csv_file_path = os.getenv('CSV_FILE_PATH')

    if not csv_file_path or not os.path.isfile(csv_file_path):
        return jsonify({"error": "Invalid or missing CSV file path"}), 500

    df = pd.read_csv(csv_file_path)

    # Convert the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'])

    # Filter the dataframe based on the time range
    mask = (df['time'] >= start_time) & (df['time'] <= end_time)
    df_filtered = df.loc[mask]

    result = {}
    for appliance in appliances:
        # Use 'equipment' column instead of 'appliance'
        appliance_data = df_filtered[df_filtered['equipment'] == appliance]
        result[appliance] = {
            'timestamp': appliance_data['time'].tolist(),
            'power': appliance_data['power'].tolist()
        }

    response = {
        'data': result,
        'graph_type': graph_type,
        'num_graphs': num_graphs
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=7000)
