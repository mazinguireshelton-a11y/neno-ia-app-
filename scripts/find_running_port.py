#!/usr/bin/env python3
# 🔍 DESCOBRIR EM QUAL PORTA ESTÁ RODANDO

import subprocess
import requests
import time
import os

def find_running_port():
    print("🔍 PROCURANDO PORTA DO SERVIDOR")
    print("=" * 40)
    
    # Verificar processos Python
    result = subprocess.run(["pgrep", "-f", "python.*app.py"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        pids = result.stdout.strip().split('\n')
        print(f"📊 Processos encontrados: {len(pids)}")
        
        for pid in pids:
            if pid:
                # Verificar portas usadas pelo processo
                result = subprocess.run(["netstat", "-tlnp"], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if pid in line and 'python' in line:
                        print(f"🔧 Processo {pid} usando: {line.strip()}")
    else:
        print("❌ Nenhum processo app.py encontrado")
    
    # Testar portas comuns
    common_ports = [5000, 8000, 8080, 3000, 8001, 5001]
    
    print("\n🔍 Testando portas comuns...")
    for port in common_ports:
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=2)
            if response.status_code == 200:
                print(f"🎯 SERVIDOR ENCONTRADO NA PORTA {port}!")
                print(f"   📡 URL: http://localhost:{port}")
                print(f"   📄 Status: {response.json()}")
                return port
        except:
            pass
    
    print("❌ Servidor não encontrado em nenhuma porta comum")
    return None

if __name__ == "__main__":
    find_running_port()
