from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import pathlib

from app.schemas import UploadResponse, ResetResponse, ChatRequest, ChatResponse
from app.state import app_state
from app.upload import extract_text
from app.vectorstore import chunk_text, create_pinecone_index
from app.rag import answer_question
from pinecone import Pinecone

app = FastAPI(
    title="XplainDfile Backend",
    description="Backend API for document-grounded chat with fallback",
    version="1.0.0"
)

# ---------------- API ROUTES ----------------

@app.get("/api/health")
def health_check():
    return {"status": "XplainDfile backend running"}

@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if app_state.raw_text is not None:
        return UploadResponse(
            message="A file is already uploaded. Please reset before uploading a new file."
        )

    extracted_text = extract_text(file)
    if not extracted_text:
        raise HTTPException(status_code=400, detail="No text extracted")

    app_state.raw_text = extracted_text
    documents = chunk_text(extracted_text)
    create_pinecone_index(documents)

    return UploadResponse(message="File uploaded, indexed, and ready for chat.")

@app.post("/reset", response_model=ResetResponse)
def reset_session():
    pc = Pinecone()

    if app_state.pinecone_index_name:
        pc.delete_index(app_state.pinecone_index_name)

    app_state.raw_text = None
    app_state.retriever = None
    app_state.chat_memory = None
    app_state.pinecone_index_name = None

    return ResetResponse(message="Session reset successfully.")

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = answer_question(req.question)
    return ChatResponse(
        answer=result["answer"],
        source=result["source"]
    )


# ---------------- FRONTEND (LAST) ----------------

BASE_DIR = pathlib.Path(__file__).resolve().parents[2]
frontend_dir = BASE_DIR / "frontend"

app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
