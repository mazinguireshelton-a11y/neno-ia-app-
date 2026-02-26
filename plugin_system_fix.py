"""
SISTEMA DE PLUGINS INTELIGENTE - SIMPLES E EFETIVO
"""
import importlib
from typing import Any, Optional

def load_plugin_simple(plugin_name: str) -> Optional[Any]:
    """Carrega plugins de forma inteligente e simples"""
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        
        # 1. Tentar função register()
        if hasattr(module, 'register'):
            result = module.register()
            if result:
                return result
        
        # 2. Tentar função get_plugin()
        if hasattr(module, 'get_plugin'):
            result = module.get_plugin()
            if result:
                return result
        
        # 3. Procurar por instâncias existentes
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            attr = getattr(module, attr_name)
            # Verificar se parece um plugin
            if (hasattr(attr, 'execute') or hasattr(attr, 'name') or 
                hasattr(attr, 'version') or 'plugin' in attr_name.lower()):
                return attr
        
        # 4. Procurar por classes e instanciar
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            attr = getattr(module, attr_name)
            if (hasattr(attr, '__class__') and 
                ('Plugin' in attr_name or hasattr(attr, 'execute'))):
                try:
                    return attr()
                except:
                    continue
        
        return None
        
    except Exception as e:
        print(f"❌ Erro carregando {plugin_name}: {e}")
        return None

# Integrar com o sistema existente
try:
    from services import plugin_service as ps
    ps.load_plugin = load_plugin_simple
    print("✅ Sistema de plugins atualizado com sucesso!")
except Exception as e:
    print(f"⚠️ Não foi possível integrar com plugin_service: {e}")
