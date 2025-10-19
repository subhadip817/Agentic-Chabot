from src.langgraph_agentic_ai.state.state import State
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self, llm):
        self.tavily=TavilyClient()
        self.llm=llm
        self.state={}

    def fetch_news(self,state:State)->dict:
        frequency=state["messages"][0].content.lower()
        self.state["frequency"]=frequency
        time_range_map={
            "daily":"d",
            "weekly":"w",
            "monthly":"m",
            "yearly":"y"
        }
        day_map={
            "daily":1,
            "weekly":7,
            "monthly":30,
            "yearly":365
        }

        response=self.tavily.search(
            query="Latest AI News in India and Globally",
            topic="news",
            time_range=time_range_map[frequency],
            max_results=20,
            days=day_map[frequency],
            sort_by="relevance"
        )

        self.state["news_data"]=response.get("results",[])
        return self.state

    def summarize_news(self,state:State)->dict:
        news_data=self.state["news_data"]
        prompt_template=ChatPromptTemplate.from_messages([
            ("system","""
            Summarise AI new in markdown format. For each news please follow the following format:
            - Title: <title of the news>
            - Date: <date of the news>
            - Content: <summary of the news>
            - Link: <link to the news>
            """),
            ("user","Articles:\n{articles}")
        ])

        articles_content="\n".join([f"Title: {item['title']}\nDate: {item['published_date']}\nContent: {item['content']}\nLink: {item['url']}\n" for item in news_data])
        
        response=self.llm.invoke(prompt_template.format_messages(articles=articles_content))
        self.state["summary"]=response.content
        return self.state

    def save_results(self,state:State)->dict:
        summary=self.state["summary"]
        frequency=self.state["frequency"]
        filename=f"./AINEWS/AI_News_Summary_{frequency}.md"
        with open(filename,"w") as f:
            f.write(f"# AI News Summary - {frequency.capitalize()}\n\n")
            f.write(summary)
        self.state["filename"]=filename
        return self.state