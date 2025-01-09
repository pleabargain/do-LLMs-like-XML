import gradio as gr
import logging
from pathlib import Path
from ai_wrapper import AIProjectAssistant

# Set up logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "app.log",
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Initialize AI assistant
assistant = AIProjectAssistant()

# Project options
PROJECT_OPTIONS = {
    "Text-to-Image Generation": "Create an AI system that generates images from text descriptions",
    "GPT Chatbot Assistant": "Build a custom GPT-powered chatbot for specific domain knowledge",
    "Data Analysis Pipeline": "Develop an automated data processing and analysis system",
    "Web Scraping Tool": "Create a web scraper for collecting and organizing online data",
    "API Integration Service": "Build a service that integrates multiple third-party APIs",
    "Machine Learning Model": "Develop a machine learning model for specific use cases",
}

def get_model_choices() -> dict:
    """Get available models from the AI assistant."""
    logger.debug("Fetching available models")
    return assistant.get_available_models()

def update_model_choices(provider: str) -> gr.Dropdown:
    """Update model choices based on selected provider."""
    logger.debug(f"Updating model choices for provider: {provider}")
    models = get_model_choices()
    default_model = "gpt-4" if provider == "openai" else "llama3.2"
    return gr.Dropdown(
        choices=models.get(provider, []),
        value=default_model
    )

def process_input(input_type: str, query: str, provider: str, model: str) -> tuple[str, str]:
    """Process user input and return AI response."""
    if not query.strip():
        logger.warning("Empty query received")
        return "", "Please enter a query"
    
    logger.info(f"Processing {input_type} request")
    response = assistant.brainstorm_project(query) if input_type == "brainstorm" \
              else assistant.get_code_suggestion(query)
    
    if response["success"]:
        status = f"Success! Tokens: {response.get('tokens_used', 'N/A')}"
        logger.info(f"Request successful: {status}")
        return response["content"], status
    else:
        error_msg = f"Error: {response.get('error', 'Unknown error')}"
        logger.error(error_msg)
        return "", error_msg

def handle_project_click(project_name: str, provider: str, model: str) -> tuple[str, str, str]:
    """Handle project button clicks."""
    logger.info(f"Project selected: {project_name}")
    return (
        "brainstorm",
        PROJECT_OPTIONS[project_name],
        ""  # Clear previous output
    )

# Create Gradio interface
with gr.Blocks(title="AI Project Generator", css="footer {display: none !important}") as interface:
    gr.Markdown("# 🚀 AI Project Generator")
    gr.Markdown("Generate project ideas and get implementation guidance using AI")
    
    with gr.Tabs():
        with gr.Tab("Project Assistant"):
            with gr.Row():
                # Left sidebar
                with gr.Column(scale=1):
                    gr.Markdown("### 📂 Project Templates")
                    project_buttons = [
                        gr.Button(name, elem_classes="project-button")
                        for name in PROJECT_OPTIONS.keys()
                    ]
                
                # Main content
                with gr.Column(scale=3):
                    with gr.Row():
                        provider = gr.Radio(
                            choices=["openai", "ollama"],
                            label="🤖 AI Provider",
                            value=assistant.current_provider
                        )
                        model = gr.Dropdown(
                            choices=get_model_choices().get(
                                assistant.current_provider, []
                            ),
                            label="🔧 Model",
                            value=assistant.default_model.split(":")[0]
                        )
                    
                    input_type = gr.Radio(
                        choices=["brainstorm", "code"],
                        label="What kind of help do you need?",
                        value="brainstorm"
                    )
                    
                    query = gr.Textbox(
                        label="Enter your request",
                        placeholder="Describe your project idea or code query...",
                        lines=3
                    )
                    
                    submit_btn = gr.Button("🚀 Get AI Assistance", variant="primary")
                    
                    with gr.Column():
                        output = gr.Textbox(
                            label="AI Response",
                            lines=10
                        )
                        status = gr.Textbox(label="Status")
        
        with gr.Tab("API Configuration"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### OpenAI Configuration")
                    openai_status = gr.Textbox(
                        label="OpenAI Status",
                        value="✅ Connected" if assistant.openai_client
                        else "❌ Not Connected"
                    )
                    gr.Markdown("""
                    To use OpenAI:
                    1. Get an API key from [OpenAI](https://platform.openai.com)
                    2. Create a `.env` file in the project root
                    3. Add: `OPENAI_API_KEY=your-key-here`
                    """)
                
                with gr.Column():
                    gr.Markdown("### Ollama Configuration")
                    ollama_status = gr.Textbox(
                        label="Ollama Status",
                        value="✅ Connected" if "ollama" in get_model_choices()
                        else "❌ Not Connected"
                    )
                    gr.Markdown("""
                    To use Ollama:
                    1. [Install Ollama](https://ollama.ai)
                    2. Start the Ollama service
                    3. Pull models: `ollama pull llama3.2`
                    """)
    
    # Event handlers
    provider.change(
        fn=update_model_choices,
        inputs=[provider],
        outputs=[model]
    )
    
    submit_btn.click(
        fn=process_input,
        inputs=[input_type, query, provider, model],
        outputs=[output, status]
    )
    
    for btn in project_buttons:
        btn.click(
            fn=handle_project_click,
            inputs=[btn, provider, model],
            outputs=[input_type, query, output]
        )

# Launch the interface
if __name__ == "__main__":
    interface.launch()
