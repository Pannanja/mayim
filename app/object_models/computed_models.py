# These models are designed to eliminate hallucinations by retrieving exact text from the database. They are used in the Bible package to interact with the database containing scripture. The text field is never inferred, only retrieved. These models provide reliable and accurate data and form the bedrock of the mayim application.

# SQLModels are BOTH pydantic models (for LLM structure) and SQLAlchemy models (for database interaction)
import os
from dotenv import load_dotenv
from typing import Optional, List
from langchain_ollama import ChatOllama
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, computed_field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

load_dotenv()
uri = os.getenv("LOGOSDB_CONNECTION_STRING")
engine = create_engine(uri)
session = Session(engine)

llama3 = ChatOllama(
    model="llama3.1",
    temperature=0,
    # other params...
)

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

def fetch_scripture(book: str, chapter: int, verse: int) -> List[RetrievedVerse]:
    """ Retrieve scriptural text from the database given a reference """
    
    # assemble the reference object
    reference = BibleReference(book=book, chapter=chapter, verse=verse)
    
    # initialize the list of verses
    pydantic_verses = []

    # query the database
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

retrieved_scripture = RetrievedScripture(book="Genesis", chapter=1, verse=1)
print(retrieved_scripture.verses)