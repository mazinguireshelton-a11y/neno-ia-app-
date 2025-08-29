import groq
from typing import Dict, List, Any, Generator
from .base import BaseProvider
import logging

logger = logging.getLogger(__name__)

class GroqProvider(BaseProvider):
    """Provider para Groq API"""
    
    def setup_client(self):
        """Configura cliente Groq"""
        try:
            self.client = groq.Client(api_key=self.api_key)
            logger.info("Cliente Groq configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar Groq: {str(e)}")
            raise
    
    def generate(self, messages: List[Dict[str, str]], 
                model: str = "llama3-8b-8192", 
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        """
        Implementação específica para Groq
        """
        try:
            if stream:
                return self._generate_stream(messages, model, temperature, max_tokens)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            text = response.choices[0].message.content
            return self._format_response(True, text=text)
            
        except Exception as e:
            logger.error(f"Erro Groq: {str(e)}")
            return self._format_response(False, error=str(e))
    
    def _generate_stream(self, messages: List[Dict[str, str]], 
                        model: str, 
                        temperature: float,
                        max_tokens: int) -> Generator[Dict[str, Any], None, None]:
        """Gera resposta em streaming para Groq"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield self._format_response(
                        True, 
                        text=chunk.choices[0].delta.content,
                        finished=False
                    )
            
            yield self._format_response(True, text="", finished=True)
            
        except Exception as e:
            logger.error(f"Erro streaming Groq: {str(e)}")
            yield self._format_response(False, error=str(e))
    
    async def agenerate(self, messages: List[Dict[str, str]], 
                       model: str = "llama3-8b-8192", 
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> Dict[str, Any]:
        """Versão assíncrona para Groq"""
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            text = response.choices[0].message.content
            return self._format_response(True, text=text)
            
        except Exception as e:
            logger.error(f"Erro assíncrono Groq: {str(e)}")
            return self._format_response(False, error=str(e))
