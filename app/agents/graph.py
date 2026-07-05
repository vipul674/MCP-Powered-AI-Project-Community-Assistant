from langgraph.graph import StateGraph, START, END
from app.agents.nodes_docs import docs_node
from app.agents.state import AgentState
from app.agents.nodes_router import router_node
from app.agents.nodes_github import github_node
from app.agents.nodes_response import fallback_node
from app.agents.nodes_web import web_node
from app.agents.nodes_issue import issue_preview_node, issue_execute_node

builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("github_worker", github_node)
builder.add_node("fallback_worker", fallback_node)
builder.add_node("docs_worker", docs_node)
builder.add_node("web_worker", web_node)
builder.add_node("issue_preview_worker", issue_preview_node)
builder.add_node("issue_execute_worker", issue_execute_node)

builder.add_edge(START, "router")

def route_condition(state: AgentState):
    """Reads the state and returns the string name of the next node."""
    print(f"ROUTE CONDITION STATE: {state.get('next_node')}", flush=True)
    if state.get("next_node") == "github":
        return "github_worker"
    if state.get("next_node") == "docs":
        return "docs_worker"
    if state.get("next_node") == "web":
        return "web_worker"
    if state.get("next_node") == "issue":
        return "issue_preview_worker"
    if state.get("next_node") == "issue_execute":
        return "issue_execute_worker"
    return "fallback_worker"

builder.add_conditional_edges("router", route_condition)

builder.add_edge("github_worker", END)
builder.add_edge("fallback_worker", END)
builder.add_edge("docs_worker", END)
builder.add_edge("web_worker", END)
builder.add_edge("issue_preview_worker", END)
builder.add_edge("issue_execute_worker", END)

app_graph = builder.compile()

def run_graph(prompt: str) -> str:
    """Helper function to execute the graph and extract the response."""

    final_state = app_graph.invoke({"messages": [("user", prompt)]})
    return final_state["messages"][-1].content

async def run_graph_stream(prompt: str):
    """Helper function to execute the graph and yield tokens as they stream."""
    async for event in app_graph.astream_events({"messages": [("user", prompt)]}, version="v2"):
        if event["event"] == "on_chat_model_stream":
            if event.get("metadata", {}).get("langgraph_node") == "router":
                continue
                
            chunk = event["data"]["chunk"].content
            if chunk:
                yield chunk
        
        elif event["event"] == "on_chain_end" and event["name"] == "issue_execute_worker":
            output = event["data"].get("output")
            if output and "messages" in output:
                yield output["messages"][-1].content
