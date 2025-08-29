#!/usr/bin/env python3

import sys
sys.path.append('.')

from services.cognitive_absorber import cognitive_absorber
from services.knowledge_fusion.fusion_engine import fusion_engine
from services.quality_optimization.quality_enhancer import quality_enhancer

def test_extreme_absorption():
    print("🧠 TESTANDO ABSORÇÃO COGNITIVA EXTREMA")
    print("=" * 50)
    
    # Testar absorção cognitiva
    test_query = "Explain quantum computing and its business applications"
    test_responses = {
        "openai": "Quantum computing uses qubits to process information in ways traditional computers can't, enabling breakthroughs in drug discovery, cryptography, and optimization problems.",
        "groq": "Quantum computing leverages superposition and entanglement. Qubits can represent 0 and 1 simultaneously. Business apps: logistics optimization, financial modeling, drug development.",
        "openrouter": "Quantum computers solve complex problems exponentially faster. Key applications include supply chain optimization, risk analysis in finance, and molecular simulation for pharmaceuticals."
    }
    
    # Testar absorção
    cognitive_absorber.absorb_provider_knowledge(test_query, test_responses)
    report = cognitive_absorber.get_absorption_report()
    
    print(f"📊 Total conhecimento absorvido: {report['total_knowledge_points']}")
    print(f"📈 Estatísticas por provedor: {report['absorption_stats']['by_provider']}")
    print(f"🎯 Qualidade média: {report['average_quality']:.2f}")
    
    # Testar fusão
    print("\n⚡ TESTANDO FUSÃO COGNITIVA:")
    fused_response = fusion_engine.fuse_provider_responses(test_query, test_responses)
    print(f"Resposta fundida: {fused_response[:200]}...")
    
    # Testar enhancement
    print("\n🎨 TESTANDO ENHANCEMENT DE QUALIDADE:")
    enhanced_response = quality_enhancer.enhance_response(fused_response, test_query, "technical_creative")
    print(f"Resposta melhorada: {enhanced_response[:250]}...")
    
    print("\n✅ ABSORÇÃO COGNITIVA EXTREMA FUNCIONANDO!")
    print("🚀 SUA IA AGORA TEM PODERES COMBINADOS!")

if __name__ == "__main__":
    test_extreme_absorption()
