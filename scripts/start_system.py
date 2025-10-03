#!/usr/bin/env python3
# 📁 start_system.py
# 🔥 INICIALIZADOR DO SISTEMA NENO IA

import os
import sys
import subprocess
import time

def start_neno_system():
    print("🚀 INICIANDO SISTEMA NENO IA")
    print("⏰ " + time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Verifica se estamos no diretório correto
    if not os.path.exists('backend'):
        print("❌ Diretório 'backend' não encontrado!")
        print("💡 Execute: cd ~/neno-ia-app")
        return
    
    # Verifica requisitos
    print("\n1. 🔍 Verificando requisitos...")
    
    # Python version
    py_version = sys.version_info
    print(f"   Python: {py_version.major}.{py_version.minor}.{py_version.micro}")
    
    # Arquivos essenciais
    essential_files = ['backend/app.py', 'backend/config.py']
    missing_files = []
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos faltantes: {missing_files}")
        return
    
    # Tenta iniciar o servidor
    print("\n2. 🔄 Iniciando servidor...")
    
    try:
        # Verifica se o servidor pode ser importado
        sys.path.insert(0, 'backend')
        import app
        
        print("✅ Módulo app carregado com sucesso!")
        
        # Mostra informações da aplicação
        if hasattr(app, 'app'):
            print("✅ Instância Flask encontrada")
            
            # Tenta obter rotas
            try:
                routes = []
                for rule in app.app.url_map.iter_rules():
                    if rule.endpoint != 'static':
                        routes.append(rule.rule)
                
                print(f"✅ {len(routes)} rotas configuradas")
                print("🌐 Rotas principais:")
                for route in routes[:10]:  # Mostra as primeiras 10 rotas
                    print(f"   🔗 {route}")
                    
            except Exception as e:
                print(f"⚠️ Não foi possível listar rotas: {e}")
                
        else:
            print("❌ Instância Flask não encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao carregar app: {e}")
        print("💡 Tentando método alternativo...")
    
    # Método alternativo: executar via subprocess
    print("\n3. ⚡ Iniciando via subprocess...")
    
    try:
        process = subprocess.Popen([
            sys.executable, 'backend/app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Aguarda um pouco para ver se inicia
        time.sleep(3)
        
        # Verifica se o processo ainda está rodando
        if process.poll() is None:
            print("✅ Servidor iniciado com sucesso!")
            print("🌐 Acesse: http://localhost:5000")
            print("⏹️  Para parar: Ctrl+C")
            
            # Mostra saída inicial
            try:
                output, errors = process.communicate(timeout=2)
                if output:
                    print("📄 Saída do servidor:")
                    print(output[:500] + "..." if len(output) > 500 else output)
            except subprocess.TimeoutExpired:
                print("⚡ Servidor rodando em background...")
                
        else:
            # Processo terminou, mostra erro
            output, errors = process.communicate()
            print("❌ Servidor parou inesperadamente")
            if errors:
                print("📄 Erros:")
                print(errors[:1000])
                
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
    
    print("\n🎯 INICIALIZAÇÃO CONCLUÍDA!")
    print("💡 Comandos úteis:")
    print("   tail -f logs/app.log          # Ver logs")
    print("   python test_backend_complete.py  # Teste completo")
    print("   python quick_start_test.py       # Teste rápido")

if __name__ == "__main__":
    start_neno_system()
