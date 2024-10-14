import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from websockets.exceptions import ConnectionClosedOK
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Annotated
from utilities.dbconnection import get_session
from websocket import StreamingLLMCallbackHandler
from websocket import get_chain
from websocket import ChatResponse
from websocket import ConnectionManager
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy.ext.asyncio import AsyncSession

class BibleReference(SQLModel, table=False):
    """ Basic structure for handling scripture references """
    book: str
    chapter: int
    verse: int

class Chapter(SQLModel, table=False):
    """ A chapter of the Bible """
    book: str
    chapter: int

class Translation(SQLModel, table=True):
    """ A translation of the Bible """
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str
    language: Optional[str] = None

class Book(SQLModel, table=True):
    """ A book of the Bible. Note that the name field is never in English. Use name_in_english instead. """
    id: Optional[int] = Field(primary_key=True, default=None)
    name: Optional[str] = Field(default=None, alias="original_name")
    name_in_english: str = Field(alias="english_name")

class Verse(SQLModel, table=True):
    """ A verse of scripture """
    id: Optional[int] = Field(primary_key=True, default=None)
    book_id: Optional[int] = Field(foreign_key="book.id", default=None)
    chapter: int
    verse: int
    text: str

sqlite_file_name = "logosdb.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
connection_manager = ConnectionManager()


app = FastAPI()

# Allow all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/books/")
def read_books(
    session: SessionDep,
) -> list[Book]:
    books = session.exec(select(Book)).all()
    return books


@app.get("/books/{book_id}")
def read_books(book_id: int, session: SessionDep) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("books/{book_id}/chapters")


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