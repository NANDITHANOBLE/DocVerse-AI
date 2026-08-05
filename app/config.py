# This file handles environment variables, paths, and model settings.

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
CHROMA_DIR = os.path.join(BASE_DIR, "data", "chroma_db")
OVERVIEWS_DIR = os.path.join(BASE_DIR, "data", "overviews")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHROMA_DIR, exist_ok=True)
os.makedirs(OVERVIEWS_DIR, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")

# Groq model options (free tier): "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"
LLM_MODEL = "llama-3.3-70b-versatile"

EMBED_MODEL = "all-MiniLM-L6-v2"   # sentence-transformers, local & free

# Chunking settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval settings
TOP_K = 8

# Upload validation settings
MAX_FILE_SIZE_MB = 20
ALLOWED_EXTENSIONS = {".pdf"}