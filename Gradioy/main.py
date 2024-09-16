import gradio as gr
import random
import matplotlib.pyplot as plt

def predict(*inputs):
    kitchen_appliances = ["Refrigerator", "Oven", "Microwave", "Dishwasher", "Toaster", "Blender", "Coffee Maker", "Electric Kettle", "Food Processor", "Slow Cooker"]
    
    appliance_counts = {}
    for i in range(100):
        result = random.choice(kitchen_appliances)
        appliance_counts[result] = appliance_counts.get(result, 0) + 1

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.bar(appliance_counts.keys(), appliance_counts.values())
    ax.set_xlabel("Appliance")
    ax.set_ylabel("Chance (%)")
    ax.set_title("Kitchen Appliance Identification")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Voltage"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Current"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Active Power"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Reactive Power"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Apparent Power"),
    ],
    outputs=gr.Plot()
)

demo.launch()