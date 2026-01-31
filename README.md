XplainDfile

XplainDfile is a document-based question answering web application.
The idea behind this project is simple: upload a PDF, and then ask questions about its content. The system first tries to answer strictly from the uploaded document, and only if the document does not contain the answer, it falls back to a general language model.

This project was built to understand how Retrieval Augmented Generation (RAG) works end-to-end, including document parsing, vector storage, semantic retrieval, and controlled LLM usage.

What the project does

The user uploads a PDF file.

The backend extracts readable text from the PDF.

The text is split into smaller chunks.

Each chunk is converted into embeddings using a sentence-transformer model.

The embeddings are stored in a Pinecone vector database.

When the user asks a question:

Relevant chunks are retrieved using similarity search.

The model is instructed to answer only from the retrieved context.

If the context does not contain the answer, the system falls back to a general LLM response.

The UI clearly shows whether the answer came from the file or from the LLM.

Why this project exists

Many document chat systems blindly mix document content and model knowledge.
In this project, special care is taken to:

Prevent hallucinations when the answer is not in the file

Clearly separate “answer from document” vs “answer from model”

Keep the system state simple and explicit

Understand the full RAG pipeline instead of using black-box tools

Tech stack used

Backend:

Python

FastAPI

LangChain

Pinecone (vector database)

HuggingFace sentence-transformers

Groq LLM API

Frontend:

HTML

CSS

Vanilla JavaScript (no frameworks)

Other:

PDF parsing using PyPDF

Environment-based configuration using python-dotenv

Project structure (high level)

backend/
Contains the FastAPI server, RAG logic, vector store handling, and session state.

frontend/
A simple chat interface that allows PDF upload, chatting, and session reset.

xplaindfile-env/
Python virtual environment used during development.

Backend design overview

The backend is modular and intentionally split into small files:

main.py
Entry point of the FastAPI application. Defines API routes for upload, chat, reset, and health check. Also serves the frontend.

upload.py
Responsible for validating and extracting text from PDF files.

vectorstore.py
Handles text chunking, embedding generation, and Pinecone index creation.

rag.py
Implements the core RAG logic:

Retrieve relevant chunks

Force the model to answer only from context

Fall back to LLM if context is insufficient

state.py
Holds in-memory session state such as current document, retriever, and index name.

schemas.py
Defines request and response models using Pydantic.

config.py
Central place for API keys, model names, and tuning parameters.

Frontend design overview

The frontend is intentionally kept simple:

Upload a PDF (PDF-only enforced)

Chat interface similar to a messaging app

Shows whether an answer came from:

the uploaded file

or the language model

Reset button clears the session and deletes the vector index

The frontend communicates with the backend using plain fetch API calls.

How to run the project locally

Clone the repository

Create and activate a Python virtual environment

Install dependencies:

pip install -r requirements.txt


Create a .env file in the backend directory with:

GROQ_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here


Start the backend server:

uvicorn app.main:app --reload


Open the browser at:

http://localhost:8000

Key learnings from this project

How RAG actually works beyond tutorials

Why chunking strategy matters

How vector similarity search influences answer quality

How to control LLM behavior using prompt constraints

How to avoid hallucinations in document-based QA systems

How frontend and backend coordinate in a full-stack ML app

Future improvements

Support for multiple document uploads

Persistent chat memory across sessions

Support for more document formats

Authentication and user-level sessions

Better relevance ranking and citations

