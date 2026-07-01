import os

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import get_settings

settings = get_settings()


def load_faiss_embeddings_file(
    embeddings_path: str,
):
    """
    Load a FAISS vector store.
    """

    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(
            f"Embedding folder not found: {embeddings_path}"
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=settings.google_api_key,
    )

    db = FAISS.load_local(
        folder_path=embeddings_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    return db