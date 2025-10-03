#!/usr/bin/env python3
# 🧪 TESTE NA PORTA 5000

import subprocess
import time
import requests
import os
import sys

def test_port_5000():
    print("🎯 TESTANDO SERVIDOR NA PORTA 5000")
    print("=" * 45)
    
    # Parar processos
    os.system("pkill -f 'python.*app.py' 2>/dev/null")
    time.sleep(2)
    
    # Iniciar servidor
    print("🚀 Iniciando servidor na porta 5000...")
    process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguardar
    print("⏳ Aguardando 10 segundos...")
    time.sleep(10)
    
    # Testar várias portas
    ports_to_test = [5000, 8000, 8080]
    
    for port in ports_to_test:
        try:
            print(f"🔍 Testando porta {port}...")
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ PORTA {port} FUNCIONANDO!")
                print(f"   📄 Resposta: {response.json()}")
                
                # Testar chat também
                response = requests.post(
                    f"http://localhost:{port}/api/chat",
                    json={"message": "Teste de funcionamento", "mode": "standard"},
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"   💬 Chat funcionando na porta {port}!")
                break
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Porta {port} recusou conexão")
        except Exception as e:
            print(f"   ⚠️ Erro na porta {port}: {e}")
    
    # Parar servidor
    if process.poll() is None:
        process.terminate()
        process.wait()
        print("🛑 Servidor parado")

if __name__ == "__main__":
    test_port_5000()
