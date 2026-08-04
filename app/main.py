#This is the FastAPI app itself — defines all your API endpoints.

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil, os, uuid

from app.config import UPLOAD_DIR
from app.document_loader import load_and_chunk
from app.vector_store import add_documents, semantic_search
from app.chat_chain import chat_with_document
from app.memory_store import clear_history

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
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported currently")

    doc_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}.pdf")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = load_and_chunk(file_path)
    add_documents(chunks, collection_name=doc_id)

    return {
        "message": "Document uploaded, chunked, and embedded successfully",
        "collection_name": doc_id,
        "num_chunks": len(chunks)
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
    try:
        result = chat_with_document(
            request.session_id,
            request.collection_name,
            request.message
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/reset")
async def reset_chat(session_id: str):
    clear_history(session_id)
    return {"message": f"Chat history cleared for session {session_id}"}

@app.get("/")
async def root():
    return {"message": "DocVerse AI is running. Visit /docs for API reference."}