from datetime import datetime

from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import get_settings

settings = get_settings()


class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

        self.message_history = InMemoryChatMessageHistory()

        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.google_api_key,
            temperature=self.temperature,
        )

        retriever = self.vectors.as_retriever(
            search_kwargs={"k": 4}
        )

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question, "
            "rewrite the question so it is understandable without "
            "the chat history. Do not answer the question."
        )

        contextualize_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            self.llm,
            retriever,
            contextualize_prompt,
        )

        qa_system_prompt = (
            "You are a helpful AI assistant."
            "\n\n"
            "Use the retrieved context to answer the question."
            " If the answer is not present in the context,"
            " say you don't know."
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(
            self.llm,
            qa_prompt,
        )

        self.rag_chain = create_retrieval_chain(
            history_aware_retriever,
            question_answer_chain,
        )

    def conversational_chat(
        self,
        query,
        conversation_id,
        session_id,
    ):

        self.message_history.add_user_message(query)

        response = self.rag_chain.invoke(
            {
                "input": query,
                "chat_history": self.message_history.messages,
            }
        )

        answer = response["answer"]

        self.message_history.add_ai_message(answer)

        return {
            "answer": answer,
            "conversation_id": conversation_id,
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat(),
        }