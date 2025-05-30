# Prompt Playground

A versatile playground for experimenting with different AI models and prompt templates. This application allows you to test various AI models with different types of prompts, making it easy to compare responses and optimize your prompts.

## Features

- Multiple AI model support (OpenAI GPT-4, Anthropic Claude, Google Gemini)
- Pre-built prompt templates for different use cases
- Interactive UI with Streamlit
- Example inputs and outputs for each prompt template
- Secure API key management

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Running the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. Select an AI model from the dropdown menu
2. Choose a prompt template
3. Review the example input and output
4. Enter your input in the text area
5. Click "Generate Response" to see the AI's output

## Available Prompt Templates

- Customer Service Response
- Financial Analysis
- JSON Formatter

## Security Note

Never commit your `.env` file or expose your API keys. The `.env` file is included in `.gitignore` to prevent accidental commits.

## Contributing

Feel free to add more prompt templates or AI models by modifying the `prompts.py` and `models.py` files. # promptplayground
