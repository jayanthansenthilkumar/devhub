import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import io
import json
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Function to convert image to byte array
def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# Get API Key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Path to store chat history file
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history from a JSON file
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Function to save chat history to a JSON file
def save_chat_history():
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(st.session_state.history, file)

# Create tabs in Streamlit
tabs = st.tabs(["Chatbot"])

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state.history = load_chat_history()

# Function to update chat history
def update_history(user_input, bot_response):
    st.session_state.history.append({"user": user_input, "bot": bot_response})
    save_chat_history()  # Save history to file after each update

# Function to add custom CSS styles
def add_custom_css():
    # Custom CSS for styling prompt area
    st.markdown("""
        <style>
            .prompt-textarea {
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                width: 100%;
                height: 150px;
                background-color: #f9f9f9;
                color: #333;
                box-sizing: border-box;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 4px;
                padding: 12px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

# Main function for the chatbot interface
def main():
    # Add custom CSS for styling
    add_custom_css()

    # Move the logo to the sidebar header
    with st.sidebar:
        st.image("./devhub.png", width=250)  # Display the logo in the sidebar
        st.write("### Chat History")

    with tabs[0]:  # Access the first (and only) tab
        st.header("Interact with Chatbot")
        st.write("")

        # Text area for prompt input with custom CSS class
        prompt = st.text_area(
            "Prompt", 
            placeholder="Enter your prompt here...", 
            height=150, 
            key="prompt",
            help="Type your query or message for the AI here.",
            label_visibility="visible"
        )

        # Display chat history in the sidebar (this will always be visible on the side)
        with st.sidebar:
            if len(st.session_state.history) == 0:
                st.write("No conversation yet.")
            else:
                # Display only keywords (first 3 words of user input)
                for i, entry in enumerate(st.session_state.history):
                    keyword = entry['user'][:30]  # Show the first 30 characters of the user input
                    if st.button(f"Show response for: {keyword}", key=f"show_{i}"):
                        # When clicked, display the full conversation
                        st.write(f"**User {i+1}:** {entry['user']}")
                        st.write(f"**AI {i+1}:** {entry['bot']}")
                        st.markdown("---")

        # Button to send the prompt
        if st.button("SEND", use_container_width=True):
            if prompt:
                # Initialize the model and generate content
                model = genai.GenerativeModel("gemini-pro")  # Adjust if needed for specific model

                # Generate the bot's response
                response = model.generate_content(prompt)
                bot_response = response.text

                # Display response in the main area
                st.write("### :blue[Response]")
                st.markdown(bot_response)

                # Save the conversation to history
                update_history(prompt, bot_response)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()