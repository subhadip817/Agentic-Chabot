from langgraph.graph import StateGraph,START,END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_graph(self):
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def setup_graph(self,use_case):
        if use_case=="Basic Chatbot":
            self.basic_chatbot_graph()
        return self.graph_builder.compile()


    