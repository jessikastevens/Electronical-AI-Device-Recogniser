import random
from flask import Flask, jsonify, request
import numpy as np
from tensorflow.keras.models import load_model

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    # Load your pre-trained model (this is just an example, adjust according to your model and framework)

    model = load_model('path_to_your_model.h5')

    # Preprocess the input data as required by your model
    input_data = np.array(data['input'])  # Assuming the input data is in the 'input' field of the JSON
    input_data = input_data.reshape((1, -1))  # Reshape if necessary

    # Make a prediction using the model
    raw_prediction = model.predict(input_data)[0]

    # Get the index of the highest value of raw_prediction
    predicted_class = int(np.argmax(raw_prediction))

    # Generate random raw prediction (10 items with positive probabilities that sum up to 1)
    raw_prediction = np.random.dirichlet(np.ones(15))


    #the index of the hightst value of raw_prediction
    predicted_class = int(np.argmax(raw_prediction))
    
    return jsonify({
        "predicted_class": predicted_class,
        "raw_prediction": raw_prediction.tolist()  # Convert numpy array to list
    })

if __name__ == '__main__':
    app.run(debug=True, port=6000)