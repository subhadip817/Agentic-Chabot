import streamlit as st

from src.langgraph_agentic_ai.ui.streamlit_ui.loadui import LoadStreamlitUI
from src.langgraph_agentic_ai.LLMs.openai_llm import OpanAILLM
from src.langgraph_agentic_ai.graph.graph_builder import GraphBuilder
from src.langgraph_agentic_ai.ui.streamlit_ui.display_result import DisplayResult

def load_app_ui():
    ui_loader=LoadStreamlitUI()
    user_inputs=ui_loader.load_ui()

    if not user_inputs:
        st.error("Failed to load UI components.")
        return None
    
    if st.session_state.IsFetchButtonClicked:
        user_message=st.session_state.time_frame
    else:
        user_message=st.chat_input("Enter your message here...")

    if user_message:
        try:
            llm_model=OpanAILLM(user_controls_input=user_inputs).get_llm_model()

            if not llm_model:
                st.error("Failed to initialize LLM model.")
                return None
            
            usecase=user_inputs.get("selected_use_case")

            if not usecase:
                st.error("No use case selected.")
                return None
            
            graph_builder=GraphBuilder(llm_model)
            try:
                graph=graph_builder.setup_graph(usecase)
            except Exception as e:
                st.error(f"Error setting up graph: {e}")

            try:
                DisplayResult(usecase,graph,user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error displaying result: {e}")

        except Exception as e:
            st.error(f"Error loading LLM model: {e}")
