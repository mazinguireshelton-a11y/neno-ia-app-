#!/usr/bin/env python3
# 🧪 TESTE SIMPLES E DIRETO

import subprocess
import time
import requests
import os

def test_simple():
    print("🎯 TESTE SIMPLES - SERVIDOR NENO IA")
    print("=" * 40)
    
    # 1. Parar processos anteriores
    os.system("pkill -f 'python.*app.py' 2>/dev/null")
    time.sleep(2)
    
    # 2. Iniciar servidor
    print("🚀 Iniciando...")
    process = subprocess.Popen(
        ["python", "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 3. Aguardar e testar
    time.sleep(8)
    
    # 4. Testar conexão
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        if response.status_code == 200:
            print("✅ SERVIDOR FUNCIONANDO!")
            print(f"📄 Resposta: {response.json()}")
        else:
            print(f"❌ Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Não consegui conectar: {e}")
    
    # 5. Parar servidor
    process.terminate()
    process.wait()
    print("🎯 TESTE CONCLUÍDO")

if __name__ == "__main__":
    test_simple()
