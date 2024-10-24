from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Commentary(SQLModel, table=False):
    """ A commentary on scripture """
    id: Optional[int] = Field(primary_key=True, default=None)
    title: str

class CommentaryChapter(SQLModel, table=True):
    """ A chapter of a commentary """
    id: Optional[int] = Field(primary_key=True, default=None)
    commentary_id: int = Field(foreign_key="commentary.id")
    chapter: int

class CommentarySection(SQLModel, table=True):
    """ A section of a commentary """
    id: Optional[int] = Field(primary_key=True, default=None)
    commentary_id: int = Field(foreign_key="commentary.id")
    chapter_id: int = Field(foreign_key="commentary_chapter.id")
    section: int
