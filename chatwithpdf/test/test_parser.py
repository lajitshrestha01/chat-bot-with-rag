"""
Test the parser.

First Principle: Test each module in isolation before wiring them together.
If parsing is broken, you'll waste hours debugging chunking, embedding, retrieval.
"""

import sys
import os

# Add project root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.parsers.pdf_parser import PDFParser


def test_basic_parse():
    """Test with any PDF you have."""
    parser = PDFParser()
    
    # Put a PDF in data/raw_pdfs/ first
    test_pdf ="data/raw_pdfs/Applied_AI_Engineering_90_Day_Plan.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"ERROR: Place a PDF at {test_pdf} first")
        return
    
    pages = parser.parse_with_metadata("data/raw_pdfs/test.pdf")
    print(f"Title: {pages[0]['document_title']}")
    print(f"Total pages: {pages[0]['total_pages']}")
    print(f"Word count page 1: {pages[0]['word_count']}")

    print(f"✓ Parsed {len(pages)} pages")
    
    for p in pages[:3]:
        preview = p['text'][:150].replace('\n', ' ')
        print(f"  Page {p['page']}: {preview}...")
    
    # Assertions that must pass
    assert len(pages) > 0, "PDF should have at least one page with text"
    assert all('text' in p for p in pages), "Every page must have text"
    assert all('page' in p for p in pages), "Every page must have page number"
    assert all(p['page'] >= 1 for p in pages), "Page numbers start at 1"
    
    print("\n✓ All assertions passed")


def test_empty_pdf():
    """Test that empty/scanned PDFs are handled gracefully."""
    # This test needs a scanned PDF or you can mock it
    print("\nNote: Test with a scanned PDF to see empty page filtering")


if __name__ == "__main__":
    test_basic_parse()