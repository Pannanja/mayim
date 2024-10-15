# This file contains logical models for handling structured objects like Bible books, verses, and relationships
# SQLModels are BOTH pydantic models (for LLM structure) and SQLAlchemy models (for database interaction)

from typing import Optional, List
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, computed_field


# SQLModels which are reflected as tables in the database

# Verses are the basic unit of scripture and form the backbone of the database
class Verse(SQLModel, table=True):
    """ A verse of scripture. This provides a basic structure for interacting with the database containing scripture. The text field should never be inferred."""
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int
    chapter: int
    verse: int
    text: str


# Books refer specifically to books of the Bible and used for organizing verses
class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    english_name: str

# Translations are used to store different versions of the Bible
# The translations table may include loose translations or commentaries which closely follow the text structure
class Translation:
    id: Optional[int] = Field(default=None)
    name: str
    language: str


# -------------------------------------------------------
# Pydantic models which are not reflected as tables in the database but are used for logical structure

# Chapters are lists of verses, useful for organizing verses into coherent sections
class Chapter(BaseModel):
    id: Optional[int] = None
    book: str
    chapter: int
    verses: list[Verse]


# BibleReference is a simple structure for extracting, retrieving, and keeping track of textual references
class BibleReference(BaseModel):
    book: str
    chapter: int
    verse: int
