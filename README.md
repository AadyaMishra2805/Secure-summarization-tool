# AI PDF Research Assistant

A modern AI-powered PDF Assistant that allows users to:

- Upload PDFs
- Generate summaries
- Ask questions from PDFs
- Store chat history
- Manage multiple chats
- Merge multiple PDFs in one chat
- Perform semantic search using Vector Databases (FAISS)
- Use Local LLMs for question answering

Built using:

- FastAPI
- FAISS
- Sentence Transformers
- HuggingFace Transformers
- HTML/CSS/JavaScript

---

# 🚀 Features

## ✅ PDF Upload
Upload any PDF document into the system.

## ✅ AI Summarization
Generate intelligent summaries from uploaded PDFs.

## ✅ Ask Questions
Ask natural language questions from PDFs.

## ✅ Semantic Search
Uses embeddings + FAISS similarity search for retrieval.

## ✅ Multi-PDF Chat Support
Supports multiple PDFs inside same chat.

## ✅ Chat History
- New Chat
- Rename Chat
- Delete Chat
- Pin Chat

## ✅ Modern UI
Inspired by ChatGPT/Gemini/Claude.

---

# 🧠 System Architecture

PDF Upload
↓
Text Extraction
↓
Chunking
↓
Embeddings
↓
FAISS Vector Database
↓
Semantic Retrieval
↓
Local LLM
↓
Generated Answer

---

# 🛠 Tech Stack

- FastAPI
- FAISS
- Sentence Transformers
- HuggingFace Transformers
- PyMuPDF
- HTML/CSS/JS

---

# ▶️ Run Backend

```bash
uvicorn main:app --reload