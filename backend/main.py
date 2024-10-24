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
from websocket.graph import invoke_our_graph
from utilities.cust_logger import logger, set_files_message_color
from websocket import ChatResponse
from websocket import ConnectionManager
from schemas.bible import Translation, Book, Verse, BibleReference, Chapter, TranslationBook
from database.queries import get_all_translations, get_books_by_translation, get_verses_by_book_and_chapter
import json
from datetime import datetime
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

@app.get("/verses/{book_id}/{chapter}", response_model=List[Verse])
async def verses(request: Request, book_id: int, chapter: int):
    verses = get_verses_by_book_and_chapter(session, book_id, chapter)
    return verses


# WebSocket endpoint for real-time communication with the frontend
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # unless described (error) logging is in {"timestamp": "YYYY-MM-DDTHH:MM:SS.MS", "uuid": "", "op": ""} format,
    # {timestamp, designated uuid, and what operation was done}

    await websocket.accept()  # Accept ANY WebSocket connection
    user_uuid = None  # Placeholder for the conversation UUID
    try:
        while True:
            data = await websocket.receive_text()  # Receive message from client
            # Log the received data in {"timestamp": "YYYY-MM-DDTHH:MM:SS.MS", "uuid": "", "received": {"uuid": "", "init": bool}} format
            logger.info(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "received": json.loads(data)}))

            try:
                # parse the data extracting the UUID and Message and if its the first message of the conversation
                payload = json.loads(data)
                user_uuid = payload.get("uuid")
                message = payload.get("message")
                init = payload.get("init", False)

                # If it's the first message, log the conversation initialization process
                if init:
                    logger.info(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "op": "Initializing ws with client."}))
                else:
                    if message:
                        # If a message is provided, invoke the LangGraph, websocket for send, user message, and passing conversation ID
                        await invoke_our_graph(websocket, message, user_uuid)
            except json.JSONDecodeError as e:
                logger.error(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "op": f"JSON encoding error - {e}"}))
    except Exception as e:
        # Catch all other unexpected exceptions and log the error
        logger.error(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "op": f"Error: {e}"}))
    finally:
        # before the connection is closed, check if its already closed from the client side before trying to close from our side
        if user_uuid:
            logger.info(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "op": "Closing connection."}))
        try:
            await websocket.close()
        except RuntimeError as e:
            # uncaught connection was already closed error
            logger.error(json.dumps({"timestamp": datetime.now().isoformat(), "uuid": user_uuid, "op": f"WebSocket close error: {e}"}))

