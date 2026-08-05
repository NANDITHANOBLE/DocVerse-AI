<div align="center">

# 🪐 DocVerse AI

### 📄 Upload Documents • 💬 Ask Questions • 🤖 Get AI-Powered Answers

A production-grade **Retrieval-Augmented Generation (RAG)** application that enables intelligent conversations with PDF documents using **FastAPI**, **LangChain**, **ChromaDB**, **Groq LLM**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&n
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=forlogo=fastapi
![Streamlit](https://img.shields.io/badge/Streamlit-Frontendr-the-badge&logo=streamlit
![LangChain](https://img.shields.io/badge/LangChain-Rle=for-the-badge
![Chs://img.shields.io/badge/ChromaDB-VectorDB-purple?style=for-the-badge
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the 🌟 Intelligent Document Conversations with Source Citations

[Featuress •
[Architecturee •
[Techh-stack •
#-getting-started •
[APIi-endpoints

</div>

---

# 📖 Overview

**DocVerse AI** allows users to upload PDF documents and interact with them through natural language conversations.

Instead of relying only on traditional semantic retrieval, it uses a **hybrid retrieval strategy** combining:

✅ Semantic Search (MMR)

✅ Keyword Search Fallback

✅ Document Overview Generation

✅ Source Citation Tracking

✅ Conversational Memory

This enables accurate responses even for complex structural questions such as:

- "How many chapters are there?"
- "List all sections in order."
- "What is the last story in the document?"
- "Summarize Chapter 5."

---

# ✨ Features

## 📤 Document Processing

- PDF Upload Support
- File Validation
- Corrupted PDF Detection
- Duplicate Document Detection
- Automatic Chunking
- Metadata Assignment

## 🔍 Intelligent Retrieval

- Semantic Search
- Hybrid Retrieval
- Keyword-Based Search
- Structural Query Detection
- Document Overview Generation
- Persistent ChromaDB Storage

## 💬 AI Chat Experience

- Context-Aware Conversations
- Multi-turn Question Answering
- Source Citations
- Session Memory
- Fast Groq LLM Responses

## 🛠 Engineering Quality

- FastAPI REST APIs
- Streamlit Frontend
- Docker Support
- Unit Testing
- Modular Architecture
- Error Handling

---

# 🏗 Architecture

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

┌─────────────────┐      ┌──────────────────┐
│ Semantic Search │      │ Keyword Search   │
└────────┬────────┘      └────────┬─────────┘
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

---

# 🛠 Tech Stack

## Backend

- FastAPI
- Python
- LangChain

## AI & RAG

- Groq LLM
- ChromaDB
- Sentence Transformers
- Retrieval-Augmented Generation

## Frontend

- Streamlit

## Testing

- Pytest

## DevOps

- Docker
- Docker Compose

---

# 📂 Project Structure

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

# ⚡ Getting Started

## Prerequisites

- Python 3.10+
- Groq API Key

Get your free API key:

https://console.groq.com

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/NANDITHANOBLE/DocVerse-AI.git
cd DocVerse-AI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

# 🚀 Running the Application

## Start Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Docs:

```text
http://localhost:8000/docs
```

---

## Start Frontend

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

# 🐳 Docker Deployment

```bash
docker-compose up --build
```

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:8501
```

---

# 🧪 Running Tests

```bash
pytest -v
```

### ✅ Current Status

- 24 / 24 Tests Passing

Covered Areas:

- API Testing
- Upload Validation
- Duplicate Detection
- Chunking Logic
- Metadata Generation
- ChromaDB Operations
- Retrieval Functions

---

# 🎯 API Endpoints

| Method | Endpoint |
|----------|----------|
| POST | `/upload` |
| POST | `/chat` |
| POST | `/search` |
| POST | `/chat/reset` |
| GET | `/documents` |
| GET | `/document/{id}/overview` |
| DELETE | `/document/{id}` |
| DELETE | `/documents/clear-all` |
| GET | `/` |

---

# 🎬 Example Interaction

### User

> What is the moral of The Warm Whale?

### DocVerse AI

The story teaches that relying too much on comfort and reacting strongly to small inconveniences can make life harder than it really is. Resilience and adaptability are important life skills.

📚 Sources:

- Page 42
- Page 43

---

### User

> Can you list all stories in order?

### DocVerse AI

1. The Wind and the Sun
2. The Villager and the Spectacles
3. As You Sow, So Shall You Reap
4. ...
5. Remaining stories in correct order

---

# 🗺️ Roadmap

- [ ] DOCX Support
- [ ] TXT Support
- [ ] Persistent Chat History
- [ ] Multi-Document Conversations
- [ ] Streaming Responses
- [ ] Authentication System
- [ ] Cloud Deployment
- [ ] Multi-User Workspace

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/new-feature
git commit -m "Add new feature"
git push origin feature/new-feature
```

Then create a Pull Request.

---

# 📜 License

Licensed under the MIT License.

---

<div align="center">

## 🌌 Built with Curiosity and Open-Source AI

### ⭐ If you found this project useful, consider giving it a star!

</div>
