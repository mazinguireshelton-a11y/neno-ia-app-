import os
from dataclasses import dataclass

@dataclass
class Config:
    # Banco de dados - Usa Supabase PostgreSQL por padrão
    DATABASE_URL: str = os.getenv("DATABASE_URL", os.getenv("SUPABASE_DB_URL", "sqlite+aiosqlite:///data/neno_ia.db"))
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Configurações
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))

config = Config()
