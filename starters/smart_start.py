#!/usr/bin/env python3
"""
🎯 INICIALIZADOR INTELIGENTE - USA SEUS ARQUIVOS ORIGINAIS!
"""

import sys
import os

# Configurar environment
sys.path.insert(0, os.getcwd())

print("🚀 Iniciando NENO IA com arquivos ORIGINAIS...")

# Apenas patches ESSENCIAIS
try:
    from scipy import integrate
except ImportError:
    print("🔧 Usando shim para scipy.integrate...")
    from scipy_integrate_shim import integrate
    sys.modules['scipy.integrate'] = integrate

# Importar e iniciar SEU código original
from app import main

if __name__ == "__main__":
    main()
