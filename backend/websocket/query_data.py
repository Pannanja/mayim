"""Create a ChatVectorDBChain for question/answering."""
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationChain, ConversationalRetrievalChain
from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)



def get_chain(stream_handler, tracing: bool = False) -> ConversationChain:
    """Create a ConversationChain for question/answering."""

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."
            ),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}"),
        ]
    )
    manager = AsyncCallbackManager([])
    stream_manager = AsyncCallbackManager([stream_handler])
    streaming_llm = ChatOllama(
        model="llama3.2",
        stream=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0,
        api_key="",
    )

    memory = ConversationBufferMemory(return_messages=True)

    qa = ConversationChain(
        callback_manager=manager, memory=memory, llm=streaming_llm, verbose=True, prompt=prompt
    )

    return qa

