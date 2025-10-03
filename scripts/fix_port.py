#!/usr/bin/env python3
# 🔧 CORREÇÃO DA PORTA DO SERVIDOR

import os
import re

def fix_port():
    print("🔧 CORRIGINDO PORTA DO SERVIDOR")
    print("=" * 45)
    
    # Ler o arquivo atual
    with open("backend/app.py", "r") as f:
        content = f.read()
    
    # Verificar porta atual
    port_match = re.search(r'port=(\d+)', content)
    if port_match:
        current_port = port_match.group(1)
        print(f"📡 Porta atual: {current_port}")
    else:
        print("❌ Porta não encontrada no código")
        return
    
    # Mudar porta 8000 para 5000
    if current_port == "8000":
        new_content = content.replace("port=8000", "port=5000")
        
        # Fazer backup
        os.rename("backend/app.py", "backend/app.py.backup")
        
        # Salvar novo conteúdo
        with open("backend/app.py", "w") as f:
            f.write(new_content)
        
        print("✅ Porta alterada de 8000 para 5000")
        print("📁 Backup salvo como: backend/app.py.backup")
    else:
        print(f"✅ Porta já está como {current_port}")

if __name__ == "__main__":
    fix_port()
