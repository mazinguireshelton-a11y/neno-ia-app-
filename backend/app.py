from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncpg
import redis
import logging

from config import config
from routes import auth, chat, voice, cooperative, super_compute, modes, uploads

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Iniciando NENO IA Backend")
    
    # Conectar ao banco
    try:
        app.state.db = await asyncpg.connect(config.DATABASE_URL)
        logger.info("✅ Conectado ao banco de dados")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao banco: {e}")
        app.state.db = None
    
    # Conectar ao Redis
    try:
        app.state.redis = redis.Redis.from_url(config.REDIS_URL)
        app.state.redis.ping()
        logger.info("✅ Conectado ao Redis")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar ao Redis: {e}")
        app.state.redis = None
    
    yield
    
    # Shutdown
    if app.state.db:
        await app.state.db.close()
    if app.state.redis:
        app.state.redis.close()

app = FastAPI(
    title="NENO IA API",
    description="API da IA mais poderosa do mundo",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(voice.router, prefix="/voice", tags=["voice"])
app.include_router(cooperative.router, prefix="/cooperative", tags=["cooperative"])
app.include_router(super_compute.router, prefix="/super-compute", tags=["super-compute"])
app.include_router(modes.router, prefix="/modes", tags=["modes"])
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])

@app.get("/")
async def root():
    return {"message": "🚀 NENO IA API está funcionando!", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected" if app.state.db else "disconnected",
        "redis": "connected" if app.state.redis and app.state.redis.ping() else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
