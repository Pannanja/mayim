from fastapi.responses import StreamingResponse
from langchain_ollama import ChatOllama
import asyncio
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

async def respond(input: str):
    agent = ChatOllama(model="llama3.1", temperature=0, stream=True, api_key="")
    response_message = await agent.ainvoke(input)  # Await the coroutine
    
    async def response_generator():
        # Assuming response_message is an AIMessage object
        print(response_message.content)
        yield response_message.content
    
    return StreamingResponse(response_generator(), media_type="text/plain")

# Example usage to test the streaming functionality
async def main():
    input = "hello, how are you?"
    response = await respond(input)
    async for chunk in response.body_iterator:
        print(chunk)  # Directly print the chunk since it's already a string

if __name__ == "__main__":
    asyncio.run(main())