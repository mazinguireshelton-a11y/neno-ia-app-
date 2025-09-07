#!/usr/bin/env python3
"""
🎬 IMAX Terminal Starter - Versão Termux
"""

import sys
import os

# Adicionar o backend ao path
sys.path.append('backend')

def main():
    print("🎬 Iniciando Hollywood IMAX Studio (Termux)...")
    
    try:
        from plugins.imax_interface_termux import main as imax_main
        imax_main()
    except ImportError as e:
        print(f"❌ Erro: {e}")
        print("💡 Verifique se o arquivo imax_interface_termux.py existe")

if __name__ == "__main__":
    main()
