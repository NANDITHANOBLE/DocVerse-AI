# 📄 DocVerse AI

<div align="center">

### 🚀 Upload Documents • Ask Questions • Get AI-Powered Answers

A Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and have intelligent conversations with them using AI.

Built with FastAPI, LangChain, ChromaDB, Sentence Transformers, Groq LLM, and Streamlit.

<br>

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?style=for-the-badge&logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange?style=for-the-badge)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?style=for-the-badge&logo=streamlit)

</div>

---

## 🌟 Features

- ✅ Upload PDF Documents
- ✅ Automatic Text Extraction
- ✅ Text Chunking for Better Retrieval
- ✅ Semantic Search with Embeddings
- ✅ Context-Aware AI Answers
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ FastAPI REST APIs
- ✅ Streamlit User Interface
- ✅ Vector Storage with ChromaDB
- ✅ Open Source & Easy to Extend

---

## 🏗️ Architecture

```text
PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
ChromaDB Vector Store
    │
    ▼
Semantic Retrieval
    │
    ▼
Groq LLM
    │
    ▼
AI Generated Answer
```

---

## 💡 Project Workflow

```text
User Uploads PDF
       │
       ▼
PDF Processed
       │
       ▼
Documents Split Into Chunks
       │
       ▼
Embeddings Generated
       │
       ▼
Stored In ChromaDB
       │
       ▼
User Asks Question
       │
       ▼
Relevant Chunks Retrieved
       │
       ▼
Groq LLM Generates Answer
       │
       ▼
Response Displayed To User
```

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Python
- Uvicorn

### AI & RAG
- LangChain
- Groq LLM
- ChromaDB
- Sentence Transformers
- HuggingFace Embeddings

### Frontend
- Streamlit

### Utilities
- PyPDF
- Python Dotenv

---

## 📂 Project Structure

```text
DocVerse-AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app & API endpoints
│   ├── config.py            # Environment variables & model settings
│   ├── document_loader.py   # PDF text extraction & chunking
│   ├── vector_store.py      # Embeddings & ChromaDB operations
│   ├── chat_chain.py        # RAG chat chain with Groq LLM
│   └── memory_store.py      # Per-session chat history
│
├── data/
│   ├── uploads/             # Uploaded PDF files
│   └── chroma_db/           # ChromaDB vector database
│
├── streamlit_app.py         # Streamlit frontend
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/nandithanoble/DocVerse-AI.git
cd DocVerse-AI
```

### 2️⃣ Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
```

Get your free API key:

🔗 https://console.groq.com

---

## ▶️ Running The Application

### Start Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Start Frontend

```bash
streamlit run streamlit_app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|----------|----------|-------------|
| POST | `/upload` | Upload and Process PDF |
| POST | `/search` | Semantic Search |
| POST | `/chat` | Ask Questions |
| POST | `/chat/reset` | Reset Chat Session |
| GET | `/` | Health Check |

---

## 📖 API Documentation

FastAPI automatically generates Swagger documentation.

```text
http://127.0.0.1:8000/docs
```

---

## 🚀 Future Enhancements

- [ ] DOCX Support
- [ ] TXT File Support
- [ ] Multi-Document Chat
- [ ] Conversation Memory
- [ ] User Authentication
- [ ] Redis Integration
- [ ] Response Streaming
- [ ] Docker Deployment
- [ ] Cloud Deployment (AWS / Azure)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

```bash
# Fork the repository

# Create a feature branch
git checkout -b feature-name

# Commit changes
git commit -m "Add new feature"

# Push code
git push origin feature-name
```

Create a Pull Request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🎯 Project Highlights

This project demonstrates practical experience with:

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- LangChain
- ChromaDB Vector Database
- Embeddings & Semantic Search
- FastAPI Development
- API Design & Deployment
- Prompt Engineering
- Document Intelligence Systems
- End-to-End AI Application Development
- Full Stack AI Engineering

---

<div align="center">

### ⭐ If You Found This Project Useful, Please Give It A Star

Built with ❤️ using FastAPI, LangChain, ChromaDB, Groq, and Streamlit.

</div>