import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from websockets.exceptions import ConnectionClosedOK
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from utilities.dbconnection import get_session
from websocket import StreamingLLMCallbackHandler
from websocket import get_chain
from websocket import ChatResponse
from websocket import ConnectionManager
from schemas.bible import Translation, Book, Verse, BibleReference, Chapter, TranslationBook


from api.chat import router as chat_router

app = FastAPI()

# Allow all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Database session
session = get_session()

# Websocket connection manager
connection_manager = ConnectionManager()


def get_all_translations(session: Session) -> List[Translation]:
    """Retrieve all translations from the database."""
    translations = session.query(Translation).all()
    return translations

def get_books_by_translation(session: Session, translation_id: int) -> List[Book]:
    """Retrieve books by translation ID."""
    books = session.query(Book).join(Translation, Book.id == Translation.id).filter(Translation.id == translation_id).all()
    return books
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

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# app.include_router(chat_router)
@app.get("/translations")
async def get_translations(request: Request):
    translations = get_all_translations(session)
    return translations

@app.get("/books/{translation_id}", response_model=List[Book])
async def books(request: Request, translation_id: int):
    books = get_books_by_translation(session, translation_id)
    return books

@app.get("/books/{book_id}/{chapter}", response_model=List[Verse])
async def verses(request: Request, book_id: int, chapter: int):
    verses = get_verses_by_book_and_chapter(session, book_id, chapter)
    return verses

@app.get("/verses/{book_id}/{chapter}")
async def verses(request: Request, book_id: int, chapter: int):
    verses = get_verses_by_book_and_chapter(session, book_id, chapter)
    return verses


@app.websocket("/ws")
async def open_websocket(websocket: WebSocket):
    await connection_manager.connect(websocket)
    stream_handler = StreamingLLMCallbackHandler(websocket)
    qa_chain = get_chain(stream_handler)
    try:
        while True:
            user_msg = await websocket.receive_text()
            resp = ChatResponse(sender="human", message=user_msg, type="stream")
            await websocket.send_json(resp.dict())

            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            # Await the coroutine to get the response
            response = await qa_chain.acall({"input": user_msg})
            for token in response.get("tokens", []):
                stream_resp = ChatResponse(sender="bot", message=token, type="stream")
                await websocket.send_json(stream_resp.dict())

            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await websocket.close()
    except ConnectionClosedOK:
        logging.info("ConnectionClosedOK")
        await websocket.close()

