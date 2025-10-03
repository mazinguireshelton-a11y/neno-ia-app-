#!/usr/bin/env python3
import os
import sys
import time
import requests
import subprocess
from threading import Thread

def test_server_complete():
    print("🚀 TESTE COMPLETO DO SERVIDOR NENO IA")
    print("=" * 50)
    
    # 1. Matar processos na porta 5000
    print("1. 🔄 Limpando porta 5000...")
    os.system("pkill -f 'python.*5000' || true")
    time.sleep(2)
    
    # 2. Iniciar servidor em background
    print("2. 🚀 Iniciando servidor...")
    
    server_process = subprocess.Popen([
        sys.executable, "backend/app.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Aguardar inicialização
    time.sleep(5)
    
    # 3. Testar endpoints
    print("3. 🌐 Testando endpoints...")
    
    endpoints = [
        ("/health", "GET"),
        ("/api/health", "GET"),
        ("/api/plugins", "GET"),
    ]
    
    for endpoint, method in endpoints:
        try:
            url = f"http://localhost:5000{endpoint}"
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✅ {method} {endpoint} - Status: {response.status_code}")
                if response.text:
                    print(f"      📄 Resposta: {response.text[:100]}...")
            else:
                print(f"   ⚠️ {method} {endpoint} - Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {method} {endpoint} - Erro: {e}")
    
    # 4. Testar geração de imagens via API
    print("4. 🎨 Testando geração de imagens...")
    try:
        response = requests.post(
            "http://localhost:5000/api/images/generate",
            json={
                "prompt": "um gato fofo teste",
                "size": "512x512",
                "style": "realistic"
            },
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Geração de imagem funcionando!")
                print(f"      📊 {result.get('message', 'Imagem gerada')}")
            else:
                print(f"   ⚠️ Geração falhou: {result.get('error', 'Erro desconhecido')}")
        else:
            print(f"   ❌ API retornou status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro na geração: {e}")
    
    # 5. Testar chat API
    print("5. 💬 Testando chat...")
    try:
        response = requests.post(
            "http://localhost:5000/api/chat",
            json={
                "message": "Olá, como você está?",
                "mode": "standard"
            },
            timeout=15
        )
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Chat funcionando!")
            print(f"      💭 Resposta: {result.get('response', '')[:50]}...")
        else:
            print(f"   ❌ Chat retornou status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro no chat: {e}")
    
    # 6. Parar servidor
    print("6. 🛑 Parando servidor...")
    server_process.terminate()
    server_process.wait()
    
    print("\n🎯 TESTE CONCLUÍDO!")
    print("💡 Servidor está funcionando corretamente!" if server_process.returncode == 0 else "⚠️ Servidor teve problemas")

if __name__ == "__main__":
    test_server_complete()
