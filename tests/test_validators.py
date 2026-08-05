import pytest
from fastapi import HTTPException
from app.validators import (
    validate_file_extension,
    validate_file_size,
    validate_pdf_content,
    compute_file_hash,
    validate_upload
)
from tests.conftest import create_minimal_pdf_bytes

def test_validate_file_extension_accepts_pdf():
    validate_file_extension("document.pdf")  # should not raise

def test_validate_file_extension_rejects_non_pdf():
    with pytest.raises(HTTPException) as exc_info:
        validate_file_extension("document.txt")
    assert exc_info.value.status_code == 400

def test_validate_file_size_rejects_empty_file():
    with pytest.raises(HTTPException) as exc_info:
        validate_file_size(b"")
    assert exc_info.value.status_code == 400

def test_validate_file_size_rejects_too_large_file():
    huge_file = b"0" * (21 * 1024 * 1024)  # 21MB, over the 20MB limit
    with pytest.raises(HTTPException) as exc_info:
        validate_file_size(huge_file)
    assert exc_info.value.status_code == 400

def test_validate_file_size_accepts_normal_file():
    normal_file = create_minimal_pdf_bytes()
    validate_file_size(normal_file)  # should not raise

def test_validate_pdf_content_accepts_valid_pdf():
    pdf_bytes = create_minimal_pdf_bytes()
    validate_pdf_content(pdf_bytes)  # should not raise

def test_validate_pdf_content_rejects_fake_pdf():
    fake_pdf = b"This is not a real PDF file"
    with pytest.raises(HTTPException) as exc_info:
        validate_pdf_content(fake_pdf)
    assert exc_info.value.status_code == 400

def test_compute_file_hash_is_consistent():
    data = b"some test data"
    hash1 = compute_file_hash(data)
    hash2 = compute_file_hash(data)
    assert hash1 == hash2

def test_compute_file_hash_differs_for_different_data():
    hash1 = compute_file_hash(b"data one")
    hash2 = compute_file_hash(b"data two")
    assert hash1 != hash2

def test_validate_upload_full_pipeline():
    pdf_bytes = create_minimal_pdf_bytes()
    file_hash = validate_upload("test.pdf", pdf_bytes)
    assert isinstance(file_hash, str)
    assert len(file_hash) == 64  # SHA-256 hash length