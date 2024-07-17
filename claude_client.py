import gradio as gr
import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

def chat_with_claude(prompt):
    url = "https://api.claude.ai/v1/engines/claude-3.5/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 150  # Adjust max tokens as needed
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text")
    else:
        return f"Error: {response.status_code} - {response.text}"

def process_file(file):
    try:
        df = pd.read_csv(file.name)
        file_content = df.to_string()
        return chat_with_claude(file_content)
    except Exception as e:
        return f"Error processing file: {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("# Claude 3.5 Chatbot")
    with gr.Tab("Text Input"):
        text_input = gr.Textbox(label="Enter your prompt")
        text_output = gr.Textbox(label="Claude's response")
        text_submit = gr.Button("Submit")
        text_submit.click(fn=chat_with_claude, inputs=text_input, outputs=text_output)
    
    with gr.Tab("File Upload"):
        file_input = gr.File(label="Upload a CSV file")
        file_output = gr.Textbox(label="Claude's response from file content")
        file_submit = gr.Button("Submit")
        file_submit.click(fn=process_file, inputs=file_input, outputs=file_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)

