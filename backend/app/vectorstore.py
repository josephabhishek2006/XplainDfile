import uuid
from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from app.state import app_state
from app.config import EMBEDDING_MODEL_NAME, TOP_K


def chunk_text(raw_text: str) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    documents = splitter.create_documents([raw_text])
    return documents


def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME
    )


def create_pinecone_index(documents: List[Document]):
    pc = Pinecone()

    # 🔴 IMPORTANT: delete old index if it exists
    if app_state.pinecone_index_name:
        try:
            pc.delete_index(app_state.pinecone_index_name)
        except Exception:
            pass

    index_name = f"xplaindfile-{uuid.uuid4().hex[:8]}"

    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    embeddings = get_embedding_model()

    vectorstore = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=index_name
    )

    app_state.pinecone_index_name = index_name
    app_state.retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )
