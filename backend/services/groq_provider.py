"""
Groq Provider - Shim correto seguindo interface BaseProvider
"""
from .base import BaseProvider
from typing import Dict, List, Any, Generator
import logging

logger = logging.getLogger(__name__)

class GroqProvider(BaseProvider):
    def __init__(self, api_key: str = "dummy_key", base_url: str = None):
        super().__init__(api_key, base_url)
        self.name = "Groq"
        self.available = True
    
    def setup_client(self):
        self.client = {"type": "groq_dummy_client"}
        return True

    def generate(self, messages: List[Dict[str, str]],
                model: str = "groq/llama3",
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        
        last_message = messages[-1]["content"] if messages else ""
        response_text = f"Resposta ultrarrápida do Groq para: {last_message[:50]}..."
        
        if stream:
            def stream_generator():
                yield {"text": response_text, "ok": True}
            return stream_generator()
        else:
            return self._format_response(
                success=True,
                text=response_text,
                model=model,
                temperature=temperature,
                speed="0.2s"
            )

    async def agenerate(self, messages: List[Dict[str, str]],
                       model: str = "groq/llama3",
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> Dict[str, Any]:
        return self.generate(messages, model, temperature, max_tokens, stream=False)

groq_provider = GroqProvider(api_key="dummy_groq_key")
