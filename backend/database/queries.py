from sqlalchemy.orm import Session
from sqlalchemy.sql import literal
from sqlalchemy import case, and_, or_
from typing import Optional, List, Tuple
from sqlmodel import Field, SQLModel, select
from fuzzywuzzy import fuzz

# SqlAlchemy models are used to interact with the database.
# They have defined relationships for joins with foreign keys.
# The include fields like embeddings for cosine similarity.
from schemas.sqlalchemy_schema import (
    Translation as Sa_Translation,
    Book as Sa_Book,
    TranslationBook as Sa_TranslationBook,
    Chapter as Sa_Chapter,
    Verse as Sa_Verse,
    Section as Sa_Section,
    t_reference as Sa_Reference,
    t_chapter_verses as Sa_ChapterVerses,
)

# SqlModel models are used to define the structure of the response.
# They are used to define the structure of the response.
# They are flexible pydantic models that LLMs to keep track of metadata.
from schemas.response_models import (
    Translation,
    Book,
    BookWithMetadata,
    ReferenceType,
    Reference,
    ReferenceWithMetadata,
    Chapter,
    ChapterWithMetadata,
    Verse,
    VerseWithMetadata,
    VerseWithReferences,
    Section,
    SectionWithMetadata,
    SectionWithReferences,
)
# ==================
# GET TRANSLATIONS
# ==================
def get_all_translations(session: Session) -> List[Translation]:
    """Retrieve all translations from the database."""
    translations = session.query(Translation).all()
    return translations
    
def get_translation_by_id(session: Session, translation_id: int) -> Optional[Translation]:
    """Retrieve a specific translation by ID."""
    translation = session.query(Translation).filter_by(id=translation_id).first()
    return translation

# ==================
# GET BOOKS
# ==================

def get_all_books(session: Session) -> List[BookWithMetadata]:
    """Retrieve all books from the database with their translations."""
    # Execute the query
    results = session.query(Book, Translation).join(Sa_TranslationBook, Book.id == Sa_TranslationBook.book_id).join(Translation, Translation.id == Sa_TranslationBook.translation_id).all()

    # Convert the results into instances of BookWithTranslation
    books_with_translations = [
        BookWithMetadata(book=book, translation=translation)
        for book, translation in results
    ]
    return books_with_translations

def get_books_by_translation(session: Session, translation_id: int) -> List[Book]:
    """Retrieve books by translation ID."""
    books = session.query(Book).join(Sa_TranslationBook, Book.id == Sa_TranslationBook.book_id).filter(Sa_TranslationBook.translation_id == translation_id).all()
    return books


def normalize_book_code(session: Session, book_code: str) -> str:
    """ Validate and normalize book code """
    # Get all books and extract their codes and names
    books = session.query(Sa_Book).all()
    valid_book_codes = [book.short_code for book in books]
    valid_book_names = [book.name for book in books]
    
    # Convert input to uppercase for better matching
    book_code_upper = book_code.upper()
    
    # Direct match with valid codes
    if book_code_upper in valid_book_codes:
        return book_code_upper
        
    # Create a dictionary to map names to codes for faster lookup
    name_to_code = {book.name: book.short_code for book in books}
    
    # Fuzzy match book codes
    best_code_match = max(valid_book_codes, key=lambda code: fuzz.ratio(code, book_code))
    code_score = fuzz.ratio(best_code_match, book_code)
    
    # Fuzzy match book names
    best_name_match = max(valid_book_names, key=lambda name: fuzz.ratio(name, book_code))
    name_score = fuzz.ratio(best_name_match, book_code)
    
    # Return the book code for the better match
    if code_score > name_score:
        return best_code_match
    else:
        return name_to_code[best_name_match]


# ==================
# GET CHAPTERS
# ==================

def get_chapters_by_book(session: Session, book_code: str) -> List[Chapter]:
    """Retrieve all chapters for a specific book by book code."""
    normalized_code = normalize_book_code(session, book_code)
    chapters = session.query(Chapter).join(Book, Chapter.book_id == Book.id).filter(Book.short_code == normalized_code).order_by(Chapter.chapter_number).all()
    return chapters

