import gradio as gr
import matplotlib.pyplot as plt
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import numpy as np

load_dotenv()

OPTIONS_1 = ['Fridges & Freezers', 'TVs', 'Hi-Fi systems (with CD players)', 'Laptops', 'Computer stations', 'Incandescent lamps', 'Compact fluorescent lamps', 'Microwaves', 'Coffee machines', 'Mobile phones', 'Printers']
OPTIONS_2 = ['Line graph', 'Bar graph', 'Pie chart', 'Scatter graph', 'Violin graph']
OPTIONS_3 = [i for i in range(1, 11)]
MAX_GRAPHS = 10
DEFAULT_START_DATETIME = "2001-01-01 01:05:19"
DEFAULT_END_DATETIME = "2014-02-13 12:48:20"

def get_average_per_hour(values, timestamps):
    hourly_sums = [0] * 24
    hourly_counts = [0] * 24

    for i in range(len(values)):
        timestamp = datetime.strptime(timestamps[i], "%a, %d %b %Y %H:%M:%S %Z")
        hour = timestamp.hour
        hourly_sums[hour] += values[i]
        hourly_counts[hour] += 1

    hourly_avgs = [hourly_sums[i] / hourly_counts[i] if hourly_counts[i] > 0 else 0 for i in range(24)]
    return hourly_avgs

def plot_data_per_device(data, plot_type):
    measurement_types = ['freq', 'phAngle', 'power', 'reacPower', 'rmsCur', 'rmsVolt']
    devices = list(data.keys())
    
    num_devices = len(devices)
    num_measures = len(measurement_types)

    fig, axs = plt.subplots(num_devices, num_measures, figsize=(25, 4 * num_devices))

    # Ensure axs is always a 2D array
    axs = np.atleast_2d(axs)
    for device_index, device in enumerate(devices):
        for measure_index, measure in enumerate(measurement_types):
            if measure in data[device]:
                avg_data = get_average_per_hour(data[device][measure], data[device]['timestamp'])
                
                if plot_type == 'Line graph':
                    axs[device_index, measure_index].plot(avg_data)
                if plot_type == 'Bar graph':
                    axs[device_index, measure_index].bar(range(24), avg_data)
                if plot_type == 'Pie chart':
                    axs[device_index, measure_index].pie(avg_data)
                if plot_type == 'Violin graph':
                    axs[device_index, measure_index].violinplot(avg_data)
                if plot_type == 'Scatter graph':
                    axs[device_index, measure_index].scatter(range(24), avg_data)

                axs[device_index, measure_index].set_title(f'{device} - {measure}')
                axs[device_index, measure_index].set_xlabel('Hour of the Day')
                axs[device_index, measure_index].set_ylabel(measure.capitalize())
                axs[device_index, measure_index].grid(True)
            else:
                axs[device_index, measure_index].axis('off')

    plt.tight_layout()
    return fig

def handle_combined_input(appliances, start_datetime, end_datetime, graph_type, num_graphs):
    url = os.environ.get('Logic_API_URL_CSV')

    start_datetime_str = datetime.fromtimestamp(start_datetime).strftime("%Y-%m-%d %H:%M:%S")
    end_datetime_str = datetime.fromtimestamp(end_datetime).strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "Appliances": appliances,
        "start": start_datetime_str,
        "end": end_datetime_str,
        "graph_type": graph_type,
        "num_graphs": num_graphs
    }

    # print("API URL:", url)
    # print("Payload:", json.dumps(payload, indent=4))

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    # print('Response Status Code:', response.status_code)
    # print('Response Text:', response.text)

    if response.status_code == 200:
        try:
            data = response.json()['data']
            plot_type = response.json().get('graph_type')
            fig = plot_data_per_device(data , plot_type)
            return fig
        except json.JSONDecodeError:
            return "Error: Invalid JSON response from the server."
        except KeyError:
            return "Error: Unexpected data format in the response."
    else:
        return f"Error: API request failed with status code {response.status_code}"

