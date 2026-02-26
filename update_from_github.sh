#!/bin/bash
cd ~/neno-ia-app

echo "🔄 INICIANDO ATUALIZAÇÃO DO GITHUB"

# 1. Backup extra de segurança
echo "📦 Fazendo backup extra..."
BACKUP_DIR="../neno-ia-app-PRE-UPDATE-$(date +%Y%m%d_%H%M%S)"
cp -r . "$BACKUP_DIR"
echo "✅ Backup salvo em: $BACKUP_DIR"

# 2. Status atual
echo "🔍 Status atual do Git:"
git status --short

# 3. Salvar trabalho local
echo "💾 Salvando alterações locais..."
git add .
git commit -m "UPDATE: Backup local $(date '+%Y-%m-%d %H:%M:%S')" || echo "⚠️ Nada para commitar"

# 4. Buscar do GitHub
echo "🌐 Buscando do GitHub..."
git fetch origin

# 5. Ver diferenças
echo "📋 Mudanças no GitHub:"
git log HEAD..origin/main --oneline

# 6. Atualizar
echo "🚀 Atualizando..."
git pull origin main --rebase

# 7. Status final
echo "✅ ATUALIZAÇÃO CONCLUÍDA!"
echo "📊 Status final:"
git status --short
echo "🎯 Últimos commits:"
git log --oneline -5

echo "💡 Dica: Se houver problemas, seu backup está em: $BACKUP_DIR"
