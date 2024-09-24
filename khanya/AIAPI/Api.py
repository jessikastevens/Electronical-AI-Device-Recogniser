import random
from flask import Flask, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    # TODO: Implement actual AI prediction logic here
    # This is a dummy response for now

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