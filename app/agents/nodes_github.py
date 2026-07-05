from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.agents.state import AgentState
from app.tools.github_tools import search_repositories, get_repository_readme, get_repository_metadata
from langchain_core.tools import tool

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
    """Fetch the basic metadata abour a GitHub repository (stars, issues, language)."""
    return get_repository_metadata(owner, repo)

tools = [search_github, get_readme, get_metadata]
github_agent = create_react_agent(llm, tools)

def github_node(state: AgentState):
    """This node takes the user's message, runs it through the GitHub agent, and returns the response."""
    response = github_agent.invoke({"messages": state["messages"]})

    final_answer = response["messages"][-1].content
    return {"messages": [AIMessage(content=final_answer)]}
