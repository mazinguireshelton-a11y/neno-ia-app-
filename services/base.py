from abc import ABC, abstractmethod
from typing import Dict, List, Any, Generator
import logging

logger = logging.getLogger(__name__)

class BaseProvider(ABC):
    """Classe base abstrata para todos os providers LLM"""
    
    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url
        self.client = None
        self.setup_client()
    
    @abstractmethod
    def setup_client(self):
        """Configura o cliente específico do provider"""
        pass
    
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], 
                model: str, 
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        """
        Gera resposta para mensagens dadas
        
        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "..."}]
            model: Modelo a ser usado
            temperature: Criatividade da resposta
            max_tokens: Tokens máximos de resposta
            stream: Se deve retornar streaming
        
        Returns:
            Dict com texto completo ou generator para streaming
        """
        pass
    
    @abstractmethod
    async def agenerate(self, messages: List[Dict[str, str]], 
                       model: str, 
                       temperature: float = 0.7,
                       max_tokens: int = 1000) -> Dict[str, Any]:
        """Versão assíncrona do generate"""
        pass
    
    def _format_response(self, success: bool, text: str = "", 
                        error: str = None, **kwargs) -> Dict[str, Any]:
        """Formata resposta consistente para todos os providers"""
        response = {
            "ok": success,
            "text": text,
            "error": error,
            **kwargs
        }
        return response
