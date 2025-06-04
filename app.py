import streamlit as st
from models import ModelHandler
from prompts import PromptTemplates
import re

# Initialize handlers
model_handler = ModelHandler()
prompt_handler = PromptTemplates()

# Set up the page
st.set_page_config(page_title="Prompt Playground", layout="wide")
st.title("Prompt Playground")

# Get available models
available_models = model_handler.get_available_models()

if not available_models:
    st.error("No AI models available. Please check your API keys in the .env file.")
    st.stop()

# Model selection
model_provider = st.selectbox(
    "Select Model Provider",
    options=list(set(model['provider'] for model in available_models.values()))
)

# Filter models by provider
provider_models = {
    model_id: model for model_id, model in available_models.items()
    if model['provider'] == model_provider
}

selected_model = st.selectbox(
    "Select Model",
    options=list(provider_models.keys()),
    format_func=lambda x: provider_models[x]['name']
)

# Prompt template selection
available_prompts = prompt_handler.get_available_prompts()
template_key = st.selectbox(
    "Select Prompt Template",
    options=list(available_prompts.keys())
)
template_data = available_prompts[template_key]
template_str = template_data['template']

# Show example input and output
st.markdown("**Example Input:**")
st.code(template_data.get('example_input', ''), language='text')
st.markdown("**Example Output:**")
st.code(template_data.get('example_output', ''), language='text')

# Extract template variables using regex
vars_in_template = re.findall(r'\{(\w+)\}', template_str)
user_inputs = {}

# Create input fields for template variables
for var in vars_in_template:
    user_inputs[var] = st.text_input(f"Enter {var}")

# Generate response directly
if st.button("Generate Response"):
    try:
        prompt = prompt_handler.get_prompt(template_key, **user_inputs)
        st.markdown("**Generated Prompt:**")
        st.text_area("Prompt Sent to Model", prompt, height=150)
        response = model_handler.generate_response(selected_model, prompt)
        st.markdown("**Model Response:**")
        st.text_area("Model Response", response, height=400)
    except Exception as e:
        st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 