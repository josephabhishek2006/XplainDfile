XplainDfile

XplainDfile is a document-based question answering web application.
Users can upload a PDF and ask questions about its content. The system first tries to answer strictly from the uploaded document, and only if the document does not contain the answer, it falls back to a general language model.

The main goal of this project was to understand and implement a Retrieval Augmented Generation (RAG) pipeline from scratch rather than relying on black-box tools.

What this project does

Accepts a PDF upload from the user

Extracts readable text from the PDF

Splits the text into manageable chunks

Converts chunks into vector embeddings

Stores embeddings in a Pinecone vector database

On every user question:

Retrieves the most relevant chunks using similarity search

Forces the model to answer only from the retrieved context

Falls back to a general LLM response if the document does not contain the answer

Clearly shows whether the response came from the file or the LLM

Why XplainDfile

Most document chat systems mix document content and model knowledge, which can lead to hallucinations.
XplainDfile was designed to:

Enforce document-grounded answers

Detect when a document does not contain the answer

Transparently fall back to general knowledge

Keep the architecture simple and explainable

This project focuses more on correctness and clarity than on UI complexity.

Tech stack
Backend

Python

FastAPI

LangChain

Pinecone (vector database)

HuggingFace sentence-transformers

Groq LLM API

PyPDF for PDF parsing

Frontend

HTML

CSS

Vanilla JavaScript (no frameworks)

Project structure
XplainDfile/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── rag.py
│   │   ├── upload.py
│   │   ├── vectorstore.py
│   │   ├── state.py
│   │   ├── schemas.py
│   │   └── config.py
│   ├── requirements.txt
│   └── .env (not committed)
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
├── README.md

Backend architecture overview

main.py
Entry point of the FastAPI server. Defines API routes for uploading files, chatting, resetting the session, and serves the frontend.

upload.py
Handles PDF validation and text extraction. Rejects unsupported or empty PDFs.

vectorstore.py
Splits text into chunks, generates embeddings, and manages Pinecone index creation and deletion.

rag.py
Core RAG logic. Retrieves relevant chunks, enforces context-only answering, and handles fallback to the LLM.

state.py
Maintains in-memory session state (current document, retriever, index name).

schemas.py
Defines request and response models using Pydantic.

config.py
Centralized configuration for API keys, model names, and retrieval parameters.

Frontend overview

The frontend is intentionally minimal:

PDF-only upload

Chat-style interface

Clear indicator showing whether an answer came from:

the uploaded document

or the language model

Reset button to clear the session and vector index

The frontend communicates with the backend using simple fetch calls.

How to run locally
1. Clone the repository
git clone https://github.com/your-username/XplainDfile.git
cd XplainDfile

2. Create and activate a virtual environment
python -m venv xplaindfile-env
source xplaindfile-env/bin/activate   # Linux/Mac
xplaindfile-env\Scripts\activate      # Windows

3. Install dependencies
pip install -r backend/requirements.txt

4. Set environment variables

Create a .env file inside backend/:

GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key

5. Run the backend
uvicorn app.main:app --reload

6. Open in browser
http://localhost:8000

Key learnings

How RAG works end-to-end

Importance of chunking and embedding choice

Practical use of vector similarity search

Preventing hallucinations in document QA

Structuring a clean FastAPI backend

Coordinating frontend and backend in an AI application

Future improvements

Multiple document support

Persistent chat history

More document formats

User authentication

Citation highlighting in responses
