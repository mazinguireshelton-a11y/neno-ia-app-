#!/usr/bin/env python3
# 🗣️ COMANDO RÁPIDO PARA FAZER A IA FALAR

import sys
from voz_termux import VozTermux

def main():
    if len(sys.argv) > 1:
        texto = ' '.join(sys.argv[1:])
    else:
        texto = "Olá! Eu sou a NENO IA."
    
    voz = VozTermux()
    voz.falar(texto)

if __name__ == "__main__":
    main()
