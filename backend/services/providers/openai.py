import openai
from typing import Dict, List, Any, Generator
from .base import BaseProvider
import logging

logger = logging.getLogger(__name__)

class OpenAIProvider(BaseProvider):
    """Provider para OpenAI API"""
    
    def setup_client(self):
        """Configura cliente OpenAI"""
        try:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            logger.info("Cliente OpenAI configurado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao configurar OpenAI: {str(e)}")
            raise
    
    def generate(self, messages: List[Dict[str, str]], 
                model: str = "gpt-3.5-turbo", 
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        """
        Implementação específica para OpenAI
        """
        try:
            if stream:
                return self._generate_stream(messages, model, temperature, max_tokens)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            
            text = response.choices[0].message.content
            return self._format_response(True, text=text)
            
        except Exception as e:
            logger.error(f"Erro OpenAI: {str(e)}")
            return self._format_response(False, error=str(e))
    
    def _generate_stream(self, messages: List[Dict[str, str]], 
                        model: str, 
                        temperature: float,
                        max_tokens: int) -> Generator[Dict[str, Any], None, None]:
        """Gera resposta em streaming"""
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
            logger.error(f"Erro streaming OpenAI: {str(e)}")
            yield self._format_response(False, error=str(e))
    
    async def agenerate(self, messages: List[Dict[str, str]], 
                       model: str = "gpt-3.5-turbo", 
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> Dict[str, Any]:
        """Versão assíncrona para OpenAI"""
        try:
            from openai import AsyncOpenAI
            
            aclient = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
            response = await aclient.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            text = response.choices[0].message.content
            return self._format_response(True, text=text)
            
        except Exception as e:
            logger.error(f"Erro assíncrono OpenAI: {str(e)}")
            return self._format_response(False, error=str(e))
