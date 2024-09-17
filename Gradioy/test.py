import gradio as gr

preprocessed_standardised_values = {
    "Refrigerator": 0.25,
    "Oven": 1.0,
    "Microwave": 0.6,
    "Dishwasher": 0.75,
    "Toaster": 0.4,
    "Blender": 0.2,
    "Coffee Maker": 0.3,
    "Electric Kettle": 0.85,
    "Food Processor": 0.5,
    "Slow Cooker": 0.35
}

def calculate_standardised_value(real_power, reactive_power, rms_current, frequency, rms_voltage, phase):
    return (real_power / 3000 * 0.25 + 
            reactive_power / 500 * 0.2 + 
            rms_current / 100 * 0.2 +
            frequency / 100 * 0.1 +
            rms_voltage / 300 * 0.1 +
            (phase + 100) / 200 * 0.15)

def find_closest_standardised(standardized_value):
    return min(preprocessed_standardised_values.items(), 
               key=lambda x: abs(x[1] - standardized_value))[0]

def predict(real_power, reactive_power, rms_current, frequency, rms_voltage, phase):
    standardised_value = calculate_standardised_value(
        real_power, reactive_power, rms_current, frequency, rms_voltage, phase
    )
    
    closest_appliance = find_closest_standardised(standardised_value)
    
    largest_item_image = f"Gradioy/pictures/{closest_appliance}.jpg"
    
    return closest_appliance, largest_item_image

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Slider(minimum=0, maximum=3000, step=25, value=1500, label="Real Power (W)"),
        gr.Slider(minimum=0, maximum=500, step=5, value=250, label="Reactive Power (var)"),
        gr.Slider(minimum=0, maximum=100, step=0.05, value=50, label="RMS Current (A)"),
        gr.Slider(minimum=0, maximum=100, step=5, value=50, label="Frequency (Hz)"),
        gr.Slider(minimum=0, maximum=300, step=5, value=150, label="RMS Voltage (V)"),
        gr.Slider(minimum=-100, maximum=100, step=2.5, value=0, label="Phase Angle (φ)"),
    ],
    outputs=[gr.Text(label="Identified Appliance"), gr.Image(type="filepath", label="Appliance Image")],
    theme=gr.themes.Monochrome(),
    examples=[
        [ 800, 400, 6.5, 50, 230, 0],  # Example tosta
    ]
)

demo.launch(share=True)