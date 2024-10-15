from typing import Optional, List
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, computed_field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, AliasPath
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class BibleReference(BaseModel):
    """ Basic structure for handling scripture references """
    book: str
    chapter: int
    verse: int

class Translation(SQLModel, table=True):
    """ A translation of the Bible """
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    language: Optional[str] = None

class Book(SQLModel, table=True):
    """ A book of the Bible. Note that the name field is never in English. Use name_in_english instead. """
    id: Optional[int] = Field(primary_key=True, default=None)
    name: Optional[str] = Field(default=None, alias="original_name")
    name_in_english: str = Field(alias="english_name")


engine = create_engine("postgresql://anthropos:humanity@localhost:5432/logosdb")
session = Session(engine)


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

    # This is a computed field that turns a book, chapter, and verse into a structured bible reference
    @computed_field
    @property
    def reference(self) -> BibleReference:
        return BibleReference(book=self.book, chapter=self.chapter, verse=self.verse)

    # This is a computed field that performs a database query to retrieve verses based on the reference
    @computed_field
    @property
    def verses(self) -> List[Verse]:
        return fetch_scripture(self.reference.book, self.reference.chapter, self.reference.verse)


returned_scripture = RetrievedScripture(book="Genesis", chapter=1, verse=1)