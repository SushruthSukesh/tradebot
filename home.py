import streamlit as st
import base64
import google.generativeai as genai

class AIStockChatbot:
    def __init__(self):
        """Initialize the AI Stock Market Chatbot"""
        self.model = self.initialize_ai_model()
        self.initialize_session()
        self.display_ui()

    def get_api_key(self, file_name):
        """Retrieve API key from a file"""
        with open(file_name, 'r') as file:
            return file.read().strip()

    def initialize_ai_model(self):
        """Initialize the generative AI model"""
        genai.configure(api_key=self.get_api_key('key.txt'))

        return genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=''' 
                You are a financial expert with deep knowledge of stock markets, trading strategies, technical analysis, 
                fundamental analysis, risk management, and economic trends. Your goal is to provide accurate, insightful, 
                and up-to-date financial advice to users.
            ''',
            generation_config={
                "temperature": 2,
                "top_p": 0.95,
                "top_k": 30,
                "max_output_tokens": 10000
            }
        )

    def initialize_session(self):
        """Initialize chat session"""
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = self.model.start_chat(history=[])

    def translate_role(self, user_role):
        """Translate role from model to Streamlit format"""
        return "assistant" if user_role == "model" else user_role

    def display_ui(self):
        """Render the UI components"""
        st.markdown("<h1>🤖 Welcome to AI Stock Market</h1>", unsafe_allow_html=True)

        # Add a futuristic stock market animation
        st.image("https://source.unsplash.com/1600x900/?stock,market,3d,ai", use_column_width=True)

        st.markdown("""
            <div style="text-align: center;">
                <h2 style="color: white;">🚀 Powered by AI & Machine Learning</h2>
                <p style="color: #00FFEA; font-size: 18px;">Analyze stock trends with powerful AI algorithms.</p>
            </div>
        """, unsafe_allow_html=True)

        # Display chat history
        for message in st.session_state.chat_session.history:
            with st.chat_message(self.translate_role(message.role)):
                st.markdown(message.parts[0].text)

        # Handle user input
        prompt = st.chat_input("What do you wish to know?")
        if prompt:
            st.chat_message("user").markdown(prompt)
            response = st.session_state.chat_session.send_message(prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
