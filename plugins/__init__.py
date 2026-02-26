"""
Plugins do NENO - Sistema de Geração de Imagens
"""
import importlib
from pathlib import Path

def load_plugins():
    """Carrega todos os plugins disponíveis"""
    plugins = {}
    plugins_dir = Path(__file__).parent
    
    # Mapeamento manual dos plugins
    plugin_mapping = {
        'web_search': ('web_search', 'WebSearchPlugin'),
        'calculator': ('calculator', 'CalculatorPlugin'),
        'code_executor': ('code_executor', 'CodeExecutorPlugin'),
        'image_generator': ('image_generator', 'register_image_generator'),
        'animacao_3d': ('animacao_3d', 'get_plugin'),
        'viz_engine': ('viz_engine', 'VisualizationEngine'),
        'physics_plugin': ('physics_plugin', 'PhysicsPlugin'),
        'super_ia_module': ('super_ia_module', 'SuperIAPlugin'),
        'imax_interface_termux': ('imax_interface_termux', 'IMAXTerminalInterface')
    }
    
    for plugin_name, (module_name, attr_name) in plugin_mapping.items():
        try:
            module = importlib.import_module(f'plugins.{module_name}')
            plugin_func = getattr(module, attr_name)
            plugins[plugin_name] = plugin_func()
            print(f'✅ {plugin_name} carregado como {attr_name}')
        except Exception as e:
            print(f'⚠️  {plugin_name} não disponível: {e}')
    
    return plugins

# Carregamento rápido para teste
if __name__ == '__main__':
    print("🔧 Carregando plugins...")
    plugins = load_plugins()
    print(f"🎯 {len(plugins)} plugins carregados com sucesso!")
    print("📋 Plugins disponíveis:", list(plugins.keys()))
