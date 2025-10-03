#!/usr/bin/env python3
# 🔍 INSPECIONAR ARQUIVO app.py

import os

def inspect_app():
    print("🔍 INSPEÇÃO DO backend/app.py")
    print("=" * 50)
    
    if not os.path.exists("backend/app.py"):
        print("❌ Arquivo não encontrado")
        return
    
    with open("backend/app.py", 'r') as f:
        content = f.read()
    
    print(f"📏 Tamanho: {len(content)} caracteres")
    print(f"📄 Linhas: {len(content.splitlines())}")
    
    # Analisar conteúdo
    lines = content.splitlines()
    
    print("\n🔧 DETALHES IMPORTANTES:")
    
    # Procurar por padrões importantes
    patterns = {
        'if __name__': 'Ponto de entrada principal',
        'app.run': 'Inicialização do servidor',
        'uvicorn.run': 'Inicialização Uvicorn (FastAPI)',
        'port=': 'Configuração de porta',
        'host=': 'Configuração de host',
        'import Flask': 'Import do Flask',
        'import FastAPI': 'Import do FastAPI',
    }
    
    for i, line in enumerate(lines):
        for pattern, description in patterns.items():
            if pattern in line:
                print(f"   ✅ Linha {i+1}: {description}")
                print(f"      {line.strip()}")
    
    # Mostrar as primeiras 10 linhas
    print("\n📋 PRIMEIRAS LINHAS:")
    for i, line in enumerate(lines[:10]):
        print(f"   {i+1:2d}: {line}")
    
    # Mostrar as últimas 10 linhas
    print("\n📋 ÚLTIMAS LINHAS:")
    for i, line in enumerate(lines[-10:], start=len(lines)-9):
        print(f"   {i+1:2d}: {line}")

if __name__ == "__main__":
    inspect_app()
