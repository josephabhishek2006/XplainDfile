XplainDfile

XplainDfile is a document-based question answering web application.
Users can upload a PDF file and ask questions about its content. The system first tries to answer strictly from the uploaded document. If the document does not contain the answer, it transparently falls back to a general language model.

The project was built to understand and implement a Retrieval Augmented Generation (RAG) pipeline end-to-end, with clear separation between document-grounded answers and model-based answers.

What the application does

Accepts a PDF file from the user

Extracts readable text from the document

Splits the text into smaller chunks

Converts chunks into vector embeddings

Stores embeddings in a vector database

Retrieves relevant chunks for each question

Forces the model to answer only from retrieved context

Falls back to a general LLM when the document does not contain the answer

Clearly shows the source of each answer

Why this project

Many document chat systems mix document content and model knowledge, which can lead to hallucinated or misleading answers.
XplainDfile was designed with the following goals:

Enforce document-grounded responses

Detect when a document does not contain the answer

Keep the system behavior transparent and explainable

Understand how RAG systems work internally instead of relying on black-box tools

Tech stack

Backend

Python

FastAPI

LangChain

Pinecone (vector database)

HuggingFace sentence-transformers

Groq LLM API

PyPDF

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
│   └── .env            (not committed)
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
│
└── README.md

Backend architecture overview

main.py
Entry point of the FastAPI application. Defines API routes for file upload, chat, session reset, and also serves the frontend.

upload.py
Handles PDF validation and text extraction. Rejects unsupported file formats and empty PDFs.

vectorstore.py
Splits extracted text into chunks, generates embeddings, and manages Pinecone index creation and deletion.

rag.py
Implements the core RAG logic. Retrieves relevant chunks, enforces context-only answering, and falls back to the language model when required.

state.py
Maintains in-memory session state such as the active document, retriever, and vector index name.

schemas.py
Defines request and response models using Pydantic.

config.py
Centralized configuration for API keys, model selection, and retrieval parameters.

Frontend overview

The frontend is intentionally minimal and framework-free:

PDF-only file upload

Chat-style interface

Clear indicator showing whether an answer came from the document or the language model

Reset button to clear the current session

The frontend communicates with the backend using simple fetch API calls.

How the system works (high level flow)

User uploads a PDF

Text is extracted and split into chunks

Chunks are embedded and stored in Pinecone

User asks a question

Relevant chunks are retrieved using similarity search

The model is instructed to answer only from the retrieved context

If context is insufficient, the system falls back to the LLM

How to run locally
Clone the repository
git clone https://github.com/your-username/XplainDfile.git
cd XplainDfile

Create and activate a virtual environment
python -m venv xplaindfile-env


Windows:

xplaindfile-env\Scripts\activate


Linux / macOS:

source xplaindfile-env/bin/activate

Install dependencies
pip install -r backend/requirements.txt

Set environment variables

Create a .env file inside the backend/ directory:

GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key

Run the backend server
uvicorn app.main:app --reload

Open in browser
http://localhost:8000

Key learnings

End-to-end implementation of a RAG system

Practical use of vector databases for semantic search

Importance of chunking and retrieval strategy

Prompt control to reduce hallucinations

Clean FastAPI backend structuring

Frontend and backend integration for AI applications

Future improvements

Support for multiple documents

Persistent chat history

Additional document formats

Citation highlighting

User authentication
