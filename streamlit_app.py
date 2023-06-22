import streamlit as st
import requests
import json

# OpenAI API configuration
OPENAI_API_KEY = 'YOUR_API_KEY'
API_ENDPOINT = 'https://api.openai.com/v1/engines/davinci-codex/completions'

# Streamlit app configuration
st.set_page_config(
    page_title="PDF Question Answering",
    layout="wide"
)

# Streamlit app title and description
st.title("PDF Question Answering with Instruct GPT-3.5")
st.markdown("Upload a PDF file and ask questions about its content.")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Display uploaded file details
    st.write("Uploaded file:", uploaded_file.name)
    
    # Read PDF content
    pdf_content = uploaded_file.read()

    # User question
    question = st.text_input("Enter your question")

    if st.button("Get Answer"):
        # Prepare the payload for OpenAI API
        payload = {
            'prompt': question,
            'documents': [pdf_content.decode('utf-8')],
            'max_tokens': 100
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }

        # Send request to OpenAI API
        response = requests.post(API_ENDPOINT, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            # Extract and display the answer
            data = response.json()
            answer = data['choices'][0]['text'].strip()
            st.success(f"Answer: {answer}")
        else:
            st.error("Something went wrong. Please try again later.")
