import pytest
import uuid
from langchain_core.documents import Document
from app.vector_store import (
    add_documents,
    semantic_search,
    get_retriever,
    delete_collection,
    list_all_collections
)

@pytest.fixture
def test_collection_name():
    """Creates a unique collection name for each test, and cleans up after."""
    name = f"test-collection-{uuid.uuid4()}"
    yield name
    try:
        delete_collection(name)
    except Exception:
        pass

def test_add_and_search_documents(test_collection_name):
    docs = [
        Document(page_content="The sky is blue and beautiful.", metadata={"file_name": "test.pdf", "page_number": 1}),
        Document(page_content="Cats are wonderful pets.", metadata={"file_name": "test.pdf", "page_number": 2}),
    ]

    add_documents(docs, collection_name=test_collection_name)
    results = semantic_search("What color is the sky?", test_collection_name, k=1)

    assert len(results) > 0
    assert "sky" in results[0].page_content.lower()

def test_get_retriever_returns_relevant_docs(test_collection_name):
    docs = [
        Document(page_content="Python is a popular programming language.", metadata={"file_name": "test.pdf", "page_number": 1}),
        Document(page_content="Bananas are yellow fruits.", metadata={"file_name": "test.pdf", "page_number": 2}),
    ]

    add_documents(docs, collection_name=test_collection_name)
    retriever = get_retriever(test_collection_name, k=1)
    results = retriever.invoke("Tell me about programming languages")

    assert len(results) > 0
    assert "python" in results[0].page_content.lower()

def test_delete_collection_removes_data(test_collection_name):
    docs = [Document(page_content="Temporary test content.", metadata={"file_name": "test.pdf"})]
    add_documents(docs, collection_name=test_collection_name)

    delete_collection(test_collection_name)

    # After deletion, the collection should no longer appear in the list
    remaining = list_all_collections()
    assert test_collection_name not in remaining