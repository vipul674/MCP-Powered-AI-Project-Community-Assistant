from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from app.agents.state import AgentState
from app.tools.doc_tools import search_uploaded_docs

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)
docs_agent = create_react_agent(llm, tools=[search_uploaded_docs])

def docs_node(state: AgentState):
    """Takes the user's message, runs it through the Docs agent, and returns the response."""
    response = docs_agent.invoke({"messages": state["messages"]})
    final_answer = response["messages"][-1].content
    return {"messages": [AIMessage(content=final_answer)]}
    