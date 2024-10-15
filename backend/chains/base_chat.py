import asyncio
from typing import Annotated, Optional, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from starlette.responses import StreamingResponse
from pydantic import BaseModel, Field, computed_field
from .database.sqlalchemy_models import Translation as TranslationData, Book as BookData, Verse as VerseData, TranslationBook
from .extraction.inferred_models import Book, Chapter, Verse, Translation
from .database.dbconnection import get_session
from sqlalchemy import select

session = get_session()



class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = ChatOllama(model="llama3.1", temperature=0, stream=True)


def chatbot(state: State):
    return {"messages": llm.invoke(state["messages"])}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()


class Chapter(BaseModel):
    book: str = Field(alias="book_name")
    chapter: int = Field(alias="chapter_number")
    verses: List[Verse]

class BibleReference(BaseModel):
    book: str
    chapter: int
    verse: int

class RetrievedVerse(BaseModel):
    id: int
    book_id: int
    book_name: str
    book_english_name: str
    chapter: int
    verse_number: int
    original_text: str
    translated_text: Optional[str] = None
    translation_id: Optional[int] = None
    translation_name: Optional[str] = None

@tool
def fetch_scripture(book: str, chapter: int, verse: int) -> List[RetrievedVerse]:
    """ Retrieve scriptural text from the database given a reference """
    reference = BibleReference(book=book, chapter=chapter, verse=verse)
    pydantic_verses = []
    results = select(Verse).join(Book, Verse.book_id == Book.id).join(Translation, Verse.translation_id == Translation.id).where(Book.name_in_english == book).where(Verse.chapter == reference.chapter).where(Verse.verse == reference.verse)
    for result in session.scalars(results):
        pydantic_verses.append(Verse(id=result.id, book=result.book.name_in_english, chapter=result.chapter, verse=result.verse, text=result.text))
    return pydantic_verses

class RetrievedScripture(BaseModel):
    book: str
    chapter: int
    verse: int

    @computed_field
    @property
    def reference(self) -> BibleReference:
        return BibleReference(book=self.book, chapter=self.chapter, verse=self.verse)

    @computed_field
    @property
    def verses(self) -> List[Verse]:
        return fetch_scripture(self.reference.book, self.reference.chapter, self.reference.verse)


# Create the agent
memory = MemorySaver()
tools = [fetch_scripture]
model = llm
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}



async def stream_agent_responses(user_input: str):
    loop = asyncio.get_event_loop()
    for chunk in await loop.run_in_executor(None, lambda: list(agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]}, config
    ))):
        if isinstance(chunk, dict):
            if 'agent' in chunk:
                for message in chunk['agent']['messages']:
                    if isinstance(message, AIMessage):
                        yield message.content
            elif 'tools' in chunk:
                for message in chunk['tools']['messages']:
                    if isinstance(message, ToolMessage):
                        yield f"Tool Response: {message.content}"
        elif isinstance(chunk, AIMessage):
            yield chunk.content
        elif isinstance(chunk, ToolMessage):
            yield f"Tool Response: {chunk.content}"
        else:
            yield str(chunk)