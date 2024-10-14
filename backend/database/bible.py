from typing import Optional, List
from sqlmodel import Field, SQLModel, select
from pydantic import BaseModel, AliasPath

class BibleReference(SQLModel, table=False):
    """ Basic structure for handling scripture references """
    book: str
    chapter: int
    verse: int

class Chapter(SQLModel, table=False):
    """ A chapter of the Bible """
    book: str
    chapter: int

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

class Verse(SQLModel, table=True):
    """ A verse of scripture """
    id: Optional[int] = Field(primary_key=True, default=None)
    book_id: Optional[int] = Field(foreign_key="book.id", default=None)
    chapter: int
    verse: int
    text: str