import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from backend.websocket.schemas import ChatResponse
from backend.websocket.callback import StreamingLLMCallbackHandler
from websockets.exceptions import ConnectionClosedOK
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from backend.database.dbconnection import get_session
from backend.websocket.schemas import ChatResponse
from backend.websocket.callback import StreamingLLMCallbackHandler
from backend.websocket.query_data import get_chain
from backend.chains.base_chat import stream_agent_responses
from backend.database.sqlalchemy_models import Translation as TranslationData, Book as BookData, Verse as VerseData, TranslationBook

app = FastAPI()

# # Allow all origins (for development purposes)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database session
session = get_session()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


# Websocket connection manager
connection_manager = ConnectionManager()


@app.get("/transaltions")
async def index(request: Request):
    translations = session.query(TranslationData).all()
    return templates.TemplateResponse('translations.html', {"request": request, "translations": translations})

@app.get("/books/{translation_id}")
async def books(request: Request, translation_id: int):
    books = session.query(BookData).join(TranslationBook).filter(TranslationBook.translation_id == translation_id).all()
    return templates.TemplateResponse('books.html', {"request": request, "books": books, "translation_id": translation_id})

@app.get("/verses/{book_id}/{chapter}")
async def verses(request: Request, book_id: int, chapter: int):
    verses = session.query(VerseData).filter_by(book_id=book_id, chapter=chapter).all()
    return templates.TemplateResponse('verses.html', {"request": request, "verses": verses, "book_id": book_id, "chapter": chapter})

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream_handler = StreamingLLMCallbackHandler(websocket)
    qa_chain = get_chain(stream_handler)

    while True:
        try:
            # Receive and send back the client message
            user_msg = await websocket.receive_text()
            resp = ChatResponse(sender="human", message=user_msg, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            # Send the message to the chain and feed the response back to the client
            output = await qa_chain.acall(
                {
                    "input": user_msg,
                }
            )

            # Send the end-response back to the client
            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("WebSocketDisconnect")
            # TODO try to reconnect with back-off
            break
        except ConnectionClosedOK:
            logging.info("ConnectionClosedOK")
            # TODO handle this?
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)