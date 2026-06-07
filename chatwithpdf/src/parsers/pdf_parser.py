"""
PDF parser using PyMUPDF (fitz)

first principal: pdf are not text files with pages. They are visual layouts. Text extraction is reconstruction, not reading, PyMuPDF is the best open-source reconstructor. 
key insight: "parse" means "turn visual pdf into struct ured text we can chunk and embed.
"""

import fitz
from typing import List, Dict
from src.parsers.base import DocumentParser


class PDFParser(DocumentParser):
    """
     Parse PDFs with PyMupdf. 

     Why pymupdf over pdypdf2, pdfplumber, etc? 
     -Faster(c++ backend, not pure python)
     -Better at complex layout (columns, tables, headers)
     -hanldes more pdf variants
    """

    def supports(self, file_path: str) -> bool:
        """
         Check if the file is pdf. 
         simple, but critical. In multi-parser system, thos is the routing signal. 
        """

        return file_path.lower().endswith('.pdf')

    def parse(self, file_path: str) -> List[Dict]:
        """
        Extract text form pdf, page by page. 

        First principal: Perserve Structure. 
        A pdf is a sequence of pages. We return a sequence of page objects. The chunker will decicde how to split. the parser's  job is not to chunk. 
        Separation of concerns: parser extracts, chunker splits, embedder encodes
        """

        doc = fitz.open(file_path)
        pages = []

        for page_num in range(len(doc)):
            page = doc[page_num]

            # get_text() recontrut reading order form visual layout
            # This is htehar part of pymupdf sovles

            text = page.get_text()

            # filter: skip emtpy pages(common in scanned pdf, intor blanks)
            # why? empty pages creates empty chunks, empty chunks waste storage and retrieval time

            if not text.strip():
                continue
            
            #Structure: one dict per page. 
            #why dict, not tuple? Extensible. Add metadate later without breaking chunker. 
            
            pages.append({
                "text": text, 
                "page": page_num + 1, 
                "source": file_path
            })
            
        doc.close()
        
        return pages