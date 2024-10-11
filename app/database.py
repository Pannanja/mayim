import os
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, computed_field
from sqlalchemy import create_engine, select
import justpy as jp
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from object_models.models import Verse, Book, Translation

# Set up SQLAlchemy
Base = declarative_base()

load_dotenv()
uri = os.getenv("LOGOSDB_CONNECTION_STRING")
# engine with tables: book, chapter, verse, and translation
engine = create_engine(uri)

Session = sessionmaker(bind=engine)


# Models (as provided)
class Verse(Base):
    __tablename__ = 'verse'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    chapter = Column(Integer)
    verse = Column(Integer)
    text = Column(String)

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    name_in_english = Column(String)

class Translation(Base):
    __tablename__ = 'translation'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)

class BibleApp:
    def __init__(self):
        self.wp = jp.WebPage()
        self.session = Session()
        self.title_div = jp.Div(a=self.wp, classes="text-center my-8")
        self.instruction_div = jp.Div(a=self.wp, classes="text-center mt-4 mb-2")
        self.book_div = jp.Div(a=self.wp, classes="flex flex-wrap justify-center")
        self.chapter_div = jp.Div(a=self.wp, classes="mt-8 text-center")
        self.verse_div = jp.Div(a=self.wp, classes="mt-8 text-center max-w-4xl mx-auto")

    def books_list(self):
        self.book_div.delete_components()
        books = self.session.query(Book).all()
        for book in books:
            link = jp.A(
                text=book.name_in_english, 
                href='#', 
                a=self.book_div, 
                classes='m-2 p-2 bg-blue-500 text-white rounded hover:bg-blue-700 transition duration-300'
            )
            link.book_id = book.id
            link.on('click', self.show_chapters)


    def show_chapters(self, msg):
        self.chapter_div.delete_components()
        self.verse_div.delete_components()
        book_id = msg.target.book_id
        book_name = self.session.query(Book).filter_by(id=book_id).first().name_in_english
        jp.Div(text=f"Chapters in {book_name}", a=self.chapter_div, classes="text-2xl font-bold mb-4")
        chapter_container = jp.Div(a=self.chapter_div, classes="flex flex-wrap justify-center")
        max_chapter = self.session.query(Verse).filter_by(book_id=book_id).order_by(Verse.chapter.desc()).first().chapter
        for chapter in range(1, max_chapter + 1):
            link = jp.A(
                text=f"{chapter}", 
                href='#', 
                a=chapter_container, 
                classes='m-1 p-2 bg-green-500 text-white rounded hover:bg-green-700 transition duration-300'
            )
            link.book_id = book_id
            link.chapter = chapter
            link.on('click', self.show_verses)

    def show_verses(self, msg):
        self.verse_div.delete_components()
        book_id = msg.target.book_id
        chapter = msg.target.chapter
        book_name = self.session.query(Book).filter_by(id=book_id).first().name_in_english
        jp.Div(text=f"{book_name} Chapter {chapter}", a=self.verse_div, classes="text-2xl font-bold mb-4")
        verses = self.session.query(Verse).filter_by(book_id=book_id, chapter=chapter).order_by(Verse.verse).all()
        for verse in verses:
            jp.P(text=f"{verse.verse}. {verse.text}", a=self.verse_div, classes="mb-2")

    def bible_interface(self):
        # Create title
        jp.Div(text="Bible Explorer", a=self.title_div, classes="text-4xl font-bold")
        
        # Create instruction
        jp.Div(text="Select a Book:", a=self.instruction_div, classes="text-2xl font-semibold")
        
        # Generate book list
        self.books_list()
        
        return self.wp


def bible_app():
    app = BibleApp()
    return app.bible_interface()

jp.justpy(bible_app)