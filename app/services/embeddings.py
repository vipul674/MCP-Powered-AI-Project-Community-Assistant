from langchain_ollama import OllamaEmbeddings
import os

ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
embeddings_model = OllamaEmbeddings(model="nomic-embed-text", base_url=ollama_host)
