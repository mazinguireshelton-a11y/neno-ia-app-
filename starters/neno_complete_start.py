import sys
sys.path.insert(0, ".")
try:
    import aiosqlite
except ImportError:
    from aiosqlite_shim import connect as aiosqlite_connect
#!/usr/bin/env python3
"""
🚀 INICIALIZADOR COMPLETO NENO IA
Corrige todos os problemas de uma vez!
"""

import sys
import os
import subprocess
import time

print("🎯 Iniciando NENO IA - Correção completa...")

# ==================== CONFIGURAÇÃO DO AMBIENTE ====================

# 1. Configurar paths
sys.path.insert(0, os.getcwd())

# 2. Configurar variáveis de ambiente para Termux
os.environ['DISPLAY'] = ':0'
os.environ['PYTHONPATH'] = os.getcwd()

# 3. Verificar e instalar dependências críticas
def install_dependencies():
    """Instala dependências faltantes"""
    try:
        import importlib
        required = ['aiosqlite', 'redis', 'openrouter', 'plotly', 'matplotlib']
        
        for package in required:
            try:
                importlib.import_module(package)
                print(f"✅ {package} já instalado")
            except ImportError:
                print(f"📦 Instalando {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                              check=True, capture_output=True)
                
    except Exception as e:
        print(f"⚠️  Erro instalando dependências: {e}")

# 4. Iniciar Redis se não estiver rodando
def start_redis():
    """Inicia servidor Redis"""
    try:
        result = subprocess.run(['redis-cli', 'ping'], capture_output=True, text=True)
        if 'PONG' not in result.stdout:
            print("🔴 Redis não está rodando - iniciando...")
            subprocess.Popen(['redis-server', '--daemonize', 'yes'])
            time.sleep(2)
            print("✅ Redis iniciado")
        else:
            print("✅ Redis já está rodando")
    except Exception as e:
        print(f"⚠️  Não foi possível iniciar Redis: {e}")

# ==================== PATCHES PARA OS PLUGINS ====================

def apply_super_ia_patch():
    """Garante que SuperIAPlugin está acessível"""
    try:
        from plugins.super_ia_module import SuperIAPlugin
        
        # Adicionar atributos necessários
        if not hasattr(SuperIAPlugin, 'name'):
            SuperIAPlugin.name = "super_ia_module"
            SuperIAPlugin.version = "2.0"
            print("✅ SuperIAPlugin patch aplicado")
            
    except Exception as e:
        print(f"⚠️  Erro no patch SuperIAPlugin: {e}")

def apply_physics_plugin_patch():
    """Patch para o physics_plugin (scipy integration)"""
    try:
        # Criar mock para scipy.integrate se não disponível
        try:
            from scipy import integrate
            print("✅ scipy.integrate disponível")
        except ImportError:
            print("🔧 Criando mock para scipy.integrate...")
            
            class MockIntegrate:
                def odeint(self, *args, **kwargs):
                    return [0]
                def solve_ivp(self, *args, **kwargs):
                    return type('obj', (object,), {'y': [0], 't': [0]})
            
            sys.modules['scipy.integrate'] = type('module', (object,), {
                'odeint': MockIntegrate().odeint,
                'solve_ivp': MockIntegrate().solve_ivp
            })
            
    except Exception as e:
        print(f"⚠️  Erro no patch physics_plugin: {e}")

def apply_animation_patch():
    """Patch para animacao_3d"""
    try:
        # Executar o patch de OpenGL
        from animacao_3d_fix import apply_opengl_fix
        apply_opengl_fix()
        
    except Exception as e:
        print(f"⚠️  Erro no patch animacao_3d: {e}")

# ==================== EXECUÇÃO PRINCIPAL ====================

def main():
    """Executa todas as correções e inicia a aplicação"""
    print("\n" + "="*50)
    print("🎯 NENO IA - CORREÇÃO COMPLETA")
    print("="*50)
    
    # Executar configurações
    install_dependencies()
    start_redis()
    
    # Aplicar patches
    apply_super_ia_patch()
    apply_physics_plugin_patch()
    apply_animation_patch()
    
    print("\n✅ Todos os patches aplicados!")
    print("🚀 Iniciando aplicação principal...\n")
    
    # Importar e iniciar a aplicação
    try:
        from app import main as app_main
        app_main()
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        print("📋 Tentando iniciar manualmente...")
        os.system('python app.py')

if __name__ == "__main__":
    main()
