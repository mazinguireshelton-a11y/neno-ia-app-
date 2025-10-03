import importlib
import inspect
import os
import sys

def analyze_plugin_simple(plugin_name):
    """Análise simples e direta dos plugins"""
    try:
        print(f"\n🔍 {plugin_name}:")
        
        # Importar o módulo
        module = importlib.import_module(f"plugins.{plugin_name}")
        
        # Verificar funções de registro
        if hasattr(module, 'register'):
            reg_func = getattr(module, 'register')
            if callable(reg_func):
                try:
                    result = reg_func()
                    print(f"✅ register() -> {type(result).__name__}")
                    if hasattr(result, 'name'):
                        print(f"   Nome: {result.name}")
                except Exception as e:
                    print(f"❌ register() erro: {e}")
        
        if hasattr(module, 'get_plugin'):
            get_func = getattr(module, 'get_plugin')
            if callable(get_func):
                try:
                    result = get_func()
                    print(f"✅ get_plugin() -> {type(result).__name__}")
                    if hasattr(result, 'name'):
                        print(f"   Nome: {result.name}")
                except Exception as e:
                    print(f"❌ get_plugin() erro: {e}")
        
        # Procurar por instâncias de plugin
        plugin_instances = []
        for name in dir(module):
            obj = getattr(module, name)
            if (not name.startswith('_') and not inspect.isclass(obj) and
                (hasattr(obj, 'execute') or hasattr(obj, 'name') or 'plugin' in name.lower())):
                plugin_instances.append((name, obj))
        
        if plugin_instances:
            print("✅ Instâncias encontradas:")
            for name, obj in plugin_instances:
                obj_type = type(obj).__name__
                if hasattr(obj, 'name'):
                    print(f"   {name} ({obj_type}): {getattr(obj, 'name', 'Sem nome')}")
                else:
                    print(f"   {name} ({obj_type})")
        
        # Procurar por classes de plugin
        plugin_classes = []
        for name in dir(module):
            obj = getattr(module, name)
            if (inspect.isclass(obj) and 
                ('Plugin' in name or hasattr(obj, 'execute'))):
                plugin_classes.append((name, obj))
        
        if plugin_classes:
            print("✅ Classes encontradas:")
            for name, obj in plugin_classes:
                print(f"   {name}")
                
    except Exception as e:
        print(f"❌ Erro analisando {plugin_name}: {e}")

# Lista de plugins para analisar
plugins = [
    'super_ia_module',
    'animacao_3d',
    'physics_plugin',
    'web_search',
    'calculator',
    'code_executor', 
    'image_generator',
    'viz_engine',
    'imax_interface_termux'
]

print("🎯 ANÁLISE COMPLETA DOS PLUGINS")
print("=" * 50)

for plugin in plugins:
    analyze_plugin_simple(plugin)

print("\n" + "=" * 50)
print("✅ Análise concluída!")
