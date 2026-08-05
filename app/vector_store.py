# This handles embeddings generation and storing/retrieving vectors from ChromaDB.

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document
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

def get_retriever(collection_name: str, k: int = TOP_K, use_mmr: bool = True):
    """
    Returns a retriever using MMR (Maximal Marginal Relevance) by default.
    MMR balances relevance with diversity, reducing redundant chunks.
    """
    store = get_vector_store(collection_name)

    if use_mmr:
        return store.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": k * 5,
                "lambda_mult": 0.7
            }
        )
    else:
        return store.as_retriever(search_kwargs={"k": k})

def delete_collection(collection_name: str):
    """Deletes a specific document's collection from ChromaDB."""
    store = get_vector_store(collection_name)
    store.delete_collection()

def list_all_collections():
    """Returns a list of all collection names currently in ChromaDB."""
    import chromadb
    from app.config import CHROMA_DIR

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collections = client.list_collections()
    return [c.name for c in collections]

def collection_exists(collection_name: str) -> bool:
    """Checks if a collection actually exists before deleting it."""
    existing = list_all_collections()
    return collection_name in existing

def keyword_search(collection_name: str, query: str, max_results: int = 5):
    """
    Scans ALL stored chunks in a collection and returns those containing
    keywords from the query (case-insensitive). Useful for exact title/name
    matches that semantic search might miss.
    """
    store = get_vector_store(collection_name)

    raw_data = store.get()
    all_docs = raw_data.get("documents", [])
    all_metadatas = raw_data.get("metadatas", [])

    query_lower = query.lower()

    stopwords = {"the", "a", "an", "of", "in", "is", "what", "give", "me", "can", "you", "please", "story", "moral"}
    query_words = [w.strip(".,!?") for w in query_lower.split() if w.strip(".,!?") not in stopwords and len(w) > 2]

    matches = []
    for content, metadata in zip(all_docs, all_metadatas):
        content_lower = content.lower()
        match_count = sum(1 for word in query_words if word in content_lower)
        if match_count > 0:
            matches.append((match_count, content, metadata))

    matches.sort(key=lambda x: x[0], reverse=True)

    return [Document(page_content=c, metadata=m) for _, c, m in matches[:max_results]]