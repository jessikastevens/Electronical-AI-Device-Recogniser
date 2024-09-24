import random
from flask import Flask, jsonify, request
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    '''
        This is the json format the data will be inputed as

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
    # Load your pre-trained model (this is just an example, adjust according to your model and framework)
    model = load_model(r'khanya/data managment/saved models/appliance_recogniser#2.keras')

    # Extract the relevant fields from the input data and convert them into a list
    input_list = [
        data["Real Power"],
        data["Reactive Power"],
        data["RMS Current"],
        data["Frequency"],
        data["RMS Voltage"],
        data["Phase Angle"]
    ]

    # Convert the list to a numpy array and reshape if necessary
    input_data = np.array(input_list).reshape((1, -1))

    # Make a prediction using the model
    raw_prediction = model.predict(input_data)[0]

    # Get the index of the highest value of raw_prediction
    predicted_class = int(np.argmax(raw_prediction))

    # Generate random raw prediction (10 items with positive probabilities that sum up to 1)
    raw_prediction = np.random.dirichlet(np.ones(15))

    # The index of the highest value of raw_prediction
    predicted_class = int(np.argmax(raw_prediction))
    
    return jsonify({
        "predicted_class": predicted_class,
        "raw_prediction": raw_prediction.tolist()  # Convert numpy array to list
    })

if __name__ == '__main__':
    app.run(debug=True, port=6000)