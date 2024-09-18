import gradio as gr
import random
import matplotlib.pyplot as plt
import requests
import json

def plot(x , y):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.bar(x, y)
    ax.set_xlabel("Appliance")
    ax.set_ylabel("Chance (%)")
    ax.set_title("Kitchen Appliance Identification")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig

def predict(real_power, reactive_power, rms_current, frequency, rms_voltage, phase_angle, Mode):
    url = "http://127.0.0.1:5000/api"

    payload = json.dumps({
        "Real Power": real_power,
        "Reactive Power": reactive_power,
        "RMS Current": rms_current,
        "Frequency": frequency,
        "RMS Voltage": rms_voltage,
        "Phase Angle": phase_angle,
        "mode": Mode
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = json.loads(response.text)

    largest_item_image = response_dict['imagie_path']

    x = response_dict['xvalue']
    y = response_dict['yvalue']

    fig = plot(x , y)

    appliance = response_dict['appliance']

    return fig , largest_item_image , appliance

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Slider(minimum=0, maximum=4000, step=50, value=1550, label="Real Power (W)"),
        gr.Slider(minimum=0, maximum=500, step=10, value=250, label="Reactive Power (var)"),
        gr.Slider(minimum=0, maximum=100, step=0.1, value=7.75, label="RMS Current (A)"),
        gr.Slider(minimum=0, maximum=100, step=10, value=50, label="Frequency (Hz)"),
        gr.Slider(minimum=0, maximum=300, step=10, value=220, label="RMS Voltage (V)"),
        gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Phase Angle (φ)"),
        gr.Dropdown(['Random' ,'WeightedPrediction'], label='Mode', info='Pick Mode')
    ],
    outputs=[gr.Plot(), gr.Image(type="filepath"), gr.Textbox(label="Appliance")],
    theme=gr.themes.Monochrome(),
    examples = [
        [ 800, 400, 6.5, 50, 230, 0, 'WeightedPrediction'],
        [2450, 650, 8.0, 50, 230, 20, 'WeightedPrediction']
    ],
    examples_per_page=5,
    example_labels=["Toaster", "Dishwasher"],
    title="Electronical AI Device Recognizer"
)

demo.launch(share=True)