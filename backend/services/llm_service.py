"""
Serviço centralizado para gerenciamento de modelos de linguagem
"""
from typing import Dict, List, Optional, Union, Generator
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.providers = self._initialize_providers()
        self.provider_priority = self._get_provider_priority()
        self.cooperative_orchestrator = None
        self._init_cooperative_system()
        
    def _initialize_providers(self) -> Dict:
        """Inicializa todos os provedores de IA configurados"""
        providers = {}
        
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            try:
                from .openai_provider import OpenAIProvider
                providers["openai"] = OpenAIProvider()
                logger.info("✅ Provedor OpenAI inicializado")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar OpenAI: {e}")
            
        # OpenRouter
        if os.getenv("OPENROUTER_API_KEY"):
            try:
                from .openrouter_provider import OpenRouterProvider
                providers["openrouter"] = OpenRouterProvider()
                logger.info("✅ Provedor OpenRouter inicializado")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar OpenRouter: {e}")
            
        # Groq
        if os.getenv("GROQ_API_KEY"):
            try:
                from .groq_provider import GroqProvider
                providers["groq"] = GroqProvider()
                logger.info("✅ Provedor Groq inicializado")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar Groq: {e}")
            
        # Local (Ollama, etc)
        if os.getenv("LOCAL_LLM_URL"):
            try:
                from .local_provider import LocalProvider
                providers["local"] = LocalProvider()
                logger.info("✅ Provedor Local inicializado")
            except Exception as e:
                logger.error(f"❌ Erro ao inicializar Local: {e}")
            
        return providers
    
    def _get_provider_priority(self) -> List[str]:
        """Define a prioridade dos provedores"""
        priority = []
        
        # Ordem de preferência inteligente
        if "openai" in self.providers:
            priority.append("openai")  # Melhor qualidade
        if "openrouter" in self.providers:
            priority.append("openrouter")  # Flexibilidade
        if "groq" in self.providers:
            priority.append("groq")  # Máxima velocidade
        if "local" in self.providers:
            priority.append("local")  # Fallback local
            
        return priority
    
    def _init_cooperative_system(self):
        """Inicializa sistema cooperativo"""
        try:
            from .cooperative_orchestrator import init_cooperative_orchestrator
            self.cooperative_orchestrator = init_cooperative_orchestrator(self)
            logger.info("✅ Sistema cooperativo inicializado")
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar sistema cooperativo: {e}")
    
    def get_response(self, messages: List[Dict], stream: bool = False,
                    provider: str = "auto", cooperative: bool = True, 
                    mode: str = "default", lang: str = "auto", **kwargs) -> Union[Dict, Generator]:
        """
        Obtém resposta dos provedores de IA com fallback automático
        """
        if not self.providers:
            raise Exception("Nenhum provedor de IA configurado")
        
        # Construir system prompt com modo e idioma
        system_prompt = build_system_prompt(mode, lang)
        
        # Adicionar system prompt às mensagens se não existir
        if not any(msg.get('role') == 'system' for msg in messages):
            messages = [{"role": "system", "content": system_prompt}] + messages
        
        # Extrair prompt para análise de complexidade
        user_prompt = next((msg['content'] for msg in reversed(messages) 
                          if msg['role'] == 'user'), '')
        
        # Verificar se deve usar cooperação
        if cooperative and self.cooperative_orchestrator and user_prompt:
            try:
                complexity = self.cooperative_orchestrator.analyze_complexity(user_prompt)
                
                if complexity["needs_cooperation"]:
                    logger.info(f"🏗️  Usando cooperação no modo {mode} (score: {complexity['complexity_score']})")
                    
                    # Usar asyncio para execução cooperativa
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(
                        self.cooperative_orchestrator.execute_cooperative_task(user_prompt, stream)
                    )
                    loop.close()
                    return result
                    
            except Exception as e:
                logger.error(f"❌ Cooperação falhou: {e}, usando fallback normal")

        # Modo normal (não cooperativo)
        if provider != "auto" and provider in self.providers:
            try:
                result = self.providers[provider].get_response(messages, stream, **kwargs)
                logger.info(f"✅ Resposta do provedor {provider} (modo {mode})")
                return result
            except Exception as e:
                logger.warning(f"⚠️ Provedor {provider} falhou: {e}")

        # Tentativa automática com fallback na ordem de prioridade
        errors = []
        for provider_name in self.provider_priority:
            try:
                result = self.providers[provider_name].get_response(messages, stream, **kwargs)
                logger.info(f"✅ Resposta do provedor {provider_name} (modo {mode})")
                return result
            except Exception as e:
                error_msg = f"{provider_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"⚠️ Provedor {provider_name} falhou: {e}")
                continue

        # Todos os provedores falharam
        error_message = "Todos os provedores de IA falharam:\n" + "\n".join(errors)
        logger.error(f"❌ {error_message}")
        raise Exception(error_message)
    
    def get_available_providers(self) -> List[Dict]:
        """Retorna lista de provedores disponíveis com status"""
        providers_info = []
        for name, provider in self.providers.items():
            providers_info.append({
                "name": name,
                "status": "available",
                "model": getattr(provider, 'model', 'unknown')
            })
        return providers_info
    
    def get_provider_stats(self) -> Dict:
        """Retorna estatísticas de uso dos provedores"""
        return {
            "total_providers": len(self.providers),
            "available_providers": list(self.providers.keys()),
            "priority_order": self.provider_priority,
            "timestamp": datetime.now().isoformat()
        }
    
    def set_provider_priority(self, priority: List[str]) -> bool:
        """Define prioridade personalizada dos provedores"""
        available_providers = list(self.providers.keys())
        valid_priority = [p for p in priority if p in available_providers]
        
        if valid_priority:
            self.provider_priority = valid_priority
            logger.info(f"✅ Prioridade atualizada: {valid_priority}")
            return True
        
        return False

