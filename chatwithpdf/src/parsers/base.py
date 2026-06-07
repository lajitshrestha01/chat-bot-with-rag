"""
    Base parser module. 
    
    first principal: All document types (pdf, docs, html) should share the same interfece. This let usswap parseres without breaking chunkers, embeders, or anything downstream. 
    design pattern: Abstract Base Class(ABC). 
    Forces every parser to implement the same methods. NO "oops, forgot to add parse().
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class DocumentParser(ABC): 
    """
    Abstract base for all document parsers. 
    
    Why ABC? 
    -you cannot instantiate this directly. 
    -Subclasses must implement these methods, or python throws an error. 
    -Gurantees consistency across pdf, docs, html parsers. 
    
    """
    @abstractmethod
    def parse(self, file_path: str) -> List[Dict]: 
        """ 
        Parse a document into a list of pages. 
        
        Return list of dicts, each representing one page: 
        [
            {
                "text": str,
                "page": int, 
                "source": int
            }, 
        ]
        Why page-level? 
        -chunking needs to know where page boundaries are. 
        -Citations need page numbers. 
        -Cross-page chunks are confusing
        """
        pass
    
    @abstractmethod
    def supports(self, file_path: str) -> bool: 
        """
        Check if this parser can handle the given file
        
        why? 
        -In production you recieve unknown fiels. 
        -Router pucks the right parser automatically. 
        -Prevents "why did my pdf parser crash on .jph? --bugs??
        """
        pass
        

    