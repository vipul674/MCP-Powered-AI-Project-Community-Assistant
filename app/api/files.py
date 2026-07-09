import uuid
from fastapi import APIRouter, UploadFile, File
from app.services.doc_parser import parse_and_store_file

import os

router = APIRouter(prefix="/api/files", tags=["files"])

@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    contents = file.file.read()
    if not contents or len(contents) == 0:
        return {"file_id": None, "filename": file.filename, "chunks": 0, "warning": "Empty file uploaded. No content to process."}

    file_id = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(contents)

    chunk_count = parse_and_store_file(file_path, file_id)

    return {"file_id": file_id, "filename": file.filename, "chunks": chunk_count}
    