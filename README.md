# Multi-Model Chatbot with LangChain and Pinecone

This project is a web-based client for interacting with the Claude 3.5 API, OpenAI API, DeepSeek-Coder-V2 model, and Pinecone using Gradio. It allows you to enter text prompts or upload CSV/TXT files to chat with different models, with optional context management and efficient data storage using Pinecone.

## Features

- Text input for prompts with Claude
- Text input for prompts with OpenAI (via LangChain)
- Text input for prompts with DeepSeek-Coder-V2
- CSV and TXT file upload for processing file content
- Context-aware prompts using LangChain
- Session management to maintain context
- Responsive web interface using Gradio
- Ability to switch between different models
- Efficient data storage and retrieval using Pinecone

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

4. Create a `.env` file in the root directory and add your API keys and the URL for the DeepSeek-Coder-V2 model:

   ```bash
   echo "CLAUDE_API_KEY=your_claude_api_key
   OPENAI_API_KEY=your_openai_api_key
   DEEPSEEK_API_URL=https://api.deepseek-ai.com/v2/completions
   DEEPSEEK_API_KEY=your_deepseek_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment" > .env
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
- **Text Input with DeepSeek:** Enter a prompt and optional context. The context will be used to provide more accurate responses from DeepSeek-Coder-V2.
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

4. **Text Input with DeepSeek:**
   - Context: "You are an AI assistant."
   - Prompt: "What is the capital of France?"
   - Response: "The capital of France is Paris."

## License

This project is licensed under the MIT License.

