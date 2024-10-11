# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)    
    name = Column(String(50))
    name_in_english = Column(String(50))


class Translation(Base):
    __tablename__ = 'translation'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    language = Column(String(50))


class TranslationBook(Base):
    __tablename__ = 'translation_book'

    id = Column(Integer, primary_key=True)
    translation_id = Column(ForeignKey('translation.id'))
    book_id = Column(ForeignKey('book.id'))

    book = relationship('Book')
    translation = relationship('Translation')


class Verse(Base):
    __tablename__ = 'verse'

    id = Column(Integer, primary_key=True)   
    book_id = Column(ForeignKey('book.id'))
    chapter = Column(Integer)
    verse = Column(Integer)
    text = Column(Text)

    book = relationship('Book')