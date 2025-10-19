from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    tools=[TavilySearchResults(max_results=3)]
    return tools

def create_tool_node(tools):
    tool_node=ToolNode(tools=tools)
    return tool_node