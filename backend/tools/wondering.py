from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from typing import AsyncGenerator

class Wondering(BaseModel):
    topic: str
    question: str

@tool
async def generate_wondering(topic: str) -> AsyncGenerator[str, None]:
    """Generate a wondering based on the topic."""
    llm = ChatOllama(
        model="Llama3.2",
        max_tokens=10,
        temperature=0.5,
        stream=True,
        api_key="",
    )
    structured_llm = llm #.with_structured_output(Wondering)
    async for token in structured_llm.astream(f"Ponder {topic}"):
        yield token