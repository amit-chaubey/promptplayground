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
        # Initialize API clients
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        return {
            'gpt-4': {
                'name': 'GPT-4',
                'provider': 'OpenAI',
                'description': 'Most capable GPT model, optimized for complex tasks'
            },
            'claude-3-opus': {
                'name': 'Claude 3 Opus',
                'provider': 'Anthropic',
                'description': 'Most powerful Claude model for complex tasks'
            },
            'gemini-pro': {
                'name': 'Gemini Pro',
                'provider': 'Google',
                'description': 'Google\'s advanced language model'
            }
        }
    
    async def generate_response(self, model: str, prompt: str) -> str:
        try:
            if model.startswith('gpt'):
                response = await self.openai_client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            
            elif model.startswith('claude'):
                response = await self.anthropic_client.messages.create(
                    model=model,
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            
            elif model.startswith('gemini'):
                model = genai.GenerativeModel(model)
                response = await model.generate_content(prompt)
                return response.text
            
            else:
                raise ValueError(f"Unsupported model: {model}")
                
        except Exception as e:
            return f"Error generating response: {str(e)}" 