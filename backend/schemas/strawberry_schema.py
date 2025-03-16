import strawberry
from typing import List, Optional
from enum import Enum
from database.dbconnection import get_session
from database import queries

# Define Strawberry types that correspond to your existing models

@strawberry.type
class Translation:
    id: int
    name: Optional[str] = None
    language: Optional[str] = None

@strawberry.type
class Book:
    id: int
    name: Optional[str] = None
    name_in_original_language: Optional[str] = None
    short_code: Optional[str] = None
    has_inner_meaning: Optional[bool] = None
    tags: Optional[List[str]] = None

@strawberry.type
class BookWithMetadata:
    book: Book
    translation: Translation

@strawberry.enum
class ReferenceTypeEnum(str, Enum):
    VERSE = "verse"
    SECTION = "section"

@strawberry.type
class Reference:
    id: Optional[int] = None
    from_type: str
    to_type: str
    from_id: int
    to_id: int
    notes: Optional[str] = None

@strawberry.type
class Chapter:
    id: int
    book_id: Optional[int] = None
    chapter_number: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    tokens: Optional[int] = None
    book: Optional[Book] = None

@strawberry.type
class Verse:
    id: int
    book_id: Optional[int] = None
    verse: Optional[int] = None
    text: Optional[str] = None
    chapter_id: Optional[int] = None
    book: Optional[Book] = None

@strawberry.type
class VerseWithMetadata:
    translation: Translation
    book: Book
    chapter: Chapter
    verse: Verse

@strawberry.type
class VerseWithReferences:
    translation: Translation
    book: Book
    chapter: Chapter
    verse: Verse
    from_references: Optional[List[Reference]] = None
    to_references: Optional[List[Reference]] = None

@strawberry.type
class Section:
    id: int
    book_id: Optional[int] = None
    section: Optional[int] = None
    text: Optional[str] = None
    tokens: Optional[int] = None
    book: Optional[Book] = None

@strawberry.type
class SectionWithMetadata:
    translation: Translation
    book: Book
    section: Section

@strawberry.type
class SectionWithReferences:
    translation: Translation
    book: Book
    section: Section
    from_references: Optional[List[Reference]] = None
    to_references: Optional[List[Reference]] = None

# Define the GraphQL Query type
@strawberry.type
class Query:
    @strawberry.field
    def translations(self) -> List[Translation]:
        session = get_session()
        return queries.get_all_translations(session)

    @strawberry.field
    def books(self) -> List[BookWithMetadata]:
        session = get_session()
        return queries.get_all_books(session)

    @strawberry.field
    def books_by_translation(self, translation_id: int) -> List[Book]:
        session = get_session()
        return queries.get_books_by_translation(session, translation_id)

    @strawberry.field
    def chapters_by_book(self, book_code: str) -> List[Chapter]:
        session = get_session()
        return queries.get_chapters_by_book(session, book_code)

    @strawberry.field
    def verses_by_chapter(self, book_code: str, chapter: int) -> List[Verse]:
        session = get_session()
        return queries.get_verses_by_book_and_chapter(session, book_code, chapter)

    @strawberry.field
    def verse(self, book_code: str, chapter: int, verse: int) -> VerseWithMetadata:
        session = get_session()
        return queries.get_verse_by_book_chapter_and_verse_number(session, book_code, chapter, verse)

    @strawberry.field
    def verse_with_references(self, book_code: str, chapter: int, verse: int) -> VerseWithReferences:
        session = get_session()
        return queries.get_verse_with_references(session, book_code, chapter, verse)

    @strawberry.field
    def sections_by_book(self, book_code: str) -> List[Section]:
        session = get_session()
        return queries.get_sections_by_book(session, book_code)

    @strawberry.field
    def section(self, book_code: str, section_number: int) -> SectionWithMetadata:
        session = get_session()
        return queries.get_section_by_book_and_section_number(session, book_code, section_number)

    @strawberry.field
    def section_with_references(self, book_code: str, section_number: int) -> SectionWithReferences:
        session = get_session()
        return queries.get_section_with_references(session, book_code, section_number)

# Create the schema
schema = strawberry.Schema(query=Query)
