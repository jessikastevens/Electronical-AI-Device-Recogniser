
import gradio as gr
import matplotlib.pyplot as plt
import requests
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import numpy as np
import google.generativeai as genai

load_dotenv()

# Initialize the generative AI model variable
model = None


OPTIONS_1 = ['Fridges & Freezers', 'TVs', 'Hi-Fi systems (with CD players)', 'Laptops', 
             'Computer stations', 'Incandescent lamps', 'Compact fluorescent lamps', 
             'Microwaves', 'Coffee machines', 'Mobile phones', 'Printers']
OPTIONS_2 = ['Line graph', 'Bar graph', 'Pie chart', 'Scatter graph', 'Violin graph']
OPTIONS_3 = [i for i in range(1, 11)]
MAX_GRAPHS = 10
DEFAULT_START_DATETIME = "2001-01-01 01:05:19"
DEFAULT_END_DATETIME = "2014-02-13 12:48:20"

def configure_model(api_key):
    global model, chat  # Ensure chat is defined globally

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Initialize the chat object
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"}
        ]
    )
    try:
        models = client.list_models()
        print("API key is working. Available models:", models)
    except Exception as e:
        print("API key is not working. Error:", e)


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

def plot_data_per_device(data, plot_type, chat_history):
    measurement_types = ['freq', 'phAngle', 'power', 'reacPower', 'rmsCur', 'rmsVolt']
    devices = list(data.keys())
    
    num_devices = len(devices)
    num_measures = len(measurement_types)

    fig, axs = plt.subplots(num_devices, num_measures, figsize=(25, 4 * num_devices))
    axs = np.atleast_2d(axs)

    raw_data_text = "Raw Data:\n"

    for device_index, device in enumerate(devices):
        for measure_index, measure in enumerate(measurement_types):
            if measure in data[device]:
                avg_data = get_average_per_hour(data[device][measure], data[device]['timestamp'])
                
                if plot_type == 'Line graph':
                    axs[device_index, measure_index].plot(avg_data)
                elif plot_type == 'Bar graph':
                    axs[device_index, measure_index].bar(range(24), avg_data)
                elif plot_type == 'Pie chart':
                    axs[device_index, measure_index].pie(avg_data)
                elif plot_type == 'Violin graph':
                    axs[device_index, measure_index].violinplot(avg_data)
                elif plot_type == 'Scatter graph':
                    axs[device_index, measure_index].scatter(range(24), avg_data)

                axs[device_index, measure_index].set_title(f'{device} - {measure}')
                axs[device_index, measure_index].set_xlabel('Hour of the Day')
                axs[device_index, measure_index].set_ylabel(measure.capitalize())
                axs[device_index, measure_index].grid(True)

                raw_data_text += f"{device} - {measure}:\n{avg_data}\n\n"

    plt.tight_layout()

    # Add the raw data text to chat interaction

    try:
        message, chat_history = chat_interaction(raw_data_text, chat_history)
    except NameError:
        pass 

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

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()['data']
            plot_type = response.json().get('graph_type')
            fig = plot_data_per_device(data, plot_type, [])
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
    
    plt.tight_layout()
    return fig

def update_dropdown_visibility(num):
    return [gr.update(visible=i < num) for i in range(MAX_GRAPHS)]

def gather_inputs(num, *args):
    appliances = [arg for arg in args[:num] if arg] 
    start_dt, end_dt, graph_type = args[-3:]
    return handle_combined_input(appliances, start_dt, end_dt, graph_type, num)

