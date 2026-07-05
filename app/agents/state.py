from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    This directory represents the entire state of our application at any given moment.
    Every node in our graph will receive this dictionary, and can update parts of it.
    """

    messages: Annotated[list, add_messages]

    next_node: str
    