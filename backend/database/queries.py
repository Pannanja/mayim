from sqlalchemy.orm import Session
from typing import Optional, List
from sqlmodel import Field, SQLModel, select
from pydantic import AliasPath

def get_all_translations(session: Session) -> List[TranslationModel]:
    """Retrieve all translations from the database."""
    translations = session.query(Translation).all()
    return [TranslationModel.from_orm(translation) for translation in translations]

def get_books_by_translation(session: Session, translation_id: int) -> List[BookModel]:
    """Retrieve books by translation ID."""
    results = session.query(Book).join(TranslationBook).filter(TranslationBook.translation_id == translation_id).all()
    return [BookModel.from_orm(book) for book in results]

def get_verses_by_book_and_chapter(session: Session, book_id: int, chapter: int) -> List[VerseModel]:
    """Retrieve verses by book ID and chapter."""
    verses = session.query(Verse).filter_by(book_id=book_id, chapter=chapter).all()
    return [VerseModel.from_orm(verse) for verse in verses]

def get_translation_by_id(session: Session, translation_id: int) -> Optional[TranslationModel]:
    """Retrieve a specific translation by ID."""
    translation = session.query(Translation).filter_by(id=translation_id).first()
    return TranslationModel.from_orm(translation) if translation else None

def get_book_by_id(session: Session, book_id: int) -> Optional[BookModel]:
    """Retrieve a specific book by ID."""
    book = session.query(Book).filter_by(id=book_id).first()
    return BookModel.from_orm(book) if book else None

def get_verse_by_id(session: Session, verse_id: int) -> Optional[VerseModel]:
    """Retrieve a specific verse by ID."""
    verse = session.query(Verse).filter_by(id=verse_id).first()
    return VerseModel.from_orm(verse) if verse else None