# This file contains SQLModels for generating queries and interacting with the database
# SQLModels are BOTH pydantic models (for LLM structure) and SQLAlchemy models (for database interaction)

from typing import Optional, List
from sqlmodel import Field, SQLModel


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
    """ A book of the Bible. This provides a basic structure for interacting with the database containing scripture. """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    english_name: str

# Translations are used to store different versions of the Bible
# The translations table may include loose translations or commentaries which closely follow the text structure
class Translation(SQLModel, table=True):
    """ A translation of the Bible. Translations are used to store different versions of the Bible. The translations table may include loose translations or commentaries which closely follow the text structure. """
    id: Optional[int] = Field(default=None)
    name: str
    language: str


class TranslationBook(SQLModel, table=True):
    """ A table linking translations to books. This is used to store which books are available in which translations. """
    id: Optional[int] = Field(default=None, primary_key=True)
    translation_id: int
    book_id: int
