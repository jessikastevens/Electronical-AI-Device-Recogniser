#AI API
import numpy as np
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model
import joblib
from dotenv import load_dotenv
import os

load_dotenv()
MODEL_PATH = os.getenv('MODEL_PATH', 'model.h5')
SCALER_PATH = os.getenv('SCALER_PATH', 'scaler.pkl')

print(f"Current working directory: {os.getcwd()}")
print(f"MODEL_PATH: {MODEL_PATH}")
print(f"SCALER_PATH: {SCALER_PATH}")
print(f"Files in current directory: {os.listdir('.')}")

model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    '''
    Expected JSON format:
    {
        "Real Power": 100,
        "Reactive Power": 50,
        "RMS Current": 10,
        "Frequency": 60,
        "RMS Voltage": 220,
        "Phase Angle": 30,
        "Date": "2022-01-01",
        "time": "12:00:00"
    }
    '''
    # Extract the relevant fields from the input data
    input_list = [
        data.get("Real Power", 0),
        data.get("Reactive Power", 0),
        data.get("RMS Current", 0),
        data.get("Frequency", 0),
        data.get("RMS Voltage", 0),
        data.get("Phase Angle", 0)
    ]

    # Convert the list to a numpy array and reshape to the correct format for the model
    input_data = np.array(input_list).reshape((1, -1))

    # Scale the input data
    input_data = scaler.transform(input_data)

    # Make a prediction using the loaded model
    raw_prediction = model.predict(input_data)[0]

    # Get the index of the highest value from the raw prediction
    predicted_class = int(np.argmax(raw_prediction))

    # Return the predicted class and the raw prediction probabilities
    return jsonify({
        "predicted_class": predicted_class,
        "raw_prediction": raw_prediction.tolist()  # Convert numpy array to list
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)