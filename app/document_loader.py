# This handles PDF text extraction and splitting into chunks.

import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def load_and_chunk(file_path: str, original_filename: str = None, doc_id: str = None):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    upload_time = datetime.datetime.utcnow().isoformat()

    for i, chunk in enumerate(chunks):
        # PyPDFLoader already sets "page" (0-indexed) in metadata
        page_number = chunk.metadata.get("page", 0) + 1  # convert to human-readable 1-indexed

        chunk.metadata.update({
            "file_name": original_filename or "unknown.pdf",
            "doc_id": doc_id or "unknown",
            "chunk_id": f"{doc_id}_{i}" if doc_id else str(i),
            "page_number": page_number,
            "upload_time": upload_time
        })

    return chunks