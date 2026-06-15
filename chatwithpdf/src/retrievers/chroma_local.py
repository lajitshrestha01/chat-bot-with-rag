from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from config.setting import SETTINGS


class ChromaLocalRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=SETTINGS.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=SETTINGS.chroma_collection_name
        )

    def add_documents(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]]
    ):
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        output = []
        for i in range(len(results["ids"][0])):
            output.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "score": results["distances"][0][i] if results.get("distances") else 0.0
            })
        return output

    def get_collection_count(self) -> int:
        return self.collection.count()
