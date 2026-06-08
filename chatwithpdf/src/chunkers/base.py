"""Abstract base class form chunking Strategies"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Chunker(ABC): 
    """Abstract base class for chunking strategies."""
    @abstractmethod
    def chunk(self, page: List[Dict[str, Any]]) -> List[Dict[str, Any]]: 
        """
        Args: 
            pages: List of page dicts from parser. Each dict has at least: 
                {"text": str, "page": int, "sourec": str}
            
            Returns: 
                List of chunks dicts, each with: 
                {"text": str, "page": int, "source": stre, "chunk_index": int, ...}
        """
        pass
    
    
          