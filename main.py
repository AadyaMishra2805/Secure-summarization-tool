from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid
import warnings
import webbrowser
from threading import Timer

warnings.filterwarnings("ignore")

from utils import (
    extract_text_from_pdf,
    split_text,
    create_embeddings,
    store_in_faiss,
    search_chunks,
    generate_answer
)

from transformers import pipeline

# =========================
# 🚀 FASTAPI APP
# =========================
app = FastAPI()
def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

Timer(1, open_browser).start()
from fastapi.responses import FileResponse
@app.get("/")
async def home():
    return FileResponse("index.html")
# =========================
# 🔧 HELPERS
# =========================
def clean_name(filename):
    return filename.replace(".pdf", "")

# =========================
# 🌍 GLOBAL STORAGE
# =========================
documents = {}

current_doc_id = None

summarizer = None

# =========================
# 🔥 LOAD MODEL
# =========================
@app.on_event("startup")
def load_model():

    global summarizer

    print("🔥 Loading summarizer model...")

    summarizer = pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )

    print("✅ Model loaded")


# =========================
# 🌐 CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 📁 UPLOAD DIRECTORY
# =========================
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# 📄 UPLOAD PDF
# =========================
@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    doc_id: str = Form(None)
):

    global documents, current_doc_id

    # ✅ validate
    if file.content_type != "application/pdf":
        return {"message": "Only PDF files allowed"}

    # =========================
    # SAVE PDF
    # =========================
    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # =========================
    # EXTRACT TEXT
    # =========================
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        return {"message": "Empty PDF"}

    # =========================
    # SPLIT CHUNKS
    # =========================
    chunks = split_text(text)

    # =========================
    # NEW CHAT OR EXISTING CHAT
    # =========================
    if doc_id and doc_id in documents:

        current_doc_id = doc_id

    else:

        doc_id = str(uuid.uuid4())

        documents[doc_id] = {

            "name": clean_name(file.filename),

            "pdfs": {},

            "chat": [],

            "pinned": False
        }

        current_doc_id = doc_id

    doc = documents[current_doc_id]

    # =========================
    # CREATE PDF OBJECT
    # =========================
    pdf_id = str(uuid.uuid4())

    embeddings = create_embeddings(chunks)

    index = store_in_faiss(embeddings)

    # =========================
    # SUMMARY
    # =========================
    try:

        input_text = " ".join(chunks[:3])

        input_text = (
            "Summarize the following text:\n"
            + input_text
        )

        summary = summarizer(
            input_text,
            max_length=120,
            min_length=40,
            do_sample=False
        )[0]["summary_text"]

        summary = summary.replace(
            "Summarize the following text:",
            ""
        ).strip()

        lines = summary.split(". ")

        summary = "\n".join([
            f"• {line.strip()}"
            for line in lines
            if line.strip()
        ])

    except Exception as e:

        print("Summary error:", e)

        summary = text[:300]

    # =========================
    # STORE PDF SEPARATELY
    # =========================
    doc["pdfs"][pdf_id] = {

        "name": clean_name(file.filename),

        "chunks": chunks,

        "index": index,

        "summary": summary
    }

    # =========================
    # RESPONSE
    # =========================
    return {

        "message": "PDF uploaded successfully",

        "doc_id": current_doc_id,

        "summary": summary,

        "name": clean_name(file.filename)
    }

# =========================
# ❓ ASK QUESTION
# =========================
@app.post("/ask")
async def ask_question(data: dict):

    question = data.get("question")

    doc_id = data.get("doc_id")

    if doc_id not in documents:
        return {"answer": "Invalid chat"}

    doc = documents[doc_id]

    # =========================
    # SINGLE PDF
    # =========================
    if len(doc["pdfs"]) == 1:

        pdf = list(doc["pdfs"].values())[0]

    else:

        # 🔥 MULTI PDF LOGIC
        # choose best matching pdf

        best_pdf = None
        best_score = 999999

        for pdf in doc["pdfs"].values():

            query_embedding = create_embeddings([question])

            D, I = pdf["index"].search(
                query_embedding,
                1
            )

            score = D[0][0]

            if score < best_score:

                best_score = score

                best_pdf = pdf

        pdf = best_pdf

    # =========================
    # SEARCH CHUNKS
    # =========================
    relevant_chunks = search_chunks(
        question,
        pdf["index"],
        pdf["chunks"]
    )

    # =========================
    # CONTEXT
    # =========================
    context = "\n".join(relevant_chunks)

    # =========================
    # GENERATE ANSWER
    # =========================
    answer = generate_answer(
        context,
        question
    )

    # =========================
    # SAVE CHAT
    # =========================
    doc["chat"].append({

        "question": question,

        "answer": answer
    })

    return {
        "answer": answer
    }

# =========================
# 📚 SUMMARY
# =========================
@app.get("/summary")
async def get_summary():

    if (
        not current_doc_id
        or current_doc_id not in documents
    ):
        return {
            "summary": "Upload PDF first"
        }

    doc = documents[current_doc_id]

    # latest pdf
    latest_pdf = list(doc["pdfs"].values())[-1]

    return {
        "summary": latest_pdf["summary"]
    }

# =========================
# 📂 HISTORY
# =========================
@app.get("/documents")
async def get_documents():

    sorted_docs = sorted(
        documents.items(),
        key=lambda x: x[1]["pinned"],
        reverse=True
    )

    return [

        {
            "id": doc_id,
            "name": doc["name"],
            "pinned": doc["pinned"]
        }

        for doc_id, doc in sorted_docs
    ]

# =========================
# 📄 LOAD DOCUMENT
# =========================
@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):

    if doc_id not in documents:
        return {"error": "Not found"}

    doc = documents[doc_id]

    latest_pdf = list(doc["pdfs"].values())[-1]

    return {

        "summary": latest_pdf["summary"],

        "name": doc["name"],

        "chat": doc["chat"]
    }

# =========================
# ➕ NEW CHAT
# =========================
@app.post("/new-chat")
async def new_chat():

    global current_doc_id

    current_doc_id = None

    return {
        "message": "New chat"
    }

# =========================
# ✏️ RENAME CHAT
# =========================
@app.post("/rename/{doc_id}")
async def rename_chat(
    doc_id: str,
    data: dict
):

    if doc_id in documents:

        documents[doc_id]["name"] = data["name"]

    return {
        "message": "renamed"
    }

# =========================
# 🗑 DELETE CHAT
# =========================
@app.delete("/delete/{doc_id}")
async def delete_chat(doc_id: str):

    if doc_id in documents:

        del documents[doc_id]

    return {
        "message": "deleted"
    }

# =========================
# 📌 PIN CHAT
# =========================
@app.post("/pin/{doc_id}")
async def pin_chat(doc_id: str):

    if doc_id in documents:

        documents[doc_id]["pinned"] = not documents[doc_id]["pinned"]

    return {
        "message": "updated"
    }