def get_chapter_by_book_and_number(session: Session, book_id: int, chapter_number: int) -> Optional[Chapter]:
    """Retrieve a specific chapter by book ID and chapter number."""
    chapter = session.query(Chapter).filter(
        Chapter.book_id == book_id, 
        Chapter.chapter_number == chapter_number
    ).first()
    return chapter

# ==================
# GET VERSES
# ==================

def get_verses_by_book_and_chapter(session: Session, book_code: str, chapter_number: int) -> List[Verse]:
    """Retrieve verses by book code and chapter number using the chapter table."""
    normalized_code = normalize_book_code(session, book_code)
    verses = (
        session.query(Verse)
        .join(Book, Verse.book_id == Book.id)
        .join(Chapter, Verse.chapter_id == Chapter.id)
        .filter(Book.short_code == normalized_code, Chapter.chapter_number == chapter_number)
        .all()
    )
    return verses

def get_verse_by_book_chapter_and_verse_number(session: Session, book_code: str, chapter_number: int, verse_number: int) -> VerseWithMetadata:
    """Retrieve a specific verse by book code, chapter number, and verse number."""
    normalized_code = normalize_book_code(session, book_code)
    result = session.query(
        Sa_Verse.id.label("verse_id"),
        Sa_Verse.text.label("verse_text"),
        Sa_Verse.verse.label("verse_number"),
        Sa_Translation.id.label("translation_id"),
        Sa_Translation.name.label("translation_name"),
        Sa_Translation.language.label("translation_language"),
        Sa_Book.id.label("book_id"),
        Sa_Book.name.label("book_name"),
        Sa_Book.short_code.label("book_code"),
        Sa_Book.name_in_original_language.label("book_original_name"),
        Sa_Book.has_inner_meaning.label("book_inner_meaning"),
        Sa_Book.tags.label("book_tags"),
        Sa_Chapter.id.label("chapter_id"),
        Sa_Chapter.chapter_number.label("chapter_number"),
        Sa_Chapter.title.label("chapter_title"),
        Sa_Chapter.tokens.label("tokens"),
    ).join(
        Sa_Book, Sa_Verse.book_id == Sa_Book.id
    ).join(
        Sa_Chapter, Sa_Verse.chapter_id == Sa_Chapter.id
    ).join(
        Sa_TranslationBook, Sa_Book.id == Sa_TranslationBook.book_id
    ).join(
        Sa_Translation, Sa_TranslationBook.translation_id == Sa_Translation.id
    ).filter(
        Sa_Book.short_code == normalized_code,
        Sa_Chapter.chapter_number == chapter_number,
        Sa_Verse.verse == verse_number
    ).first()

    # Create the nested objects
    translation = Translation(
        id=result.translation_id,
        name=result.translation_name,
        language=result.translation_language
    )

    book = Book(
        id=result.book_id,
        name=result.book_name,
        short_code=result.book_code,
        name_in_original_language=result.book_original_name,
        has_inner_meaning=result.book_inner_meaning,
        tags=result.book_tags
    )

    chapter = Chapter(
        id=result.chapter_id,
        book_id=result.book_id,
        chapter_number=result.chapter_number,
        title=result.chapter_title,
        book=book
    )

    verse = Verse(
        id=result.verse_id,
        book_id=result.book_id,
        chapter_id=result.chapter_id,
        verse=result.verse_number,
        text=result.verse_text,
        book=book,
        chapter=chapter,
        tokens=result.tokens
    )

    # Create the final VerseWithMetadata object with nested objects
    verse_with_metadata = VerseWithMetadata(
        translation=translation,
        book=book,
        chapter=chapter,
        verse=verse
    )
    
    return verse_with_metadata

