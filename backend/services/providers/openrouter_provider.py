"""
OpenRouter Provider - Shim correto seguindo interface BaseProvider
"""
from .base import BaseProvider
from typing import Dict, List, Any, Generator
import logging

logger = logging.getLogger(__name__)

class OpenRouterProvider(BaseProvider):
    def __init__(self, api_key: str = "dummy_key", base_url: str = None):
        super().__init__(api_key, base_url)
        self.name = "OpenRouter"
        self.available = True
    
    def setup_client(self):
        self.client = {"type": "openrouter_dummy_client"}
        return True

    def generate(self, messages: List[Dict[str, str]],
                model: str = "openrouter/mistral-7b",
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        
        last_message = messages[-1]["content"] if messages else ""
        response_text = f"Resposta simulada do OpenRouter para: {last_message[:50]}..."
        
        if stream:
            def stream_generator():
                yield {"text": response_text, "ok": True}
            return stream_generator()
        else:
            return self._format_response(
                success=True,
                text=response_text,
                model=model,
                temperature=temperature
            )

    async def agenerate(self, messages: List[Dict[str, str]],
                       model: str = "openrouter/mistral-7b",
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> Dict[str, Any]:
        return self.generate(messages, model, temperature, max_tokens, stream=False)

openrouter_provider = OpenRouterProvider(api_key="dummy_openrouter_key")
