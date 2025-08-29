from services.cognitive_absorber import cognitive_absorber
from services.knowledge_fusion.fusion_engine import fusion_engine
from services.quality_optimization.quality_enhancer import quality_enhancer
from typing import Dict, List, Any, Generator, Optional
from .openai import OpenAIProvider
from .groq import GroqProvider
from .openrouter import OpenRouterProvider
import os
import logging

logger = logging.getLogger(__name__)

class ProviderRouter:
    """
    Roteador inteligente que seleciona automaticamente o melhor provider
    baseado nas chaves de API disponíveis e configurações
    """
    
    def __init__(self):
        self.providers = {}
        self._setup_providers()
        self.default_provider = self._select_default_provider()
    
    def _setup_providers(self):
        """Configura todos os providers baseado nas variáveis de ambiente"""
        try:
            # OpenAI
            if os.getenv('OPENAI_API_KEY'):
                self.providers['openai'] = OpenAIProvider(
                    api_key=os.getenv('OPENAI_API_KEY'),
                    base_url=os.getenv('OPENAI_BASE_URL')
                )
            
            # Groq
            if os.getenv('GROQ_API_KEY'):
                self.providers['groq'] = GroqProvider(
                    api_key=os.getenv('GROQ_API_KEY')
                )
            
            # OpenRouter
            if os.getenv('OPENROUTER_API_KEY'):
                self.providers['openrouter'] = OpenRouterProvider(
                    api_key=os.getenv('OPENROUTER_API_KEY'),
                    base_url=os.getenv('OPENROUTER_BASE_URL')
                )
            
            logger.info(f"Providers configurados: {list(self.providers.keys())}")
            
        except Exception as e:
            logger.error(f"Erro ao configurar providers: {str(e)}")
            raise
    
    def _select_default_provider(self) -> Optional[str]:
        """Seleciona o provider padrão baseado na disponibilidade"""
        priority_order = ['openai', 'groq', 'openrouter']
        
        for provider in priority_order:
            if provider in self.providers:
                logger.info(f"Provider padrão selecionado: {provider}")
                return provider
        
        logger.warning("Nenhum provider disponível")
        return None
    
    def get_provider(self, provider_name: str = None):
        """
        Obtém um provider específico ou o padrão
        
        Args:
            provider_name: Nome do provider ('openai', 'groq', 'openrouter')
        
        Returns:
            Instância do provider ou None se não disponível
        """
        if provider_name:
            return self.providers.get(provider_name)
        return self.providers.get(self.default_provider) if self.default_provider else None
    
    def generate(self, 
                messages: List[Dict[str, str]], 
                model: str = None,
                provider: str = None,
                temperature: float = 0.7,
                max_tokens: int = 1000,
                stream: bool = False) -> Dict[str, Any]:
        """
        Gera resposta usando o provider selecionado
        
        Args:
            messages: Lista de mensagens
            model: Modelo específico (opcional)
            provider: Provider específico (opcional)
            temperature: Criatividade da resposta
            max_tokens: Tokens máximos
            stream: Se deve usar streaming
        
        Returns:
            Resposta formatada
        """
        provider_instance = self.get_provider(provider)
        
        if not provider_instance:
            return {
                "ok": False,
                "error": "Nenhum provider LLM disponível. Configure as variáveis de ambiente.",
                "text": ""
            }
        
        # Seleção inteligente de modelo padrão baseado no provider
        if not model:
            model = self._get_default_model(provider_instance)
        
