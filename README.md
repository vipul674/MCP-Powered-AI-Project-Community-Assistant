# MCP-Powered AI Community Assistant

A completely local, privacy-first AI Assistant built with LangGraph, FastAPI, and Streamlit. This assistant is capable of routing user requests to specialized AI workers to query GitHub, search local documents via FAISS, or browse the open web.

## 🌟 Features

*   **LangGraph Orchestration**: Uses a deterministic router to parse user intent and direct traffic to specialized worker nodes.
*   **Model Context Protocol (MCP)**: Implements standard standard I/O server architecture to expose GitHub API tools securely.
*   **Local RAG (Retrieval-Augmented Generation)**: Uses Ollama embeddings (`nomic-embed-text`) and FAISS to chunk, store, and semantically search uploaded PDFs and text files without relying on paid APIs.
*   **Live Web Search**: Integrates DuckDuckGo via LangChain community tools for real-time web querying.
*   **100% Local Inference**: Runs entirely on open-weights models (via Ollama) ensuring absolute data privacy.
*   **Dual-Container Docker Deployment**: Fully dockerized backend (FastAPI) and frontend (Streamlit) communicating over a private virtual network.

## 🏗️ Architecture

1.  **Streamlit Frontend**: Provides a chat interface and file-upload widget.
2.  **FastAPI Backend**: Exposes the chat completion and file upload endpoints.
3.  **LangGraph Router**: 
    *   `github_worker`: Connects to the FastMCP server to search repositories.
    *   `docs_worker`: Embeds uploaded files and performs FAISS similarity search.
    *   `web_worker`: Uses DuckDuckGo to browse the open internet.
    *   `fallback_worker`: Handles unknown queries gracefully.

## 🚀 How to Run (Docker)

1. Ensure you have Docker and Docker Compose installed.
2. Create a `.env` file at the root and add your GitHub token:
   ```env
   GITHUB_TOKEN=your_token_here
   ```
3. Build and run the containers:
   ```bash
   docker compose up --build
   ```
4. Open `http://localhost:8501` in your browser!
