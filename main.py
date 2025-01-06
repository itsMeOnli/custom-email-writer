import streamlit as st
import requests
import google.generativeai as genai
from openai import OpenAI
from typing import Dict

def get_openai_response(template: str, context: str, comments: str, model: str, api_key: str) -> str:
    """Handle OpenAI API requests"""
    if not api_key:
        raise ValueError("Please enter your OpenAI API key")
    
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    Email Template:
    {template}
    
    Recipient Context:
    {context}
    
    Additional Comments:
    {comments}
    
    Please customize this email template based on the recipient context and any additional comments provided.
    Make sure to maintain a professional tone while personalizing the content.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def get_google_response(template: str, context: str, comments: str, model: str, api_key: str) -> str:
    """Handle Google Gemini API requests"""
    if not api_key:
        raise ValueError("Please enter your Google API key")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    
    prompt = f"""
    Email Template:
    {template}
    
    Recipient Context:
    {context}
    
    Additional Comments:
    {comments}
    
    Please customize this email template based on the recipient context and any additional comments provided.
    Make sure to maintain a professional tone while personalizing the content.
    """
    
    response = model.generate_content(prompt)
    return response.text

def get_anthropic_response(template: str, context: str, comments: str, model: str, api_key: str) -> str:
    """Handle Anthropic API requests"""
    if not api_key:
        raise ValueError("Please enter your Anthropic API key")
    
    headers = {
        "x-api-key": api_key,
        "content-type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    
    prompt = f"""
    Email Template:
    {template}
    
    Recipient Context:
    {context}
    
    Additional Comments:
    {comments}
    
    Please customize this email template based on the recipient context and any additional comments provided.
    Make sure to maintain a professional tone while personalizing the content.
    """
    
    data = {
        "model": model,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    return response.json()['content'][0]['text']

def main():
    st.title("Email Template Customizer")
    
    st.write("""
    This app helps you customize email templates based on recipient context.
    Choose your preferred AI model and enter your API key below.
    """)
    
    # Initialize session state for storing API key
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    # API and Model Selection
    api_provider = st.selectbox(
        "Select API Provider",
        ["OpenAI", "Google", "Anthropic"]
    )
    
    # Model selection based on provider
    if api_provider == "OpenAI":
        model = st.selectbox(
            "Select Model",
            ["gpt-4", "gpt-3.5-turbo"]
        )
    elif api_provider == "Google":
        model = st.selectbox(
            "Select Model",
            ["gemini-pro"]
        )
    else:  # Anthropic
        model = st.selectbox(
            "Select Model",
            ["claude-3-sonnet-20240229", "claude-3-opus-20240229"]
        )
    
    # API Key input
    api_key = st.text_input(
        f"Enter your {api_provider} API Key",
        type="password",
        value=st.session_state.api_key
    )
    
    # Store API key in session state
    st.session_state.api_key = api_key
    
    # Input fields
    template = st.text_area(
        "Email Template",
        height=200,
        placeholder="Enter your email template here..."
    )
    
    context = st.text_area(
        "Recipient Context",
        height=150,
        placeholder="Enter information about the recipient..."
    )
    
    comments = st.text_area(
        "Additional Comments",
        height=100,
        placeholder="Any additional instructions or comments..."
    )
    
    if st.button("Customize Email"):
        if not template or not context:
            st.error("Please provide both template and recipient context.")
            return
        
        if not api_key:
            st.error(f"Please enter your {api_provider} API key.")
            return
        
        try:
            with st.spinner("Customizing your email..."):
                # Get response based on selected API
                if api_provider == "OpenAI":
                    customized_email = get_openai_response(template, context, comments, model, api_key)
                elif api_provider == "Google":
                    customized_email = get_google_response(template, context, comments, model, api_key)
                else:  # Anthropic
                    customized_email = get_anthropic_response(template, context, comments, model, api_key)
                
                # Display result
                st.subheader("Customized Email")
                st.text_area(
                    "Result",
                    value=customized_email,
                    height=300,
                    key="result"
                )
                
                # Copy button
                st.button(
                    "Copy to Clipboard",
                    on_click=lambda: st.write(
                        "<script>navigator.clipboard.writeText('''{}''')</script>".format(
                            customized_email
                        ),
                        unsafe_allow_html=True
                    )
                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
