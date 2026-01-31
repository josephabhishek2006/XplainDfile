from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from app.config import (
    LLM_MODEL_NAME,
    SIMILARITY_THRESHOLD
)
from app.state import app_state


llm = ChatGroq(
    model=LLM_MODEL_NAME,
    temperature=0.3
)


def answer_question(question: str) -> dict:
    if not app_state.retriever:
        return {
            "answer": "No file is uploaded yet.",
            "source": "system"
        }

    docs = app_state.retriever.invoke(question)

    # No retrieved docs → fallback
    if not docs:
        return llm_fallback(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    file_prompt = ChatPromptTemplate.from_template(
        """Answer the question using ONLY the context below.
If the context does not contain the answer, reply exactly with:
"The context does not contain the answer."

Context:
{context}

Question:
{question}
"""
    )

    chain = file_prompt | llm | StrOutputParser()
    file_answer = chain.invoke({
        "context": context,
        "question": question
    })

    # 🔑 CRITICAL FALLBACK CHECK
    if "does not contain the answer" in file_answer.lower():
        return llm_fallback(question)

    return {
        "answer": file_answer,
        "source": "file"
    }

def llm_fallback(question: str) -> dict:
    prompt = ChatPromptTemplate.from_template(
        """The uploaded file does not contain the answer.
Based on general knowledge, answer the question clearly.

Question:
{question}
"""
    )

    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"question": question})

    return {
        "answer": answer,
        "source": "llm"
    }
