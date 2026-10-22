# 🎓 EduRAG: AI-Powered Study Assistant

> A Retrieval-Augmented Generation (RAG) system built as a Capstone Project at Masai School. It enables students to query study materials (PDFs, notes, textbooks) and receive accurate, context-aware answers with exact source citations.

---

## 📌 Problem Statement

Students often struggle to navigate dense textbooks, long lecture notes, and revision materials efficiently. Standard Large Language Models (LLMs) frequently hallucinate or generate overly generic responses without referencing specific course content. 

**EduRAG** addresses this issue by combining document retrieval with generative AI. It anchors LLM responses strictly in the student’s uploaded study materials, delivering verifiable, accurate answers alongside direct page and section references.

---

## ✨ Features

- **Document Ingestion & Parsing:** Upload PDFs, TXT, or DOCX files (lecture notes, past papers, syllabus).
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

    subgraph Response Generation
        H --> I[Prompt Engineering + Context]
        E --> I
        I --> J[LLM API: OpenAI / Gemini / Groq]
        J --> K[Formatted Response + Citations]
    end
