import os

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq


# Load the embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def extract_text(pdf_file):
    """Extract text from an uploaded PDF."""

    reader = PdfReader(pdf_file)

    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    return "\n".join(pages)


def split_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks."""

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + chunk_size])

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def create_vector_index(chunks):
    """Generate embeddings and create a FAISS index."""

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, embeddings


def retrieve_context(question, chunks, index, top_k=3):
    """Retrieve the most relevant document chunks."""

    question_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    k = min(top_k, len(chunks))

    scores, indices = index.search(question_embedding, k)

    results = []

    for idx in indices[0]:
        if idx >= 0:
            results.append(chunks[idx])

    return "\n\n".join(results)


def generate_answer(question, context):
    """Generate an answer using the Groq API."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is not configured.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        ),
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer questions using only the supplied "
                    "document context. If the answer is not "
                    "available in the context, say you could "
                    "not find the answer in the document."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Document context:\n{context}\n\n"
                    f"Question: {question}"
                )
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
