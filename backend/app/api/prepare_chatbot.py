import os
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .chatbot import Chatbot
from .load_faiss_embeddings import load_faiss_embeddings_file

from app.config import get_settings

settings = get_settings()

chatbot_router = APIRouter()

embeddings_folder_path = os.path.join(
    Path(__file__).parent.parent,
    "Embeddings",
)

session_id_temp = None


def get_chatbot_for_user_selected_file(file_path: str):

    filename = Path(file_path).stem

    embeddings_path = os.path.join(
    embeddings_folder_path,
    filename,
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