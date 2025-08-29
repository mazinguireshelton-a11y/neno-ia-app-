#!/bin/bash

echo "🚀 Iniciando deploy da NENO IA para hospedagem gratuita"
echo "======================================================"

# Verificar dependências
if ! command -v git &> /dev/null; then
    echo "❌ Git não instalado. Instale primeiro."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "⚠️ Docker não instalado. Alguns deploys podem não funcionar."
fi

# Escolher provedor
echo "🌐 Escolha o provedor de hospedagem:"
echo "1) Render.com"
echo "2) Railway.app" 
echo "3) Heroku"
echo "4) Fly.io"
read -p "Digite o número (1-4): " choice

case $choice in
    1)
        echo "🚀 Configurando para Render.com..."
        # Configurar Render
        if [ ! -f "render.yaml" ]; then
            echo "❌ render.yaml não encontrado. Criando..."
            cat > render.yaml << 'RENDER'
services:
  - type: web
    name: neno-ia-backend
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:\$PORT --workers 2 --timeout 120
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: neno-db
          property: connectionString
RENDER
        fi
        echo "✅ Execute: git push render main"
        ;;
    2)
        echo "⚡ Configurando para Railway.app..."
        # Configurar Railway
        if [ ! -f "railway.toml" ]; then
            cat > railway.toml << 'RAILWAY'
[build]
builder = "nixpacks"

[deploy]
startCommand = "gunicorn app:app --bind 0.0.0.0:\$PORT --workers 2 --timeout 120"

[env]
DATABASE_URL = { from = "POSTGRES_URL" }
RAILWAY
        fi
        echo "✅ Execute: railway link && railway deploy"
        ;;
    3)
        echo "🔧 Configurando para Heroku..."
        # Configurar Heroku
        if [ ! -f "Procfile" ]; then
            echo "web: gunicorn app:app --bind 0.0.0.0:\$PORT --workers 2 --timeout 120" > Procfile
        fi
        echo "✅ Execute: heroku create && git push heroku main"
        ;;
    4)
        echo "🐳 Configurando para Fly.io..."
        # Configurar Fly
        if [ ! -f "fly.toml" ]; then
            cat > fly.toml << 'FLY'
app = "neno-ia"
primary_region = "iad"

[build]

[env]
PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"
  [services.concurrency]
    hard_limit = 25
    soft_limit = 20

  [[services.ports]]
    port = 80
    handlers = ["http"]
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [[services.tcp_checks]]
    interval = 10000
    timeout = 2000
FLY
        fi
        echo "✅ Execute: fly launch && fly deploy"
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo "🎉 Configuração de deploy concluída!"
echo "📋 Siga as instruções acima para fazer deploy"
