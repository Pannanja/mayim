from database.queries import get_all_translations, get_books_by_translation, get_verses_by_book_and_chapter, get_translation_by_id, get_book_by_id, get_verse_by_id
from langchain_core.tools import tool

from schemas.bible import Translation, Book, Verse, BibleReference, Chapter

@tool
def get_chapter(translation_id: int, book_id: int, chapter: int) -> List[Verse]: 
    """Retrieve verses by translation ID, book ID, and chapter."""
    verses = get_verses_by_book_and_chapter(translation_id, book_id, chapter)
    return verses

