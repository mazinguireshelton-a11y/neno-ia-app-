#!/usr/bin/env python3
# 🔧 CORREÇÃO AUTOMÁTICA DO SERVIDOR

import os
import shutil

def fix_server():
    print("🔧 CORRIGINDO SERVIDOR NENO IA")
    print("=" * 50)
    
    # 1. Backup do arquivo original
    if os.path.exists("backend/app.py"):
        shutil.copy2("backend/app.py", "backend/app.py.backup")
        print("✅ Backup criado: backend/app.py.backup")
    
    # 2. Verificar qual framework está sendo usado
    with open("backend/app.py", 'r') as f:
        content = f.read()
    
    is_flask = 'Flask' in content
    is_fastapi = 'FastAPI' in content
    
    print(f"🔧 Framework detectado: {'Flask' if is_flask else 'FastAPI' if is_fastapi else 'Não identificado'}")
    
    # 3. Criar versão corrigida
    if is_fastapi:
        corrected_content = '''#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from config import Config

app = FastAPI(title="NENO IA API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "NENO IA API está funcionando!", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "NENO IA"}

@app.get("/api/health")
async def api_health():
    return {"status": "healthy", "api": "v1"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Iniciando NENO IA na porta {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
'''
    else:
        # Versão Flask
        corrected_content = '''#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys
from pathlib import Path

# Adicionar o diretório atual ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

app = Flask(__name__)
CORS(app)

@app.route("/")
def root():
    return jsonify({"message": "NENO IA está funcionando!", "status": "online"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "NENO IA"})

@app.route("/api/health")
def api_health():
    return jsonify({"status": "healthy", "api": "v1"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"🚀 Iniciando NENO IA na porta {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
'''
    
    # 4. Salvar arquivo corrigido
    with open("backend/app.py", 'w') as f:
        f.write(corrected_content)
    
    print("✅ Arquivo app.py corrigido")
    
    # 5. Testar a correção
    print("\n🧪 Testando correção...")
    try:
        # Testar import
        sys.path.insert(0, 'backend')
        import app
        print("✅ Importação bem-sucedida")
        
        # Verificar se tem as rotas básicas
        if hasattr(app, 'app'):
            print("✅ Aplicação inicializada")
        else:
            print("❌ Problema na aplicação")
            
    except Exception as e:
        print(f"❌ Erro na correção: {e}")
        # Restaurar backup
        if os.path.exists("backend/app.py.backup"):
            shutil.copy2("backend/app.py.backup", "backend/app.py")
            print("✅ Backup restaurado")

if __name__ == "__main__":
    fix_server()
