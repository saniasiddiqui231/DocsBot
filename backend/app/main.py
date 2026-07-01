print("1. Starting main.py")

from pathlib import Path

print("2. Imported pathlib")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    UPLOAD_DIR = Path(__file__).parent / "Uploads"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
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

    return app


app = create_application()