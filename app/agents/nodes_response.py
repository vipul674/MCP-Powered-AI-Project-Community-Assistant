from langchain_core.messages import AIMessage
from app.agents.state import AgentState

def fallback_node(state: AgentState):
    """A simple hardcoded fallback for when the router doesn't know what to do."""

    reply = "I'm sorry, I am a specialized community assistant. I only know how to help with GitHub repositories right now! Ask me to search for a repo."

    return {"messages": [AIMessage(content=reply)]}