def predict(real_power, reactive_power, rms_current, frequency, rms_voltage, phase_angle, single_datetime):
    url = os.environ.get('Logic_API_URL_AI')

    dt_object = datetime.fromtimestamp(single_datetime)
    date_str = dt_object.strftime('%Y-%m-%d')
    time_str = dt_object.strftime('%H:%M:%S')

    payload = {
        "Real Power": real_power,
        "Reactive Power": reactive_power,
        "RMS Current": rms_current,
        "Frequency": frequency,
        "RMS Voltage": rms_voltage,
        "Phase Angle": phase_angle,
        "Date": date_str,
        "time": time_str,
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        predicted_appliance = data.get('predicted_appliance', 'Unknown')
        fig = predict_graph(data)
        return f"Predicted Appliance: {predicted_appliance}", fig
    else:
        error_message = f"Error: API request failed with status code {response.status_code}"
        return error_message, None

def predict_graph(data):
    predictions = data['raw_predictions']
    
    appliances = list(predictions.keys())
    probabilities = list(predictions.values())
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(appliances, probabilities)
    
    ax.set_title('Appliance Prediction Probabilities')
    ax.set_xlabel('Appliances')
    ax.set_ylabel('Probability')
    plt.xticks(rotation=45, ha='right')
    
    predicted_appliance = data['predicted_appliance']
    predicted_index = appliances.index(predicted_appliance)
    bars[predicted_index].set_color('green')
    
    # ax.text(predicted_index, probabilities[predicted_index], 'Predicted', 
    #         ha='center', va='bottom', color='green')
    
    plt.tight_layout()
    return fig

def update_dropdown_visibility(num):
    return [gr.update(visible=i < num) for i in range(MAX_GRAPHS)]

def gather_inputs(num, *args):
    appliances = [arg for arg in args[:num] if arg] 
    start_dt, end_dt, graph_type = args[-3:]
    return handle_combined_input(appliances, start_dt, end_dt, graph_type, num)

# Gradio interface
with gr.Blocks(theme="monochrome") as demo: 
    with gr.Tab("View Data"):
        with gr.Row():
            with gr.Column():
                num_graphs = gr.Dropdown(choices=OPTIONS_3, label="Select Number of Graphs", value=1)
                appliance_dropdowns = [gr.Dropdown(choices=OPTIONS_1, label=f"Select Appliance {i+1}", visible=i==0) for i in range(MAX_GRAPHS)]
                start_datetime = gr.DateTime(label="Start Date and Time", value=DEFAULT_START_DATETIME)
                end_datetime = gr.DateTime(label="End Date and Time", value=DEFAULT_END_DATETIME)
                graph_type = gr.Dropdown(choices=OPTIONS_2, label="Select Graph Type")
                submit_button = gr.Button("Submit")

        result_output = gr.Plot(label="Graph Output")

        num_graphs.change(
            fn=update_dropdown_visibility,
            inputs=[num_graphs],
            outputs=appliance_dropdowns
        )

        submit_button.click(
            fn=gather_inputs,
            inputs=[num_graphs] + appliance_dropdowns + [start_datetime, end_datetime, graph_type],
            outputs=[result_output]
        )

    with gr.Tab("Device Prediction"):
        with gr.Row():
            with gr.Column():
                real_power_slider = gr.Slider(minimum=0, maximum=4000, step=50, value=1550, label="Real Power (W)")
                reactive_power_slider = gr.Slider(minimum=0, maximum=500, step=10, value=250, label="Reactive Power (var)")
                rms_current_slider = gr.Slider(minimum=0, maximum=100, step=0.1, value=7.75, label="RMS Current (A)")
                frequency_slider = gr.Slider(minimum=0, maximum=100, step=10, value=50, label="Frequency (Hz)")
                rms_voltage_slider = gr.Slider(minimum=0, maximum=300, step=10, value=220, label="RMS Voltage (V)")
                phase_angle_slider = gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Phase Angle (φ)")
                single_datetime = gr.DateTime(label="Select a Date and Time")
                predict_button = gr.Button("Predict")

        predict_output_text = gr.Textbox(label="Prediction Result")
        predict_output = gr.Plot(label="Prediction Probabilities")

        predict_button.click(
            fn=predict,
            inputs=[real_power_slider, reactive_power_slider, rms_current_slider, frequency_slider,
                    rms_voltage_slider, phase_angle_slider, single_datetime],
            outputs=[predict_output_text, predict_output]
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    demo.launch(server_port=port, server_name="0.0.0.0")
