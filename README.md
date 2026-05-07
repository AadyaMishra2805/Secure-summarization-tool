# AI PDF Research Assistant

A modern AI-powered PDF Assistant that allows users to:

<<<<<<< HEAD
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
=======
* Upload PDFs
* Generate summaries
* Ask questions from PDFs
* Store chat history
* Manage multiple chats
* Merge multiple PDFs in one chat
* Perform semantic search using Vector Databases (FAISS)
* Use Local LLMs for question answering

This project was built using:

* FastAPI
* FAISS
* Sentence Transformers
* HuggingFace Transformers
* HTML/CSS/JavaScript
>>>>>>> 8e9c80421f713915f2eda00513aa33c726efdcbc

---

# 🚀 Features

## ✅ PDF Upload
<<<<<<< HEAD
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
=======

Upload any PDF document into the system.

---

## ✅ AI Summarization

Generate intelligent summaries from uploaded PDFs.

---

## ✅ Ask Questions

Ask natural language questions from PDFs.

Example:

```text
Who was the petitioner?
What is the main topic?
Explain the case in detail.
```

---

## ✅ Semantic Search

Uses:

* Embeddings
* Vector Databases
* FAISS similarity search

to retrieve the most relevant chunks before generating answers.

---

## ✅ Multi-PDF Chat Support

You can:

* upload multiple PDFs into the same chat
* ask questions from specific PDFs
* maintain separate vector databases internally

---

## ✅ Chat History

Supports:

* New Chat
* Rename Chat
* Delete Chat
* Pin Chat

like modern AI assistants.

---

## ✅ Modern UI

Inspired by:

* ChatGPT
* Gemini
* Claude

with:

* sidebar history
* chat bubbles
* dark mode interface
* modern responsive design
>>>>>>> 8e9c80421f713915f2eda00513aa33c726efdcbc

---

# 🧠 System Architecture

<<<<<<< HEAD
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
=======
```text
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
```
>>>>>>> 8e9c80421f713915f2eda00513aa33c726efdcbc

---

# 🛠 Tech Stack

<<<<<<< HEAD
- FastAPI
- FAISS
- Sentence Transformers
- HuggingFace Transformers
- PyMuPDF
- HTML/CSS/JS
=======
| Technology               | Purpose             |
| ------------------------ | ------------------- |
| FastAPI                  | Backend API         |
| FAISS                    | Vector database     |
| Sentence Transformers    | Embeddings          |
| HuggingFace Transformers | Local LLM           |
| PyMuPDF                  | PDF text extraction |
| HTML/CSS/JS              | Frontend            |

---

# 📂 Project Structure

```text
project/
│
├── main.py
├── utils.py
├── index.html
├── uploads/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

# 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

# 2️⃣ Open Project Folder

```bash
cd YOUR_REPO
```

---

# 3️⃣ Create Virtual Environment

## Windows

```bash
python -m venv .venv
```

---

# 4️⃣ Activate Virtual Environment

## Git Bash

```bash
source .venv/Scripts/activate
```

## CMD

```bash
.venv\Scripts\activate
```

## PowerShell

```bash
.venv\Scripts\Activate.ps1
```

---

# 5️⃣ Install Dependencies

```bash
pip install fastapi uvicorn python-multipart pymupdf sentence-transformers faiss-cpu transformers torch numpy
```
>>>>>>> 8e9c80421f713915f2eda00513aa33c726efdcbc

---

# ▶️ Run Backend

```bash
<<<<<<< HEAD
uvicorn main:app --reload
=======
uvicorn main:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

# 🌐 Run Frontend

Simply open:

```text
index.html
```

in your browser.

Recommended:

* VS Code Live Server
* Chrome browser

---

# 📄 How PDF Processing Works

## Step 1 — Extract Text

Using:

```python
fitz
```

from PyMuPDF.

---

## Step 2 — Split Text

Large text is divided into chunks.

Example:

```python
chunk_size=500
overlap=50
```

This improves retrieval quality.

---

## Step 3 — Create Embeddings

Using:

```python
SentenceTransformer("all-MiniLM-L6-v2")
```

Embeddings convert text into numerical vectors.

---

## Step 4 — Store in FAISS

FAISS stores vector embeddings for semantic search.

---

## Step 5 — Semantic Retrieval

When user asks a question:

* question embedding is generated
* similar chunks are retrieved
* most relevant chunks become context

---

## Step 6 — Generate Answer

Using:

```python
google/flan-t5-base
```

Local LLM generates final answer.

---

# 🧠 Multi-PDF Logic

Each PDF stores:

* separate chunks
* separate embeddings
* separate FAISS index
* separate summary

This prevents:

* mixed answers
* wrong retrieval
* summary corruption

---

# 💬 Example Workflow

## Upload PDF

```text
case_law.pdf
```

---

## Generate Summary

```text
• Civil Appeal dismissed
• Property dispute discussed
• Co-heirs issue explained
```

---

## Ask Questions

```text
Who was the petitioner?
```

Answer:

```text
The petitioner was Sengalani Chettiar.
```

---

# 📌 Chat Features

## New Chat

Creates completely separate conversation.

---

## Rename Chat

Rename chats like:

```text
Research Notes
Legal Case Study
ML Notes
```

---

## Pin Chat

Pin important chats to top.

---

## Delete Chat

Delete unwanted conversations.

---

# 🔒 Security Features

* Local LLM usage
* No external APIs required
* PDFs processed locally
* Vector search runs locally

---

# 📈 Future Improvements

Possible future upgrades:

* Authentication system
* Database storage
* Persistent chat memory
* OCR for scanned PDFs
* Streaming responses
* LangChain integration
* Docker deployment
* Cloud deployment
* Citation highlighting
* PDF page references

---

# 🧪 Example Interview Concepts Used

This project demonstrates:

* NLP
* Embeddings
* Vector Databases
* Semantic Search
* Retrieval Augmented Generation (RAG)
* FastAPI
* Transformers
* Local LLMs
* Full Stack AI Systems

---

# 📚 Important ML Concepts

## Embeddings

Convert text into vectors.

---

## Vector Database

Stores vectors for similarity search.

---

## Semantic Search

Searches meaning instead of keywords.

---

## RAG (Retrieval Augmented Generation)

Retrieves relevant context before generating answers.

---

# 🤝 Contributing

Pull requests and improvements are welcome.

---

# 📜 License

MIT License

---

# 👨‍💻 Author

Built by Aadya Mishra

AI/ML + Full Stack Development Project

>>>>>>> 8e9c80421f713915f2eda00513aa33c726efdcbc
