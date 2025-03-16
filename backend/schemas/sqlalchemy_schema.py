from typing import Any, List, Optional

from pgvector.sqlalchemy.halfvec import HALFVEC
from pgvector.sqlalchemy.vector import VECTOR
from sqlalchemy import ARRAY, Boolean, Column, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Translation(Base):
    __tablename__ = 'translation'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='translation_pkey'),
        {'comment': 'Collections of books by translation. Also contains texts in original languages.'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for translations, auto-incremented via sequence')
    name: Mapped[Optional[str]] = mapped_column(String(50))
    language: Mapped[Optional[str]] = mapped_column(String(50))

    translation_book: Mapped[List['TranslationBook']] = relationship('TranslationBook', back_populates='translation')


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='book_pkey'),
        {'comment': "Books of the Old Testament, New Testament, and Swedenborg's writings."}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for books, auto-incremented via sequence')
    name_in_original_language: Mapped[Optional[str]] = mapped_column(String(50))
    name: Mapped[Optional[str]] = mapped_column(String(50))
    short_code: Mapped[Optional[str]] = mapped_column(String(8))
    has_inner_meaning: Mapped[Optional[bool]] = mapped_column(Boolean)
    tags: Mapped[Optional[list]] = mapped_column(ARRAY(String()))

    translation_book: Mapped[List['TranslationBook']] = relationship('TranslationBook', back_populates='book')
    chapter: Mapped[List['Chapter']] = relationship('Chapter', back_populates='book')
    verse: Mapped[List['Verse']] = relationship('Verse', back_populates='book')
    section: Mapped[List['Section']] = relationship('Section', back_populates='book')


t_chapter_verses = Table(
    'chapter_verses', Base.metadata,
    Column('book_id', Integer),
    Column('chapter_number', Integer),
    Column('verse_number', Integer),
    Column('verse_text', Text)
)


t_reference = Table(
    'reference', Base.metadata,
    Column('from_type', Text, nullable=False),
    Column('to_type', Text, nullable=False),
    Column('from_id', Integer, nullable=False),
    Column('to_id', Integer, nullable=False),
    Column('notes', Text),
    comment="intertextual references to verses and/or sections. from_type and to_type should ALWAYS list either 'verse' or 'section'"
)



class Chapter(Base):
    __tablename__ = 'chapter'
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ['book.id'], ondelete='CASCADE', name='fk_chapter_book'),
        PrimaryKeyConstraint('id', name='chapter_pkey'),
        UniqueConstraint('book_id', 'chapter_number', name='unique_book_chapter'),
        {'comment': 'Chapters of Bible books.'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for chapters, auto-incremented via sequence')
    book_id: Mapped[int] = mapped_column(Integer)
    chapter_number: Mapped[int] = mapped_column(Integer)
    title: Mapped[Optional[str]] = mapped_column(Text)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    tokens: Mapped[Optional[int]] = mapped_column(Integer)
    embedding_large: Mapped[Optional[Any]] = mapped_column(HALFVEC(3072), comment='embedding created using OpenAI text-embedding-3-large, halfvec(3072), from original language')
    embedding_bge_m3: Mapped[Optional[Any]] = mapped_column(VECTOR(1024), comment='embedding created using bge-m3, vector(1024), from original language')

    book: Mapped['Book'] = relationship('Book', back_populates='chapter')


class Section(Base):
    __tablename__ = 'section'
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ['book.id'], name='book_id'),
        PrimaryKeyConstraint('id', name='section_pkey'),
        {'comment': "Sections of Swedenborg's writings."}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for sections, auto-incremented via sequence')
    book_id: Mapped[int] = mapped_column(Integer)
    section: Mapped[int] = mapped_column(Integer)
    text: Mapped[Optional[str]] = mapped_column(Text)
    tokens: Mapped[Optional[int]] = mapped_column(Integer)
    embedding_large: Mapped[Optional[Any]] = mapped_column(HALFVEC(3072), comment='embedding created using OpenAI text-embedding-3-large, halfvec(3072), from original language')
    embedding_bge_m3: Mapped[Optional[Any]] = mapped_column(VECTOR(1024), comment='embedding created using bge-m3, vector(1024), from original language')

    book: Mapped['Book'] = relationship('Book', back_populates='section')


class TranslationBook(Base):
    __tablename__ = 'translation_book'
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ['book.id'], name='translation_book_book_id_fkey'),
        ForeignKeyConstraint(['translation_id'], ['translation.id'], name='translation_book_translation_id_fkey'),
        PrimaryKeyConstraint('id', name='translation_book_pkey'),
        {'comment': 'Join table for translation and book tables.'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for translation_books, auto-incremented via sequence')
    translation_id: Mapped[Optional[int]] = mapped_column(Integer)
    book_id: Mapped[Optional[int]] = mapped_column(Integer)

    book: Mapped[Optional['Book']] = relationship('Book', back_populates='translation_book')
    translation: Mapped[Optional['Translation']] = relationship('Translation', back_populates='translation_book')


class Verse(Base):
    __tablename__ = 'verse'
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ['book.id'], name='verse_book_fkey'),
        PrimaryKeyConstraint('id', name='verse_pkey'),
        {'comment': 'Individual verses of Bible text.'}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='Unique identifier for verses, auto-incremented via sequence')
    book_id: Mapped[Optional[int]] = mapped_column(Integer)
    verse: Mapped[Optional[int]] = mapped_column(Integer)
    text: Mapped[Optional[str]] = mapped_column(Text)
    chapter_id: Mapped[Optional[int]] = mapped_column(Integer)

    book: Mapped[Optional['Book']] = relationship('Book', back_populates='verse')