def get_verse_with_references(session: Session, book_code: str, chapter: int, verse: int ) -> VerseWithReferences:
    """ Retrieve a verse with its metadata and references """
    normalized_code = normalize_book_code(session, book_code)
    verse_with_metadata = get_verse_by_book_chapter_and_verse_number(session, normalized_code, chapter, verse)
    from_references, to_references = get_references_by_verse_id_or_section_id(session, ReferenceType.VERSE, verse_with_metadata.verse.id)

    translation = Translation(
        id=verse_with_metadata.translation.id,
        name=verse_with_metadata.translation.name,
        language=verse_with_metadata.translation.language
    )

    book = Book(
        id=verse_with_metadata.book.id,
        name=verse_with_metadata.book.name,
        short_code=verse_with_metadata.book.short_code,
        name_in_original_language=verse_with_metadata.book.name_in_original_language,
        has_inner_meaning=verse_with_metadata.book.has_inner_meaning,
        tags=verse_with_metadata.book.tags
    )

    chapter = Chapter(
        id=verse_with_metadata.chapter.id,
        book_id=verse_with_metadata.chapter.book_id,
        chapter_number=verse_with_metadata.chapter.chapter_number,
        title=verse_with_metadata.chapter.title,
        book=book
    )

    verse = Verse(
        id=verse_with_metadata.verse.id,
        book_id=verse_with_metadata.verse.book_id,
        chapter_id=verse_with_metadata.verse.chapter_id,
        verse=verse_with_metadata.verse.verse,
        text=verse_with_metadata.verse.text
    )

    verse_with_metadata_and_references = VerseWithReferences(
        translation=translation,
        book=book,
        chapter=chapter,
        verse=verse,
        from_references=from_references,
        to_references=to_references
    )
    return verse_with_metadata_and_references


# ==================
# GET SECTIONS
# ==================

def get_sections_by_book(session: Session, book_code: str) -> List[Section]:
    """Retrieve all sections for a specific book ID."""
    normalized_code = normalize_book_code(session, book_code)
    sections = session.query(Section).join(Sa_Book, Sa_Section.book_id == Sa_Book.id).filter(Sa_Book.short_code == normalized_code).order_by(Section.section).all()
    return sections

def get_section_by_book_and_section_number(session: Session, book_code: str, section_number: int) -> SectionWithMetadata:
    """Retrieve a specific section by book code and section number."""
    normalized_code = normalize_book_code(session, book_code)
    result = session.query(
        Sa_Section.id.label("section_id"),
        Sa_Section.text.label("section_text"),
        Sa_Section.section.label("section_number"),
        Sa_Section.tokens.label("tokens"),
        Sa_Translation.id.label("translation_id"),
        Sa_Translation.name.label("translation_name"),
        Sa_Translation.language.label("translation_language"),
        Sa_Book.id.label("book_id"),
        Sa_Book.name.label("book_name"),
        Sa_Book.short_code.label("book_code"),
        Sa_Book.name_in_original_language.label("book_original_name"),
        Sa_Book.has_inner_meaning.label("book_inner_meaning"),
        Sa_Book.tags.label("book_tags")
    ).join(
        Sa_Book, Sa_Section.book_id == Sa_Book.id
    ).join(
        Sa_TranslationBook, Sa_Book.id == Sa_TranslationBook.book_id
    ).join(
        Sa_Translation, Sa_TranslationBook.translation_id == Sa_Translation.id
    ).filter(
        Sa_Book.short_code == normalized_code,
        Sa_Section.section == section_number
    ).first()

    # Create the nested objects
    translation = Translation(
        id=result.translation_id,
        name=result.translation_name,
        language=result.translation_language
    )

    book = Book(
        id=result.book_id,
        name=result.book_name,
        short_code=result.book_code,
        name_in_original_language=result.book_original_name,
        has_inner_meaning=result.book_inner_meaning,
        tags=result.book_tags
    )

    section = Section(
        id=result.section_id,
        book_id=result.book_id,
        section=result.section_number,
        text=result.section_text,
        book=book,
        tokens=result.tokens
    )

    section_with_metadata = SectionWithMetadata(
        translation=translation,
        book=book,
        section=section
    )
    return section_with_metadata


