import fitz
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline

# =========================
# 📄 Extract text from PDF
# =========================
def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


# =========================
# ✂️ Split text into chunks
# =========================
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# =========================
# 🔢 Embedding model
# =========================
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# 🔢 Create embeddings
# =========================
def create_embeddings(chunks):

    # 🔥 if metadata chunks
    if isinstance(chunks[0], dict):
        texts = [chunk["text"] for chunk in chunks]
    else:
        texts = chunks

    embeddings = embedding_model.encode(texts)

    return np.array(embeddings).astype("float32")


# =========================
# 📦 Store in FAISS
# =========================
def store_in_faiss(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


# =========================
# 🔍 Search chunks
# =========================
def search_chunks(query, index, chunks, top_k=4):

    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results


# =========================
# 🤖 QA MODEL
# =========================
qa_model = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    framework="pt"
)


# =========================
# 🧠 Generate answer
# =========================
def generate_answer(context, question):

    prompt = f"""
Use the context below to answer the question clearly and completely.

Context:
{context}

Question:
{question}

Answer:
"""

    result = qa_model(
        prompt,
        max_new_tokens=120,
        do_sample=False,
        temperature=0.0,
        repetition_penalty=1.2
    )

    answer = result[0]["generated_text"]

    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()

    return answer