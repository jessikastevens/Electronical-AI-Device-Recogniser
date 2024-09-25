import gradio as gr
import random
import matplotlib.pyplot as plt
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


options_1 = ['Fridges & Freezers', 'TVs', 'Hi-Fi systems (with CD players)', 'Laptops', 'Computer stations', 'Incandescent lamps',
             'Compact fluorescent lamps', 'Microwaves', 'Coffee machines', 'Mobile phones', 'Printers']

options_2 = ['Line graph', 'Bar graph', 'Pie chart', 'Scatter graph', 'Violin graph']

options_3 = [i for i in range(1, 5)]  


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

    print("API URL:", url)
    print("Payload:", json.dumps(payload, indent=4))

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)

    print('Response Status Code:', response.status_code)
    print('Response Text:', response.text)

    return response.text

def predict(real_power_slider, reactive_power_slider, rms_current_slider, frequency_slider, rms_voltage_slider, 
            phase_angle_slider, single_datetime):
    url = os.environ.get('Logic_API_URL_AI')

    dt_object = datetime.fromtimestamp(float(single_datetime))
    date_str = dt_object.strftime('%Y-%m-%d')
    time_str = dt_object.strftime('%H:%M:%S')

    payload = {
        "Real Power": real_power_slider,
        "Reactive Power": reactive_power_slider,
        "RMS Current": rms_current_slider,
        "Frequency": frequency_slider,
        "RMS Voltage": rms_voltage_slider,
        "Phase Angle": phase_angle_slider,
        "Date": date_str,
        "time": time_str,
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)

    return response.text

MAX_GRAPHS = 4

# Set default start and end dates using the specified dates
default_start_datetime = datetime(2001, 1, 1, 1, 5, 19)  # Earliest date
default_end_datetime = datetime(2014, 2, 13, 12, 48, 20)  # Oldest date

# In your Blocks definition:
with gr.Blocks(theme="monochrome") as demo:  # This applies the theme to everything
    with gr.Tab("Dropdown & Date Range"):
        with gr.Row():
            with gr.Column():
                num_graphs = gr.Dropdown(choices=options_3, label="Select Number of Graphs", value=default_num_graphs)
                appliance_dropdowns = [gr.Dropdown(choices=options_1, label=f"Select Appliance {i+1}", 
                                                    value=default_appliances if i == 0 else None, 
                                                    visible=i==0) for i in range(MAX_GRAPHS)]
                start_datetime = gr.DateTime(label="Start Date and Time", value=default_start_datetime)
                end_datetime = gr.DateTime(label="End Date and Time", value=default_end_datetime)
                graph_type = gr.Dropdown(choices=options_2, label="Select Graph Type", value=default_graph_type)
                submit_button = gr.Button("Submit")

        result_output = gr.Textbox(label="Output")

        def update_dropdown_visibility(num):
            return [gr.update(visible=i < num) for i in range(MAX_GRAPHS)]

        num_graphs.change(
            fn=update_dropdown_visibility,
            inputs=[num_graphs],
            outputs=appliance_dropdowns
        )

        # Update your gather_inputs function to handle the new structure
        def gather_inputs(num, *args):
            appliances = args[:num]
            start_dt, end_dt, graph_type = args[-3:]
            return handle_combined_input(appliances, start_dt, end_dt, graph_type, num)

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

        predict_output = gr.Textbox(label="Prediction Output")

        predict_button.click(
            fn=predict,
            inputs=[real_power_slider, reactive_power_slider, rms_current_slider, frequency_slider,
                    rms_voltage_slider, phase_angle_slider, single_datetime],
            outputs=[predict_output]
        )

demo.launch(share=True)