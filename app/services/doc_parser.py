import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store import add_texts_to_faiss

def parse_and_store_file(file_path: str, file_id: str) -> int:
    """Reads a file from disk, chunks it, stores it, and returns chunk count."""

    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        loader = PyPDFLoader(file_path)

        pages = loader.load()
        raw_text = "\n".join([page.page_content for page in pages])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = text_splitter.split_text(raw_text)

    add_texts_to_faiss(chunks)

    return len(chunks)
