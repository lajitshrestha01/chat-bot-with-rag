from abc import ABC, abstractmethod

from typing import List, Dict, Any


class GeneratorBase(ABC): 
    @abstractmethod
    def generate(self, prompt: str) -> str: 
        """generate text from a sinlge prompt string"""
        pass
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str: 
        """ggenerate from a lsit of messages (for multi-trun)"""
        pass