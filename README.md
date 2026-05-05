# secure-summary
An AI-powered PDF assistant that allows users to:

* Upload one or multiple PDFs
* Get automatic summaries
* Ask questions from documents
* Maintain separate chat history per session (like ChatGPT)

---

## 🚀 Features

### 🧠 AI Capabilities

* 📚 Automatic PDF summarization (HuggingFace Transformers)
* 🔍 Semantic search using embeddings (SentenceTransformers)
* 💬 Question-answering using local LLM (FLAN-T5)

### 📂 Multi-PDF Support

* Upload multiple PDFs into **same chat**
* System merges documents into a single knowledge base
* Ask questions across all uploaded PDFs

### 🗂️ Chat History System

* Each "New Chat" creates a **new session**
* Each session stores:

  * Summary
  * Chat history
  * Uploaded PDFs
* Sidebar shows chat history like ChatGPT

### 🎨 Modern UI

* ChatGPT-style interface
* Sidebar history
* Chat bubbles
* Upload icon 📎 near input
* Smooth UX

---

## 🏗️ Tech Stack

### Backend

* FastAPI
* FAISS (Vector DB)
* SentenceTransformers (Embeddings)
* HuggingFace Transformers (LLM)

### Frontend

* HTML + CSS + JavaScript
* Fetch API (no frameworks)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pdf-chatgpt.git
cd pdf-chatgpt
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install fastapi uvicorn python-multipart pymupdf \
sentence-transformers faiss-cpu transformers torch
```

---

### 4️⃣ Run Backend

```bash
uvicorn main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

### 5️⃣ Run Frontend

Just open:

```
index.html
```

in your browser

---

## 📁 Project Structure

```
project/
│── main.py          # FastAPI backend
│── utils.py         # PDF processing + embeddings + QA
│── index.html       # Frontend UI
│── uploads/         # Stored PDFs
```

---

## 🔄 How It Works

### 📄 Step 1: Upload PDF

* File is saved in `/uploads`
* Text extracted using PyMuPDF

### ✂️ Step 2: Chunking

* Text split into smaller chunks
* Helps in better semantic search

### 🔢 Step 3: Embeddings

* Each chunk converted into vector using:

```
all-MiniLM-L6-v2
```

### 📦 Step 4: FAISS Index

* Vectors stored in FAISS for fast similarity search

### 🧠 Step 5: Summary

* Uses:

```
distilbart-cnn-12-6
```

* Generates bullet-point summary

### ❓ Step 6: Ask Questions

* Query → converted to embedding
* Top relevant chunks retrieved
* Passed to FLAN-T5 model

---

## 🔁 Multi-PDF Logic

### Same Chat

* PDFs are **merged**
* Chunks added to existing FAISS index
* Summary updated

### New Chat

* New document created
* New history entry
* Fresh chat

---

## 🧠 Chat Memory System

Each document stores:

```python
documents = {
  doc_id: {
    "chunks": [...],
    "index": faiss_index,
    "summary": "...",
    "name": "...",
    "chat": [
        {"question": "...", "answer": "..."}
    ]
  }
}
```

---

## 🌐 API Endpoints

### 📄 Upload PDF

```
POST /upload
```

### ❓ Ask Question

```
POST /ask
```

### 📚 Get Summary

```
GET /summary
```

### 📂 Get All Documents

```
GET /documents
```

### 📄 Get One Document

```
GET /documents/{doc_id}
```

### ➕ New Chat

```
POST /new-chat
```

---

## 🎯 Key Concepts Used

* Retrieval Augmented Generation (RAG)
* Vector Databases (FAISS)
* Embeddings
* Chunking
* Prompt Engineering
* Session Management

---

## 💬 Interview Explanation

You can say:

> "I built a multi-document AI assistant using a RAG pipeline. It supports session-based chat memory, incremental FAISS indexing, and local LLM inference using HuggingFace models."

---

## 🚀 Future Improvements

* 🗃️ Persistent storage (SQLite / MongoDB)
* 🧾 PDF previews
* ✏️ Rename chats
* ❌ Delete chats
* 🌐 Deploy (Render / Vercel)
* ⚡ Streaming responses

---

## 🙌 Author

**Aadya Mishra**

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and share!
