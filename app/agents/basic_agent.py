from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from app.tools.github_tools import search_repositories, get_repository_readme, get_repository_metadata

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

@tool
def search_github(query: str, limit: int = 5) -> list[dict]:
    """Search for GitHub repositories using a text query."""
    return search_repositories(query, limit)

@tool
def get_readme(owner: str, repo: str) -> str:
    """Fetch the decoded README content of a specific GitHub repository."""
    return get_repository_readme(owner, repo)

@tool
def get_metadata(owner: str, repo: str) -> dict:
    """Fetch basic metadata about a GitHub repository (stars, issues, language."""
    return get_repository_metadata(owner, repo)

tools = [search_github, get_readme, get_metadata]

agent_executor = create_react_agent(llm, tools)

def run_agent(prompt: str) -> str:
    """Helper function to run the agent and extract the final text response."""
    response = agent_executor.invoke({"messages": [("user", prompt)]})

    return response["messages"][-1].content