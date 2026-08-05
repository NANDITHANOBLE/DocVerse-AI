import pytest
from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import create_minimal_pdf_bytes

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_upload_rejects_non_pdf():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"just some text", "text/plain")}
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]

def test_upload_rejects_empty_file():
    response = client.post(
        "/upload",
        files={"file": ("empty.pdf", b"", "application/pdf")}
    )
    assert response.status_code == 400

def test_upload_rejects_fake_pdf():
    response = client.post(
        "/upload",
        files={"file": ("fake.pdf", b"not a real pdf content", "application/pdf")}
    )
    assert response.status_code == 400

def test_upload_valid_pdf():
    pdf_bytes = create_minimal_pdf_bytes()
    response = client.post(
        "/upload",
        files={"file": ("test.pdf", pdf_bytes, "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "collection_name" in data

def test_chat_rejects_empty_question():
    response = client.post(
        "/chat",
        json={"session_id": "test", "collection_name": "some-id", "message": "   "}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()

def test_chat_rejects_missing_collection():
    response = client.post(
        "/chat",
        json={"session_id": "test", "collection_name": "", "message": "Hello"}
    )
    assert response.status_code == 400

def test_list_documents_endpoint():
    response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert "documents" in data
    assert "count" in data

def test_delete_nonexistent_document():
    response = client.delete("/document/nonexistent-id-12345")
    assert response.status_code == 404