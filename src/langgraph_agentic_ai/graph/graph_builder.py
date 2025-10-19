from langgraph.graph import StateGraph,START,END
from src.langgraph_agentic_ai.state.state import State
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.tools.search_tools import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraph_agentic_ai.nodes.chatbot_with_tools_node import ChatbotWithToolsNode
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_graph(self):
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_graph(self):
        tools=get_tools()
        tool_node=create_tool_node(tools)
        llm=self.llm

        chatbot_with_tools=ChatbotWithToolsNode(llm)
        chatbot_node=chatbot_with_tools.create_chatbot(tools)
        
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")

    def ai_news_builder_graph(self):

        news_node=AINewsNode(self.llm)

        self.graph_builder.add_node("fetch_news",news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",news_node.summarize_news)
        self.graph_builder.add_node("save_results",news_node.save_results)

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_results")
        self.graph_builder.add_edge("save_results",END)
    
    def setup_graph(self,use_case):
        if use_case=="Basic Chatbot":
            self.basic_chatbot_graph()
        elif use_case=="Chatbot with Tools":
            self.chatbot_with_tools_graph()
        elif use_case=="AI News":
            self.ai_news_builder_graph()

        return self.graph_builder.compile()


