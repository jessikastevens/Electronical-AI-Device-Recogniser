from flask import Flask, request, jsonify
import pandas as pd
import os
import requests
from io import StringIO
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def stream_csv(url):
    try:
        logger.info(f"Attempting to fetch CSV from: {url}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            buffer = StringIO()
            for chunk in r.iter_content(chunk_size=8192):
                buffer.write(chunk.decode('utf-8'))
            buffer.seek(0)
        logger.info("CSV file successfully fetched and loaded into buffer")
        df = pd.read_csv(buffer)
        logger.info(f"CSV parsed into DataFrame. Shape: {df.shape}")
        return df
    except requests.RequestException as e:
        logger.error(f"Failed to fetch CSV: {str(e)}")
        raise Exception(f"Failed to fetch CSV: {str(e)}")
    except pd.errors.EmptyDataError:
        logger.error("The CSV file is empty")
        raise Exception("The CSV file is empty")
    except Exception as e:
        logger.error(f"Unexpected error while processing CSV: {str(e)}")
        raise Exception(f"Unexpected error while processing CSV: {str(e)}")

@app.route('/', methods=['POST'])
def api():
    try:
        logger.info("Received API request")
        request_data = request.get_json()
        logger.info(f"Request data: {request_data}")

        # Validation
        required_keys = ['Appliances', 'start', 'end', 'graph_type', 'num_graphs']
        for key in required_keys:
            if key not in request_data:
                logger.error(f"'{key}' key is missing in request data")
                return jsonify({"error": f"'{key}' key is missing"}), 400

        appliances = request_data['Appliances']
        start_time = request_data['start']
        end_time = request_data['end']
        graph_type = request_data['graph_type']
        num_graphs = request_data['num_graphs']

        csv_url = os.getenv('CSV_FILE_PATH', 'https://raw.githubusercontent.com/jessikastevens/Electronical-AI-Device-Recogniser/refs/heads/main/Theo/CSV/acs-f2-datasetOG.csv')
        
        df = stream_csv(csv_url)
        
        logger.info("Processing data")
        
        # Convert the 'time' column to datetime
        df['time'] = pd.to_datetime(df['time'])
        
        # Filter the dataframe based on the time range
        mask = (df['time'] >= start_time) & (df['time'] <= end_time)
        df_filtered = df.loc[mask]
        
        result = {}
        for appliance in appliances:
            appliance_data = df_filtered[df_filtered['equipment'] == appliance]
            if not appliance_data.empty:
                result[appliance] = {
                    'timestamp': appliance_data['time'].tolist(),
                    'power': appliance_data['power'].tolist(),
                    'freq': appliance_data['freq'].tolist(),
                    'phAngle': appliance_data['phAngle'].tolist(),
                    'reacPower': appliance_data['reacPower'].tolist(),
                    'rmsCur': appliance_data['rmsCur'].tolist(),
                    'rmsVolt': appliance_data['rmsVolt'].tolist(),
                }
        
        response = {
            'data': result,
            'graph_type': graph_type,
            'num_graphs': num_graphs
        }
        
        logger.info("Request processed successfully")
        return jsonify(response)
    except Exception as e:
        logger.exception("An error occurred while processing the request")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting application on port {port}")
    app.run(host='0.0.0.0', port=port)