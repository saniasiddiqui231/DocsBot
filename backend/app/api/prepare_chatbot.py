import os
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .chatbot import Chatbot
from .load_faiss_embeddings import load_faiss_embeddings_file
from .store_faiss_embeddings import save_faiss_embeddings_file

from app.config import get_settings

settings = get_settings()

chatbot_router = APIRouter()

embeddings_folder_path = os.path.join(
    Path(__file__).parent.parent,
    "Embeddings",
)
upload_folder_path = os.path.join(
    Path(__file__).parent.parent,
    "Uploads",
)

os.makedirs(embeddings_folder_path, exist_ok=True)
os.makedirs(upload_folder_path, exist_ok=True)

session_id_temp = None


def _resolve_uploaded_file(file_path: str) -> str | None:
    candidate_paths = []
    raw_path = Path(file_path)

    if raw_path.is_absolute():
        candidate_paths.append(raw_path)
    else:
        candidate_paths.append(raw_path)
        candidate_paths.append(Path(upload_folder_path) / raw_path.name)
        candidate_paths.append(Path(upload_folder_path) / raw_path.stem)

    for candidate in candidate_paths:
        if candidate.exists() and candidate.is_file():
            return str(candidate)

    return None


def get_chatbot_for_user_selected_file(file_path: str):

    filename = Path(file_path).stem

    embeddings_path = os.path.join(
        embeddings_folder_path,
        filename,
    )

    resolved_file_path = _resolve_uploaded_file(file_path)

    if not os.path.exists(embeddings_path):
        if resolved_file_path is None:
            raise FileNotFoundError(
                f"Uploaded file not found and embeddings folder is missing: {file_path}"
            )

        save_faiss_embeddings_file(
            file_path=resolved_file_path,
            embeddings_folder_path=embeddings_folder_path,
        )

    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(
            f"Embedding folder not found after regeneration: {embeddings_path}"
        )

    db = load_faiss_embeddings_file(
        embeddings_path=embeddings_path
    )

    chatbot = Chatbot(
        model_name=settings.model_name,
        temperature=0.2,
        vectors=db,
    )

    return chatbot, str(uuid.uuid4())


@chatbot_router.post(
    "/prepare_chatbot",
    description="Prepare chatbot",
)
async def prepare_chatbot_over_subset(
    uploaded_filepath: str,
):

    global session_id_temp

    if not uploaded_filepath:
        raise HTTPException(
            status_code=400,
            detail="Please upload a file first.",
        )

    chatbot, session_id = get_chatbot_for_user_selected_file(
        uploaded_filepath
    )

    chatbot_router.chatbot = chatbot
    session_id_temp = session_id

    return {
        "status": "Chatbot ready",
        "session_id": session_id,
    }


class Response(BaseModel):
    answer: str


@chatbot_router.post(
    "/chat",
    response_model=Response,
)
async def chat_with_bot(query: str):

    if not hasattr(chatbot_router, "chatbot"):
        raise HTTPException(
            status_code=400,
            detail="Prepare chatbot first.",
        )

    conversation_id = str(uuid.uuid4())

    response = chatbot_router.chatbot.conversational_chat(
        query=query,
        conversation_id=conversation_id,
        session_id=session_id_temp,
    )

    return {
        "answer": response["answer"],
    }


@chatbot_router.get("/chat_history")
async def get_chat_history():

    if not hasattr(chatbot_router, "chatbot"):
        raise HTTPException(
            status_code=400,
            detail="Prepare chatbot first.",
        )

    return {
        "chat_history":
        chatbot_router.chatbot.message_history.messages
    }