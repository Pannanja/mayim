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

# app.include_router(chat_router)

@app.get("/translations")
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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)