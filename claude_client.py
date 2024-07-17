import gradio as gr
import requests
import pandas as pd
import pinecone
from dotenv import load_dotenv
import os
from langchain import LLMChain, PromptTemplate, OpenAI

# Load API keys from .env file
load_dotenv()
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index_name = "context-index"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=512)

index = pinecone.Index(index_name)

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
    url = DEEPSEEK_API_URL
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
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

# Function to generate and store vectors using Pinecone
def generate_and_store_vectors(prompt, context, model):
    combined_text = f"{context} {prompt}"
    # Generate vector (dummy example; replace with actual embedding generation)
    vector = [0.0] * 512  # Replace with actual embedding
    response_text = ""
    if model == "Claude":
        response_text = chat_with_claude(prompt, context)
    elif model == "OpenAI":
        response_text = chat_with_openai(prompt, context)
    elif model == "DeepSeek":
        response_text = chat_with_open_source_model(prompt, context)
    # Store vector in Pinecone
    index.upsert([(response_text, vector)])
    return response_text

# Function to process CSV files
def process_file(file, context, model):
    try:
        df = pd.read_csv(file.name)
        file_content = df.to_string()
        return generate_and_store_vectors(file_content, context, model)
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Function to process TXT files
def process_txt_file(file, context, model):
    try:
        with open(file.name, 'r') as f:
            file_content = f.read()
        return generate_and_store_vectors(file_content, context, model)
    except Exception as e:
        return f"Error processing file: {str(e)}"

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Multi-Model Chatbot with LangChain and Pinecone")
    
    # Session management
    context_state = gr.State("")
    
    with gr.Tab("Text Input"):
        context_input = gr.Textbox(label="Enter context (optional)")
        text_input = gr.Textbox(label="Enter your prompt")
        model_choice = gr.Radio(label="Choose Model", choices=["Claude", "OpenAI", "DeepSeek"], value="Claude")
        text_output = gr.Textbox(label="Model's response")
        text_submit = gr.Button("Submit")
        
        def handle_text_input(prompt, context, model):
            context_state.value = context
            return generate_and_store_vectors(prompt, context, model)

        text_submit.click(fn=handle_text_input, inputs=[text_input, context_input, model_choice], outputs=text_output)
    
    with gr.Tab("File Upload"):
        file_input = gr.File(label="Upload a file (CSV or TXT)")
        context_input_file = gr.Textbox(label="Enter context for file (optional)")
        model_choice_file = gr.Radio(label="Choose Model", choices=["Claude", "OpenAI", "DeepSeek"], value="Claude")
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