def chat_interaction(message, history):
    global chat
    if chat is None:
        return "Error: API key not set.", history

    # Include the user's message in the chat
    personality = r'''You are an AI assistant tasked with answering questions about the ACS-F2 dataset. The dataset contains electrical signals from various household and office appliances. Here's an overview of the dataset acquisition process:

Acquisition Details:
Sampling Frequency: 0.1 Hz (low sampling rate to capture long-term electrical consumption signatures instead of high-frequency noise).
Duration: 2 sessions, 1 hour each, ensuring a comprehensive capture of different running states of each appliance.
Number of Categories: 15 appliance categories, including:
Fridges & Freezers
TVs (LCD)
Hi-Fi Systems (with CD players)
Laptops
Computer Stations (with monitors)
Compact Fluorescent Lamps (CFL)
Microwaves
Coffee Machines
Mobile Phones (via battery chargers)
Printers
Fans
Shavers
Monitors
Incandescent Lamps
Kettles
Appliance Instances per Category: 15
Acquisition Device: PLOGG (records disaggregated signals from one appliance at a time).
Measured Parameters:
Real Power (W)
Reactive Power (VAR)
RMS Current (A)
Frequency (Hz)
RMS Voltage (V)
Phase Angle (φ) (Voltage relative to current)
Task Workflow:
Users interact with a UI to select an appliance and a date range, which generates a graph based on the selected data.
You will receive raw data before it is plotted, allowing you to assist users with their questions. If a user sends a message before you receive any data, this indicates they have not selected data for plotting yet. Encourage them to select the relevant parameters in that case.
UI Overview:
The interface is divided into two main sections: View Data and Device Prediction, set against a modern dark-themed background. The components include:

Appliance Graph Selection: Dropdown menus to choose the number of graphs and appliances (e.g., "Fridges & Freezers").
Date-Time Picker: Users select the start and end date/time for the data (e.g., Start Date: "2001-01-01 01:05:19", End Date: "2014-02-13 12:48:20").
Graph Type Selection: Users can choose the graph type (default: "Line Graph").
Submit Button: A button to generate the graph based on selected parameters.
Chat with AI: A chat interface for users to interact with you, located on the right side of the UI. Below this is an input box where users type their messages.
Clear Chat Button: Clears the conversation history.
Graph Output Area: Displays the generated graph based on the user’s selection.
Note: The UI is designed for simplicity and efficiency, helping users visualise data easily while offering interactive AI support.
If the user inputs multiple devices and asks about one of them seperatly still give them more infomation, dont ask them to sumbit the form again unless theres is no data AT ALL on the device the user is asking about

'''
    question = f'Your Personality is {personality}. The user\'s message is "{message}"'
    
    response = chat.send_message(question)

    # Add the user message and the model's response to the history
    history.append((message, response.text))
    return "", history

css = """
button:active {
  transform: scale(0.95);
}
"""

with gr.Blocks(css=css, theme="monochrome") as demo:
    # API Key input and setup
    with gr.Row():
        api_key_input = gr.Textbox(label="Enter your Gemini API Key", type="text")
        api_key_button = gr.Button("Set API Key")
    
    api_key_button.click(fn=configure_model, inputs=api_key_input, outputs="")

    with gr.Tab("View Data"):
        with gr.Row():
            with gr.Column(scale=2):
                num_graphs = gr.Dropdown(choices=OPTIONS_3, label="Select Number of Applience Graphs", value=1)
                appliance_dropdowns = [gr.Dropdown(choices=OPTIONS_1 , value='Fridges & Freezers', label=f"Select Appliance {i+1}", visible=i==0) for i in range(MAX_GRAPHS)]
                start_datetime = gr.DateTime(label="Start Date and Time", value=DEFAULT_START_DATETIME)
                end_datetime = gr.DateTime(label="End Date and Time", value=DEFAULT_END_DATETIME)
                graph_type = gr.Dropdown(choices=OPTIONS_2, label="Select Graph Type", value='Line graph')
                submit_button = gr.Button("Submit")

            with gr.Column(scale=1):
                chatbot = gr.Chatbot(label="Chat with AI")
                msg = gr.Textbox(label="Type your message here")
                clear = gr.Button("Clear Chat")

        with gr.Row():
            result_output = gr.Plot(label="Graph Output")

        # Ensure this is within the gr.Blocks context
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

        msg.submit(chat_interaction, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    with gr.Tab("Device Prediction"):
        with gr.Row():
            with gr.Column():
                real_power_slider = gr.Slider(minimum=0, maximum=4000, step=50, value=1550, label="Real Power (W)")
                reactive_power_slider = gr.Slider(minimum=0, maximum=500, step=10, value=250, label="Reactive Power (var)")
                rms_current_slider = gr.Slider(minimum=0, maximum=100, step=0.1, value=7.75, label="RMS Current (A)")
                frequency_slider = gr.Slider(minimum=0, maximum=100, step=10, value=50, label="Frequency (Hz)")
                rms_voltage_slider = gr.Slider(minimum=0, maximum=300, step=10, value=220, label="RMS Voltage (V)")
                phase_angle_slider = gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Phase Angle (φ)")
                single_datetime = gr.DateTime(label="Select a Date and Time",value='2001-01-01 01:05:19')
                predict_button = gr.Button("Predict")

        predict_output_text = gr.Textbox(label="Prediction Result")
        predict_output = gr.Plot(label="Prediction Probabilities")

        predict_button.click(
            fn=predict,
            inputs=[real_power_slider, reactive_power_slider, rms_current_slider, frequency_slider,
                    rms_voltage_slider, phase_angle_slider, single_datetime],
            outputs=[predict_output_text, predict_output]
        )

demo.launch()

