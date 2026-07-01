import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

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

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
    )

    db = FAISS.load_local(
        folder_path=embeddings_path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )

    return db