def get_section_with_references(session: Session, book_code: str, section: int) -> SectionWithReferences:
    """ Retrieve a section with its metadata and references """
    normalized_code = normalize_book_code(session, book_code)
    section_with_metadata = get_section_by_book_and_section_number(session, normalized_code, section)
    from_references, to_references = get_references_by_verse_id_or_section_id(session, ReferenceType.SECTION, section_with_metadata.section.id)
    
    translation = Translation(
        id=section_with_metadata.translation.id,
        name=section_with_metadata.translation.name,
        language=section_with_metadata.translation.language
    )

    book = Book(
        id=section_with_metadata.book.id,
        name=section_with_metadata.book.name,
        short_code=section_with_metadata.book.short_code,
        name_in_original_language=section_with_metadata.book.name_in_original_language,
        has_inner_meaning=section_with_metadata.book.has_inner_meaning,
        tags=section_with_metadata.book.tags
    )

    section = Section(
        id=section_with_metadata.section.id,
        book_id=section_with_metadata.section.book_id,
        section=section_with_metadata.section.section,
        text=section_with_metadata.section.text
    )

    section_with_metadata_and_references = SectionWithReferences(
        translation=translation,
        book=book,
        section=section,
        from_references=from_references,
        to_references=to_references
    )
    return section_with_metadata_and_references
    
# ==================
# GET IDS
# ==================

def get_id_by_translation_name(session: Session, translation_name: str) -> int:
    """ Retrieve the ID of a translation by its name """
    result = session.query(Sa_Translation.id).filter(Sa_Translation.name == translation_name).first()
    return result.id

def get_id_by_book_code(session: Session, book_code: str) -> int:
    """ Retrieve the ID of a book by its short code """
    normalized_code = normalize_book_code(session, book_code)
    result = session.query(Sa_Book.id).filter(Sa_Book.short_code == normalized_code).first()
    return result.id

def get_id_by_book_chapter(session: Session, book_code: str, chapter_number: int) -> int:
    """ Retrieve the ID of a chapter by book code and chapter number """
    normalized_code = normalize_book_code(session, book_code)
    result = session.query(Sa_Chapter.id).join(Sa_Book, Sa_Chapter.book_id == Sa_Book.id).filter(
        Sa_Book.short_code == normalized_code,
        Sa_Chapter.chapter_number == chapter_number
    ).first()
    return result.id

def get_id_by_book_chapter_verse(session: Session, book_code: str, chapter_number: int, verse_number: int) -> int:
    """ Retrieve the ID of a verse by book code, chapter number, and verse number """
    normalized_code = normalize_book_code(session, book_code)
    result = session.query(Sa_Verse.id).join(Sa_Book, Sa_Verse.book_id == Sa_Book.id).filter(
        Sa_Book.short_code == normalized_code,
        Sa_Verse.verse == verse_number
    ).first()
    return result.id

# ==================
# GET REFERENCES
# ==================

def get_references_by_verse_id_or_section_id(session: Session, reference_type: ReferenceType, id: int) -> Tuple[List[Reference], List[Reference]]:
    """ Retrieve references by verse ID or section ID """
    from_results = session.query(
        literal('from').label('direction'),
        Reference.to_type.label('related_type'),
        Reference.to_id.label('related_id'),
        Reference.notes
    ).filter(
        Reference.from_type == reference_type,
        Reference.from_id == id
    ).all()

    to_results = session.query(
        literal('to').label('direction'),
        Reference.from_type.label('related_type'),
        Reference.from_id.label('related_id'),
        Reference.notes
    ).filter(
        Reference.to_type == reference_type,
        Reference.to_id == id
    ).all()

    from_references = [Reference(from_type=reference_type, from_id=id, to_type=row.related_type, to_id=row.related_id, notes=row.notes) for row in from_results]
    to_references = [Reference(from_type=row.related_type, from_id=row.related_id, to_type=reference_type, to_id=id, notes=row.notes) for row in to_results]

    return from_references, to_references

