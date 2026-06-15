from typing import List
from openai import OpenAI

from config.setting import SETTINGS
from src.embedders.base import EmbeddeerBase


class OpenAIEmbedder(EmbeddeerBase):
    def __init__(self):
        self.client = OpenAI(api_key=SETTINGS.openai_api_key)
        self.model = SETTINGS.embedding_model

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]
