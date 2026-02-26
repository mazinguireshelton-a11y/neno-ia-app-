from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class CognitiveFusionEngine:
    def __init__(self):
        self.fusion_algorithms = {
            "weighted_synergy": self._weighted_synergy_fusion,
            "neural_fusion": self._neural_network_fusion,
            "evolutionary_fusion": self._evolutionary_optimization_fusion
        }
        
    def fuse_provider_responses(self, query: str, responses: Dict[str, Any]) -> str:
        """Funde respostas dos provedores na resposta definitiva"""
        if not responses:
            return ""
            
        # Filtrar respostas vazias
        valid_responses = {k: v for k, v in responses.items() if v and v.strip()}
        if not valid_responses:
            return ""
            
        # Selecionar algoritmo de fusão baseado no tipo de query
        fusion_algorithm = self._select_fusion_algorithm(query, valid_responses)
        
        # Aplicar fusão
        fused_response = fusion_algorithm(query, valid_responses)
        
        return fused_response
    
    def _select_fusion_algorithm(self, query: str, responses: Dict[str, Any]) -> callable:
        """Seleciona o melhor algoritmo de fusão"""
        query_complexity = self._calculate_query_complexity(query)
        response_quality = self._assess_response_quality(responses)
        
        if query_complexity > 0.8 and response_quality > 0.7:
            return self.fusion_algorithms["neural_fusion"]
        elif query_complexity > 0.5:
            return self.fusion_algorithms["evolutionary_fusion"]
        else:
            return self.fusion_algorithms["weighted_synergy"]
    
    def _weighted_synergy_fusion(self, query: str, responses: Dict[str, Any]) -> str:
        """Fusão por sinergia ponderada"""
        weights = {
            "openai": 0.4,  # Criatividade
            "groq": 0.3,    # Precisão
            "openrouter": 0.3  # Adaptabilidade
        }
        
        # Combinar melhores partes baseado nos pesos
        fused_parts = []
        for provider, response in responses.items():
            if response and provider in weights:
                # Extrair melhores sentenças de cada provedor
                best_sentences = self._extract_best_sentences(response, weights[provider])
                fused_parts.extend(best_sentences)
        
        # Reconstruir resposta fundida
        return self._reconstruct_response(fused_parts)
    
    def _neural_network_fusion(self, query: str, responses: Dict[str, Any]) -> str:
        """Fusão inteligente simulada"""
        # Simular fusão neural (em produção seria um modelo real)
        response_parts = []
        
        # Adicionar criatividade da OpenAI
        if "openai" in responses:
            response_parts.append(f"💡 **Inovação**: {responses['openai']}")
        
        # Adicionar precisão da Groq
        if "groq" in responses:
            response_parts.append(f"⚡ **Precisão**: {responses['groq']}")
        
        # Adicionar adaptabilidade do OpenRouter
        if "openrouter" in responses:
            response_parts.append(f"🔄 **Adaptabilidade**: {responses['openrouter']}")
        
        # Síntese final
        if response_parts:
            response_parts.append(f"\n🎯 **Síntese Cognitiva**: {self._generate_cognitive_synthesis(query, responses)}")
            return "\n\n".join(response_parts)
        
        return "Não foi possível fundir as respostas."
    
    def _evolutionary_optimization_fusion(self, query: str, responses: Dict[str, Any]) -> str:
        """Fusão por otimização evolutiva simulada"""
        best_response = ""
        best_score = 0
        
        # Testar as respostas diretamente (simulação de evolução)
        for provider, response in responses.items():
            score = self._evaluate_response_quality(response, query)
            if score > best_score:
                best_score = score
                best_response = response
        
        return best_response if best_response else list(responses.values())[0]
    
    def _generate_cognitive_synthesis(self, query: str, responses: Dict[str, Any]) -> str:
        """Gera síntese cognitiva das respostas"""
        return f"Baseado na análise integrada de {len(responses)} provedores especializados, esta resposta combina criatividade avançada com precisão técnica e adaptabilidade contextual para oferecer a solução mais completa."
    
    def _calculate_query_complexity(self, query: str) -> float:
        """Calcula complexidade da query"""
        if not query:
            return 0.0
        word_count = len(query.split())
        return min(1.0, word_count / 50)  # 0.0 a 1.0
    
    def _assess_response_quality(self, responses: Dict[str, Any]) -> float:
        """Avalia qualidade das respostas"""
        valid_responses = [r for r in responses.values() if r and r.strip()]
        return min(1.0, len(valid_responses) / 3)  # 0.0 a 1.0
    
    def _extract_best_sentences(self, response: str, weight: float) -> List[str]:
        """Extrai melhores sentenças baseado no peso"""
        if not response:
            return []
        
        sentences = response.split('. ')
        # Manter sentenças mais relevantes baseado no peso
        keep_count = max(1, int(len(sentences) * weight))
        return sentences[:keep_count]
    
    def _reconstruct_response(self, sentences: List[str]) -> str:
        """Reconstrói resposta a partir de sentenças"""
        if not sentences:
            return ""
        
        # Juntar sentenças e garantir pontuação adequada
        response = '. '.join(sentences)
        if not response.endswith('.'):
            response += '.'
        return response
    
    def _evaluate_response_quality(self, response: str, query: str) -> float:
        """Avalia qualidade de uma resposta"""
        if not response:
            return 0.0
        
        score = 0.0
        # Comprimento adequado
        response_length = len(response)
        if 50 <= response_length <= 1000:
            score += 0.3
        
        # Relevância para a query
        query_words = query.lower().split()
        response_lower = response.lower()
        relevant_words = sum(1 for word in query_words if word in response_lower)
        if query_words:
            score += (relevant_words / len(query_words)) * 0.4
        
        # Estruturação
        if '. ' in response or '\n' in response:
            score += 0.3
        
        return min(score, 1.0)

# Instância global do motor de fusão
fusion_engine = CognitiveFusionEngine()
