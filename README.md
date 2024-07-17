# Multi-Model Chatbot with LangChain

This project is a web-based client for interacting with the Claude 3.5 API, OpenAI API, and an open-source model using Gradio. It allows you to enter text prompts or upload CSV/TXT files to chat with different models, with optional context management to optimize responses.

## Features

- Text input for prompts with Claude
- Text input for prompts with OpenAI (via LangChain)
- Text input for prompts with an open-source model
- CSV and TXT file upload for processing file content
- Context-aware prompts using LangChain
- Session management to maintain context
- Responsive web interface using Gradio
- Ability to switch between different models

## Setup Instructions

### Prerequisites

- Python 3.6 or higher
- Virtualenv (recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/toniilic/claude-client-gradio.git
   cd claude-client-gradio
   ```

2. Set up the virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your API keys and the URL for the open-source model:

   ```bash
   echo "CLAUDE_API_KEY=your_claude_api_key
   OPENAI_API_KEY=your_openai_api_key
   OPEN_SOURCE_MODEL_API_URL=https://your_open_source_model_api_url" > .env
   ```

### Running the Application

To start the Gradio interface, run:

```bash
python claude_client.py
```

Open your web browser and navigate to `http://localhost:8080`.

### Usage

- **Text Input with Claude:** Enter a prompt and optional context. The context will be used to provide more accurate responses from Claude.
- **Text Input with OpenAI:** Enter a prompt and optional context. The context will be used to provide more accurate responses from OpenAI via LangChain.
- **Text Input with OpenSource:** Enter a prompt and optional context. The context will be used to provide more accurate responses from the open-source model.
- **File Upload:** Upload a CSV or TXT file and optionally provide context. The content of the file and context will be used to generate a response from the chosen model.

### Example

1. **Text Input with Claude:**
   - Context: "You are an AI assistant."
   - Prompt: "What is the capital of France?"
   - Response: "The capital of France is Paris."

2. **File Upload with Claude:**
   - Context: "Analyze the sales data."
   - File: `sales_data.csv`
   - Response: "The sales data indicates a 20% increase in revenue for Q2."

3. **Text Input with OpenAI:**
   - Context: "You are an AI assistant."
   - Prompt: "What is the capital of France?"
   - Response: "The capital of France is Paris."


