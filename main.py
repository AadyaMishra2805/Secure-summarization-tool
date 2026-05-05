from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import uuid 

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
# GLOBALS
# =========================
documents = {}
current_doc_id = None  

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

app = FastAPI()

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =========================
# 📄 UPLOAD / MERGE PDF
# =========================
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global documents, current_doc_id

    if file.content_type != "application/pdf":
        return {"message": "Only PDF files allowed ❌"}

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    if not text.strip():
        return {"message": "Empty PDF ❌"}

    # =========================
    # SPLIT
    # =========================
    chunks = split_text(text)

    # =========================
    # 🔥 CREATE NEW CHAT IF NONE
    # =========================
    if not current_doc_id:
        doc_id = str(uuid.uuid4())

        documents[doc_id] = {
            "chunks": [],
            "index": None,
            "summary": "",
            "name": file.filename,
            "chat": []
        }

        current_doc_id = doc_id

    doc_id = current_doc_id
    doc = documents[doc_id]

    # =========================
    # 🔥 MERGE CHUNKS
    # =========================
    doc["chunks"].extend(chunks)

    # =========================
    # 🔥 MERGE FAISS
    # =========================
    new_embeddings = create_embeddings(chunks)

    if doc["index"] is None:
        doc["index"] = store_in_faiss(new_embeddings)
    else:
        doc["index"].add(new_embeddings)

    # =========================
    # 🔥 UPDATE SUMMARY (COMBINED)
    # =========================
    try:
        merged_chunks = doc["chunks"]

        sample = (
            merged_chunks[:2] +
            merged_chunks[len(merged_chunks)//2:len(merged_chunks)//2+1] +
            merged_chunks[-1:]
        )

        input_text = " ".join(sample)
        input_text = "Summarize the following text:\n" + input_text

        summary = summarizer(
            input_text,
            max_length=140,
            min_length=50,
            do_sample=False
        )[0]["summary_text"]

        summary = summary.replace("Summarize the following text:", "").strip()
        summary = summary.replace(" .", ".").replace(" ,", ",")

        lines = summary.split(". ")
        summary = "\n".join([f"• {line.strip()}" for line in lines if line.strip()])

    except Exception as e:
        print("Summary error:", e)
        summary = doc["summary"]

    doc["summary"] = summary

    # optional: show merged file names
    doc["name"] = f"{doc['name']} + {file.filename}"

    return {
        "message": "PDF added to current chat ✅",
        "doc_id": doc_id,
        "summary": summary,
        "name": doc["name"]
    }


# =========================
# ❓ ASK QUESTION
# =========================
@app.post("/ask")
async def ask_question(data: dict):
    question = data.get("question")
    doc_id = data.get("doc_id")

    if doc_id not in documents:
        return {"answer": "Invalid document selected"}

    doc = documents[doc_id]

    relevant_chunks = search_chunks(
        question,
        doc["index"],
        doc["chunks"]
    )

    context = "\n".join(relevant_chunks)

    answer = generate_answer(context, question)

    # 🔥 STORE CHAT
    doc["chat"].append({
        "question": question,
        "answer": answer
    })

    return {"answer": answer}


# =========================
# 📚 SUMMARY
# =========================
@app.get("/summary")
async def get_summary():
    if not current_doc_id or current_doc_id not in documents:
        return {"summary": "Please upload a PDF first"}

    return {
        "summary": documents[current_doc_id]["summary"]
    }


# =========================
# 📂 HISTORY LIST
# =========================
@app.get("/documents")
async def get_documents():
    return [
        {"id": doc_id, "name": doc["name"]}
        for doc_id, doc in documents.items()
    ]


# =========================
# 📄 LOAD DOCUMENT
# =========================
@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    if doc_id not in documents:
        return {"error": "Not found"}

    doc = documents[doc_id]

    return {
        "summary": doc["summary"],
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
    return {"message": "New chat started"}