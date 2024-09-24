import numpy as np
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load the model once when the API starts to avoid reloading it on every request
model = load_model('khanya/data managment/saved models/appliance_recogniser#2.keras')

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
        data["Real Power"],
        data["Reactive Power"],
        data["RMS Current"],
        data["Frequency"],
        data["RMS Voltage"],
        data["Phase Angle"]
    ]

    # Convert the list to a numpy array and reshape to the correct format for the model
    input_data = np.array(input_list).reshape((1, -1))

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
    app.run(debug=True, port=6000)