from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

ddg_search = DuckDuckGoSearchRun()

@tool
def search_web(query: str) -> str:
    """Searches the internet for real-time information, news, and general knowledge."""
    return ddg_search.invoke(query)
    