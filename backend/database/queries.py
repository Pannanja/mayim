from sqlalchemy.orm import Session
from typing import Optional, List
from sqlmodel import Field, SQLModel, select
from schemas.bible import Translation, Book, Verse, TranslationBook


def get_all_translations(session: Session) -> List[Translation]:
    """Retrieve all translations from the database."""
    translations = session.query(Translation).all()
    return translations

def get_books_by_translation(session: Session, translation_id: int) -> List[Book]:
    """Retrieve books by translation ID."""
    books = session.query(Book).join(TranslationBook, Book.id == TranslationBook.book_id).filter(TranslationBook.translation_id == translation_id).all()
    return books

def get_verses_by_book_and_chapter(session: Session, book_id: int, chapter: int) -> List[Verse]:
    """Retrieve verses by book ID and chapter."""
    verses = session.query(Verse).filter_by(book_id=book_id, chapter=chapter).all()
    return verses

def get_translation_by_id(session: Session, translation_id: int) -> Optional[Translation]:
    """Retrieve a specific translation by ID."""
    translation = session.query(Translation).filter_by(id=translation_id).first()
    return translation

def get_book_by_id(session: Session, book_id: int) -> Optional[Book]:
    """Retrieve a specific book by ID."""
    book = session.query(Book).filter_by(id=book_id).first()
    return book

def get_verse_by_id(session: Session, verse_id: int) -> Optional[Verse]:
    """Retrieve a specific verse by ID."""
    verse = session.query(Verse).filter_by(id=verse_id).first()
    return verse