# 🚀 SYSTEM PROMPT COMPLETO COM TODOS OS MODOS
def build_system_prompt(mode: str = "default", lang: str = "auto") -> str:
    """Constrói o prompt do sistema baseado no modo e idioma"""
    
    # Prompt base universal
    base_prompt = (
        "Você é a NENO IA, uma assistente multimodal avançada de nível mundial. "
        "Responda no mesmo idioma do usuário. Seja extremamente útil, preciso e detalhado. "
        "Use markdown para formatação quando apropriado e forneça exemplos práticos."
    )
    
    # 🔥 TODOS OS MODOS ESPECIALIZADOS (DOS SEUS ARQUIVOS)
    mode_prompts = {
        # ==================== MODOS PRINCIPAIS ====================
        "default": (
            "Modo padrão: forneça respostas completas, claras e bem estruturadas. "
            "Seja abrangente mas mantenha a objetividade. Use analogias e exemplos para facilitar o entendimento."
        ),
        
        # ==================== MODOS TÉCNICOS ====================
        "programmer": (
            "🔧 MODO PROGRAMADOR AVANÇADO:\n"
            "- Forneça código bem documentado e pronto para uso\n" 
            "- Explique decisões de arquitetura e trade-offs\n"
            "- Considere performance, segurança e boas práticas\n"
            "- Inclua exemplos executáveis e testes unitários\n"
            "- Discuta alternativas e otimizações\n"
            "- Use padrões de projeto quando apropriado\n"
            "- Mantenha-se atualizado com as melhores práticas"
        ),
        
        # ==================== MODOS CIENTÍFICOS ====================
        "research": (
            "🔬 MODO PESQUISA CIENTÍFICA:\n"
            "- Seja meticuloso e baseado em evidências\n"
            "- Cite fontes confiáveis e estudos relevantes\n"
            "- Mantenha rigor científico e metodológico\n"
            "- Apresente dados factualmente precisos\n"
            "- Discuta limitações e viéses potenciais\n"
            "- Use terminologia técnica apropriada\n"
            "- Evite especulações não fundamentadas"
        ),
        
        "physics_basic": (
            "📊 MODO FÍSICA BÁSICA (3D INTEGRADO):\n"
            "- Explique conceitos físicos com clareza\n"
            "- Use visualizações e analogias práticas\n"
            "- Fornece exemplos com objetos 3D simples\n"
            "- Gere gráficos e simulações básicas\n"
            "- Mostre aplicações do mundo real\n"
            "- Use linguagem acessível para iniciantes\n"
            "- Incorpore elementos visuais quando possível"
        ),
        
        "physics_advanced": (
            "⚛️ MODO FÍSICA AVANÇADA (3D INTERATIVO):\n"
            "- Deep learning em conceitos físicos complexos\n"
            "- Simulações 3D interativas e tempo real\n"
            "- Modelagem matemática avançada\n"
            "- Análise de sistemas multicorpo\n"
            "- Dinâmica de fluidos e partículas\n"
            "- Campos vetoriais e tensoriais\n"
            "- Equações diferenciais e métodos numéricos\n"
            "- Visualização volumétrica e renderização física"
        ),
        
        # ==================== MODOS CRIATIVOS ====================
        "creative": (
            "🎨 MODO CRIATIVO:\n"
            "- Seja imaginativo e inovador\n"
            -"Explore perspectivas não convencionais\n"
            "- Sugira ideias originais e disruptivas\n"
            "- Pense fora da caixa sistematicamente\n"
            "- Combine conceitos de forma única\n"
            "- Mantenha coerência narrativa\n"
            "- Use linguagem vibrante e envolvente"
        ),
        
        # ==================== MODOS DE COMUNICAÇÃO ====================
        "voice": (
            "🎙️ MODO VOZ (MULTILÍNGUE):\n"
            "- Respostas concisas e naturais para voz\n"
            "- Linguagem coloquial e fluida\n"
            "- Estruturação para fácil compreensão auditiva\n"
            "- Ênfase em clareza e naturalidade\n"
            "- Adaptação para conversação contínua\n"
            "- Uso de pausas e entonação apropriada\n"
            "- Correção fonética e melhoria de dicção"
        ),
        
        # ==================== MODO SUPER COMPUTAÇÃO ====================
        "super_compute": (
            "🚀 MODO SUPER COMPUTAÇÃO:\n"
            "- Otimização de algoritmos complexos\n"
            "- Processamento distribuído e paralelismo\n"
            "- Análise de big data e computação de alto desempenho\n"
            "- Modelagem matemática avançada\n"
            "- Simulações em larga escala\n"
            "- Resolução de problemas computacionalmente intensivos\n"
            "- Cluster computing e load balancing\n"
            "- Análise assintótica e complexidade algorítmica"
        )
    }
    
    # Mensagem de modo não encontrado
    mode_not_found = (
        "Modo especializado: forneça respostas técnicas detalhadas e precisas. "
        "Use metodologia científica e mantenha rigor analítico."
    )
    
    # Nota de idioma
    language_note = ""
    if lang != "auto":
        language_note = f" Responda estritamente em {lang} mantendo a precisão técnica."
    
    # Combinação final
    mode_instruction = mode_prompts.get(mode, mode_not_found)
    
    return f"{base_prompt}\n\n{mode_instruction}\n\n{language_note}"

# Instância global do serviço
llm_service = LLMService()
