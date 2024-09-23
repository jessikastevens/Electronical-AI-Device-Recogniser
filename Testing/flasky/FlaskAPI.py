from flask import Flask, jsonify, request
import time
import json
import random


app = Flask(__name__)


preprocessed_standardised_values = {
    "Refrigerator": 0.3,
    "Oven": 1.2,
    "Microwave": 0.65,
    "Dishwasher": 0.75,
    "Toaster": 0.4,
    "Blender": 0.25,
    "Coffee Maker": 0.35,
    "Electric Kettle": 0.85,
    "Food Processor": 0.55,
    "Slow Cooker": 0.4
}

def calculate_standardised_value(real_power, reactive_power, rms_current, frequency, rms_voltage, phase):
    return (real_power / 3000 * 0.3 + 
            reactive_power / 500 * 0.2 + 
            rms_current / 100 * 0.2 +
            frequency / 100 * 0.1 +
            rms_voltage / 300 * 0.1 +
            (phase + 100) / 200 * 0.1)

def find_closest_standardised(standardized_value):
    return min(preprocessed_standardised_values.items(), 
               key=lambda x: abs(x[1] - standardized_value))[0]

def weightedpredict(real_power, reactive_power, rms_current, frequency, rms_voltage, phase):
    standardised_value = calculate_standardised_value(
        real_power, reactive_power, rms_current, frequency, rms_voltage, phase
    )
    
    closest_appliance = find_closest_standardised(standardised_value)
    largest_item_image = f"Gradioy/pictures/{closest_appliance}.jpg"
    

    kitchen_appliances = ["Refrigerator", "Oven", "Microwave", "Dishwasher", "Toaster", "Blender", "Coffee Maker", "Electric Kettle", "Food Processor", "Slow Cooker"]

    appliance_counts = {}
    for i in range(90):
        result = random.choice(kitchen_appliances)
        appliance_counts[result] = appliance_counts.get(result, 0) + 1

    appliance_counts[closest_appliance] = max(appliance_counts.values()) + 10


    xvalue = list(appliance_counts.keys()) 
    yvalue = list(appliance_counts.values()) 


    result_dict = {
        'xvalue': xvalue,
        'yvalue': yvalue,
        'imagie_path': largest_item_image,
        'appliance': closest_appliance    }

    return result_dict 


def predict(Electric_values):

    kitchen_appliances = ["Refrigerator", "Oven", "Microwave", "Dishwasher", "Toaster", "Blender", "Coffee Maker", "Electric Kettle", "Food Processor", "Slow Cooker"]
    
    appliance_counts = {}
    for i in range(100):
        result = random.choice(kitchen_appliances)
        appliance_counts[result] = appliance_counts.get(result, 0) + 1


    xvalue = list(appliance_counts.keys()) 
    yvalue = list(appliance_counts.values()) 

    largest_item = max(appliance_counts, key=appliance_counts.get)
    largest_item_image = r"Gradioy/pictures/" + largest_item + ".jpg"

    result_dict = {
        'xvalue': xvalue,
        'yvalue': yvalue,
        'imagie_path': largest_item_image,
        'appliance': largest_item    }

    return result_dict 

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.get_json()
        Electric_values_list = list(data.values())[:-1]
        print(data)
        if data.get('mode') == 'Random':
            result = predict(Electric_values_list)

            print('ooga')
            print(result)
            return jsonify(result)  # jsonify will convert the dictionary to a JSON response

        if data.get('mode') == 'WeightedPrediction':
            # Unpack the Electric_values_list into individual arguments
            result = weightedpredict(*Electric_values_list)

            print('ooga')
            print(result)
            return jsonify(result)  # jsonify will convert the dictionary to a JSON response

    else:
        return 'gulp'





if __name__ == '__main__':
    app.run(debug=True)