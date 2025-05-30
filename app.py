import streamlit as st
import asyncio
from models import ModelHandler
from prompts import PromptTemplates

# Initialize handlers
model_handler = ModelHandler()
prompt_templates = PromptTemplates()

# Set page config
st.set_page_config(
    page_title="Prompt Playground",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("🤖 Prompt Playground")
st.markdown("""
This playground allows you to experiment with different AI models and prompt templates.
Select a model and prompt type, then provide your input to see the results.
""")

# Create two columns for the layout
col1, col2 = st.columns([1, 1])

with col1:
    # Model selection
    st.subheader("Select Model")
    available_models = model_handler.get_available_models()
    selected_model = st.selectbox(
        "Choose an AI model",
        options=list(available_models.keys()),
        format_func=lambda x: f"{available_models[x]['name']} ({available_models[x]['provider']})"
    )
    
    # Display model description
    if selected_model:
        st.info(available_models[selected_model]['description'])

    # Prompt template selection
    st.subheader("Select Prompt Template")
    available_prompts = prompt_templates.get_available_prompts()
    selected_prompt = st.selectbox(
        "Choose a prompt template",
        options=list(available_prompts.keys()),
        format_func=lambda x: available_prompts[x]['name']
    )

    # Display prompt template details
    if selected_prompt:
        st.markdown("**Description:**")
        st.write(available_prompts[selected_prompt]['description'])
        
        st.markdown("**Example Input:**")
        st.code(available_prompts[selected_prompt]['example_input'])
        
        st.markdown("**Example Output:**")
        st.code(available_prompts[selected_prompt]['example_output'])

with col2:
    # User input
    st.subheader("Your Input")
    user_input = st.text_area(
        "Enter your input here",
        height=200,
        placeholder="Type your input here..."
    )

    # Generate button
    if st.button("Generate Response", type="primary"):
        if not user_input:
            st.warning("Please enter some input first!")
        else:
            with st.spinner("Generating response..."):
                # Get the formatted prompt
                prompt = prompt_templates.get_prompt(
                    selected_prompt,
                    query=user_input,
                    data=user_input,
                    text=user_input
                )
                
                # Generate response
                response = asyncio.run(
                    model_handler.generate_response(selected_model, prompt)
                )
                
                # Display response
                st.subheader("Generated Response")
                st.markdown(response)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit") 