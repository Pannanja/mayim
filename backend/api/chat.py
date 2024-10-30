from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from tools.wondering import generate_wondering, Wondering
import json
from typing import AsyncGenerator

router = APIRouter()

async def generate_wondering_stream(topic: str) -> AsyncGenerator[str, None]:
    async for token in generate_wondering(topic):
        yield json.dumps({"topic": topic, "question": str(token) + " "}) + "\n"

@router.get("/wondering")
async def get_wondering(topic: str) -> StreamingResponse:
    return StreamingResponse(generate_wondering_stream(topic), media_type="application/json")