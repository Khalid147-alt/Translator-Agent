import streamlit as st
from agents import Agent, Runner
import os

# Load the Gemini API key from secrets
gemini_api_key = st.secrets["GEMINI_API_KEY"]
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Create the translator agent using OpenAI Agents SDK with Gemini model via LiteLLM
translator_agent = Agent(
    name="Translator Agent",
    instructions="You are a translator. Translate the given text from English to the specified language.",
    model="gemni-2.0-flash",
)

# Streamlit UI
st.title("Translator Agent")
st.write("Enter text in English and select a target language to get your translation.")

# Input components
input_text = st.text_area("Text to translate:", height=100, placeholder="Type your English text here...")
target_language = st.selectbox(
    "Target language:",
    ["French", "Spanish", "German", "Italian", "Japanese", "Urdu"],
    help="Choose the language to translate into"
)

# Translate button and logic
if st.button("Translate", key="translate_button"):
    if input_text.strip() and target_language:
        prompt = f"Translate to {target_language}: {input_text}"
        with st.spinner("Translating..."):
            try:
                result = Runner.run_sync(translator_agent, prompt)
                translated_text = result.final_output
                st.success("Translation completed!")
                st.write("Translated text:")
                st.text_area("", value=translated_text, height=100, disabled=True, key="output")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter text and select a target language.")