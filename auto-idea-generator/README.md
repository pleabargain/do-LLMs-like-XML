# AI Project Generator


# video
https://www.youtube.com/watch?v=XSS_KIHoQtE

# repo
https://github.com/pleabargain/do-LLMs-like-XML

# why

I kept reading that LLMs like XML so I tested it. I forked some code that worked. I made it better then I told Antrhopic to write a detailed XML describing the code. I then passed that XML to Anthropic to write the code. It did. It worked. In this case, Anthropic was able to create an entire piece of code using an XML description..

An AI-powered application that helps generate project ideas and implementation guidance using either OpenAI's GPT models or local Ollama models.

## Features

- Dual AI provider support (OpenAI and Ollama)
- Project brainstorming assistance
- Code implementation guidance
- Pre-defined project templates
- Real-time model switching
- Detailed logging system

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional)
- Ollama installed (optional)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd auto-idea-generator
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/macOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AI providers:

### OpenAI (Optional)
1. Get an API key from [OpenAI Platform](https://platform.openai.com)
2. Create a `.env` file in the project root (or edit the existing one)
3. Add your API key: `OPENAI_API_KEY=your-key-here`

### Ollama (Optional)
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Start the Ollama service
3. Pull the default model: `ollama pull llama3.2`

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:7860`

3. Choose your AI provider:
   - OpenAI: Requires API key, provides access to GPT models
   - Ollama: Free, runs locally, requires more system resources

4. Select your task type:
   - Brainstorm: Get project ideas and detailed outlines
   - Code: Get implementation guidance and code suggestions

5. Use pre-defined templates or enter your own project idea/query

## Project Structure

- `ai_wrapper.py`: Core AI functionality and provider integration
- `app.py`: Gradio web interface and application logic
- `requirements.txt`: Project dependencies
- `.env`: Configuration file for API keys
- `logs/`: Directory for application logs

## Logging

The application maintains detailed logs in the `logs/` directory:
- Debug level for detailed execution flow
- Info for general operational messages
- Warning for concerning but non-critical issues
- Error for failures that need attention

## Troubleshooting

### OpenAI Issues
- Verify API key format in `.env`
- Check OpenAI service status
- Ensure sufficient API credits

### Ollama Issues
- Verify Ollama is running: `curl http://localhost:11434/api/version`
- Check available models: `ollama list`
- Ensure sufficient system resources

### General Issues
- Check logs in `logs/app.log`
- Verify Python version compatibility
- Ensure all dependencies are installed
- Check network connectivity for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
