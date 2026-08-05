<div align="center">

# 🪐 DocVerse AI

### 📄 Upload Documents • 💬 Ask Questions • 🤖 Get AI-Powered Answers

A production-grade **Retrieval-Augmented Generation (RAG)** application that enables intelligent conversations with PDF documents using **FastAPI**, **LangChain**, **ChromaDB**, **Groq LLM**, and **Streamlit**.

<br>

### 🌟 Intelligent Document Conversations with Source Citations

[Features](#-features) •
[Architecture](#-architecture) •
[Tech Stack](#-tech-stack) •
[Getting Started](#-getting-started) •
[API Endpoints](#-api-endpoints)

</div>

<div align="center">

# 🪐 DocVerse AI

### 📄 Upload Documents • 💬 Ask Questions • 🤖 Get AI-Powered Answers

A production-grade **Retrieval-Augmented Generation (RAG)** application that enables intelligent conversations with PDF documents using **FastAPI, LangChain, ChromaDB, Groq LLM, and Streamlit**.

### 🌟 Intelligent Document Conversations with Source Citations

[**Features**](#-features) • [**Architecture**](#-architecture) • [**Tech Stack**](#-tech-stack) • [**Getting Started**](#-getting-started) • [**API Endpoints**](#-api-endpoints)

</div>


---

## 📖 Overview

**DocVerse AI** is a production-grade RAG application that allows users to upload PDF documents and interact with them through natural language conversations.

Unlike traditional RAG systems that rely only on semantic search, DocVerse AI combines:

✅ Semantic Search (MMR)

✅ Keyword Search Fallback

✅ Document Overview Generation

✅ Source Citation Tracking

✅ Session-Based Memory

✅ Persistent ChromaDB Storage

This enables accurate responses even for structural questions such as:

- How many chapters are there?
- List all sections in order.
- What is the last story in the document?
- Summarize Chapter 5.
- Rank all stories as they appear.

---

## ✨ Features

### 📤 Document Processing

- PDF Upload Support
- File Validation
- Corrupted PDF Detection
- Duplicate Document Detection
- SHA-256 Hash Verification
- Automatic Chunking
- Metadata Assignment

### 🔍 Intelligent Retrieval

- Semantic Search (MMR)
- Keyword Search Fallback
- Hybrid Retrieval Strategy
- Structural Query Detection
- Overview-Based Context Injection
- Persistent ChromaDB Storage

### 💬 AI Chat Experience

- Conversational Question Answering
- Follow-Up Question Support
- Context-Aware Responses
- Source Citations
- Session Memory
- Fast Groq LLM Responses

### 🛠 Engineering Quality

- FastAPI REST APIs
- Streamlit Frontend
- Docker Support
- Unit Testing
- Error Handling
- Modular Architecture
- Production-Ready Design

---

## 🏗 Architecture

```text
                 ┌──────────────┐
                 │ PDF Upload   │
                 └──────┬───────┘
                        │
                        ▼
              ┌──────────────────┐
              │ Validation Layer │
              └──────┬───────────┘
                     │
                     ▼
              ┌──────────────────┐
              │ PDF Chunking     │
              └──────┬───────────┘
                     │
                     ▼
              ┌──────────────────┐
              │ Embeddings       │
              └──────┬───────────┘
                     │
                     ▼
            ┌──────────────────────┐
            │ Chroma Vector Store  │
            └──────────┬───────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼

 ┌─────────────────┐      ┌─────────────────┐
 │ Semantic Search │      │ Keyword Search  │
 └────────┬────────┘      └────────┬────────┘
          └──────────┬─────────────┘
                     ▼

          ┌─────────────────────┐
          │ Hybrid Retrieval    │
          └─────────┬───────────┘
                    ▼

          ┌─────────────────────┐
          │ Groq LLM (RAG)      │
          └─────────┬───────────┘
                    ▼

          ┌─────────────────────┐
          │ Answer + Sources    │
          └─────────────────────┘
```

<details>
<summary><b>🔬 Hybrid Retrieval Explained</b></summary>

### Step 1: Semantic Search

Uses embeddings and MMR retrieval to identify contextually relevant chunks.

### Step 2: Keyword Search

Performs exact title and phrase matching.

### Step 3: Result Merging

Combines semantic and keyword results while removing duplicates.

### Step 4: Structural Query Detection

Questions like:

- List all chapters
- How many sections are there?
- What is the last topic?
- Rank all stories

automatically include the generated document overview.

### Step 5: Response Generation

Groq LLM generates an answer using retrieved context and provides citations.

</details>

---

## 🛠 Tech Stack

| Layer | Technology |
|---------|-----------|
| Backend | FastAPI |
| Language | Python |
| Frontend | Streamlit |
| LLM | Groq (Llama 3.3 70B) |
| Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| PDF Processing | PyPDF |
| Testing | Pytest |
| Containerization | Docker |

---

## 📂 Project Structure

```text
DocVerse-AI
│
├── app
│   ├── main.py
│   ├── config.py
│   ├── document_loader.py
│   ├── vector_store.py
│   ├── chat_chain.py
│   ├── summarizer.py
│   ├── memory_store.py
│   └── validators.py
│
├── tests
│
├── data
│   ├── uploads
│   ├── chroma_db
│   └── overviews
│
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .env.example
└── README.md
```

---

## ⚡ Getting Started

### Prerequisites

- Python 3.10+
- Groq API Key

Get a free API key:

https://console.groq.com

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/NANDITHANOBLE/DocVerse-AI.git
cd DocVerse-AI
```

### 2️⃣ Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 🚀 Running the Application

### Start Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

### Start Frontend

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

| Service | URL |
|----------|------|
| Backend | http://localhost:8000 |
| Frontend | http://localhost:8501 |

---

## 🧪 Running Tests

```bash
pytest -v
```

### ✅ Current Status

**24 / 24 Tests Passing**

Coverage Includes:

- API Endpoints
- Upload Validation
- Duplicate Detection
- PDF Processing
- Chunking Logic
- Metadata Assignment
- ChromaDB Operations
- Retrieval Workflows

---

## 🎯 API Endpoints

| Method | Endpoint | Description |
|----------|-----------|-------------|
| POST | `/upload` | Upload and process PDF |
| POST | `/chat` | Ask questions |
| POST | `/search` | Semantic search |
| POST | `/chat/reset` | Clear chat history |
| GET | `/documents` | List documents |
| GET | `/document/{id}/overview` | Get document overview |
| DELETE | `/document/{id}` | Delete document |
| DELETE | `/documents/clear-all` | Remove all documents |
| GET | `/` | Health check |

---

## 🎬 Example Interaction

### 👤 User

> What is the moral of The Warm Whale?

### 🪐 DocVerse AI

The story teaches that resilience and adaptability are more valuable than avoiding every inconvenience.

📚 Sources:

- Page 42
- Page 43

---

### 👤 User

> Can you rank all the stories in order?

### 🪐 DocVerse AI

1. The Wind and the Sun
2. The Villager and the Spectacles
3. As You Sow, So Shall You Reap
4. ...
5. Remaining stories in document order

---

## 🗺️ Roadmap

- [ ] DOCX Support
- [ ] TXT Support
- [ ] Persistent Chat History
- [ ] Multi-Document Conversations
- [ ] Streaming Responses
- [ ] Authentication System
- [ ] Cloud Deployment
- [ ] Multi-User Support

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

Open a Pull Request describing your changes.

---

## 📜 License

Licensed under the **MIT License**.

---

<div align="center">

### 🌌 Built with Curiosity & Open-Source AI

**⭐ If this project helped you, consider giving it a star!**

</div>
