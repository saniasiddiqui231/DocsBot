print("1. Starting main.py")

from pathlib import Path

print("2. Imported pathlib")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

print("3. Imported FastAPI")

from app.api.upload_file import upload_router
print("4. Imported upload_router")

from app.api.prepare_chatbot import chatbot_router
print("5. Imported chatbot_router")


def create_application() -> FastAPI:
    app = FastAPI(
        title="Gemini RAG Chatbot API",
        version="2.0.0",
        description="RAG chatbot using Gemini, Sentence Transformers and FAISS",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    UPLOAD_DIR = (Path(__file__).resolve().parent / "Uploads").resolve()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    app.mount(
        "/uploads",
        StaticFiles(directory=str(UPLOAD_DIR)),
        name="uploads",
    )

    app.include_router(upload_router, tags=["Upload"])
    app.include_router(chatbot_router, tags=["Chatbot"])

    @app.get("/")
    async def root():
        return {"message": "Gemini RAG Chatbot API is running"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    @app.get("/uploads/{filename}")
    async def get_uploaded_file(filename: str):
        file_path = (UPLOAD_DIR / filename).resolve()

        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")

        if UPLOAD_DIR not in file_path.parents:
            raise HTTPException(status_code=403, detail="Access denied")

        return FileResponse(file_path)

    return app


app = create_application()