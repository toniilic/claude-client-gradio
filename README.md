# Claude 3.5 Client with Gradio

This project is a web-based client for interacting with the Claude 3.5 API using Gradio. It allows you to enter text prompts or upload CSV files to chat with Claude 3.5.

## Features

- Text input for prompts
- CSV file upload for processing file content
- Responsive web interface using Gradio

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

4. Create a `.env` file in the root directory and add your Claude API key:

   ```bash
   echo "API_KEY=your_claude_api_key" > .env
   ```

### Running the Application

To start the Gradio interface, run:

```bash
python claude_client.py
```

Open your web browser and navigate to `http://localhost:8080`.

## License

This project is licensed under the MIT License.

