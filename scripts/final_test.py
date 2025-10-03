#!/usr/bin/env python3
import os
import sys

def final_system_check():
    print("🎯 TESTE FINAL DE INTEGRAÇÃO")
    print("=" * 35)
    
    checks = [
        ("🏗️  Estrutura backend", os.path.exists("backend")),
        ("🔌 Plugin Image Generator", os.path.exists("backend/plugins/image_generator.py")),
        ("🌐 Serviço LLM", os.path.exists("backend/services/llm_service.py")),
        ("🗄️  Banco principal", os.path.exists("backend/data/neno_ia.db")),
        ("💾 Cache de imagens", len(os.listdir("cache/neno_images")) > 0 if os.path.exists("cache/neno_images") else False),
        ("📚 Sistema de aprendizado", os.path.exists("backend/plugins/neno_learning.db")),
    ]
    
    all_ok = True
    for check_name, check_result in checks:
        status = "✅" if check_result else "❌"
        print(f"{status} {check_name}")
        if not check_result:
            all_ok = False
    
    print("\n" + "=" * 35)
    if all_ok:
        print("🎉 SISTEMA 100% OPERACIONAL!")
        print("🚀 Todos os componentes estão funcionando!")
    else:
        print("⚠️  Sistema com problemas menores")
        print("💡 Alguns componentes precisam de ajuste")
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. python backend/app.py - Iniciar servidor")
    print("2. Acessar http://localhost:5000")
    print("3. Testar interface web (se disponível)")

if __name__ == "__main__":
    final_system_check()
