"""
📦 PLUGINS DO NENO IA - Mapeamento Correto e Definitivo
"""

import importlib
from typing import Dict, Any

# MAPEAMENTO CORRETO baseado na análise REAL dos arquivos
PLUGIN_MAPPING = {
    'web_search': ('WebSearchPlugin', True),
    'calculator': ('CalculatorPlugin', True),
    'code_executor': ('CodeExecutorPlugin', True), 
    'image_generator': ('ImageGeneratorPlugin', True),
    'animacao_3d': ('get_plugin', False),  # Função que retorna plugin
    'viz_engine': ('VisualizationEngine', True),  # Correto!
    'physics_plugin': ('PhysicsPlugin', True),    # Correto!
    'super_ia_module': ('SuperIAPlugin', True),
    'imax_interface_termux': ('IMAXTerminalInterface', True)
}

PLUGINS = {}

print("🔧 Carregando plugins com mapeamento CORRETO...")

for module_name, (import_name, is_class) in PLUGIN_MAPPING.items():
    try:
        module = importlib.import_module(f'.{module_name}', __package__)
        
        if is_class:
            plugin_class = getattr(module, import_name)
            PLUGINS[module_name] = plugin_class()
        else:
            plugin_func = getattr(module, import_name)
            PLUGINS[module_name] = plugin_func()
            
        print(f"✅ {module_name} carregado como {import_name}")
        
    except Exception as e:
        print(f"⚠️  {module_name} não disponível: {e}")

# Funções de interface
def get_plugin(nome: str):
    """Retorna um plugin pelo nome"""
    return PLUGINS.get(nome)

def listar_plugins() -> Dict[str, Any]:
    """Lista todos os plugins carregados"""
    return {nome: type(plugin).__name__ for nome, plugin in PLUGINS.items()}

print(f"🎯 {len(PLUGINS)} plugins carregados com sucesso!")
print(f"📋 Plugins disponíveis: {list(PLUGINS.keys())}")
