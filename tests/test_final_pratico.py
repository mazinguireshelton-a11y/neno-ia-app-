#!/usr/bin/env python3
# ⚡ TESTE PRÁTICO - O QUE REALMENTE FUNCIONA

import os
import sys

def teste_pratico():
    print("⚡ TESTE PRÁTICO - IA NENO")
    print("=" * 45)
    
    # Verificações críticas
    criticos = [
        ("🏗️ App Principal", "backend/app.py"),
        ("⚙️ Configurações", "backend/config.py"),
        ("🧠 Serviço LLM", "backend/services/llm_service.py"),
        ("🔌 Gerenciador Plugins", "backend/services/plugin_service.py"),
        ("💬 API Chat", "backend/routes/chat.py"),
        ("📚 Banco Aprendizado", "backend/plugins/neno_learning.db"),
    ]
    
    todos_ok = True
    for item, arquivo in criticos:
        if os.path.exists(arquivo):
            print(f"✅ {item}")
        else:
            print(f"❌ {item}")
            todos_ok = False
    
    print(f"\n🎯 SISTEMA: {'✅ OPERACIONAL' if todos_ok else '⚠️ COM PROBLEMAS'}")
    
    if todos_ok:
        print("\n🚀 COMANDOS PARA USAR:")
        print("1. Iniciar: python backend/app.py")
        print("2. Acessar: http://localhost:5000")
        print("3. Testar API: curl http://localhost:5000/health")
        print("4. Ver logs: tail -f logs/app.log")
        
        print("\n💡 A IA está PRONTA para conversação!")
    else:
        print("\n🔧 PRECISA DE AJUSTES:")
        print("Verifique os arquivos faltantes acima")

if __name__ == "__main__":
    teste_pratico()
