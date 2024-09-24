import gradio as gr
import random
import matplotlib.pyplot as plt
import requests
import json

# Dropdown options for the first interface
options_1 = ['Fridges & Freezers', 'TVs', 'Hi-Fi systems (with CD players)', 'Laptops', 'Computer stations', 
             'Compact fluorescent lamps', 'Microwaves', 'Coffee machines', 'Mobile phones', 'Printers']

# Function to filter options for dropdown interface
def filter_options(option_1):
    return f"You selected '{option_1}' in the dropdown."

# Handling single datetime input
def handle_single_datetime(datetime_value):
    return f"Selected Date and Time: {datetime_value}"

# Handling date range (start and end datetime)
def handle_date_range(start_datetime, end_datetime):
    return f"Selected Date Range: {start_datetime} to {end_datetime}"

# Combine Dropdown and Date inputs in a single function
def handle_combined_input(option_1, start_datetime, end_datetime):
    dropdown_msg = f"You selected '{option_1}' in the dropdown."
    range_msg = f"Selected Date Range: {start_datetime} to {end_datetime}"
    return f"{dropdown_msg}\n{range_msg}"

# Function to plot the bar graph
def plot(x, y):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.bar(x, y)
    ax.set_xlabel("Appliance")
    ax.set_ylabel("Chance (%)")
    ax.set_title("Kitchen Appliance Identification")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig

# Function to predict appliance using external API and plot data
def predict(real_power, reactive_power, rms_current, frequency, rms_voltage, phase_angle, Mode, single_datetime):
    url = "http://127.0.0.1:5000/api"  # Make sure your API is running here!

    payload = json.dumps({
        "Real Power": real_power,
        "Reactive Power": reactive_power,
        "RMS Current": rms_current,
        "Frequency": frequency,
        "RMS Voltage": rms_voltage,
        "Phase Angle": phase_angle,
        "mode": Mode,
        "datetime": single_datetime
    })

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        response_dict = response.json()

        largest_item_image = response_dict['image_path']
        x = response_dict['xvalue']
        y = response_dict['yvalue']
        appliance = response_dict['appliance']

        fig = plot(x, y)

        return fig, largest_item_image, appliance

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None, None, "Error: Could not fetch appliance data"

# Tab 1: Dropdown and Date Range Inputs
with gr.Blocks() as input_tab:
    with gr.Row():
        with gr.Column():
            # Dropdown for appliance selection
            dropdown = gr.Dropdown(choices=options_1, label="Appliance Type")

            # Date Range Picker
            start_datetime = gr.DateTime(label="Start Date and Time")
            end_datetime = gr.DateTime(label="End Date and Time")

            # Button to submit selections
            submit_button = gr.Button("Submit")

        # Output Textbox to display results
        result_output = gr.Textbox(label="Output")

    # Bind the function to the submit button
    submit_button.click(fn=handle_combined_input, 
                        inputs=[dropdown, start_datetime, end_datetime],
                        outputs=result_output)

# Tab 2: Prediction Interface with DateTime Input
with gr.Blocks() as prediction_tab:
    # Prediction Interface
    with gr.Row():
        with gr.Column():
            real_power_slider = gr.Slider(minimum=0, maximum=4000, step=50, value=1550, label="Real Power (W)")
            reactive_power_slider = gr.Slider(minimum=0, maximum=500, step=10, value=250, label="Reactive Power (var)")
            rms_current_slider = gr.Slider(minimum=0, maximum=100, step=0.1, value=7.75, label="RMS Current (A)")
            frequency_slider = gr.Slider(minimum=0, maximum=100, step=10, value=50, label="Frequency (Hz)")
            rms_voltage_slider = gr.Slider(minimum=0, maximum=300, step=10, value=220, label="RMS Voltage (V)")
            phase_angle_slider = gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Phase Angle (φ)")
            mode_dropdown = gr.Dropdown(choices=['Random', 'WeightedPrediction'], label='Mode', info='Pick Mode')

            # Single DateTime Picker on Prediction Tab
            single_datetime = gr.DateTime(label="Select a Date and Time")

            predict_button = gr.Button("Predict")

        # Output for Prediction
        prediction_plot = gr.Plot()
        prediction_image = gr.Image(type="filepath")
        prediction_text = gr.Textbox(label="Appliance")

    # Bind the predict function to the predict button
    predict_button.click(fn=predict, 
                         inputs=[real_power_slider, reactive_power_slider, rms_current_slider, frequency_slider, 
                                 rms_voltage_slider, phase_angle_slider, mode_dropdown, single_datetime],
                         outputs=[prediction_plot, prediction_image, prediction_text])

# Combine into a Tabbed Interface
demo = gr.TabbedInterface(
    [input_tab, prediction_tab],
    ["Dropdown & Date Range", "AI Device Prediction & Date Selection"]
)

# theme = gr.themes.Soft(
#     primary_hue="cyan",
#     secondary_hue="pink",
#     neutral_hue="violet",
# )
# with gr.Blocks(theme=theme) as demo:
#        demo = gr.TabbedInterface(
#         [input_tab, prediction_tab],
#         ["Dropdown & Date Range", "AI Device Prediction & Date Selection"]
#     )

demo.launch(share=True)
