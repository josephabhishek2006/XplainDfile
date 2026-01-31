import os
from dotenv import load_dotenv

load_dotenv()

# ======================
# API KEYS
# ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

if not PINECONE_API_KEY:
    raise RuntimeError("PINECONE_API_KEY not set")

# ======================
# MODEL CONFIG
# ======================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"

# ======================
# RAG CONFIG
# ======================
SIMILARITY_THRESHOLD = 0.75
TOP_K = 3
MEMORY_WINDOW = 5
