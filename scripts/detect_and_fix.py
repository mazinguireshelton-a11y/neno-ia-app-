#!/usr/bin/env python3
# 🎯 DETECTAR E CORRIGIR FRAMEWORK

import os
import subprocess
import sys

def detect_and_fix():
    print("🎯 DETECTANDO E CORRIGINDO FRAMEWORK")
    print("=" * 50)
    
    # 1. Verificar dependências instaladas
    print("1. 🔍 Verificando dependências...")
    
    result = subprocess.run([
        sys.executable, "-c", 
        "try: import fastapi; print('FASTAPI'); exit(0)\n" +
        "except: pass\n" +
        "try: import flask; print('FLASK'); exit(0)\n" + 
        "except: print('NONE')"
    ], capture_output=True, text=True)
    
    framework_installed = result.stdout.strip()
    print(f"   📦 Framework instalado: {framework_installed}")
    
    # 2. Verificar app.py atual
    print("2. 📄 Analisando app.py...")
    
    if os.path.exists("backend/app.py"):
        with open("backend/app.py", "r") as f:
            content = f.read()
        
        is_fastapi = 'FastAPI' in content or 'fastapi' in content
        is_flask = 'Flask' in content or 'flask' in content
        
        print(f"   🔧 No código: {'FastAPI' if is_fastapi else 'Flask' if is_flask else 'Indeterminado'}")
    
    # 3. Recomendar ação
    print("3. 💡 RECOMENDAÇÃO:")
    
    if framework_installed == "FASTAPI" and is_fastapi:
        print("   ✅ Usar FastAPI (já configurado)")
        print("   🚀 Comando: python backend/app.py")
        
    elif framework_installed == "FLASK" and is_flask:
        print("   ✅ Usar Flask (já configurado)")
        print("   🚀 Comando: python backend/app.py")
        
    elif framework_installed == "FASTAPI":
        print("   🔄 FastAPI instalado, mas app.py pode estar para Flask")
        print("   💡 Converter para FastAPI")
        
    elif framework_installed == "FLASK":
        print("   🔄 Flask instalado, mas app.py pode estar para FastAPI") 
        print("   💡 Converter para Flask")
        
    else:
        print("   ❌ Nenhum framework instalado")
        print("   📦 Instalar: pip install fastapi uvicorn")

def create_simple_server():
    print("\n4. 🛠️ Criando servidor simples...")
    
    # Criar versão simples que funciona
    simple_app = '''#!/usr/bin/env python3
# 🚀 SERVIDOR SIMPLES NENO IA

try:
    from fastapi import FastAPI
    import uvicorn
    USING_FASTAPI = True
except:
    from flask import Flask, jsonify
    USING_FASTAPI = False

if USING_FASTAPI:
    app = FastAPI(title="NENO IA")
    
    @app.get("/")
    async def root():
        return {"message": "NENO IA FastAPI funcionando!"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
        
else:
    app = Flask(__name__)
    
    @app.route("/")
    def root():
        return jsonify({"message": "NENO IA Flask funcionando!"})
    
    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"})

if __name__ == "__main__":
    if USING_FASTAPI:
        print("🚀 Iniciando FastAPI na porta 5000")
        uvicorn.run(app, host="0.0.0.0", port=5000)
    else:
        print("🚀 Iniciando Flask na porta 5000")
        app.run(host="0.0.0.0", port=5000, debug=True)
'''
    
    with open("backend/app_simple.py", "w") as f:
        f.write(simple_app)
    
    print("✅ Servidor simples criado: backend/app_simple.py")
    print("🚀 Testar com: python backend/app_simple.py")

if __name__ == "__main__":
    detect_and_fix()
    create_simple_server()
