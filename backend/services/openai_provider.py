# backend/services/openai_provider.py (MANTIDO)
import openai
import os
from typing import Dict, List, Optional, Generator
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
        
    def get_response(self, messages: List[Dict], stream: bool = False, **kwargs) -> Dict:
        if not self.client:
            raise Exception("OpenAI API key não configurada")
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 4000),
                timeout=kwargs.get('timeout', 60)
            )
            
            if stream:
                return self._handle_stream(response)
            else:
                return {
                    "content": response.choices[0].message.content,
                    "model": response.model,
                    "usage": response.usage.dict() if response.usage else None,
                    "provider": "openai"
                }
                
        except Exception as e:
            logger.error(f"Erro OpenAI: {e}")
            raise
            
    def _handle_stream(self, response) -> Generator[Dict, None, None]:
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                yield {
                    "delta": chunk.choices[0].delta.content,
                    "model": chunk.model,
                    "provider": "openai"
                }
