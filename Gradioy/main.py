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


    largest_item = max(appliance_counts, key=appliance_counts.get)
    print(largest_item)    

    largest_item_image = r"Gradioy/pictures/" + largest_item + ".jpg"

    return fig , largest_item_image

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Slider(minimum=0, maximum=3000, step=50, value=1550, label="Real Power (W)"),
        gr.Slider(minimum=0, maximum=500, step=10, value=250, label="Reactive Power (var)"),
        gr.Slider(minimum=0, maximum=100, step=0.1, value=7.75, label="RMS Current (A)"),
        gr.Slider(minimum=0, maximum=100, step=10, value=50, label="Frequency (Hz)"),
        gr.Slider(minimum=0, maximum=300, step=10, value=220, label="RMS Voltage (V)"),
        gr.Slider(minimum=-100, maximum=100, step=5, value=0, label="Phase Angle (φ)"),
    ],
    outputs=[gr.Plot(), gr.Image(type="filepath")],
    theme=gr.themes.Monochrome()
)

demo.launch(share=True)