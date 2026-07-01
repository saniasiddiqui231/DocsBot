import os

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
)

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

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

    print("1. Loading document...")

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
    print("Loading document...")
    documents = loader.load()

    print("2. Splitting document...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    if filename.endswith(".csv"):
        chunks = documents
    else:
        chunks = splitter.split_documents(documents)

    print("3. Creating Google embeddings...")

    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
    )

    print("4. Building FAISS index...")

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

    print("5. Saving FAISS...")

    db.save_local(save_path)

    print("DONE")