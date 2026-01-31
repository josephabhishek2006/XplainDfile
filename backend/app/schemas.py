from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    source: str  # "file" or "llm"

class UploadResponse(BaseModel):
    message: str

class ResetResponse(BaseModel):
    message: str
