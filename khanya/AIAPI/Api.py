from flask import Flask, jsonify, request
import numpy as np
import joblib
from tensorflow.keras.models import load_model
import pandas as pd

app = Flask(__name__)


model = load_model('khanya/saved models/appliance_recogniser1.keras')  
scaler = joblib.load('scaler.pkl')   

@app.route('/', methods=['POST'])
def api():
    # Check if POST method is used
    if request.method == 'POST':
        # Parse JSON data from the request
        data = request.get_json()

        features = np.array([data])

        # Scale
        input_scaled = scaler.transform(input_data)

        # prediction
        prediction = model.predict(input_scaled)

        # Convert the prediction to a class index
        predicted_class = np.argmax(prediction, axis=1)

        # Return JSON
        return jsonify({
            'predicted_class': int(predicted_class[0]),
            'raw_prediction': prediction.tolist()
        })

if __name__ == '__main__':
    app.run(debug=True)
