"""
RAG CLI — ingest documents and chat with them.
"""
import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.setting import SETTINGS, validate_settings
from config.prompts import build_rag_prompt
from src.parsers.pdf_parser import PDFParser
from src.chunkers.recursive import RecursiveTextChunker
from src.embedders.openai import OpenAIEmbedder
from src.retrievers.chroma_local import ChromaLocalRetriever
from src.generators.groq import GroqGenerator


class RAGPipeline:
    """Orchestrates the full RAG flow."""
    
    def __init__(self):
        validate_settings()
        
        self.parser = PDFParser()
        self.chunker = RecursiveTextChunker()
        self.embedder = OpenAIEmbedder()
        self.retriever = ChromaLocalRetriever()
        self.generator = GroqGenerator()
    
    def ingest(self, folder_path: str):
        """Ingest all PDFs from a folder."""
        if not os.path.exists(folder_path):
            print(f"❌ Folder not found: {folder_path}")
            return
        
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]
        if not pdf_files:
            print(f"⚠️ No PDFs found in {folder_path}")
            return
        
        print(f"📄 Found {len(pdf_files)} PDF(s). Ingesting...")
        
        for pdf_file in pdf_files:
            file_path = os.path.join(folder_path, pdf_file)
            print(f"  → Processing {pdf_file}...")
            
            # Parse
            pages = self.parser.parse(file_path)
            if not pages:
                print(f"    ⚠️ No text extracted from {pdf_file}")
                continue
            
            # Chunk
            chunks = self.chunker.chunk(pages)
            print(f"    ✂️ {len(chunks)} chunks created")
            
            # Embed
            texts = [c["text"] for c in chunks]
            embeddings = self.embedder.embed_batch(texts)
            
            # Store
            ids = [f"{pdf_file}_{c['chunk_index']}" for c in chunks]
            metadatas = [{
                "page": c["page"],
                "source": c["source"],
                "chunk_index": c["chunk_index"]
            } for c in chunks]
            
            self.retriever.add_documents(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            print(f"    ✅ Stored in Chroma")
        
        total = self.retriever.get_collection_count()
        print(f"\n🎉 Done. Total chunks in DB: {total}")
    
    def query(self, question: str) -> str:
        """Single RAG query."""
        # Embed question
        query_embedding = self.embedder.embed(question)
        
        # Retrieve
        results = self.retriever.search(query_embedding, top_k=SETTINGS.top_k)
        
        if not results:
            return "No relevant documents found."
        
        # Build context
        context = "\n\n---\n\n".join([r["text"] for r in results])
        
        # Generate
        answer = self.generator.generate_rag(context, question)
        return answer
    
    def chat_loop(self):
        """Interactive REPL."""
        print("\n🤖 RAG Chatbot ready!")
        print(f"   Collection: {SETTINGS.chroma_collection_name}")
        print(f"   Chunks in DB: {self.retriever.get_collection_count()}")
        print("   Type 'quit' or 'exit' to stop.\n")
        
        while True:
            try:
                question = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
            
            if not question:
                continue
            
            if question.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break
            
            print("🤖 Thinking...")
            answer = self.query(question)
            print(f"Bot: {answer}\n")


def main():
    parser = argparse.ArgumentParser(description="RAG CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest PDFs from folder")
    ingest_parser.add_argument("--folder", default="./docs", help="Path to PDF folder")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument("--query", help="Single query mode (no REPL)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize pipeline
    pipeline = RAGPipeline()
    
    if args.command == "ingest":
        pipeline.ingest(args.folder)
    
    elif args.command == "chat":
        if args.query:
            # Single shot
            answer = pipeline.query(args.query)
            print(answer)
        else:
            # REPL
            pipeline.chat_loop()


if __name__ == "__main__":
    main()