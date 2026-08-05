import os
import hashlib
from fastapi import HTTPException
from app.config import MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS, UPLOAD_DIR

MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def validate_file_extension(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Only PDF files are allowed."
        )

def validate_file_size(file_bytes: bytes):
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB."
        )

def validate_pdf_content(file_bytes: bytes):
    """Basic check that the file starts with the PDF magic number."""
    if not file_bytes.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PDF (corrupted or wrong format)."
        )

def compute_file_hash(file_bytes: bytes) -> str:
    """Used to detect duplicate uploads."""
    return hashlib.sha256(file_bytes).hexdigest()

def check_duplicate_file(file_hash: str):
    """
    Checks if a file with the same hash was already uploaded.
    Returns the existing doc_id if found, else None.
    """
    hash_record_path = os.path.join(UPLOAD_DIR, "_upload_hashes.txt")
    if not os.path.exists(hash_record_path):
        return None

    with open(hash_record_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            stored_hash, stored_id = line.split(",", 1)
            if stored_hash == file_hash:
                return stored_id
    return None

def record_file_hash(file_hash: str, doc_id: str):
    hash_record_path = os.path.join(UPLOAD_DIR, "_upload_hashes.txt")
    with open(hash_record_path, "a") as f:
        f.write(f"{file_hash},{doc_id}\n")

def validate_upload(filename: str, file_bytes: bytes):
    """Runs all validation checks in sequence. Returns file_hash if valid."""
    validate_file_extension(filename)
    validate_file_size(file_bytes)
    validate_pdf_content(file_bytes)
    file_hash = compute_file_hash(file_bytes)
    return file_hash