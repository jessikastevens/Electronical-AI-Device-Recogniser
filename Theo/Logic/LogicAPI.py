from flask import Flask, jsonify, request , json
import time
import pandas as pd 


app = Flask(__name__)

@app.route('/CSV', methods=['GET', 'POST'])
def api():
    print('Start CSV')

@app.route('/AI', methods=['GET', 'POST'])
def api():
    print('StartAI')
    if request == ['POST']:
        print('Post')

        

    





if __name__ == '__main__':
    app.run(debug=True)