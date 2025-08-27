# backend/services/llm_router.py
import os
import logging
from typing import Dict, Any, List
import requests
import json

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
    def ask(self, message: str, system: str = "", temperature: float = 0.7) -> Dict[str, Any]:
        """
        Roteia a requisição para o melhor provedor LLM disponível
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": message})
        
        # Tenta OpenAI primeiro
        if self.openai_api_key:
            try:
                return self._call_openai(messages, temperature)
            except Exception as e:
                logger.warning(f"OpenAI falhou: {e}")
        
        # Fallback para OpenRouter
        if self.openrouter_api_key:
            try:
                return self._call_openrouter(messages, temperature)
            except Exception as e:
                logger.warning(f"OpenRouter falhou: {e}")
        
        # Fallback para Groq
        if self.groq_api_key:
            try:
                return self._call_groq(messages, temperature)
            except Exception as e:
                logger.warning(f"Groq falhou: {e}")
        
        raise Exception("Nenhum provedor LLM disponível")
    
    def _call_openai(self, messages: List[Dict], temperature: float) -> Dict[str, Any]:
        """Chama OpenAI API"""
        import openai
        client = openai.OpenAI(api_key=self.openai_api_key)
        
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=temperature,
            max_tokens=4000
        )
        
        return {
            "ok": True,
            "text": response.choices[0].message.content,
            "provider": "openai",
            "model": response.model
        }
    
    def _call_openrouter(self, messages: List[Dict], temperature: float) -> Dict[str, Any]:
        """Chama OpenRouter API"""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("BASE_URL", "http://localhost:5000"),
            "X-Title": "NENO IA",
        }
        
        payload = {
            "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        return {
            "ok": True,
            "text": data["choices"][0]["message"]["content"],
            "provider": "openrouter",
            "model": data["model"]
        }
    
    def _call_groq(self, messages: List[Dict], temperature: float) -> Dict[str, Any]:
        """Chama Groq API"""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 4000
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        return {
            "ok": True,
            "text": data["choices"][0]["message"]["content"],
            "provider": "groq",
            "model": data["model"]
        }
