from langchain_community.vectorstores import FAISS
from app.services.embeddings import embeddings_model
import os

FAISS_INDEX_PATH = "faiss_index"

def add_texts_to_faiss(chunks: list[str]):
    """Converts chunks of text into vectors and saves them to the FAISS database."""

    if os.path.exists(FAISS_INDEX_PATH):
        vector_store = FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings_model,
            allow_dangerous_deserialization=True
        )

        vector_store.add_texts(chunks)
    else:
        vector_store = FAISS.from_texts(chunks, embeddings_model)

    vector_store.save_local(FAISS_INDEX_PATH)

def search_faiss(query: str, top_k: int = 4) -> list[str]:
    """Converts a query to a vector, finds the closest matches, and returns the text."""
    if not os.path.exists(FAISS_INDEX_PATH):
        return ["No documents have been uploaded yet!"]

    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings_model,
        allow_dangerous_deserialization=True
    )

    results = vector_store.similarity_search(query, k=top_k)

    return [doc.page_content for doc in results]
    