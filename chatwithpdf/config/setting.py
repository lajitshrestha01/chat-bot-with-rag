import os 
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    
    #api key 
    openai_api_key: str = os.getenv("API_KEY") #openai key 
    groq_api_key: str = os.getenv("GROQ_API_KEY") #groq api key
    groq_base_url : str = os.getenv("GROQ_BASE_URL")
    
    #embedding: 
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    #generation
    groq_model: str = "llama-3.1-8b-instant"
    groq_temperature: float = 0.3
    
    #chunking:
    chunk_size: int = 500
    chunk_overlap: int = 50 
    
    #retrieval: 
    top_k: int = 3
    
    #chroma 
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection_name: str = "rag_docs"
    
#singleton instance 
SETTINGS = Settings()

def validate_settings() : 
    """call this at startup, fails fast if key missings"""
    if not SETTINGS.openai_api_key: 
        raise ValueError("Openai key is not found")   

    if not SETTINGS.groq_api_key: 
        raise ValueError("groq api key is not found")
    
