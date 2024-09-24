from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def api():
    data = request.get_json()

    # TODO: Implement actual AI prediction logic here
    # This is a dummy response for now

    #Predicted class is the applience it predicted in a tag form so it equalls somehting
    #raw prediciton is the proberplity it is one , in the real thing there will be 10 items in the list thr 1 item corosponsed with the 2st taged item ect dont worry about matching them up yet thats theos job :D

    return jsonify({
        "predicted_class": 2,
        "raw_prediction": [[0.05, 0.10, 0.85]]
    })

if __name__ == '__main__':
    app.run(debug=True, port=6000)