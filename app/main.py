from app.agents.graph import run_graph
from app.api.github import router as github_router
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Community Assistant",
    description="MCP-Powered AI Assistant",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "ok"}

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

from fastapi.responses import StreamingResponse
from app.agents.graph import run_graph, run_graph_stream

@app.post("/api/chat", response_model=ChatResponse)
def chat_placeholder(request: ChatRequest):
    """
    Takes the user's prompt from the Streamlit frontend, passes it to the LangGraph router, and returns the agent's final answer.
    """
    try:
        answer = run_graph(request.message)

        return ChatResponse(reply=answer)
    except Exception as e:
        return ChatResponse(reply=f"Error running agent: {e}")

@app.post("/api/chat_stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming version of the chat endpoint. Returns Server-Sent Events.
    """
    async def generate():
        async for chunk in run_graph_stream(request.message):
            yield chunk
    return StreamingResponse(generate(), media_type="text/event-stream")

from app.api.files import router as files_router

app.include_router(github_router)
app.include_router(files_router)