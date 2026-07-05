import json
from langchain_core.messages import AIMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from app.agents.state import AgentState
from app.tools.github_tools import create_github_issue

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

issue_agent = create_react_agent(llm, tools=[create_github_issue])

def issue_preview_node(state: AgentState):
    """
    Step 1: Parse the user's intent and generate a JSON preview.
    We inject a special [ISSUE_PREVIEW] flag that the Streamlit UI will look for.
    """
    user_message = state["messages"][-1].content

    prompt= f"""
    The user wants to create a Github issues. Extract the repo, title, 
    body and an appropriate list of labels (e.g. ["bug", "help wanted"]) from this request:
    {user_message}

    You must respond with exactly this JSON format and nothing else:
    [ISSUE_PREVIEW] {{"repo": "owner/repo", "title": "...", "body": "...", "labels": ["..."]}}
    """

    response = llm.invoke(prompt)
    return {"messages": [AIMessage(content=response.content)]}

def issue_execute_node(state: AgentState):
    """
    Step 2: The frontend sends the hidden /confirm_issue command.
    We parse the JSON and execute the actual tool.
    """
    user_message = state["messages"][-1].content
    json_str = user_message.replace("/confirm_issue ", "").strip()

    try:
        data = json.loads(json_str)

        result = create_github_issue.invoke(data)
        return {"messages": [AIMessage(content=result)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error parsing issue data: {e}")]}
