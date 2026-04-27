from typing import List
import numpy as np

from app.db.embeddings import get_embedding
from app.db.vector_store import VectorStore


def chunk_text(text: str, chunk_size: int = 300) -> List[str]:
    """
    Splits text into chunks for embedding
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def build_vector_index(text: str):
    """
    Creates vector store from text
    """
    chunks = chunk_text(text)

    embeddings = [get_embedding(chunk) for chunk in chunks]

    vector_store = VectorStore()
    vector_store.add(chunks, embeddings)

    return vector_store


def retrieve_relevant_context(query: str, vector_store, top_k: int = 3) -> List[str]:
    """
    Retrieves top-k relevant chunks
    """
    query_embedding = get_embedding(query)

    results = vector_store.search(query_embedding, top_k=top_k)

    return [r["text"] for r in results]


def build_context(query: str, text: str) -> str:
    """
    Full RAG pipeline:
    text → embeddings → retrieve → context
    """

    vector_store = build_vector_index(text)

    relevant_chunks = retrieve_relevant_context(query, vector_store)

    context = "\n\n".join(relevant_chunks)

    return context