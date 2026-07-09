from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import AgentState

class Route(BaseModel):
    step: str = Field(
        description="The next step to route to. Must be one of: 'github', 'docs', 'web', 'issue', 'fallback'"
    )
    
llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

structured_llm = llm.with_structured_output(Route)

system_prompt = """You are an intelligent router for a community assistant.
Analyze the user's message and route them to the correct department:
- 'github': If they are asking about repositories, stars, code, reading/checking existing issues, or GitHub metadata.
- 'docs': If they are asking to read documentation or upload files.
- 'web': If they are asking for real-time news, general knowledge, weather, stock prices, or internet search.
- 'issue': ONLY if they are explicitly asking to CREATE a new Github issue.
- 'fallback': For basic greetings, unknown requests, or anything else.

You MUST respond with a valid JSON object containing exactly one key 'step', whose value is one of the strings above. Do not include any other text or markdown formatting.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{user_message}")
])

router_chain = prompt | structured_llm

def router_node(state: AgentState):
    user_message = state["messages"][-1].content

    if user_message.startswith("/confirm_issue"):
        print("Router Decision: issue_execute (bypass)", flush=True)
        return {"next_node": "issue_execute"}

    try:
        result = router_chain.invoke({"user_message": user_message})
        # If it's a Route object
        if hasattr(result, "step"):
            step = result.step
        # If it somehow returned a raw dictionary
        elif isinstance(result, dict) and "step" in result:
            step = result["step"]
        # If it somehow returned a string, we might just try to guess if it's "web" or something
        elif isinstance(result, str):
            if "web" in result.lower():
                step = "web"
            elif "github" in result.lower():
                step = "github"
            else:
                step = "fallback"
        else:
            step = "fallback"
    except Exception as e:
        print(f"ROUTER ERROR: {e}")
        step = "fallback"

    print(f"ROUTER DECISION: {step}", flush=True)

    return {"next_node": step}
