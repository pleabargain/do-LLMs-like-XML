import logging
import os
import requests
from openai import OpenAI
from typing import Dict, Any, Optional
from pathlib import Path

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

class AIProjectAssistant:
    def __init__(self):
        self.openai_client = None
        self.ollama_endpoint = "http://localhost:11434"
        self.current_provider = None
        self.default_temperature = 0.7
        
        # Initialize OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                self.current_provider = "openai"
                self.default_model = "gpt-4"
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        # Check Ollama
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/version")
            if response.status_code == 200:
                self.current_provider = self.current_provider or "ollama"
                self.default_model = "llama3.2:latest"
                logger.info(f"Ollama detected: {response.json().get('version')}")
        except Exception as e:
            logger.error(f"Failed to detect Ollama: {e}")

    def get_available_models(self) -> Dict[str, list]:
        models = {"openai": [], "ollama": []}
        
        if self.openai_client:
            models["openai"] = ["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo"]
            logger.debug("Retrieved OpenAI models")
        
        try:
            response = requests.get(f"{self.ollama_endpoint}/api/tags")
            if response.status_code == 200:
                models["ollama"] = [model["name"].split(":")[0] 
                                  for model in response.json().get("models", [])]
                logger.debug(f"Retrieved Ollama models: {models['ollama']}")
        except Exception as e:
            logger.error(f"Failed to get Ollama models: {e}")
        
        return models

    def send_prompt(self, prompt: str, provider: Optional[str] = None,
                   model: Optional[str] = None, 
                   temperature: Optional[float] = None) -> Dict[str, Any]:
        provider = provider or self.current_provider
        temp = temperature or self.default_temperature
        
        if provider == "openai":
            model = model or "gpt-4"
        else:
            if model and not ":" in model:
                model = f"{model}:latest"
            else:
                model = self.default_model
        
        logger.info(f"Sending prompt using {provider} with model {model}")
        
        try:
            if provider == "openai" and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temp
                )
                logger.debug(f"OpenAI API response received")
                return {
                    "success": True,
                    "content": response.choices[0].message.content,
                    "tokens_used": response.usage.total_tokens
                }
            elif provider == "ollama":
                logger.debug(f"Sending request to Ollama")
                response = requests.post(
                    f"{self.ollama_endpoint}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "temperature": temp
                    }
                )
                response.raise_for_status()
                logger.debug("Ollama API response received")
                return {
                    "success": True,
                    "content": response.json().get("response", ""),
                    "tokens_used": "N/A"
                }
            else:
                raise ValueError(f"Invalid provider: {provider}")
        except Exception as e:
            logger.error(f"Error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def brainstorm_project(self, query: str) -> Dict[str, Any]:
        prompt = f"""Given the following project idea or requirements, provide a detailed project outline:

{query}

Include:
1. Project overview and goals
2. Key features and functionality
3. Technical requirements
4. Implementation steps
5. Potential challenges and solutions
"""
        return self.send_prompt(prompt)

    def get_code_suggestion(self, query: str) -> Dict[str, Any]:
        prompt = f"""Given the following code-related query, provide a detailed solution:

{query}

Include:
1. Code implementation
2. Explanation of the approach
3. Any important considerations
4. Best practices and optimization tips
"""
        return self.send_prompt(prompt)
