#!/usr/bin/env python3
import sys
import os
sys.path.append('backend/plugins')

def test_plugins_individually():
    print("🔌 TESTE INDIVIDUAL DE PLUGINS")
    print("=" * 40)
    
    # 1. Image Generator
    print("1. 🎨 Image Generator:")
    try:
        from image_generator import register_image_generator
        gen = register_image_generator()
        print(f"   ✅ {gen.name} v{gen.version}")
        
        # Teste rápido
        result = gen.execute("gato teste", "512x512")
        if result['success']:
            print("   ✅ Geração de imagem funcionando!")
        else:
            print(f"   ❌ Erro: {result.get('error', 'Desconhecido')}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 2. Calculator
    print("2. 🧮 Calculator:")
    try:
        from calculator import calculate
        result = calculate("2 + 2")
        print(f"   ✅ 2 + 2 = {result}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # 3. Web Search
    print("3. 🌐 Web Search:")
    try:
        from web_search import search_web
        result = search_web("teste")
        print(f"   ✅ Search funcionando - {len(result.get('results', []))} resultados")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("🎯 PLUGINS TESTADOS!")

if __name__ == "__main__":
    test_plugins_individually()
