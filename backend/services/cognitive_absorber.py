import json
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ExtremeCognitiveAbsorber:
    def __init__(self):
        self.knowledge_graph = {}
        self.cognitive_patterns = {}
        self.absorption_stats = {
            "total_absorbed": 0,
            "by_provider": {"openai": 0, "groq": 0, "openrouter": 0},
            "by_domain": {"technical": 0, "creative": 0, "cultural": 0},
            "success_rate": 1.0
        }
        
    def absorb_provider_knowledge(self, query: str, responses: Dict[str, Any]) -> None:
        """Absorve conhecimento sem dependências externas"""
        try:
            # Extrair padrões cognitivos de cada provedor
            cognitive_extraction = {
                "openai": self._extract_openai_cognitive_patterns(responses.get("openai", "")),
                "groq": self._extract_groq_cognitive_patterns(responses.get("groq", "")),
                "openrouter": self._extract_openrouter_cognitive_patterns(responses.get("openrouter", ""))
            }
            
            # Fundir em super-conhecimento
            fused_knowledge = self._fuse_cognitive_powers(cognitive_extraction)
            
            # Adicionar ao grafo de conhecimento
            self._add_to_knowledge_graph(query, fused_knowledge, cognitive_extraction)
            
            # Atualizar estatísticas
            self._update_absorption_stats(cognitive_extraction)
            
            logger.info(f"✅ Conhecimento absorvido: {query[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Erro na absorção cognitiva: {str(e)}")
    
    def _extract_openai_cognitive_patterns(self, response: str) -> Dict[str, float]:
        """Extrai padrões cognitivos da OpenAI sem numpy"""
        if not response:
            return {}
            
        return {
            "creativity_score": self._calculate_creativity(response),
            "contextual_depth": self._measure_contextual_layers(response),
            "emotional_intelligence": self._detect_emotional_iq(response),
            "narrative_quality": self._analyze_narrative_flow(response),
            "cultural_relevance": self._assess_cultural_understanding(response),
            "linguistic_richness": self._measure_linguistic_complexity(response)
        }
    
    def _extract_groq_cognitive_patterns(self, response: str) -> Dict[str, float]:
        """Extrai padrões cognitivos da Groq sem numpy"""
        if not response:
            return {}
            
        return {
            "technical_accuracy": self._measure_technical_precision(response),
            "response_efficiency": self._calculate_efficiency_score(response),
            "logical_structure": self._analyze_logical_organization(response),
            "information_density": self._measure_info_density(response),
            "computational_optimization": self._assess_computational_quality(response),
            "speed_optimization": self._calculate_speed_score(response)
        }
    
    def _extract_openrouter_cognitive_patterns(self, response: str) -> Dict[str, float]:
        """Extrai padrões cognitivos do OpenRouter sem numpy"""
        if not response:
            return {}
            
        return {
            "adaptability_score": self._measure_adaptability(response),
            "stylistic_diversity": self._analyze_style_variation(response),
            "model_fusion_quality": self._detect_multi_model_knowledge(response),
            "customization_potential": self._assess_customization_capability(response),
            "cross_domain_ability": self._measure_cross_domain_skill(response),
            "innovation_score": self._calculate_innovation(response)
        }
    
    def _fuse_cognitive_powers(self, cognitive_extraction: Dict) -> Dict[str, float]:
        """Funde os poderes cognitivos sem numpy"""
        fused_powers = {}
        
        # Combinar habilidades complementares
        openai_data = cognitive_extraction.get("openai", {})
        groq_data = cognitive_extraction.get("groq", {})
        openrouter_data = cognitive_extraction.get("openrouter", {})
        
        fused_powers["super_creativity"] = (
            openai_data.get("creativity_score", 0) * 0.4 +
            openrouter_data.get("innovation_score", 0) * 0.3 +
            groq_data.get("computational_optimization", 0) * 0.3
        )
        
        fused_powers["hyper_efficiency"] = (
            groq_data.get("response_efficiency", 0) * 0.5 +
            openai_data.get("linguistic_richness", 0) * 0.25 +
            openrouter_data.get("adaptability_score", 0) * 0.25
        )
        
        fused_powers["ultimate_adaptability"] = (
            openrouter_data.get("adaptability_score", 0) * 0.4 +
            openai_data.get("cultural_relevance", 0) * 0.3 +
            groq_data.get("technical_accuracy", 0) * 0.3
        )
        
        # Habilidades únicas da fusão (média simples)
        values = [fused_powers["super_creativity"], fused_powers["hyper_efficiency"], fused_powers["ultimate_adaptability"]]
        valid_values = [v for v in values if v is not None]
        fused_powers["cognitive_synergy"] = sum(valid_values) / len(valid_values) if valid_values else 0
        
        return fused_powers
    
    def _add_to_knowledge_graph(self, query: str, fused_knowledge: Dict, cognitive_extraction: Dict) -> None:
        """Adiciona conhecimento ao grafo global"""
        knowledge_id = f"knowledge_{datetime.now().timestamp()}"
        
        self.knowledge_graph[knowledge_id] = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "fused_knowledge": fused_knowledge,
            "provider_patterns": cognitive_extraction,
            "absorption_quality": self._calculate_absorption_quality(fused_knowledge)
        }
    
    def _calculate_absorption_quality(self, fused_knowledge: Dict) -> float:
        """Calcula qualidade da absorção cognitiva sem numpy"""
        if not fused_knowledge:
            return 0.0
        values = list(fused_knowledge.values())
        valid_values = [v for v in values if v is not None]
        return min(1.0, sum(valid_values) / len(valid_values)) if valid_values else 0.0
    
    def _update_absorption_stats(self, cognitive_extraction: Dict) -> None:
        """Atualiza estatísticas de absorção"""
        self.absorption_stats["total_absorbed"] += 1
        
        for provider in ["openai", "groq", "openrouter"]:
            if cognitive_extraction.get(provider):
                self.absorption_stats["by_provider"][provider] += 1
    
    # ================== MÉTODOS DE ANÁLISE (IMPLEMENTAÇÕES SIMPLES) ==================
    
    def _calculate_creativity(self, text: str) -> float:
        """Calcula score de criatividade"""
        if not text:
            return 0.0
        score = min(1.0, len(text) / 1000 * 0.3)
        if '!' in text:
            score += 0.1
        if '?' in text:
            score += 0.05
        return min(score, 1.0)
    
    def _measure_contextual_layers(self, text: str) -> float:
        """Mede camadas contextuais"""
        if not text:
            return 0.0
        sentences = text.split('.')
        return min(1.0, len(sentences) / 10)
    
    def _detect_emotional_iq(self, text: str) -> float:
        """Detecta inteligência emocional"""
        emotional_words = ['feel', 'emotion', 'understand', 'empathy', 'compassion']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in emotional_words if word in text_lower) / len(emotional_words)
        return min(score, 1.0)
    
    def _analyze_narrative_flow(self, text: str) -> float:
        """Analisa fluxo narrativo"""
        if not text:
            return 0.0
        paragraphs = text.split('\n\n')
        return min(1.0, len(paragraphs) / 5)
    
    def _assess_cultural_understanding(self, text: str) -> float:
        """Avalia entendimento cultural"""
        cultural_terms = ['culture', 'tradition', 'society', 'community', 'heritage']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in cultural_terms if word in text_lower) / len(cultural_terms)
        return min(score, 1.0)
    
    def _measure_linguistic_complexity(self, text: str) -> float:
        """Mede complexidade linguística"""
        if not text:
            return 0.0
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        return min(1.0, avg_word_length / 10)
    
    def _measure_technical_precision(self, text: str) -> float:
        """Mede precisão técnica"""
        technical_terms = ['algorithm', 'function', 'variable', 'protocol', 'interface', 'API']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in technical_terms if word in text_lower) / len(technical_terms)
        return min(score, 1.0)
    
    def _calculate_efficiency_score(self, text: str) -> float:
        """Calcula score de eficiência"""
        if not text:
            return 0.0
        # Respostas mais curtas são mais eficientes
        return min(1.0, 1.0 - (len(text) / 2000))
    
    def _analyze_logical_organization(self, text: str) -> float:
        """Analiza organização lógica"""
        if not text:
            return 0.0
        logical_indicators = ['first', 'second', 'then', 'therefore', 'because']
        text_lower = text.lower()
        score = sum(1 for word in logical_indicators if word in text_lower) / len(logical_indicators)
        return min(score, 1.0)
    
    def _measure_info_density(self, text: str) -> float:
        """Mede densidade de informação"""
        if not text:
            return 0.0
        words = text.split()
        unique_words = set(words)
        return min(1.0, len(unique_words) / len(words)) if words else 0.0
    
    def _assess_computational_quality(self, text: str) -> float:
        """Avalia qualidade computacional"""
        computational_terms = ['compute', 'process', 'calculate', 'optimize', 'efficient']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in computational_terms if word in text_lower) / len(computational_terms)
        return min(score, 1.0)
    
    def _calculate_speed_score(self, text: str) -> float:
        """Calcula score de velocidade (baseado em concisão)"""
        if not text:
            return 0.0
        return min(1.0, 1.0 - (len(text) / 1500))
    
    def _measure_adaptability(self, text: str) -> float:
        """Mede adaptabilidade"""
        adaptive_terms = ['adapt', 'flexible', 'adjust', 'modify', 'customize']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in adaptive_terms if word in text_lower) / len(adaptive_terms)
        return min(score, 1.0)
    
    def _analyze_style_variation(self, text: str) -> float:
        """Analiza variação de estilo"""
        if not text:
            return 0.0
        # Verifica se tem diferentes tipos de pontuação
        style_marks = ['.', '!', '?', ':', ';']
        score = sum(1 for mark in style_marks if mark in text) / len(style_marks)
        return min(score, 1.0)
    
    def _detect_multi_model_knowledge(self, text: str) -> float:
        """Detecta conhecimento multi-modelo"""
        model_terms = ['model', 'approach', 'method', 'technique', 'framework']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in model_terms if word in text_lower) / len(model_terms)
        return min(score, 1.0)
    
    def _assess_customization_capability(self, text: str) -> float:
        """Avalia capacidade de customização"""
        custom_terms = ['custom', 'personalize', 'tailor', 'configure', 'settings']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in custom_terms if word in text_lower) / len(custom_terms)
        return min(score, 1.0)
    
    def _measure_cross_domain_skill(self, text: str) -> float:
        """Mede habilidade cross-domain"""
        domain_terms = ['domain', 'field', 'area', 'discipline', 'specialty']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in domain_terms if word in text_lower) / len(domain_terms)
        return min(score, 1.0)
    
    def _calculate_innovation(self, text: str) -> float:
        """Calcula score de inovação"""
        innovation_terms = ['innovate', 'create', 'invent', 'disrupt', 'transform']
        if not text:
            return 0.0
        text_lower = text.lower()
        score = sum(1 for word in innovation_terms if word in text_lower) / len(innovation_terms)
        return min(score, 1.0)
    
    def get_absorption_report(self) -> Dict[str, Any]:
        """Retorna relatório completo de absorção"""
        total_points = len(self.knowledge_graph)
        qualities = [v["absorption_quality"] for v in self.knowledge_graph.values() if v.get("absorption_quality") is not None]
        avg_quality = sum(qualities) / len(qualities) if qualities else 0
        
        return {
            "total_knowledge_points": total_points,
            "absorption_stats": self.absorption_stats,
            "average_quality": avg_quality,
            "knowledge_domains": self._analyze_knowledge_domains()
        }
    
    def _analyze_knowledge_domains(self) -> Dict[str, int]:
        """Analiza distribuição de domínios de conhecimento"""
        domains = {"technology": 0, "science": 0, "arts": 0, "business": 0, "other": 0}
        # Implementação básica - pode ser melhorada
        return domains

# Instância global para absorção cognitiva
cognitive_absorber = ExtremeCognitiveAbsorber()
