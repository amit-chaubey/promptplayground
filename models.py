import os
from typing import Dict, Any
import openai
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelHandler:
    def __init__(self):
        # Initialize API clients with error handling
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        google_key = os.getenv('GOOGLE_API_KEY')
        
        # Debug prints
        print("API Keys Status:")
        print(f"OpenAI Key: {'Present' if openai_key else 'Missing'}")
        print(f"Anthropic Key: {'Present' if anthropic_key else 'Missing'}")
        print(f"Google Key: {'Present' if google_key else 'Missing'}")
        
        if not openai_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        if not anthropic_key:
            print("Warning: ANTHROPIC_API_KEY not found in environment variables")
        if not google_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables")
            
        self.openai_client = openai.OpenAI(api_key=openai_key) if openai_key else None
        self.anthropic_client = Anthropic(api_key=anthropic_key) if anthropic_key else None
        if google_key:
            genai.configure(api_key=google_key)
        
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        models = {}
        
        if self.openai_client:
            models['gpt-4'] = {
                'name': 'GPT-4',
                'provider': 'OpenAI',
                'description': 'Most capable GPT model, optimized for complex tasks'
            }
            
        if self.anthropic_client:
            models['claude-3-opus'] = {
                'name': 'Claude 3 Opus',
                'provider': 'Anthropic',
                'description': 'Most powerful Claude model for complex tasks'
            }
            
        if os.getenv('GOOGLE_API_KEY'):
            models['gemini-pro'] = {
                'name': 'Gemini Pro',
                'provider': 'Google',
                'description': 'Google\'s advanced language model'
            }
            
        return models
    
    def _limit_words(self, text: str, max_words: int = 200) -> str:
        """Limit text to approximately max_words."""
        words = text.split()
        if len(words) <= max_words:
            return text
        return ' '.join(words[:max_words]) + '...'
    
    def generate_response(self, model: str, prompt: str) -> str:
        try:
            if model.startswith('gpt'):
                if not self.openai_client:
                    return "Error: OpenAI API key not configured"
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500  # Limit tokens to control response length
                )
                return self._limit_words(response.choices[0].message.content)
            
            elif model.startswith('claude'):
                if not self.anthropic_client:
                    return "Error: Anthropic API key not configured"
                response = self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=500,  # Limit tokens to control response length
                    messages=[{"role": "user", "content": prompt}]
                )
                return self._limit_words(response.content[0].text)
            
            elif model.startswith('gemini'):
                if not os.getenv('GOOGLE_API_KEY'):
                    return "Error: Google API key not configured"
                model = genai.GenerativeModel(model)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=500  # Limit tokens to control response length
                    )
                )
                return self._limit_words(response.text)
            
            else:
                raise ValueError(f"Unsupported model: {model}")
                
        except Exception as e:
            return f"Error generating response: {str(e)}" 