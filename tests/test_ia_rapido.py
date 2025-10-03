#!/usr/bin/env python3
# ⚡ TESTE RÁPIDO DA IA

import os
import sys

def teste_rapido():
    print("⚡ TESTE RÁPIDO DA IA NENO")
    print("=" * 40)
    
    # Verificações básicas
    checks = [
        ("🏗️ Backend", os.path.exists("backend")),
        ("🧠 LLM Service", os.path.exists("backend/services/llm_service.py")),
        ("🔌 Plugins", len([f for f in os.listdir("backend/plugins") if f.endswith('.py') and f != '__init__.py']) > 0),
        ("💬 Chat API", os.path.exists("backend/routes/chat.py")),
        ("📚 Aprendizado", os.path.exists("backend/plugins/neno_learning.db")),
        ("🎛️ Modos", os.path.exists("backend/services/mode_manager.py")),
    ]
    
    for nome, status in checks:
        print(f"{'✅' if status else '❌'} {nome}")
    
    # Testar importação básica
    try:
        import backend.config as config
        import backend.app as app
        print("✅ Imports principais funcionando")
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
    
    print("\n🎯 STATUS:", "PRONTA" if all([c[1] for c in checks]) else "COM PROBLEMAS")
    print("💡 Comando: python backend/app.py")

if __name__ == "__main__":
    teste_rapido()
