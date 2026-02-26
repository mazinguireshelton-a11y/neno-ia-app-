import importlib
import inspect
from pathlib import Path

def analyze_plugin(plugin_path):
    """Analisa um plugin completamente"""
    try:
        plugin_name = Path(plugin_path).stem
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        print(f"\n🔍 {plugin_name}:")
        
        # Verificar função register
        if hasattr(module, 'register'):
            print("✅ Tem register()")
            reg = module.register()
            print(f"   register() retorna: {type(reg)}")
        
        # Verificar função get_plugin  
        if hasattr(module, 'get_plugin'):
            print("✅ Tem get_plugin()")
            plugin = module.get_plugin()
            print(f"   get_plugin() retorna: {type(plugin)}")
        
        # Verificar instâncias
        instances = []
        for name, obj in inspect.getmembers(module):
            if (hasattr(obj, '__class__') and not inspect.isclass(obj) and
                (hasattr(obj, 'execute') or hasattr(obj, 'name'))):
                instances.append((name, type(obj)))
        
        if instances:
            print("✅ Instâncias encontradas:")
            for name, obj_type in instances:
                print(f"   {name}: {obj_type}")
        
        # Verificar classes
        classes = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if 'Plugin' in name or hasattr(obj, 'execute'):
                classes.append((name, obj))
        
        if classes:
            print("✅ Classes encontradas:")
            for name, obj in classes:
                print(f"   {name}: {obj}")
                
    except Exception as e:
        print(f"❌ Erro analisando {plugin_path}: {e}")

# Analisar todos os plugins
for plugin_file in Path('plugins').glob('*.py'):
    if plugin_file.name != '__init__.py':
        analyze_plugin(plugin_file)
