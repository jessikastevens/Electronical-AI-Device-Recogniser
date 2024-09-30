import gradio as gr
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

def create_oauth_flow():
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email']
    )
    return flow

def login():
    flow = create_oauth_flow()
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return authorization_url

def callback(code):
    flow = create_oauth_flow()
    flow.fetch_token(code=code)
    credentials = flow.credentials
    return f"Logged in successfully! Access token: {credentials.token}"

with gr.Blocks() as demo:
    gr.Markdown("# Google OAuth Login")
    login_button = gr.Button("Login with Google")
    output = gr.Textbox(label="Result")
    
    login_button.click(login, outputs=gr.Textbox())
    demo.load(lambda: gr.update(visible=True), outputs=login_button)

demo.launch(share=True)