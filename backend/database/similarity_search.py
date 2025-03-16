from ollama import embed
from typing import List, Tuple
from schemas.sqlalchemy_schema import (
    Chapter,
    Section
)
from pgvector.sqlalchemy.vector import VECTOR

EMBEDDING_MODEL = "bge-m3"

def similarity_search(session: session, query: str, find_chapters: bool=True, find_sections: bool=True) -> Tuple[List[Chapter], List[Section]]:
    """ Search for similar chapters and sections based on the query """
    # Generate embedding of the query
    # Ollama.embed accepts an "input" parameter, not "prompt", and we must select the first element of the "embeddings" list in the response
    query_embedding = embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    
    similar_chapters = []
    similar_sections = []
    if (find_chapters):
        similar_chapters = session.scalars(select(Chapter).filter(Item.embedding.vector_cosine_ops(query_embedding)))

    if (find_sections):
        similar_sections = session.scalars(select(Section).filter(Item.embedding.vector_cosine_ops(query_embedding)))
        