import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment
Google_API = os.getenv('GOOGLE_API_KEY')

# Ensure the API key is provided
if not Google_API:
    st.error("API key not found. Please set the `GOOGLE_API_KEY` in the .env file.")
    st.stop()

# Configure the API key
genai.configure(api_key=Google_API)

# Initialize the generative AI model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get chat response from the model
def get_chat_response(user_input):
    response = model.generate_content(user_input)
    return response.text

# Streamlit UI configuration
st.set_page_config(page_title="Shamas' Personal Chatbot", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS for better UI
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }
        .stApp {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }
        h1 {
            font-family: 'Arial', sans-serif;
            color: #333333;
        }
        .user-input {
            font-size: 1.1rem;
            font-family: 'Arial', sans-serif;
            color: #333333;
            background-color: #e6e6e6;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 1rem;
        }
        .bot-response {
            font-size: 1.1rem;
            font-family: 'Arial', sans-serif;
            color: #ffffff;
            background-color: #007bff;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            font-size: 1rem;
            font-family: 'Arial', sans-serif;
            border-radius: 5px;
            padding: 10px 20px;
        }
        .stTextInput>div>input {
            border: 2px solid #007bff;
            padding: 10px;
            border-radius: 5px;
            font-family: 'Arial', sans-serif;
            font-size: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

st.title("Shamas' Personal Chatbot 🤖")
st.write("Welcome to Shamas' personal chatbot powered by Google Generative AI. Ask anything, and get instant responses!")

if 'history' not in st.session_state:
    st.session_state['history'] = []

# Chat form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input('Your message:', max_chars=2000, label_visibility="collapsed")
    submit_button = st.form_submit_button('Send')

    if submit_button:
        if user_input:
            response = get_chat_response(user_input)
            st.session_state.history.append((user_input, response))
        else:
            st.warning('Please enter your prompt.')

# Display chat history
for user_input, response in st.session_state.history:
    st.markdown(f'<div class="user-input">**You:** {user_input}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bot-response">**Bot:** {response}</div>', unsafe_allow_html=True)

# Option to clear chat
if st.button('Clear Chat'):
    st.session_state.history = []
