from typing import List, Dict, Any 
from openai import OpenAI

from config.setting import SETTINGS
from config.prompts import build_rag_prompt
from src.generators.base import GeneratorBase

class GroqGenerator(GeneratorBase): 
    def __init__(self): 
        self.client = OpenAI(api_key=SETTINGS.groq_api_key, base_url=SETTINGS.groq_base_url)
        self.model = SETTINGS.groq_model
        self.temperature = SETTINGS.groq_temperature
        
        
    def generate(self, prompt: str) -> str: 
        """single prompt generation (rag model)"""
        response = self.client.chat.completions.create(
            model=self.model, 
            messages=[
                {"role": "system", "content": "you are helpful assistant with funny humor"}, 
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )
        return response.choices[0].message.content
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature
        )
        return response.choices[0].message.content

    def generate_rag(self, context: str, question: str) -> str:
        prompt = build_rag_prompt(context, question)
        return self.generate(prompt)