def get_references_with_metadata(session: Session, reference_type: ReferenceType, id: int) -> Tuple[List[ReferenceWithMetadata], List[ReferenceWithMetadata]]:
    """ Retrieve a list of passages that reference a verse or section and a list of passages that are referenced by that verse or section """
    target_verse_or_section = get_verse_with_metadata(session, id) if reference_type == ReferenceType.VERSE else get_section_with_metadata(session, id)

    from_query = session.query(
        literal('from').label('direction'),
        Reference.to_type.label('related_type'),
        Reference.to_id.label('related_id'),
        Reference.notes,
        Translation.name.label('from_translation'),
        Book.name.label('from_book'),
        case(
            (Reference.to_type == ReferenceType.VERSE, Verse.chapter),
            else_=None
        ).label('from_chapter'),
        case(
            (Reference.to_type == ReferenceType.VERSE, Verse.verse),
            (Reference.to_type == ReferenceType.SECTION, Section.section),
            else_=None
        ).label('from_verse_or_section'),
        case(
            (Reference.to_type == ReferenceType.VERSE, Verse.text),
            (Reference.to_type == ReferenceType.SECTION, Section.text),
            else_=None
        ).label('from_text'),
        Translation.language.label('from_language')
    ).outerjoin(Verse, and_(Reference.to_type == ReferenceType.VERSE, Reference.to_id == Verse.id)
    ).outerjoin(Section, and_(Reference.to_type == ReferenceType.SECTION, Reference.to_id == Section.id)
    ).join(Book, or_(Verse.book_id == Book.id, Section.book_id == Book.id)
    ).join(Sa_TranslationBook, Book.id == Sa_TranslationBook.book_id
    ).join(Translation, Sa_TranslationBook.translation_id == Translation.id
    ).filter(
        Reference.from_type == reference_type,
        Reference.from_id == id
    )

    to_query = session.query(
        literal('to').label('direction'),
        Reference.from_type.label('related_type'),
        Reference.from_id.label('related_id'),
        Reference.notes,
        Translation.name.label('to_translation'),
        Book.name.label('to_book'),
        case(
            (Reference.from_type == ReferenceType.VERSE, Verse.chapter),
            else_=None
        ).label('to_chapter'),
        case(
            (Reference.from_type == ReferenceType.VERSE, Verse.verse),
            (Reference.from_type == ReferenceType.SECTION, Section.section),
            else_=None
        ).label('to_verse_or_section'),
        case(
            (Reference.from_type == ReferenceType.VERSE, Verse.text),
            (Reference.from_type == ReferenceType.SECTION, Section.text),
            else_=None
        ).label('to_text'),
        Translation.language.label('to_language')
    ).outerjoin(Verse, and_(Reference.from_type == ReferenceType.VERSE, Reference.from_id == Verse.id)
    ).outerjoin(Section, and_(Reference.from_type == ReferenceType.SECTION, Reference.from_id == Section.id)
    ).join(Book, or_(Verse.book_id == Book.id, Section.book_id == Book.id)
    ).join(Sa_TranslationBook, Book.id == Sa_TranslationBook.book_id
    ).join(Translation, Sa_TranslationBook.translation_id == Translation.id
    ).filter(
        Reference.to_type == reference_type,
        Reference.to_id == id
    )

    from_results = from_query.all()
    to_results = to_query.all()

    from_references = [ReferenceWithMetadata(
        from_type=reference_type,
        to_type=row.related_type,
        from_id=id,
        to_id=row.related_id,
        notes=row.notes,
        from_translation=row.from_translation,
        from_book=row.from_book,
        from_chapter=row.from_chapter,
        from_verse_or_section=row.from_verse_or_section,
        from_text=row.from_text,
        from_language=row.from_language,
        to_translation=target_verse_or_section.translation,
        to_book=target_verse_or_section.book,
        to_chapter=target_verse_or_section.chapter,
        to_verse_or_section=target_verse_or_section.verse if reference_type == ReferenceType.VERSE else target_verse_or_section.section,
        to_text=target_verse_or_section.text,
        to_language=target_verse_or_section.language
    ) for row in from_results]

    to_references = [ReferenceWithMetadata(
        from_type=row.related_type,
        to_type=reference_type,
        from_id=row.related_id,
        to_id=id,
        notes=row.notes,
        from_translation=target_verse_or_section.translation,
        from_book=target_verse_or_section.book,
        from_chapter=target_verse_or_section.chapter,
        from_verse_or_section=target_verse_or_section.verse if reference_type == ReferenceType.VERSE else target_verse_or_section.section,
        from_text=target_verse_or_section.text,
        from_language=target_verse_or_section.language,
        to_translation=row.to_translation,
        to_book=row.to_book,
        to_chapter=row.to_chapter,
        to_verse_or_section=row.to_verse_or_section,
        to_text=row.to_text,
        to_language=row.to_language
    ) for row in to_results]

    return from_references, to_references
