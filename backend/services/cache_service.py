import redis
import json
from typing import Optional, Any
from functools import wraps
import hashlib
import time

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
        
    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except (redis.RedisError, json.JSONDecodeError):
            return None
            
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Define valor no cache"""
        try:
            serialized = json.dumps(value)
            return self.redis_client.setex(key, expire, serialized)
        except (redis.RedisError, TypeError):
            return False
            
    def delete(self, key: str) -> bool:
        """Remove valor do cache"""
        try:
            return self.redis_client.delete(key) > 0
        except redis.RedisError:
            return False

# Decorator para cache automático
def cached(expire: int = 300, key_prefix: str = "cache"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_service = current_app.cache_service
            # Gerar chave única baseada nos argumentos
            key = f"{key_prefix}:{f.__name__}:{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # Tentar obter do cache
            cached_result = cache_service.get(key)
            if cached_result is not None:
                return cached_result
                
            # Executar função e cachear resultado
            result = f(*args, **kwargs)
            cache_service.set(key, result, expire)
            return result
        return decorated_function
    return decorator
