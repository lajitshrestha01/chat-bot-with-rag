"""Recursive character text splitter with metadata preservation"""

from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chunkers.base import Chunker


class RecursiveTextChunker(Chunker):
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        global_idx = 0
        for page in pages:
            docs = self.splitter.split_documents([
                Document(
                    page_content=page["text"],
                    metadata={"page": page["page"], "source": page["source"]}
                )
            ])
            for doc in docs:
                chunks.append({
                    "text": doc.page_content,
                    "page": doc.metadata["page"],
                    "source": doc.metadata["source"],
                    "chunk_index": global_idx
                })
                global_idx += 1
        return chunks
