from fastapi import UploadFile, HTTPException
from pypdf import PdfReader


def extract_text(file: UploadFile) -> str:
    # 1️⃣ Enforce PDF only
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    try:
        reader = PdfReader(file.file)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF file"
        )

    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    final_text = "\n".join(text).strip()

    # 2️⃣ Guard against empty PDFs
    if not final_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the PDF"
        )

    return final_text
