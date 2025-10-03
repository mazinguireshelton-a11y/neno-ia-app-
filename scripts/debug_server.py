#!/usr/bin/env python3
# 🔧 DEBUG COMPLETO DO SERVIDOR

import os
import sys
import subprocess
import time
import signal

def debug_server():
    print("🔧 DEBUG DO SERVIDOR NENO IA")
    print("=" * 50)
    
    # 1. Verificar se o arquivo app.py existe
    if not os.path.exists("backend/app.py"):
        print("❌ backend/app.py não encontrado!")
        return
    
    print("✅ backend/app.py encontrado")
    
    # 2. Verificar o conteúdo do app.py
    with open("backend/app.py", 'r') as f:
        content = f.read()
        lines = content.split('\n')
        print(f"📄 Arquivo tem {len(lines)} linhas")
        
        # Verificar se é Flask ou FastAPI
        if 'Flask' in content:
            print("🔧 Framework: Flask")
        elif 'FastAPI' in content:
            print("🔧 Framework: FastAPI")
        else:
            print("⚠️ Framework não identificado")
    
    # 3. Testar importação básica
    print("\n🧪 Testando importação...")
    try:
        sys.path.insert(0, 'backend')
        import app
        print("✅ Importação bem-sucedida")
        
        # Verificar tipo da aplicação
        if hasattr(app, 'app'):
            app_type = type(app.app).__name__
            print(f"🔧 Tipo da app: {app_type}")
        else:
            print("❌ App não tem atributo 'app'")
            
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return
    
    # 4. Verificar configurações
    try:
        import config
        print("✅ Configurações carregadas")
        if hasattr(config, 'PORT'):
            print(f"🔧 Porta configurada: {config.PORT}")
        else:
            print("⚠️ Porta não configurada")
    except Exception as e:
        print(f"⚠️ Configurações: {e}")
    
    # 5. Iniciar servidor com debug detalhado
    print("\n🚀 Iniciando servidor com debug...")
    
    # Parar qualquer processo anterior
    os.system("pkill -f 'python.*app.py' 2>/dev/null")
    time.sleep(2)
    
    # Iniciar processo com output em tempo real
    process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    print("⏳ Aguardando inicialização (15 segundos)...")
    
    # Ler output em tempo real
    start_time = time.time()
    output_lines = []
    error_lines = []
    
    while time.time() - start_time < 15:
        # Ler stdout
        stdout_line = process.stdout.readline()
        if stdout_line:
            print(f"📄 [STDOUT] {stdout_line.strip()}")
            output_lines.append(stdout_line)
        
        # Ler stderr
        stderr_line = process.stderr.readline()
        if stderr_line:
            print(f"❌ [STDERR] {stderr_line.strip()}")
            error_lines.append(stderr_line)
        
        # Verificar se processo ainda está rodando
        if process.poll() is not None:
            print("⚠️ Processo terminou prematuramente!")
            break
        
        time.sleep(0.1)
    
    # 6. Verificar status do processo
    if process.poll() is None:
        print("✅ Processo ainda está rodando")
        
        # Testar conexão
        try:
            import requests
            response = requests.get("http://localhost:5000/health", timeout=5)
            print(f"✅ Servidor respondendo: {response.status_code}")
        except Exception as e:
            print(f"❌ Servidor não responde: {e}")
    else:
        return_code = process.poll()
        print(f"❌ Processo terminou com código: {return_code}")
        
        # Mostrar últimas linhas de erro
        if error_lines:
            print("\n🔍 Últimos erros:")
            for line in error_lines[-5:]:
                print(f"   {line.strip()}")
    
    # 7. Parar processo
    if process.poll() is None:
        process.terminate()
        process.wait()
        print("🛑 Processo finalizado")
    
    print(f"\n📊 RESUMO:")
    print(f"   Linhas de output: {len(output_lines)}")
    print(f"   Linhas de erro: {len(error_lines)}")

if __name__ == "__main__":
    debug_server()
