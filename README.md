# 🎓 EduRAG: AI-Powered Study Assistant

> A Retrieval-Augmented Generation (RAG) system built as a Capstone Project at Masai School. It enables students to query study materials (PDFs, notes, textbooks) and receive accurate, context-aware answers with exact source citations.

---

## 📌 Problem Statement

Students often struggle to navigate dense textbooks, long lecture notes, and revision materials efficiently. Standard Large Language Models (LLMs) frequently hallucinate or generate overly generic responses without referencing specific course content. 

**EduRAG** addresses this issue by combining document retrieval with generative AI. It anchors LLM responses strictly in the student’s uploaded study materials, delivering verifiable, accurate answers alongside direct page and section references.

---

## ✨ Features

- **"Document Ingestion & Parsing:"** Upload PDFs, TXT, or DOCX files (lecture notes, past papers, syllabus).
- **Semantic Vector Search:** Leverages dense vector embeddings for accurate concept retrieval.
- **Context-Grounded Q&A:** Answers queries based strictly on uploaded context to prevent hallucinations.
- **Source Citation:** Highlights exact source files, pages, and text chunks used to generate answers.
- **Interactive Chat Interface:** User-friendly UI with chat history and streaming responses.
- **Context Compression & Re-Ranking:** (Optional) Optimizes context window for better response quality and lower latency.

---

## 🏗️ Architecture Diagram

```mermaid
flowchart TD
    subgraph Ingestion Pipeline
        A[User Uploads Documents] --> B[Text Extraction & Chunking]
        B --> C[Embedding Generation]
        C --> D[(Vector Database: ChromaDB/FAISS)]
    end

    subgraph Query & Retrieval Pipeline
        E[User Query] --> F[Query Embedding]
        F --> G[Similarity Search]
        D --> G
        G --> H[Top-K Relevant Chunks]
    end
masaimind-rag-study-assistant/
├── backend/
│   ├── main.py
│   ├── rag.py
│   ├── ingest.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   └── requirements.txt
├── evaluation/
│   ├── test_questions.csv
│   └── evaluate.py
├── data/
│   └── sample_notes.pdf
├── .env.example
├── README.md
└── docker-compose.yml
    subgraph Response Generation
        H --> I[Prompt Engineering + Context]
        E --> I
        I --> J[LLM API: OpenAI / Gemini / Groq]
        J --> K[Formatted Response + Citations]
    end
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install fastapi uvicorn streamlit langchain langchain-community \
    pypdf sentence-transformers chromadb python-dotenv ragas
OPENAI_API_KEY=your_key_here
PDF → extract text → split into chunks → create embeddings → store in vector DB
POST /upload      → upload and process a PDF
POST /chat        → ask a question and receive an answer
GET /health       → check that the API is running
question,reference_answer,source_file,page_number
What is recursion?,Recursion is when a function calls itself until it reaches a base case.,recursion_notes.pdf,3
What is a Python dictionary?,A dictionary stores key-value pairs.,python_basics.pdf,7
evaluation_data = [
    {
        "user_input": "What is recursion?",
        "response": generated_answer,
        "retrieved_contexts": retrieved_chunks,
        "reference": "Recursion is when a function calls itself until it reaches a base case."
    }
]
