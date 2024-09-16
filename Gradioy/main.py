import gradio as gr

def predict(*args):
    #Sumbit Button
    return "Prediction result"

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Voltage"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Current"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Active Power"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Reactive Power"),
        gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Apparent Power"),
    ],
    outputs="text"
)

demo.launch(share=True)