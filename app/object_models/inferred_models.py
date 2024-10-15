# This file contains intuitive, logical object models for handling scriptural references and exerpts

from typing import Optional, List
from pydantic import BaseModel, Field, AliasPath

# SQLModels which are reflected as tables in the database


# Verses are the basic unit of scripture and form the backbone of the database
class Verse(BaseModel):
    """ A verse of scripture. This provides a basic structure for interacting with the database containing scripture. The text field should never be inferred."""
    book: str 
    chapter: int
    verse: int
    text: Optional[str] = None
    language: Optional[str] = None

# Verses are the basic unit of scripture and form the backbone of the database
class InferredVerse(Verse):
    """ A verse of scripture. This provides a basic structure for interacting with the database containing scripture. The text field should never be inferred."""
    book: str 
    chapter: int
    verse: int
    text: Optional[str] = None
    language: Optional[str] = None

# Books refer specifically to books of the Bible and used for organizing verses
class Book(BaseModel):
    name: str = Field(validation_alias=AliasPath("original_name"))
    name_in_english: str = Field(validation_alias=AliasPath("english_name"))

# Translations are used to store different versions of the Bible
# The translations table may include loose translations or commentaries which closely follow the text structure
class Translation(BaseModel):
    name: str
    language: str

# -------------------------------------------------------
# SQLModels which are not reflected as tables in the database

# Chapters are lists of verses, useful for organizing verses into coherent sections
class Chapter(BaseModel):
    book: str = Field(alias="book_name")
    chapter: int = Field(alias="chapter_number")
    verses: List[Verse]


# BibleReference is a simple structure for extracting, retrieving, and keeping track of textual references
class BibleReference(BaseModel):
    book: str
    chapter: int
    verse: int
