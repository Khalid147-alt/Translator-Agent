import streamlit as st
from dotenv import load_dotenv
import os
import asyncio

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

# Load Gemini API Key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file.")

# Setup Gemini-compatible OpenAI client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=external_client
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Define the Translator Agent
translator = Agent(
    name="Translator Agent",
    instructions="""You are a professional translator.
Translate the given text into the target language mentioned in this format:
Translate to <language>: <text>"""
)

# Streamlit UI
st.set_page_config(page_title="Translator Agent")
st.markdown(
    """
    <style>
        body {
            background-color: #f5f0f2; /* light blue-gray */
        }

        .stApp {
            background-color: #f2f9f1;
        }

        /* Optional: Customize text colors */
        h1, h2, h3, h4, h5, h6, p {
            color: #003366; /* deep blue text */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Translator Agent ")

text_input = st.text_area("Enter text to translate:")
target_lang = st.selectbox("Translate to:", ["Urdu", "French", "Arabic", "Chinese", "Spanish", "Sindhi"])


async def translate_text(user_input):
    return await Runner.run(translator, input=user_input, run_config=config)

if st.button("Translate"):
    if text_input and target_lang:
        with st.spinner("Translating (please wait)..."):
            user_input = f"Translate to {target_lang}: {text_input}"
            result = asyncio.run(translate_text(user_input))
            st.success("✅ Translated!")
            st.markdown(f"### 🗣️ Translated Text:\n{result.final_output}")
