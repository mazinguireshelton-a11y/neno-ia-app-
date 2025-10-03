#!/usr/bin/env python3
"""
🎬 IMAX Render Starter - Inicializador da interface de renderização
"""

import sys
import os

# Adicionar o backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    print("🎬 Iniciando Hollywood IMAX Production Studio...")
    print("📂 Verificando dependências...")
    
    try:
        # Tentar importar as dependências
        from plugins.imax_interface import main as imax_main
        print("✅ Módulos carregados com sucesso!")
        print("🚀 Iniciando interface gráfica...")
        
        # Iniciar a interface
        imax_main()
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("📦 Instalando dependências necessárias...")
        
        # Instalar dependências automaticamente
        try:
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "pyqt5", "matplotlib", "numpy"], check=True)
            print("✅ Dependências instaladas com sucesso!")
            print("🔄 Reiniciando aplicação...")
            
            # Reiniciar
            from plugins.imax_interface import main as imax_main
            imax_main()
            
        except Exception as install_error:
            print(f"❌ Erro na instalação: {install_error}")
            print("💡 Execute manualmente: pip install pyqt5 matplotlib numpy")

if __name__ == "__main__":
    main()
