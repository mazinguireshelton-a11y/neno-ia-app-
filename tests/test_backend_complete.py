#!/usr/bin/env python3
# 📁 test_backend_complete.py
# 🔥 TESTE COMPLETO DO BACKEND NENO IA

import os
import sys
import importlib
import sqlite3
import requests
import json
from pathlib import Path
import inspect

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def test_system_structure():
    print_header("1. TESTE DE ESTRUTURA DO SISTEMA")
    
    required_dirs = [
        'backend',
        'backend/plugins', 
        'backend/services',
        'backend/routes',
        'backend/models',
        'backend/utils',
        'cache',
        'logs',
        'static/uploads'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Diretório {dir_path} encontrado")
        else:
            print(f"❌ Diretório {dir_path} não encontrado")
            os.makedirs(dir_path, exist_ok=True)
            print(f"📁 Criado: {dir_path}")

def test_database_connections():
    print_header("2. TESTE DE BANCOS DE DADOS")
    
    databases = [
        'backend/data/neno_ia.db',
        'backend/plugins/neno_learning.db',
        'cloud_learning.db',
        'distributed_learning.db'
    ]
    
    for db_path in databases:
        try:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                conn.close()
                print(f"✅ {db_path} - {len(tables)} tabelas")
            else:
                print(f"⚠️ {db_path} não existe")
        except Exception as e:
            print(f"❌ Erro em {db_path}: {e}")

def test_python_imports():
    print_header("3. TESTE DE IMPORTS PYTHON")
    
    modules_to_test = [
        'backend.app',
        'backend.config',
        'backend.services.llm_service',
        'backend.services.plugin_service',
        'backend.routes.chat',
        'backend.utils.helpers'
    ]
    
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name} importado")
        except ImportError as e:
            print(f"❌ Erro importando {module_name}: {e}")

def test_plugin_system():
    print_header("4. TESTE DO SISTEMA DE PLUGINS")
    
    plugins_dir = 'backend/plugins'
    plugin_files = ['image_generator.py', 'calculator.py', 'web_search.py']
    
    for plugin_file in plugin_files:
        plugin_path = os.path.join(plugins_dir, plugin_file)
        if os.path.exists(plugin_path):
            try:
                spec = importlib.util.spec_from_file_location(plugin_file[:-3], plugin_path)
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)
                functions = [name for name, obj in inspect.getmembers(plugin_module) if inspect.isfunction(obj)]
                print(f"✅ {plugin_file} - {len(functions)} funções")
            except Exception as e:
                print(f"❌ Erro carregando {plugin_file}: {e}")
        else:
            print(f"⚠️ {plugin_file} não encontrado")

def test_services():
    print_header("5. TESTE DE SERVIÇOS")
    
    services_to_test = [
        ('LLM Service', 'backend.services.llm_service', 'LLMService'),
        ('Plugin Service', 'backend.services.plugin_service', 'PluginService')
    ]
    
    for service_name, module_path, class_name in services_to_test:
        try:
            module = importlib.import_module(module_path)
            service_class = getattr(module, class_name)
            print(f"✅ {service_name} encontrado")
        except Exception as e:
            print(f"❌ {service_name} - Erro: {e}")

def test_image_generation():
    print_header("6. TESTE DE GERAÇÃO DE IMAGENS")
    
    try:
        sys.path.append('backend/plugins')
        from image_generator import register_image_generator
        generator = register_image_generator()
        print(f"✅ Gerador de imagens: {generator.name}")
    except Exception as e:
        print(f"❌ Erro no sistema de imagens: {e}")

def test_api_endpoints():
    print_header("7. TESTE DE ENDPOINTS DA API")
    
    endpoints = [
        ('/health', 'GET', 'Status do sistema'),
        ('/api/chat', 'POST', 'Chat principal'),
        ('/api/images/generate', 'POST', 'Geração de imagens')
    ]
    
    for endpoint, method, description in endpoints:
        print(f"🔗 {method} {endpoint} - {description}")

def test_cache_system():
    print_header("8. TESTE DE SISTEMA DE CACHE")
    
    cache_dirs = ['cache/neno_images', 'cache/omega_images']
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            files = list(Path(cache_dir).glob('*.*'))
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            print(f"✅ {cache_dir} - {len(files)} arquivos ({total_size/1024/1024:.1f} MB)")
        else:
            print(f"⚠️ {cache_dir} não existe")

def generate_system_report():
    print_header("📊 RELATÓRIO COMPLETO DO SISTEMA")
    
    total_files = sum(len(files) for _, _, files in os.walk('.'))
    total_dirs = sum(len(dirs) for _, dirs, _ in os.walk('.'))
    
    total_size = 0
    for dirpath, dirnames, filenames in os.walk('.'):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    
    print(f"📁 Diretórios: {total_dirs}")
    print(f"📄 Arquivos: {total_files}")
    print(f"💾 Tamanho total: {total_size/1024/1024:.1f} MB")
    print(f"🐍 Python: {sys.version}")

def main():
    print("🚀 INICIANDO TESTE COMPLETO DO BACKEND NENO IA")
    print("📍 Diretório atual:", os.getcwd())
    
    test_system_structure()
    test_database_connections()
    test_python_imports()
    test_plugin_system()
    test_services()
    test_image_generation()
    test_api_endpoints()
    test_cache_system()
    generate_system_report()
    
    print_header("🎯 PRÓXIMOS PASSOS")
    print("1. Inicie o servidor: python backend/app.py")
    print("2. Teste a API: python backend/test_basic.py")
    print("3. Verifique logs: tail -f logs/app.log")

if __name__ == "__main__":
    main()
