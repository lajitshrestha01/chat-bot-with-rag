"""Recursive character text splitter with metadata preservation"""

from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.chunkers.base import Chunker

class RecursiveTextChunker(Chunker): 
    """
    Recurise character text splitter with metadata preservation. 
    Good gnereal purpose chuker for mixed documents types: 
    """
    
    def __init__(self, chunk_size: int = 1000, 
                 chunk_overlap: int ):
        