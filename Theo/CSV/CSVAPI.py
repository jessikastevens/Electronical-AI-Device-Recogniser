from flask import Flask, jsonify, request
import time
import json
import pandas as pd 


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def api():
    print()





if __name__ == '__main__':
    app.run(debug=True)