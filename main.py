import sys
import os

print("=== DIAGNÓSTICO ===")
print(f"Python: {sys.version}")
print(f"Diretório atual: {os.getcwd()}")
print(f"Arquivos no diretório: {os.listdir('.')}")
print(f"PORT environment: {os.getenv('PORT', 'não definida')}")
print("===================")

from fastapi import FastAPI

# Criar a aplicação FastAPI
app = FastAPI(title="Neno IA App", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "API funcionando!",
        "status": "online",
        "environment": os.getenv("ENVIRONMENT", "production")
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "python": sys.version.split()[0],
        "app": "Neno IA App"
    }

@app.get("/teste")
async def teste():
    return {"mensagem": "Rota de teste funcionando!"}

# Este bloco só executa se rodar diretamente (python main.py)
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Iniciando servidor na porta {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
