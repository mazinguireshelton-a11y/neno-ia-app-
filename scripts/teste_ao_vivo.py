#!/usr/bin/env python3
import subprocess
import requests
import time
import sys
import os

def teste_ao_vivo():
    print("🎯 TESTE AO VIVO - INICIANDO SERVIDOR")
    
    # Parar servidor se estiver rodando
    os.system("pkill -f 'python.*app.py' 2>/dev/null")
    time.sleep(2)
    
    # Iniciar servidor
    print("🚀 Iniciando backend...")
    process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguardar
    print("⏳ Aguardando inicialização...")
    time.sleep(10)
    
    # Testar
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ SERVIDOR FUNCIONANDO!")
            print(f"📄 Resposta: {response.text}")
            
            # Testar chat rápido
            print("💬 Testando chat...")
            response = requests.post(
                "http://localhost:5000/api/chat",
                json={"message": "Olá, estou testando o sistema. Pode me responder?", "mode": "standard"},
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ CHAT FUNCIONANDO!")
                print(f"🤖 Resposta: {data.get('response', '')[:100]}...")
            else:
                print(f"⚠️ Chat: {response.status_code}")
                
        else:
            print(f"❌ Servidor: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Parar servidor
    print("🛑 Parando servidor...")
    process.terminate()
    process.wait()
    
    print("\n🎯 TESTE AO VIVO CONCLUÍDO!")

if __name__ == "__main__":
    teste_ao_vivo()
