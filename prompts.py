from typing import Dict, Any

class PromptTemplates:
    def __init__(self):
        self.templates = {
            'customer_service': {
                'name': 'Customer Service Response',
                'description': 'Generate a professional customer service response',
                'template': """You are a customer service representative. Please respond to the following customer query professionally and empathetically:

Customer Query: {query}

Please provide a response that:
1. Acknowledges the customer's concern
2. Provides a clear solution or next steps
3. Maintains a professional and friendly tone""",
                'example_input': "I've been waiting for my order for 2 weeks and haven't received any updates.",
                'example_output': "I understand your frustration with the delay in your order..."
            },
            'financial_analysis': {
                'name': 'Financial Analysis',
                'description': 'Analyze financial data and provide insights',
                'template': """Please analyze the following financial data and provide insights:

Data: {data}

Please provide:
1. Key financial metrics
2. Trend analysis
3. Recommendations""",
                'example_input': "Revenue: $1M, Expenses: $800K, Profit Margin: 20%",
                'example_output': "Based on the provided financial data..."
            },
            'json_formatter': {
                'name': 'JSON Formatter',
                'description': 'Convert text to structured JSON format',
                'template': """Please convert the following information into a well-structured JSON format:

Information: {text}

Requirements:
1. Use proper JSON syntax
2. Include all relevant fields
3. Maintain data hierarchy""",
                'example_input': "Name: John Doe, Age: 30, Occupation: Engineer",
                'example_output': '{"name": "John Doe", "age": 30, "occupation": "Engineer"}'
            }
        }
    
    def get_available_prompts(self) -> Dict[str, Dict[str, Any]]:
        return self.templates
    
    def get_prompt(self, prompt_type: str, **kwargs) -> str:
        if prompt_type not in self.templates:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        template = self.templates[prompt_type]['template']
        return template.format(**kwargs) 