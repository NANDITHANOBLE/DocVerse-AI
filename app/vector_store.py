# This handles embeddings generation and storing/retrieving vectors from ChromaDB.

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from app.config import CHROMA_DIR, EMBED_MODEL, TOP_K

embedding_function = SentenceTransformerEmbeddings(model_name=EMBED_MODEL)

def get_vector_store(collection_name: str):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_function,
        persist_directory=CHROMA_DIR
    )

def add_documents(chunks, collection_name: str):
    store = get_vector_store(collection_name)
    store.add_documents(chunks)
    return store

def semantic_search(query: str, collection_name: str, k: int = TOP_K):
    store = get_vector_store(collection_name)
    return store.similarity_search(query, k=k)

def get_retriever(collection_name: str, k: int = TOP_K):
    store = get_vector_store(collection_name)
    return store.as_retriever(search_kwargs={"k": k})