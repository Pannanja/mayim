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

class Verse(SQLModel, table=True):
    """ A verse of scripture """
    id: Optional[int] = Field(primary_key=True, default=None)
    book_id: Optional[int] = Field(foreign_key="book.id", default=None)
    chapter: int
    verse: int
    _text: Optional[str] = None  # Private attribute for storing the text after retrieval

    @property
    def reference(self) -> BibleReference:
        """A property that returns the Bible reference of the verse."""
        # For this to work, self.book must be retrieved separately if necessary
        # This assumes 'book' is a related model fetched earlier or available
        return BibleReference(book=self.book_id, chapter=self.chapter, verse=self.verse)

    @property
    def text(self) -> str:
        """Retrieve or return the stored verse text."""
        if self._text is None:
            raise ValueError("Text has not been fetched from the database yet.")
        return self._text

    async def fetch_text(self, session: AsyncSession) -> None:
        """Fetches the text from the database based on the verse reference."""
        statement = select(Verse).where(
            Verse.book_id == self.book_id,
            Verse.chapter == self.chapter,
            Verse.verse == self.verse
        )
        result = await session.execute(statement)
        verse_record = result.scalar_one_or_none()

        if verse_record is None:
            raise ValueError("Verse not found in the database.")
        self._text = verse_record.text


class Chapter(BaseModel): 
    book: str
    chapter: int
    verses: List[Verse]
