from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    # TODO: Implement actual AI prediction logic here
    # This is a dummy response for now
    return jsonify({
        "predicted_class": 2,
        "raw_prediction": [[0.05, 0.10, 0.85]]
    })

if __name__ == '__main__':
    app.run(debug=True, port=6000)