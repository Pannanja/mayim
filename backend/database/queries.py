from sqlalchemy.orm import Session
from sqlalchemy_models import Translation as TranslationData, Book as BookData, Verse as VerseData, TranslationBook

def get_all_translations(session: Session):
    """Retrieve all translations from the database."""
    return session.query(TranslationData).all()

def get_books_by_translation(session: Session, translation_id: int):
    """Retrieve books by translation ID."""
    return session.query(BookData).join(TranslationBook).filter(TranslationBook.translation_id == translation_id).all()

def get_verses_by_book_and_chapter(session: Session, book_id: int, chapter: int):
    """Retrieve verses by book ID and chapter."""
    return session.query(VerseData).filter_by(book_id=book_id, chapter=chapter).all()

def get_translation_by_id(session: Session, translation_id: int):
    """Retrieve a specific translation by ID."""
    return session.query(TranslationData).filter_by(id=translation_id).first()

def get_book_by_id(session: Session, book_id: int):
    """Retrieve a specific book by ID."""
    return session.query(BookData).filter_by(id=book_id).first()

def get_verse_by_id(session: Session, verse_id: int):
    """Retrieve a specific verse by ID."""
    return session.query(VerseData).filter_by(id=verse_id).first()