# This is the FastAPI app itself — defines all your API endpoints.

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, uuid

from app.config import UPLOAD_DIR
from app.document_loader import load_and_chunk
from app.vector_store import add_documents, semantic_search, delete_collection, list_all_collections, collection_exists
from app.chat_chain import chat_with_document
from app.memory_store import clear_history
from app.validators import validate_upload, check_duplicate_file, record_file_hash
from app.summarizer import generate_document_overview, save_overview, load_overview, overview_exists

app = FastAPI(title="DocVerse AI", description="Upload documents and chat with them using Groq + RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str
    collection_name: str
    message: str

class SearchRequest(BaseModel):
    collection_name: str
    query: str
    k: int = 4

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_bytes = await file.read()

    # Run all validations (raises HTTPException on failure)
    file_hash = validate_upload(file.filename, file_bytes)

    # Check for duplicates
    existing_doc_id = check_duplicate_file(file_hash)
    if existing_doc_id:
        return {
            "message": "This document was already uploaded previously.",
            "collection_name": existing_doc_id,
            "duplicate": True
        }

    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    with open(file_path, "wb") as buffer:
        buffer.write(file_bytes)

    chunks = load_and_chunk(file_path, original_filename=file.filename, doc_id=doc_id)

    if len(chunks) == 0:
        os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail="No readable text found in this PDF. It may be empty, scanned as images, or corrupted."
        )

    add_documents(chunks, collection_name=doc_id)
    record_file_hash(file_hash, doc_id)

    # Generate a document-wide overview (table of contents / topic list)
    try:
        overview_data = generate_document_overview(chunks, file.filename)
        save_overview(doc_id, overview_data)
    except Exception:
        pass  # overview generation failure shouldn't block the upload itself

    return {
        "message": "Document uploaded, chunked, and embedded successfully",
        "collection_name": doc_id,
        "num_chunks": len(chunks),
        "duplicate": False
    }

@app.post("/search")
async def search_document(request: SearchRequest):
    results = semantic_search(request.query, request.collection_name, request.k)
    return {
        "results": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    # Validate question is not empty
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty. Please type a question.")

    # Validate collection_name is provided
    if not request.collection_name or not request.collection_name.strip():
        raise HTTPException(status_code=400, detail="No document selected. Please upload a document first.")

    try:
        result = chat_with_document(
            request.session_id,
            request.collection_name,
            request.message
        )
        return result
    except HTTPException:
        raise  # already a well-formatted error, let it pass through as-is
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/chat/reset")
async def reset_chat(session_id: str):
    clear_history(session_id)
    return {"message": f"Chat history cleared for session {session_id}"}

@app.delete("/document/{collection_name}")
async def delete_document(collection_name: str):
    """Deletes a specific document's vector data and its uploaded PDF file."""
    if not collection_exists(collection_name):
        raise HTTPException(status_code=404, detail=f"Document '{collection_name}' not found.")

    try:
        delete_collection(collection_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

    file_path = os.path.join(UPLOAD_DIR, f"{collection_name}.pdf")
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"message": f"Document '{collection_name}' deleted successfully."}

@app.get("/documents")
async def list_documents():
    """Lists all currently uploaded document collections."""
    collections = list_all_collections()
    return {"documents": collections, "count": len(collections)}

@app.get("/document/{collection_name}/overview")
async def get_document_overview(collection_name: str):
    """Returns the table-of-contents style overview for a document, if available."""
    if not overview_exists(collection_name):
        raise HTTPException(status_code=404, detail="No overview available for this document.")

    overview_data = load_overview(collection_name)
    return overview_data

@app.delete("/documents/clear-all")
async def clear_all_documents():
    """Deletes ALL uploaded documents, their vector data, and resets duplicate tracking."""
    collections = list_all_collections()

    for name in collections:
        try:
            delete_collection(name)
        except Exception:
            pass

        file_path = os.path.join(UPLOAD_DIR, f"{name}.pdf")
        if os.path.exists(file_path):
            os.remove(file_path)

    # Also clear the duplicate-tracking hash file
    hash_file_path = os.path.join(UPLOAD_DIR, "_upload_hashes.txt")
    if os.path.exists(hash_file_path):
        os.remove(hash_file_path)

    return {"message": f"Deleted {len(collections)} document(s).", "deleted_count": len(collections)}

@app.get("/")
async def root():
    return {"message": "DocVerse AI is running. Visit /docs for API reference."}