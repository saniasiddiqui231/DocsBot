import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_settings

settings = get_settings()


def load_faiss_embeddings_file(embeddings_path: str):
    """
    Load a FAISS vector store saved with save_local().
    """

    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(
            f"Embedding folder not found: {embeddings_path}"
        )

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    db = FAISS.load_local(
        folder_path=embeddings_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    return db