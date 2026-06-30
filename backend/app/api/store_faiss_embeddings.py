import os
import pickle

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
)
 
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from app.config import get_settings

settings = get_settings()


def save_faiss_embeddings_file(
    file_path: str,
    embeddings_folder_path: str,
):
    """
    Create FAISS embeddings from supported documents
    and save them locally.
    """

    filename = os.path.basename(file_path)

    if filename.endswith(".pdf"):
        loader = PyPDFLoader(file_path)

    elif filename.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")

    elif filename.endswith((".doc", ".docx")):
        loader = Docx2txtLoader(file_path)

    elif filename.endswith(".csv"):
        loader = CSVLoader(file_path)

    else:
        raise ValueError(f"Unsupported file type: {filename}")

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    if filename.endswith(".csv"):
        chunks = documents
    else:
        chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    db = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    save_name = os.path.splitext(filename)[0]

    save_path = os.path.join(
    embeddings_folder_path,
    save_name,
)

    os.makedirs(save_path, exist_ok=True)

    db.save_local(save_path)