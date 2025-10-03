#!/usr/bin/env python3
import sqlite3
import os

def test_learning_systems():
    print("🧠 TESTE DOS SISTEMAS DE APRENDIZADO")
    print("=" * 45)
    
    databases = {
        'NENO Learning': 'backend/plugins/neno_learning.db',
        'Cloud Learning': 'cloud_learning.db',
        'Distributed Learning': 'distributed_learning.db'
    }
    
    for name, db_path in databases.items():
        print(f"\n📊 {name}:")
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Lista tabelas
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"   ✅ {len(tables)} tabelas encontradas")
                
                # Mostra estatísticas de cada tabela
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                    count = cursor.fetchone()[0]
                    print(f"      📁 {table_name}: {count} registros")
                
                conn.close()
            except Exception as e:
                print(f"   ❌ Erro: {e}")
        else:
            print(f"   ⚠️ Arquivo não encontrado")
    
    print("\n🎯 BANCOS DE APRENDIZADO VERIFICADOS!")

if __name__ == "__main__":
    test_learning_systems()
