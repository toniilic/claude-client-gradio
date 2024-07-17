import gradio as gr
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from langchain import LLMChain, PromptTemplate, OpenAI

# Load API keys from .env file
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPEN_SOURCE_MODEL_API_URL = os.getenv("OPEN_SOURCE_MODEL_API_URL")

# Initialize LangChain with OpenAI model
llm = OpenAI(api_key=OPENAI_API_KEY)

# Define a template for context-aware prompts
template = "Context: {context}\nPrompt: {prompt}"
prompt_template = PromptTemplate(template=template)

# Function to handle chat with context using Claude API
def chat_with_claude(prompt, context=""):
    url = "https://api.claude.ai/v1/engines/claude-3.5/completions"
    headers = {
        "Authorization": f"Bearer {CLAUDE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": f"Context: {context}\nPrompt: {prompt}",
        "max_tokens": 150  # Adjust max tokens as needed
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to handle chat with context using LangChain and OpenAI
def chat_with_openai(prompt, context=""):
    llm_chain = LLMChain(llm=llm, prompt_template=prompt_template)
    response = llm_chain.run({"context": context, "prompt": prompt})
    return response

# Function to handle chat with an open-source model via a third-party API
def chat_with_open_source_model(prompt, context=""):
    url = OPEN_SOURCE_MODEL_API_URL
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "context": context,
        "prompt": prompt
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to process CSV files
def process_file(file, context, model):
    try:
        df = pd.read_csv(file.name)
        file_content = df.to_string()
        if model == "Claude":
            return chat_with_claude(file_content, context)
        elif model == "OpenAI":
            return chat_with_openai(file_content, context)
        elif model == "OpenSource":
            return chat_with_open_source_model(file_content, context)
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Function to process TXT files
def process_txt_file(file, context, model):
    try:
        with open(file.name, 'r') as f:
            file_content = f.read()
        if model == "Claude":
            return chat_with_claude(file_content, context)
        elif model == "OpenAI":
            return chat_with_openai(file_content, context)
        elif model == "OpenSource":
            return chat_with_open_source_model(file_content, context)
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Multi-Model Chatbot with LangChain")
    
    # Session management
    context_state = gr.State("")
    
    with gr.Tab("Text Input"):
        context_input = gr.Textbox(label="Enter context (optional)")
        text_input = gr.Textbox(label="Enter your prompt")
        model_choice = gr.Radio(label="Choose Model", choices=["Claude", "OpenAI", "OpenSource"], value="Claude")
        text_output = gr.Textbox(label="Model's response")
        text_submit = gr.Button("Submit")
        
        def handle_text_input(prompt, context, model):
            context_state.value = context
            if model == "Claude":
                return chat_with_claude(prompt, context)
            elif model == "OpenAI":
                return chat_with_openai(prompt, context)
            elif model == "OpenSource":
                return chat_with_open_source_model(prompt, context)

        text_submit.click(fn=handle_text_input, inputs=[text_input, context_input, model_choice], outputs=text_output)
    
    with gr.Tab("File Upload"):
        file_input = gr.File(label="Upload a file (CSV or TXT)")
        context_input_file = gr.Textbox(label="Enter context for file (optional)")
        model_choice_file = gr.Radio(label="Choose Model", choices=["Claude", "OpenAI", "OpenSource"], value="Claude")
        file_output = gr.Textbox(label="Model's response from file content")
        file_submit = gr.Button("Submit")
        
        def handle_file_input(file, context, model):
            context_state.value = context
            if file.name.endswith('.csv'):
                return process_file(file, context, model)
            elif file.name.endswith('.txt'):
                return process_txt_file(file, context, model)
            else:
                return "Unsupported file format. Please upload a CSV or TXT file."

        file_submit.click(fn=handle_file_input, inputs=[file_input, context_input_file, model_choice_file], outputs=file_output)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)

