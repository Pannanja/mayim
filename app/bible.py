# This module exposes a chat interface for interacting with the scriptural database.
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Translate user input into pirate speak",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{text}"),
    ]
)

_model = ChatOllama(
    model="llama3.1"
)

chain = _prompt | _model