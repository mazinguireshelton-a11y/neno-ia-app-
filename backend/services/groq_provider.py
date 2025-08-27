# backend/services/groq_provider.py (MANTIDO)
import os
import requests
from typing import Dict, List, Generator
import logging
import json

logger = logging.getLogger(__name__)

class GroqProvider:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        self.base_url = "https://api.groq.com/openai/v1"
        
    def get_response(self, messages: List[Dict], stream: bool = False, **kwargs) -> Dict:
        if not self.api_key:
            raise Exception("Groq API key não configurada")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": kwargs.get('temperature', 0.7),
            "max_tokens": kwargs.get('max_tokens', 4000)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=stream,
                timeout=kwargs.get('timeout', 60)
            )
            response.raise_for_status()
            
            if stream:
                return self._handle_stream(response)
            else:
                data = response.json()
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "model": data["model"],
                    "usage": data.get("usage"),
                    "provider": "groq"
                }
                
        except Exception as e:
            logger.error(f"Erro Groq: {e}")
            raise
            
    def _handle_stream(self, response) -> Generator[Dict, None, None]:
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]
                    if data.strip() == '[DONE]':
                        break
                    try:
                        chunk = json.loads(data)
                        if chunk['choices'][0]['delta'].get('content'):
                            yield {
                                "delta": chunk['choices'][0]['delta']['content'],
                                "model": chunk['model'],
                                "provider": "groq"
                            }
                    except json.JSONDecodeError:
                        continue
