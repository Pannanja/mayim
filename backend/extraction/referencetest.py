from pydantic import BaseModel
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2")


class BibleReference(BaseModel):
    """ Basic structure for handling scripture references """
    book: str
    chapter: int
    verse: int


structured_llm = llm.with_structured_output(BibleReference)
reference = structured_llm.invoke("extract chapter three verse twenty seven")


print(reference)