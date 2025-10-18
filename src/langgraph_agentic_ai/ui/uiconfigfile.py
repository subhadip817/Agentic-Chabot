from configparser import ConfigParser

class Config:
    def __init__(self, config_file="./src/langgraph_agentic_ai/ui/uiconfigfile.ini"):
        self.config_file = config_file
        self.config = ConfigParser()
        self.config.read(self.config_file)

    def get_llm_options(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS").split(", ")
    
    def get_use_cases(self):
        return self.config["DEFAULT"].get("USE_CASE").split(", ")
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    
    def get_page_icon(self):
        return self.config["DEFAULT"].get("PAGE_ICON")
    
    def get_openai_models(self):
        return self.config["DEFAULT"].get("OPENAI_MODEL").split(",")
    