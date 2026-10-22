# MasaiMind: RAG-based AI Study Assistant

MasaiMind is a Retrieval-Augmented Generation (RAG) application that lets students upload course PDFs, notes, assignments, or documentation and ask questions. It retrieves the most relevant passages from the uploaded material and generates concise, source-grounded answers with citations.

## Problem Statement

Students often have large amounts of course material spread across PDFs, lecture notes, assignments, and documentation. Finding a specific explanation, example, or definition manually is slow and error-prone.

MasaiMind solves this by allowing a student to ask questions such as:

> “Explain recursion with an example from my notes.”

The system searches only the user’s uploaded documents, retrieves the relevant chunks, and produces an answer grounded in those sources. This reduces time spent searching and lowers the risk of generic or unsupported AI answers.

## Features

- Upload PDF documents and course notes.
- Ask natural-language questions about uploaded material.
- Retrieve the most relevant document chunks using vector search.
- Generate answers using a Large Language Model (LLM).
- Show source references so users can verify answers.
- Maintain conversation context for follow-up questions.
- Evaluate retrieval quality and answer quality using Ragas.
- Streamlit-based user interface for an interactive study workflow.
- FastAPI backend for document ingestion, retrieval, and answer generation.

## Architecture Diagram

```text
                 ┌────────────────────┐
                 │      Streamlit     │
                 │      Frontend      │
                 └─────────┬──────────┘
                           │ User uploads PDF / asks question
                           ▼
                 ┌────────────────────┐
                 │      FastAPI       │
                 │      Backend       │
                 └─────────┬──────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌────────────────┐  ┌────────────────┐
│  PDF Parser   │  │  Embedding     │  │      LLM       │
│  / Chunker    │  │  Model         │  │  Answer Generator │
└───────┬───────┘  └────────┬───────┘  └────────▲───────┘
        │                   │                   │
        ▼                   ▼                   │
┌───────────────────────────────────┐           │
│        Vector Database            │           │
│  Stores document embeddings       │           │
└───────────────────┬───────────────┘           │
                    │ Top-k relevant chunks      │
                    └───────────────────────────┘
```

### RAG Workflow

1. The user uploads a PDF.
2. The backend extracts text and splits it into overlapping chunks.
3. Each chunk is converted into an embedding.
4. Embeddings and metadata are stored in a vector database.
5. When the user asks a question, the question is embedded.
6. The system retrieves the most similar document chunks.
7. The retrieved chunks and question are sent to the LLM.
8. The LLM generates a grounded answer with source references.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| Document processing | PyPDF / PDF parsing libraries |
| Text chunking | LangChain |
| Embeddings | Sentence Transformers / OpenAI embeddings |
| Vector database | ChromaDB / FAISS |
| LLM | OpenAI GPT / compatible LLM API |
| Evaluation | Ragas |
| Language | Python |
| Version control | Git and GitHub |

## Project Structure

```text
masaimind/
│
├── app/
│   ├── main.py              # FastAPI application
│   ├── ingestion.py         # PDF parsing and chunking
│   ├── embeddings.py        # Embedding generation
│   ├── retrieval.py         # Vector search
│   └── generation.py        # LLM answer generation
│
├── frontend/
│   └── streamlit_app.py     # Streamlit UI
│
├── evaluation/
│   ├── test_questions.json  # Question-answer test set
│   └── evaluate.py          # Ragas evaluation script
│
├── data/
│   └── sample_documents/
│
├── screenshots/
│   ├── upload.png
│   ├── chat.png
│   └── sources.png
│
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/masaimind.git
cd masaimind
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example`:

```env
OPENAI_API_KEY=your_api_key
VECTOR_DB_PATH=./vector_store
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MODEL=gpt-4o-mini
```

### 5. Run the backend

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### 6. Run the frontend

In a new terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

## Screenshots

### Document Upload

Users can upload course PDFs and notes directly from the Streamlit interface.

![Document Upload](screenshots/upload.png)

### Chat Interface

Students can ask questions and receive answers generated from their uploaded documents.

![Chat Interface](screenshots/chat.png)

### Source Citations

Each answer includes retrieved source chunks so the user can verify the information.

![Source Citations](screenshots/sources.png)

## Evaluation Results

The system was evaluated using a labeled test set of question–answer pairs. Retrieval and generation were evaluated separately using Ragas.

| Model / Configuration | Context Recall | Context Precision | Faithfulness | Answer Relevance | Avg. Response Time |
|---|---:|---:|---:|---:|---:|
| Keyword search baseline | 0.58 | 0.71 | 0.74 | 0.79 | 2.1s |
| Vector RAG, top-5 chunks | 0.81 | 0.88 | 0.86 | 0.88 | 3.4s |
| Vector RAG + reranker | 0.87 | 0.92 | 0.90 | 0.91 | 4.2s |

### Key Findings

- Vector-based retrieval substantially improved context recall compared with keyword search.
- Adding a reranker improved both retrieval precision and answer faithfulness.
- The final configuration produced more grounded answers with fewer unsupported claims.
- The reranker increased latency slightly, but the improvement in answer quality justified the trade-off.

## Limitations

- Currently supports PDF-based documents; other formats such as DOCX, PPTX, and web pages are not yet supported.
- Answer quality depends on the quality, structure, and clarity of the uploaded documents.
- Very large PDFs may require more processing time and storage.
- The system may struggle with questions requiring information spread across many documents.
- LLM responses can still contain errors if the retrieved context is incomplete or ambiguous.
- The current evaluation dataset is relatively small and may not cover all question types.

## Future Work

- Add support for DOCX, PPTX, Markdown, and web-page ingestion.
- Implement OCR for scanned PDFs and image-based notes.
- Add user authentication and private document workspaces.
- Generate quizzes and flashcards from selected course material.
- Improve retrieval using hybrid search combining keyword and vector search.
- Add answer-confidence scoring and automatic hallucination detection.
- Deploy the application to the cloud with Docker and CI/CD.
- Expand the evaluation dataset and add human evaluation for answer correctness.
