import os
import streamlit as st
from langchain_openai import ChatOpenAI

class OpanAILLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            openai_api_key=self.user_controls_input["openai_api_key"]
            selected_openai_model=self.user_controls_input["selected_openai_model"]

            if not openai_api_key:
                st.error("OpenAI API Key is required.")

            llm=ChatOpenAI(model=selected_openai_model, api_key=openai_api_key, temperature=0)

        except Exception as e:
            raise ValueError(f"Error initializing OpenAI LLM: {e}")
        return llm