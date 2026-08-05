<div align="center">

# 🪐 DocVerse AI

### 📄 Upload Documents • 💬 Ask Questions • 🤖 Get AI-Powered Answers

A production-grade **Retrieval-Augmented Generation (RAG)** application that enables intelligent conversations with PDF documents using **FastAPI**, **LangChain**, **ChromaDB**, **Groq LLM**, and **Streamlit**.

<br>

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-logo=python
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688the-badge&logo=fastapi
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4-the-badge&logo=streamlit

![LangChain](https://img.shields.io/badgeG-orange?style=for-the-badge
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple?style=for-the-badge)
![Tests](https://img.shields.io/badge/Tests-24%2F24_Passing-success?style=for-the-bs://img.shields.io/badge/License-MIT-yellow?style=for-the-badge

### 🌟 Intelligent Document Conversations with Source Citations

[Featuress •
#-architecture •
#-tech-stack •
[Gettingg-started •
[API Endpoints](#-api-endpoints)

� Overview

**DocVerse AI** is a production-grade RAG application that allows users to upload PDF documents and interact with them through natural conversations.

Unlike traditional RAG systems that rely only on semantic search, DocVerse AI combines:

✅ Semantic Search (MMR)

✅ Keyword Search Fallback

✅ Document Overview Generation

✅ Source Citation Tracking

✅ Session-Based Memory

✅ Persistent Vector Storage

This enables accurate responses even for complex questions such as:

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
- Automatic Chunking
- Metadata Assignment
- SHA-256 Hash Verification

### 🔍 Intelligent Retrieval

- Semantic Search (MMR)
- Keyword Search Fallback
- Hybrid Retrieval Strategy
- Structural Query Detection
- Overview-Based Context Injection
- Persistent ChromaDB Storage

### 💬 AI Chat Experience

- Conversational Question Answering
- Source Citations
- Follow-Up Question Support
- Session Memory
- Fast Response Generation
- Context-Aware Retrieval

### 🛠 Engineering Quality

- FastAPI Backend
- Streamlit Frontend
- Docker Support
- Unit Testing
- Error Handling
- Modular Architecture
- Production-Ready APIs

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
          ┌────────────┴────────────┐
          ▼                         ▼

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

Uses embeddings and MMR retrieval to find contextually relevant chunks.

### Step 2: Keyword Search

Searches for exact title and phrase matches.

### Step 3: Merge Results

Combines and removes duplicate chunks.

### Step 4: Structural Query Detection

Questions such as:

- List all chapters
- How many sections
- What's the last topic
- Rank all stories

will automatically include the generated document overview.

### Step 5: Generate Final Answer

Groq LLM receives the retrieved context and produces an answer with citations.

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

Get a free key:

https://console.groq.com

---

### 1️⃣ Clone Repository

```bash
git clone https://github.com/NANDITHANOBLE/DocVerse-AI.git
cd DocVerse-AI
```

### 2️⃣ Create Virtual Environment

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

Backend:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

### Start Frontend

```bash
streamlit run streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

| Service | URL |
|---------|------|
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
|----------|----------|-------------|
| POST | `/upload` | Upload and process PDF |
| POST | `/chat` | Ask questions |
| POST | `/search` | Semantic search |
| POST | `/chat/reset` | Clear chat history |
| GET | `/documents` | List documents |
| GET | `/document/{id}/overview` | Get overview |
| DELETE | `/document/{id}` | Delete document |
| DELETE | `/documents/clear-all` | Remove all documents |
| GET | `/` | Health Check |

---

## 🎬 Example Interaction

### 👤 User

> What is the moral of The Warm Whale?

### 🪐 DocVerse AI

The story teaches that relying too much on comfort and reacting strongly to small inconveniences can make life harder than they really are. Resilience and adaptability are important life skills.

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
5. All stories listed in document order

---

## 🗺️ Roadmap

- [ ] DOCX Support
- [ ] TXT Support
- [ ] Persistent Chat History
- [ ] Multi-Document Conversations
- [ ] Streaming Responses
- [ ] User Authentication
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

Create a Pull Request and describe your changes.

---

## 📜 License

Licensed under the **MIT License**.

---

<div align="center">

## 🌌 Built with Curiosity & Open-Source AI

### ⭐ If this project helped you, consider giving it a Star!

#-docverse-ai

</div>
