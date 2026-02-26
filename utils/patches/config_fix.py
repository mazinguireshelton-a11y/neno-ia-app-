import os

# Configurações corrigidas para Termux
class Config:
    # Usar SQLite em vez de Redis para Termux
    REDIS_URL = "redis://localhost:6379"  # Mas vamos desativar Redis
    USE_REDIS = False  # Desativa Redis no Termux
    
    # Configuração do servidor
    HOST = "0.0.0.0"
    PORT = 5000  # Usar porta 5000 em vez de 8000
    DEBUG = True
    
    # Configurações de banco de dados
    DATABASE_URL = "sqlite:///./neno_ia.db"
    
    # Configurações de API
    API_PREFIX = "/api"
    
    @classmethod
    def check_redis(cls):
        """Verifica se Redis está disponível"""
        try:
            import redis
            r = redis.Redis.from_url(cls.REDIS_URL, socket_connect_timeout=1)
            r.ping()
            return True
        except:
            return False

# Atualiza USE_REDIS baseado na disponibilidade
Config.USE_REDIS = Config.check_redis()
print(f"🔧 Redis {'✅ disponível' if Config.USE_REDIS else '❌ não disponível - usando fallback'}")
