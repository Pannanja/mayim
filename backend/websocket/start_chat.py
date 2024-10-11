from FastAPI import StreamingResponse
from langchain_ollama import ChatOllama
from langgraph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


agent = ChatOllama(model="llama3.1", temperature=0, stream=True)


class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
def chatbot(state: State):
    return {"messages": llm.invoke(state["messages"])}

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
