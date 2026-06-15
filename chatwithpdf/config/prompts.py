from typing import List, Dict


def build_rag_prompt(context: str, question: str) -> str:
    return f"""You are a helpful assistant. Answer the question based on the provided context.

Context:
{context}

Question:
{question}

Answer the question concisely using only the information from the context. If the context doesn't contain the answer, say "I don't have enough information to answer that."""
