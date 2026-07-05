from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, SystemMessage
from app.agents.state import AgentState
from app.tools.web_tools import search_web

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

web_agent = create_react_agent(llm, tools=[search_web])

def web_node(state: AgentState):
    """Takes the user's message, runs it through the Web agent, and returns the response."""
    
    system_msg = SystemMessage(content="You have access to the open internet. You MUST use the search_web tool to look up current stock prices, real-time news, and weather. Do NOT refuse to answer.")
    messages = [system_msg] + state["messages"]
    
    response = web_agent.invoke({"messages": messages})
    final_answer = response["messages"][-1].content
    return {"messages": [AIMessage(content=final_answer)]}
    