"""
Patch para o sistema de carregamento de plugins
"""
import importlib
from typing import Any, Dict

def smart_plugin_loader(plugin_module):
    """Carregador inteligente que detecta automaticamente o tipo de plugin"""
    try:
        # Tentar obter via register()
        if hasattr(plugin_module, 'register'):
            plugin = plugin_module.register()
            if plugin:
                return plugin
        
        # Tentar obter via get_plugin()
        if hasattr(plugin_module, 'get_plugin'):
            plugin = plugin_module.get_plugin()
            if plugin:
                return plugin
        
        # Tentar encontrar instância diretamente
        for attr_name in dir(plugin_module):
            attr = getattr(plugin_module, attr_name)
            if hasattr(attr, 'execute') or hasattr(attr, 'name'):
                return attr
        
        # Último recurso: procurar por classes Plugin
        for attr_name in dir(plugin_module):
            attr = getattr(plugin_module, attr_name)
            if 'Plugin' in str(type(attr)) or 'Plugin' in attr_name:
                return attr
                
    except Exception as e:
        print(f"⚠️  Erro no carregamento inteligente: {e}")
    
    return None

# Aplicar patch
import services.plugin_service as ps
original_loader = getattr(ps, 'load_plugin', None)

if original_loader:
    # Decorar a função original com nosso carregador inteligente
    def patched_load_plugin(plugin_name, plugin_config):
        try:
            result = original_loader(plugin_name, plugin_config)
            if result:
                return result
        except:
            pass
        
        # Fallback para nosso carregador inteligente
        try:
            module = importlib.import_module(f"plugins.{plugin_name}")
            return smart_plugin_loader(module)
        except Exception as e:
            print(f"❌ Fallback também falhou para {plugin_name}: {e}")
            return None
    
    # Substituir a função original
    ps.load_plugin = patched_load_plugin
    print("✅ Sistema de plugins patched com carregador inteligente")
