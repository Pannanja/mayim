from typing import Optional, List, Literal, Any
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, CheckConstraint, Text, Integer, Boolean, ARRAY
from pydantic import BaseModel, AliasPath

class Translation(SQLModel, table=True):
    __tablename__ = "translation"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)

class Book(SQLModel, table=True):
    """A book of the Bible."""
    __tablename__ = "book"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    name_in_original_language: Optional[str] = Field(default=None)
    short_code: Optional[str] = Field(default=None)
    has_inner_meaning: Optional[bool] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    chapters: Optional[List["Chapter"]] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete"})
    verses: Optional[List["Verse"]] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete"})
    sections: Optional[List["Section"]] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete"})


class BookWithMetadata(BaseModel):
    """ A book of the Bible with its translation """
    book: Book
    translation: Translation

class ReferenceType:
    VERSE = "verse"
    SECTION = "section"

class Reference(SQLModel, table=True):
    """ A reference between two verses and/or sections """
    __tablename__ = "reference"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    from_type: str = Field(sa_column=Column(String, CheckConstraint("name IN ('verse', 'section')")))
    to_type: str = Field(sa_column=Column(String, CheckConstraint("name IN ('verse', 'section')")))
    from_id: int = Field(default=None, foreign_key="verse.id")
    to_id: int = Field(default=None, foreign_key="verse.id")
    notes: Optional[str] = None

class ReferenceWithMetadata(BaseModel):
    """ A reference between two verses and/or sections """
    id: int
    from_type: str = Field(sa_column=Column(String, CheckConstraint("name IN ('verse', 'section')")))
    to_type: str = Field(sa_column=Column(String, CheckConstraint("name IN ('verse', 'section')")))
    from_id: int
    to_id: int
    notes: Optional[str]
    from_translation: str
    from_book: str
    from_chapter: Optional[int] = None
    from_verse_or_section: int
    from_text: str
    from_language: str
    to_translation: str
    to_book: str
    to_chapter: Optional[int] = None
    to_verse_or_section: int
    to_text: str
    to_language: str

class Chapter(SQLModel, table=True):
    __tablename__ = "chapter"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    chapter_number: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    tokens: Optional[int] = Field(default=None)
    # Embedding fields are only used to measure cosine similarity on the server and are not returned to the client
    # embedding_large: Optional[Any] = Field(default=None, sa_column=Column(HALFVEC(3072)))
    # embedding_bge_m3: Optional[Any] = Field(default=None, sa_column=Column(VECTOR(1024)))
    
    book: Optional["Book"] = Relationship(back_populates="chapters")



class ChapterWithMetadata(BaseModel):
    """ A chapter of the Bible with its translation """
    translation: Translation
    book: Book
    chapter: Chapter

class Verse(SQLModel, table=True):
    __tablename__ = "verse"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    verse: Optional[int] = Field(default=None)
    text: Optional[str] = Field(default=None)
    chapter_id: Optional[int] = Field(default=None)
    
    book: Optional["Book"] = Relationship(back_populates="verses")

class VerseWithMetadata(BaseModel):
    """ A verse of the Bible with its translation """
    translation: Translation
    book: Book
    chapter: Chapter
    verse: Verse

class VerseWithReferences(BaseModel):
    """ A section of commentary with its metadata and references """
    translation: Translation
    book: Book
    chapter: Chapter
    verse: Verse
    from_references: Optional[List[Reference]]
    to_references: Optional[List[Reference]]

class Section(SQLModel, table=True):
    __tablename__ = "section"
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key="book.id")
    section: Optional[int] = Field(default=None)
    text: Optional[str] = Field(default=None)
    tokens: Optional[int] = Field(default=None)
    # Embedding fields are only used to measure cosine similarity on the server and are not returned to the client
    # embedding_large: Optional[Any] = Field(default=None, sa_column=Column(HALFVEC(3072)))
    # embedding_bge_m3: Optional[Any] = Field(default=None, sa_column=Column(VECTOR(1024)))
    
    book: Optional["Book"] = Relationship(back_populates="sections")

class SectionWithMetadata(BaseModel):
    """ A section of commentary with its translation """
    translation: Translation
    book: Book
    section: Section

class SectionWithReferences(BaseModel):
    """ A section of commentary with its metadata and references. """
    translation: Translation
    book: Book
    section: Section
    from_references: Optional[List[Reference]]
    to_references: Optional[List[Reference]]