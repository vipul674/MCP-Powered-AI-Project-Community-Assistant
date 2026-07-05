from langchain_core.tools import tool
from app.services.vector_store import search_faiss

@tool
def search_uploaded_docs(question: str) -> str:
    """Search the uploaded knowledge base (PDFs and Text files) to find answers."""

    results = search_faiss(question, top_k=4)
    return "\n\n---\n\n".join(results)