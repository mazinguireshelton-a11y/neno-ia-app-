#!/usr/bin/env python3
# 🧪 TESTAR AMBOS OS FRAMEWORKS

import subprocess
import time
import requests
import os
import sys

def test_framework(port, framework_name):
    print(f"🧪 TESTANDO {framework_name.upper()} NA PORTA {port}")
    
    # Parar processos
    os.system(f"pkill -f 'python.*{port}' 2>/dev/null")
    time.sleep(2)
    
    # Tentar iniciar app.py original
    try:
        process = subprocess.Popen(
            [sys.executable, "backend/app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(8)
        
        # Testar conexão
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {framework_name} FUNCIONANDO na porta {port}!")
                return True, process
        except:
            pass
        
        # Se não funcionou, parar processo
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Erro com {framework_name}: {e}")
    
    return False, None

def main():
    print("🎯 TESTANDO AMBOS OS FRAMEWORKS")
    print("=" * 45)
    
    # Testar FastAPI (porta comum: 8000)
    fastapi_ok, fastapi_process = test_framework(8000, "FastAPI")
    
    # Testar Flask (porta comum: 5000) 
    flask_ok, flask_process = test_framework(5000, "Flask")
    
    # Testar porta 5000 para FastAPI também (às vezes usam 5000)
    if not fastapi_ok:
        fastapi_ok, fastapi_process = test_framework(5000, "FastAPI")
    
    print(f"\n📊 RESULTADOS:")
    print(f"   FastAPI: {'✅' if fastapi_ok else '❌'}")
    print(f"   Flask: {'✅' if flask_ok else '❌'}")
    
    # Parar processos
    for process in [fastapi_process, flask_process]:
        if process and process.poll() is None:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    main()
