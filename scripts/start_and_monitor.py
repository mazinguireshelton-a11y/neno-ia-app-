#!/usr/bin/env python3
# 🚀 INICIAR E MONITORAR SERVIDOR

import subprocess
import time
import requests
import os
import sys

def start_and_monitor():
    print("🚀 INICIANDO SERVIDOR COM MONITORAMENTO")
    print("=" * 50)
    
    # Parar processos anteriores
    os.system("pkill -f 'python.*app.py' 2>/dev/null")
    time.sleep(2)
    
    # Iniciar servidor
    print("🔥 Iniciando servidor...")
    process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Monitorar inicialização
    print("📡 Aguardando inicialização...")
    
    for i in range(30):  # 30 tentativas de 1 segundo
        time.sleep(1)
        
        # Verificar se processo ainda está rodando
        if process.poll() is not None:
            print("❌ Processo terminou prematuramente!")
            # Ler erros
            errors = process.stderr.read()
            if errors:
                print("🔍 Últimos erros:")
                print(errors[-500:])  # Últimos 500 caracteres
            return False
        
        # Testar conexão na porta 5000
        try:
            response = requests.get("http://localhost:5000/health", timeout=2)
            if response.status_code == 200:
                print("✅ SERVIDOR RODANDO NA PORTA 5000!")
                print(f"📄 Resposta: {response.json()}")
                
                # Manter servidor rodando e testar funcionalidades
                print("\n🎯 TESTANDO FUNCIONALIDADES:")
                
                # Testar chat
                try:
                    response = requests.post(
                        "http://localhost:5000/api/chat",
                        json={"message": "Olá, estou testando o sistema. Pode me responder?", "mode": "standard"},
                        timeout=10
                    )
                    if response.status_code == 200:
                        data = response.json()
                        print("💬 CHAT FUNCIONANDO!")
                        print(f"🤖 Resposta: {data.get('response', '')[:200]}...")
                    else:
                        print(f"⚠️ Chat retornou status: {response.status_code}")
                except Exception as e:
                    print(f"❌ Erro no chat: {e}")
                
                # Testar listagem de plugins
                try:
                    response = requests.get("http://localhost:5000/api/plugins", timeout=5)
                    if response.status_code == 200:
                        plugins = response.json()
                        print(f"🔌 {len(plugins.get('plugins', []))} plugins disponíveis")
                except:
                    print("⚠️ Não foi possível listar plugins")
                
                print(f"\n🎉 SERVIDOR FUNCIONANDO PERFEITAMENTE!")
                print(f"🌐 ACESSE: http://localhost:5000")
                print(f"⏹️  Para parar: Ctrl+C")
                
                # Manter processo rodando
                try:
                    process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Servidor parado pelo usuário")
                    process.terminate()
                
                return True
                
        except requests.exceptions.ConnectionError:
            if i % 5 == 0:  # Mostrar progresso a cada 5 segundos
                print(f"⏳ Aguardando... ({i+1}/30 segundos)")
        except Exception as e:
            print(f"⚠️ Erro de teste: {e}")
    
    print("❌ Servidor não iniciou em 30 segundos")
    process.terminate()
    return False

if __name__ == "__main__":
    start_and_monitor()
