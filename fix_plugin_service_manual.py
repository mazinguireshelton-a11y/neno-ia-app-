import re

# Ler o arquivo atual
with open('services/plugin_service.py', 'r') as f:
    content = f.read()

# Substituir qualquer tentativa de instanciar SuperIAPlugin
new_content = re.sub(
    r'SuperIAPlugin\(\)',
    'module.super_ia if hasattr(module, "super_ia") else None',
    content
)

# Garantir que o carregamento inteligente está ativo
if 'load_plugin(' not in new_content:
    new_content += """

# ==================== CARREGADOR INTELIGENTE ====================
def load_plugin(plugin_name, plugin_config):
    import importlib
    try:
        module = importlib.import_module(f"plugins.{plugin_name}")
        
        # SUPER IA - caso especial
        if plugin_name == "super_ia_module":
            if hasattr(module, 'super_ia'):
                return module.super_ia
            if hasattr(module, 'register'):
                return module.register()
            if hasattr(module, 'get_plugin'):
                return module.get_plugin()
        
        # OUTROS PLUGINS
        if hasattr(module, 'register'):
            return module.register()
        if hasattr(module, 'get_plugin'):
            return module.get_plugin()
            
        return None
    except Exception as e:
        print(f"❌ Erro carregando {plugin_name}: {e}")
        return None
# ==================== FIM DO CARREGADOR ====================
"""

with open('services/plugin_service.py', 'w') as f:
    f.write(new_content)

print("✅ Plugin service corrigido manualmente!")
