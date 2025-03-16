import logging
import json
from dotenv import load_dotenv
from typing import Tuple
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from websockets.exceptions import ConnectionClosedOK
from datetime import datetime
from typing import List, Optional
from strawberry.asgi import GraphQL
from database.dbconnection import get_session
from database import queries
from schemas.strawberry_schema import schema
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
    SectionWithReferences
)

print("Loading environment variables...")
load_dotenv()

print("Creating FastAPI app...")
app = FastAPI()

print("Setting up CORS middleware...")
# Allow all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Creating database session...")
# Database session
session = get_session()

# Set up GraphQL endpoint
graphql_app = GraphQL(schema)
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/translations", response_model=List[Translation])
async def get_translations(request: Request):
    translations = queries.get_all_translations(session)
    return translations

@app.get("/books", response_model=List[BookWithMetadata])
async def all_books(request: Request):
    books = queries.get_all_books(session)
    return books

@app.get("/books/{translation_id}", response_model=List[Book])
async def books(request: Request, translation_id: int):
    books = queries.get_books_by_translation(session, translation_id)
    return books

@app.get("/book/{book_code}", response_model=List[Chapter])
async def chapters(request: Request, book_code: str):
    chapters = queries.get_chapters_by_book(session, book_code)
    return chapters

@app.get("/book/{book_code}/chapter/{chapter}", response_model=List[Verse])
async def verses(request: Request, book_code: str, chapter: int):
    verses = queries.get_verses_by_book_and_chapter(session, book_code, chapter)
    return verses

@app.get("/book/{book_code}/chapter/{chapter}/{verse}", response_model=VerseWithMetadata)
async def verse(request: Request, book_code: str, chapter: int, verse: int):
    verse = queries.get_verse_by_book_chapter_and_verse_number(session, book_code, chapter, verse)
    return verse

@app.get("/book/{book_code}/chapter/{chapter}/{verse}/references", response_model=VerseWithReferences)
async def verse_references(request: Request, book_code: str, chapter: int, verse: int):
    return queries.get_verse_with_references(session, book_code, chapter, verse)

@app.get("/book/{book_code}/sections", response_model=List[Section])
async def sections(request: Request, book_code: str):
    sections = queries.get_sections_by_book(session, book_code)
    return sections

@app.get("/book/{book_code}/section/{section_number}", response_model=SectionWithMetadata)
async def section(request: Request, book_code: str, section_number: int):
    section = queries.get_section_by_book_and_section_number(session, book_code, section_number)
    return section

@app.get("/book/{book_code}/section/{section_number}/references", response_model=SectionWithReferences)
async def section_references(request: Request, book_code: str, section_number: int):
    return queries.get_section_with_references(session, book_code, section_number)
