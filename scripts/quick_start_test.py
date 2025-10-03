#!/usr/bin/env python3
# 📁 quick_start_test.py
# 🔥 TESTE RÁPIDO DO SISTEMA

import os
import sys

def quick_test():
    print("⚡ TESTE RÁPIDO DO SISTEMA NENO IA")
    print("📍 Diretório:", os.getcwd())
    
    # 1. Estrutura básica
    print("\n1. 🏗️  Estrutura do sistema:")
    essential_dirs = ['backend', 'backend/plugins', 'backend/services', 'cache']
    for dir_path in essential_dirs:
        if os.path.exists(dir_path):
            print(f"   ✅ {dir_path}")
        else:
            print(f"   ❌ {dir_path}")
    
    # 2. Arquivos principais
    print("\n2. 📄 Arquivos principais:")
    essential_files = [
        'backend/app.py',
        'backend/config.py', 
        'backend/plugins/image_generator.py',
        'backend/services/llm_service.py'
    ]
    for file_path in essential_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file_path} ({size} bytes)")
        else:
            print(f"   ❌ {file_path}")
    
    # 3. Teste de imports
    print("\n3. 🔄 Teste de imports:")
    try:
        import backend.config as config
        print("   ✅ backend.config")
    except Exception as e:
        print(f"   ❌ backend.config: {e}")
    
    try:
        import backend.app as app
        print("   ✅ backend.app")
    except Exception as e:
        print(f"   ❌ backend.app: {e}")
    
    # 4. Sistema de plugins
    print("\n4. 🔌 Plugins disponíveis:")
    plugins_dir = 'backend/plugins'
    if os.path.exists(plugins_dir):
        plugins = [f for f in os.listdir(plugins_dir) if f.endswith('.py') and f != '__init__.py']
        for plugin in plugins[:5]:  # Mostra apenas os primeiros 5
            print(f"   🔧 {plugin}")
    
    # 5. Cache e dados
    print("\n5. 💾 Cache e dados:")
    cache_dirs = ['cache/neno_images', 'cache/omega_images']
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            files = len([f for f in os.listdir(cache_dir) if os.path.isfile(os.path.join(cache_dir, f))])
            print(f"   📁 {cache_dir}: {files} arquivos")
        else:
            print(f"   📁 {cache_dir}: não existe")
    
    print("\n🎯 RESULTADO DO TESTE RÁPIDO:")
    print("💡 Comando para iniciar: python backend/app.py")
    print("🚀 Sistema pronto!" if os.path.exists('backend/app.py') else "❌ Sistema incompleto")

if __name__ == "__main__":
    quick_test()
