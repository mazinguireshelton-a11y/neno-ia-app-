# backend/services/openrouter_provider.py (NOVO - IMPLEMENTAÇÃO COMPLETA)
import os
import requests
from typing import Dict, List, Generator
import logging
import json

logger = logging.getLogger(__name__)

class OpenRouterProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.base_url = "https://openrouter.ai/api/v1"
        self.app_name = os.getenv("APP_NAME", "NENO IA")
        self.app_url = os.getenv("APP_URL", "https://github.com/neno-ia")
        
    def get_response(self, messages: List[Dict], stream: bool = False, **kwargs) -> Dict:
        if not self.api_key:
            raise Exception("OpenRouter API key não configurada")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.app_url,
            "X-Title": self.app_name
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
                    "provider": "openrouter"
                }
                
        except Exception as e:
            logger.error(f"Erro OpenRouter: {e}")
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
                                "provider": "openrouter"
                            }
                    except json.JSONDecodeError:
                        continue
    
    def get_available_models(self) -> List[Dict]:
        """Obtém lista de modelos disponíveis no OpenRouter"""
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Erro ao obter modelos OpenRouter: {e}")
            return []
