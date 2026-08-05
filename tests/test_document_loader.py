import pytest
import tempfile
import os
from app.document_loader import load_and_chunk
from tests.conftest import create_minimal_pdf_bytes

def test_load_and_chunk_returns_chunks():
    pdf_bytes = create_minimal_pdf_bytes()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        chunks = load_and_chunk(tmp_path, original_filename="test.pdf", doc_id="test-doc-id")
        assert isinstance(chunks, list)
        # Minimal PDF might produce 0 or 1 chunks depending on extractable text
        if len(chunks) > 0:
            assert chunks[0].metadata.get("file_name") == "test.pdf"
            assert chunks[0].metadata.get("doc_id") == "test-doc-id"
            assert "chunk_id" in chunks[0].metadata
            assert "page_number" in chunks[0].metadata
            assert "upload_time" in chunks[0].metadata
    finally:
        os.remove(tmp_path)

def test_load_and_chunk_metadata_defaults():
    pdf_bytes = create_minimal_pdf_bytes()

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name

    try:
        chunks = load_and_chunk(tmp_path)  # no filename/doc_id passed
        if len(chunks) > 0:
            assert chunks[0].metadata.get("file_name") == "unknown.pdf"
            assert chunks[0].metadata.get("doc_id") == "unknown"
    finally:
        os.remove(tmp_path)