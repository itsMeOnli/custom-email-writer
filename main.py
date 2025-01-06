import streamlit as st
import requests
import os
from typing import Dict

def get_llm_response(template: str, context: str, comments: str) -> Dict:
    """
    Send request to LLM API and get response.
    Note: This example uses Anthropic's API. Adjust based on your preferred LLM provider.
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found in environment variables")
    
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
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    return response.json()

def main():
    st.title("Email Template Customizer")
    
    # Add description
    st.write("""
    This app helps you customize email templates based on recipient context.
    Enter your template, provide context about the recipient, and add any additional comments.
    """)
    
    # Create input fields
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
    
    # Create submit button
    if st.button("Customize Email"):
        if not template or not context:
            st.error("Please provide both template and recipient context.")
            return
        
        try:
            with st.spinner("Customizing your email..."):
                response = get_llm_response(template, context, comments)
                
                # Extract the customized email from the response
                customized_email = response['content'][0]['text']
                
                # Display result in a new text area
                st.subheader("Customized Email")
                st.text_area(
                    "Result",
                    value=customized_email,
                    height=300,
                    key="result"
                )
                
                # Add a copy button
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
