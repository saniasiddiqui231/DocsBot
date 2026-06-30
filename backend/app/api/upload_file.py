import os
import shutil
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from .store_faiss_embeddings import save_faiss_embeddings_file

upload_router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent / "Uploads"
EMBEDDINGS_DIR = Path(__file__).parent.parent / "Embeddings"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "pdf",
    "txt",
    "doc",
    "docx",
    "csv",
}


def is_allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_router.post("/upload_process_file")
async def upload_file_create_embeddings(file: UploadFile):

    if file.filename is None:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type.",
        )

    file_path = UPLOAD_DIR / file.filename

    if not file_path.exists():

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        save_faiss_embeddings_file(
            file_path=str(file_path),
            embeddings_folder_path=str(EMBEDDINGS_DIR),
        )

        return {
            "filename": file.filename,
            "status": "Embeddings created successfully.",
        }

    return {
        "filename": file.filename,
        "status": "File already exists.",
    }