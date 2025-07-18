import streamlit as st
import google.generativeai as genai
from typing import Optional, Dict, Any
import time
import json

# Page configuration
st.set_page_config(
    page_title="AI Translator Agent",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .translation-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e1e5e9;
        padding: 1rem;
    }
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e1e5e9;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .error-message {
        background: #fee;
        color: #c33;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #c33;
        margin: 1rem 0;
    }
    .success-message {
        background: #efe;
        color: #363;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #363;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9ff 0%, #e8ecff 100%);
    }
</style>
""", unsafe_allow_html=True)

class TranslatorAgent:
    """Professional AI Translator Agent with Gemini 2.0 Flash"""
    
    def __init__(self):
        self.gemini_model = None
        self.setup_api()
    
    def setup_api(self):
        """Initialize Gemini API client with proper error handling"""
        try:
            # Gemini setup
            if "GEMINI_API_KEY" in st.secrets:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            else:
                st.error("GEMINI_API_KEY not found in secrets.toml")
                
        except Exception as e:
            st.error(f"Error setting up Gemini API: {str(e)}")
    
    def translate_with_gemini(self, text: str, target_language: str, source_language: str = "auto") -> Optional[str]:
        """Translate text using Google Gemini 2.0 Flash"""
        try:
            if not self.gemini_model:
                return None
                
            if source_language == "auto":
                prompt = f"""
                Translate the following text to {target_language}.
                Provide only the translation without any additional text or explanations.
                
                Text to translate: {text}
                """
            else:
                prompt = f"""
                Translate the following text from {source_language} to {target_language}.
                Provide only the translation without any additional text or explanations.
                
                Text to translate: {text}
                """
            
            response = self.gemini_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            st.error(f"Gemini translation error: {str(e)}")
            return None
    
    def get_language_detection(self, text: str) -> str:
        """Detect language using Gemini 2.0 Flash"""
        try:
            if self.gemini_model:
                response = self.gemini_model.generate_content(
                    f"Detect the language of this text and respond with only the language name: {text[:200]}"
                )
                return response.text.strip()
        except Exception as e:
            st.warning(f"Language detection error: {str(e)}")
        return "Unknown"

def main():
    """Main application function"""
    
    # Initialize translator agent
    if 'translator' not in st.session_state:
        st.session_state.translator = TranslatorAgent()
    
    translator = st.session_state.translator
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 AI Translator Agent</h1>
        <p>Professional translation powered by Google Gemini 2.0 Flash</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Status
        st.markdown("### 📊 API Status")
        gemini_status = "✅ Connected" if translator.gemini_model else "❌ Not Available"
        
        st.markdown(f"**Gemini 2.0 Flash:** {gemini_status}")
        
        if not translator.gemini_model:
            st.error("Gemini API key not found! Please check your .streamlit/secrets.toml file.")
            st.stop()
        
        # Translation settings
        st.markdown("### 🎯 Translation Settings")
        
        # Language options
        languages = [
            "Spanish", "French", "German", "Italian", "Portuguese", "Russian",
            "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Dutch",
            "Swedish", "Norwegian", "Danish", "Finnish", "Polish", "Turkish",
            "Greek", "Hebrew", "Thai", "Vietnamese", "Indonesian", "Malay"
        ]
        
        target_language = st.selectbox("Target Language", languages, index=0)
        
        # Advanced options
        with st.expander("Advanced Options"):
            auto_detect = st.checkbox("Auto-detect source language", value=True)
            if not auto_detect:
                source_language = st.selectbox("Source Language", ["English"] + languages)
            else:
                source_language = "auto"
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Text")
        input_text = st.text_area(
            "Enter text to translate",
            height=200,
            placeholder="Type or paste your text here..."
        )
        
        # Translation controls
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        with col_btn1:
            translate_btn = st.button("🔄 Translate", use_container_width=True)
        
        with col_btn2:
            if st.button("🔍 Detect Language", use_container_width=True):
                if input_text.strip():
                    with st.spinner("Detecting language..."):
                        detected_lang = translator.get_language_detection(input_text)
                        st.info(f"Detected language: {detected_lang}")
        
        with col_btn3:
            if st.button("🗑️ Clear", use_container_width=True):
                st.rerun()
    
    with col2:
        st.markdown("### 🎯 Translation Result")
        
        if translate_btn and input_text.strip():
            with st.spinner("Translating..."):
                translation = translator.translate_with_gemini(
                    input_text, target_language, source_language
                )
                
                if translation:
                    st.markdown(f"""
                    <div class="translation-card">
                        <h4>Translation to {target_language}:</h4>
                        <p style="font-size: 1.1em; line-height: 1.5;">{translation}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Additional features
                    col_copy, col_download = st.columns([1, 1])
                    
                    with col_copy:
                        if st.button("📋 Copy Translation", use_container_width=True):
                            st.code(translation)
                    
                    with col_download:
                        st.download_button(
                            label="💾 Download Translation",
                            data=translation,
                            file_name=f"translation_{target_language.lower()}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    st.error("Translation failed. Please try again or check your API configuration.")
    
    # Statistics and usage info
    st.markdown("---")
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    with col_stats1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔤</h3>
            <p><strong>Character Count</strong></p>
            <p>{}</p>
        </div>
        """.format(len(input_text) if input_text else 0), unsafe_allow_html=True)
    
    with col_stats2:
        st.markdown("""
        <div class="metric-card">
            <h3>📝</h3>
            <p><strong>Word Count</strong></p>
            <p>{}</p>
        </div>
        """.format(len(input_text.split()) if input_text else 0), unsafe_allow_html=True)
    
    with col_stats3:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐</h3>
            <p><strong>Target Language</strong></p>
            <p>{}</p>
        </div>
        """.format(target_language), unsafe_allow_html=True)
    
    with col_stats4:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖</h3>
            <p><strong>AI Model</strong></p>
            <p>Gemini 2.0 Flash</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🌍 AI Translator Agent - Powered by Google Gemini 2.0 Flash</p>
        <p>Built with Streamlit | Professional Translation Services</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()