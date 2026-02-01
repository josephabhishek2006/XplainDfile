# XplainDfile

XplainDfile is a document-based question answering web application. Users can upload a PDF file and ask questions about its content. The system first attempts to answer strictly from the uploaded document. If the document does not contain the answer, it transparently falls back to a general language model.

This project was built to understand and implement a Retrieval Augmented Generation (RAG) system from scratch, with explicit control over retrieval, prompting, and fallback behavior.

<img width="1887" height="849" alt="image" src="https://github.com/user-attachments/assets/24724671-a335-46f8-a6c0-41ba5b0a7afc" />

---

## Key Features

* PDF-only document upload
* Automatic text extraction from uploaded files
* Chunking and embedding of document text
* Semantic search using a vector database
* Context-restricted answering to avoid hallucinations
* Automatic fallback to LLM when the document lacks the answer
* Clear indication of answer source (document vs model)

---

## Motivation

Many document chat systems mix document content and model knowledge, which can lead to hallucinated or misleading responses. XplainDfile was designed to solve this by:

* Enforcing document-grounded answers whenever possible
* Explicitly detecting when the document does not contain the answer
* Making the system behavior transparent and explainable
* Understanding the internals of RAG instead of relying on black-box tools

---

## Tech Stack

### Backend

* Python
* FastAPI
* LangChain
* Pinecone (vector database)
* HuggingFace sentence-transformers
* Groq LLM API
* PyPDF

### Frontend

* HTML
* CSS
* Vanilla JavaScript (no frameworks)

---

## Backend Design Overview

* **main.py**
  Acts as the entry point for the FastAPI server. Defines API routes for uploading documents, chatting, resetting sessions, and serves the frontend.

* **upload.py**
  Handles PDF validation and text extraction. Ensures only readable PDF files are accepted.

* **vectorstore.py**
  Splits extracted text into chunks, generates embeddings, and manages vector index creation and deletion in Pinecone.

* **rag.py**
  Implements the core RAG logic. Retrieves relevant chunks, enforces context-only answering, and handles fallback to the language model when required.

* **state.py**
  Maintains in-memory session state, including the active document, retriever, and index name.

* **schemas.py**
  Defines request and response models using Pydantic.

* **config.py**
  Centralized configuration for API keys, model selection, and retrieval parameters.

---

## Frontend Overview

The frontend is intentionally minimal and framework-free:

* PDF upload interface
* Chat-style user interaction
* Visual indicator showing answer source
* Reset option to clear the active session

All communication with the backend is handled using standard `fetch` API calls.

---

## High-Level Workflow

1. User uploads a PDF document
2. Text is extracted and split into chunks
3. Chunks are embedded and stored in the vector database
4. User asks a question
5. Relevant chunks are retrieved using similarity search
6. The model answers strictly using retrieved context
7. If context is insufficient, the system falls back to the LLM

---

## Running the Project Locally

### Clone the repository

```bash
git clone https://github.com/your-username/XplainDfile.git
cd XplainDfile
```

### Create and activate a virtual environment

```bash
python -m venv xplaindfile-env
```

**Windows**

```bash
xplaindfile-env\Scripts\activate
```

**Linux / macOS**

```bash
source xplaindfile-env/bin/activate
```

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Configure environment variables

Create a `.env` file inside the `backend` directory:

```
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### Start the server

```bash
uvicorn app.main:app --reload
```

### Open in browser

```
http://localhost:8000
```

---

## Learnings and Takeaways

* Practical understanding of Retrieval Augmented Generation
* Importance of chunking and embedding strategies
* Real-world use of vector databases for semantic search
* Prompt control to reduce hallucinations
* Clean backend structuring using FastAPI
* Frontend-backend coordination in AI applications

---

## Future Improvements

* Support for multiple document uploads
* Persistent chat history
* Additional document formats
* Source citation highlighting
* User authentication

---


