from abc import ABC, abstractmethod
from typing import List

class EmbeddeerBase(ABC): 
    @abstractmethod
    def embed(self, text: str) -> List[float]: 
        """Embed a single text string, returns float vector."""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]: 
        """Embed multiple texts efficiently. Returns list of vectors. """
        pass
    
    