import streamlit as st
import os

from src.langgraph_agentic_ai.ui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_ui(self):
        st.set_page_config(
            page_title=self.config.get_page_title(),
            page_icon=self.config.get_page_icon(),
            layout="wide"
        )

        with st.sidebar:
            st.title("Configuration Panel")

            # Get options from Config
            llm_options=self.config.get_llm_options()
            use_case_options=self.config.get_use_cases()
        
            self.user_controls['selelcted_llm']=st.selectbox("Selelct LLM Model",llm_options)

            if self.user_controls['selelcted_llm']=="OpenAI":
                openai_models=self.config.get_openai_models()
                self.user_controls['selected_openai_model']=st.selectbox("Select OpenAI Model",openai_models)
                self.user_controls['openai_api_key']=st.text_input("Enter OpenAI API Key",type="password")

            self.user_controls['selected_use_case']=st.selectbox("Select Use Case",use_case_options)

        return self.user_controls




    