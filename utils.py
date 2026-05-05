import fitz  # PyMuPDF
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
# 🔢 Convert chunks to vectors
# =========================
def create_embeddings(chunks):
    embeddings = embedding_model.encode(chunks)

    # 🔥 FIX 1: FAISS needs float32
    return np.array(embeddings).astype("float32")


# =========================
# 📦 Store in FAISS
# =========================
def store_in_faiss(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    # already float32 now
    index.add(embeddings)

    return index


# =========================
# 🔍 Search similar chunks
# =========================
def search_chunks(query, index, chunks, top_k=3):

    # 🔥 FIX 2: ensure correct dtype + shape
    query_embedding = embedding_model.encode([query])
    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = [chunks[i] for i in indices[0]]

    return results


# =========================
# 🤖 LLM (FLAN-T5)
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

    # 🚀 IMPROVEMENT: cleaner prompt (reduces hallucination)
    prompt = f"""
Answer ONLY from the given context.
If the answer is not in context, say "Not found in document."

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

    full_text = result[0]["generated_text"]

    # extract answer cleanly
    answer = full_text.split("Answer:")[-1].strip()

    # clean incomplete sentences
    if "." in answer:
        answer = answer[:answer.rfind(".") + 1]

    return answer