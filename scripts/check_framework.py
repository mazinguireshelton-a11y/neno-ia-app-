#!/usr/bin/env python3
# 🔍 VERIFICAR SE É FASTAPI OU FLASK

import os
import re

def check_framework():
    print("🔍 ANALISANDO FRAMEWORK DO PROJETO")
    print("=" * 50)
    
    # Verificar app.py
    if os.path.exists("backend/app.py"):
        with open("backend/app.py", "r") as f:
            content = f.read()
        
        print("📄 ANALISANDO backend/app.py:")
        
        # Procurar por imports
        flask_imports = re.findall(r'from flask|import Flask', content)
        fastapi_imports = re.findall(r'from fastapi|import FastAPI', content)
        
        if flask_imports:
            print("✅ FRAMEWORK: Flask")
            print(f"   🔧 Imports encontrados: {flask_imports}")
        elif fastapi_imports:
            print("✅ FRAMEWORK: FastAPI") 
            print(f"   🔧 Imports encontrados: {fastapi_imports}")
        else:
            print("❌ Nenhum framework identificado")
        
        # Procurar por inicialização
        if 'app.run(' in content:
            print("   🚀 Inicialização: Flask app.run()")
        elif 'uvicorn.run(' in content:
            print("   🚀 Inicialização: FastAPI uvicorn.run()")
        
        # Verificar porta
        port_match = re.search(r'port=(\d+)', content)
        if port_match:
            print(f"   📡 Porta: {port_match.group(1)}")
    
    # Verificar requirements.txt
    if os.path.exists("backend/requirements.txt"):
        with open("backend/requirements.txt", "r") as f:
            req_content = f.read()
        
        print("\n📦 ANALISANDO backend/requirements.txt:")
        
        if 'fastapi' in req_content.lower():
            print("✅ FastAPI nos requirements")
        if 'flask' in req_content.lower():
            print("✅ Flask nos requirements")
        if 'uvicorn' in req_content.lower():
            print("✅ Uvicorn nos requirements (FastAPI)")
    
    # Testar importação real
    print("\n🧪 TESTANDO IMPORTAÇÃO:")
    try:
        import sys
        sys.path.insert(0, 'backend')
        
        import app
        app_type = type(app.app).__name__
        print(f"✅ App importada: {app_type}")
        
        if 'FastAPI' in app_type:
            print("🎯 CONFIRMADO: FastAPI")
        elif 'Flask' in app_type:
            print("🎯 CONFIRMADO: Flask")
        else:
            print(f"⚠️ Tipo desconhecido: {app_type}")
            
    except Exception as e:
        print(f"❌ Erro na importação: {e}")

def check_dependencies():
    print("\n🔧 VERIFICANDO DEPENDÊNCIAS INSTALADAS:")
    
    try:
        import fastapi
        print(f"✅ FastAPI instalado: {fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI não instalado")
    
    try:
        import flask
        print(f"✅ Flask instalado: {flask.__version__}")
    except ImportError:
        print("❌ Flask não instalado")
    
    try:
        import uvicorn
        print(f"✅ Uvicorn instalado: {uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn não instalado")

if __name__ == "__main__":
    check_framework()
    check_dependencies()
