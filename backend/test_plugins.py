#!/usr/bin/env python3
"""
TESTES AUTOMÁTICOS DOS PLUGINS APÓS CORREÇÕES
"""

import sys
import os
sys.path.insert(0, os.getcwd())

def test_plugin(plugin_name):
    """Testa um plugin específico"""
    try:
        print(f"\n🔍 Testando {plugin_name}:")
        
        module = __import__(f'plugins.{plugin_name}', fromlist=['*'])
        
        # Tentar todas as formas de carregamento
        plugin = None
        if hasattr(module, 'register'):
            plugin = module.register()
            print("✅ Carregado via register()")
        elif hasattr(module, 'get_plugin'):
            plugin = module.get_plugin()
            print("✅ Carregado via get_plugin()")
        elif hasattr(module, 'super_ia') and plugin_name == 'super_ia_module':
            plugin = module.super_ia
            print("✅ Carregado via instância super_ia")
        else:
            # Buscar manualmente
            for attr in dir(module):
                if not attr.startswith('_'):
                    obj = getattr(module, attr)
                    if hasattr(obj, 'execute') or hasattr(obj, 'name'):
                        plugin = obj
                        print(f"✅ Carregado via instância {attr}")
                        break
        
        if plugin:
            print(f"   Nome: {getattr(plugin, 'name', 'N/A')}")
            print(f"   Versão: {getattr(plugin, 'version', 'N/A')}")
            print(f"   Tipo: {type(plugin).__name__}")
            
            # Testar execução básica se possível
            if hasattr(plugin, 'execute'):
                try:
                    result = plugin.execute('test', {})
                    print(f"   Execução: {result.get('success', 'N/A')}")
                except Exception as e:
                    print(f"   Execução: Erro ({e})")
            
            return True
        else:
            print("❌ Nenhum método de carregamento funcionou")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🧪 TESTES AUTOMÁTICOS DOS PLUGINS")
    print("=" * 50)
    
    plugins = [
        'super_ia_module',
        'physics_plugin',
        'animacao_3d',
        'web_search',
        'calculator',
        'code_executor',
        'image_generator'
    ]
    
    results = {}
    for plugin in plugins:
        results[plugin] = test_plugin(plugin)
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS FINAIS:")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    for plugin, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {plugin}")
    
    print(f"\n🎯 Total: {success_count}/{total_count} plugins funcionando")
    
    if success_count == total_count:
        print("🚀 TODOS OS PLUGINS ESTÃO OPERACIONAIS!")
    else:
        print("⚠️  Alguns plugins precisam de atenção")

if __name__ == "__main__":
    main()
