import docker
import redis
import json
import logging
import subprocess
import time
from typing import Dict, List, Optional, Any
from threading import Thread
import os

logger = logging.getLogger(__name__)

class ComputeCluster:
    """
    Classe unificada para gerenciamento de cluster de computação
    Combina funcionalidades dos clusters anteriormente separados
    """
    
    def __init__(self, redis_url: str = None):
        self.docker_client = None
        self.redis_client = None
        self.workers = {}
        
        try:
            self.docker_client = docker.from_env()
            logger.info("Cliente Docker inicializado com sucesso")
        except Exception as e:
            logger.warning(f"Docker não disponível: {str(e)}")
        
        if redis_url:
            try:
                self.redis_client = redis.Redis.from_url(redis_url)
                self.redis_client.ping()
                logger.info("Cliente Redis conectado com sucesso")
            except Exception as e:
                logger.warning(f"Redis não disponível: {str(e)}")
    
    def start_worker(self, worker_id: str, image: str = "python:3.9-slim", 
                    command: str = "tail -f /dev/null", 
                    environment: Dict = None) -> Dict[str, Any]:
        """
        Inicia um container worker
        
        Args:
            worker_id: ID único do worker
            image: Imagem Docker a ser usada
            command: Comando para executar no container
            environment: Variáveis de ambiente
        
        Returns:
            Informações do worker criado
        """
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker não disponível"}
            
            # Para worker existente com mesmo ID
            self.stop_worker(worker_id)
            
            container = self.docker_client.containers.run(
                image,
                command,
                detach=True,
                name=f"worker_{worker_id}",
                environment=environment or {},
                network_mode="host"
            )
            
            worker_info = {
                "id": worker_id,
                "container_id": container.id,
                "status": "running",
                "image": image,
                "start_time": time.time()
            }
            
            self.workers[worker_id] = worker_info
            
            # Publica no Redis se disponível
            if self.redis_client:
                self.redis_client.hset(
                    "compute_workers", 
                    worker_id, 
                    json.dumps(worker_info)
                )
            
            logger.info(f"Worker {worker_id} iniciado: {container.id}")
            return {"success": True, "worker": worker_info}
            
        except Exception as e:
            error_msg = f"Erro ao iniciar worker {worker_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def stop_worker(self, worker_id: str) -> Dict[str, Any]:
        """Para e remove um worker"""
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker não disponível"}
            
            container_name = f"worker_{worker_id}"
            
            try:
                container = self.docker_client.containers.get(container_name)
                container.stop()
                container.remove()
                logger.info(f"Worker {worker_id} parado e removido")
            except docker.errors.NotFound:
                logger.warning(f"Worker {worker_id} não encontrado para parar")
            
            # Remove do registro local
            if worker_id in self.workers:
                del self.workers[worker_id]
            
            # Remove do Redis se disponível
            if self.redis_client:
                self.redis_client.hdel("compute_workers", worker_id)
            
            return {"success": True}
            
        except Exception as e:
            error_msg = f"Erro ao parar worker {worker_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def list_workers(self) -> List[Dict[str, Any]]:
        """Lista todos os workers ativos"""
        try:
            workers_list = []
            
            # Tenta obter do Redis primeiro
            if self.redis_client:
                try:
                    redis_workers = self.redis_client.hgetall("compute_workers")
                    for worker_id, worker_data in redis_workers.items():
                        workers_list.append(json.loads(worker_data))
                    return workers_list
                except Exception as e:
                    logger.warning(f"Erro ao obter workers do Redis: {str(e)}")
            
            # Fallback para registro local
            return list(self.workers.values())
            
        except Exception as e:
            logger.error(f"Erro ao listar workers: {str(e)}")
            return []
    
    def run_task(self, worker_id: str, command: str, 
                timeout: int = 30) -> Dict[str, Any]:
        """
        Executa um comando em um worker específico
        
        Args:
            worker_id: ID do worker
            command: Comando para executar
            timeout: Timeout em segundos
        
        Returns:
            Resultado da execução
        """
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker não disponível"}
            
            container_name = f"worker_{worker_id}"
            container = self.docker_client.containers.get(container_name)
            
            if container.status != "running":
                return {"success": False, "error": f"Container {worker_id} não está running"}
            
            # Executa o comando
            exit_code, output = container.exec_run(
                command,
                timeout=timeout
            )
            
            result = {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "output": output.decode('utf-8') if output else "",
                "worker_id": worker_id
            }
            
            logger.info(f"Task executada em {worker_id}: exit_code={exit_code}")
            return result
            
        except Exception as e:
            error_msg = f"Erro ao executar task em {worker_id}: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def get_worker_status(self, worker_id: str) -> Dict[str, Any]:
        """Obtém status de um worker específico"""
        try:
            if not self.docker_client:
                return {"status": "unknown", "error": "Docker não disponível"}
            
            container_name = f"worker_{worker_id}"
            container = self.docker_client.containers.get(container_name)
            
            return {
                "status": container.status,
                "id": worker_id,
                "image": container.image.tags[0] if container.image.tags else "unknown",
                "created": container.attrs['Created'],
                "state": container.attrs['State']
            }
            
        except docker.errors.NotFound:
            return {"status": "not_found", "id": worker_id}
        except Exception as e:
            return {"status": "error", "id": worker_id, "error": str(e)}
    
    def cleanup(self, max_age_hours: int = 24) -> Dict[str, Any]:
        """
        Limpa workers antigos
        
        Args:
            max_age_hours: Idade máxima em horas para manter workers
        
        Returns:
            Resultado da limpeza
        """
        try:
            if not self.docker_client:
                return {"success": False, "error": "Docker não disponível"}
            
            cleaned = 0
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for worker_id, worker_info in list(self.workers.items()):
                if current_time - worker_info['start_time'] > max_age_seconds:
                    self.stop_worker(worker_id)
                    cleaned += 1
            
            logger.info(f"Cleanup realizado: {cleaned} workers removidos")
            return {"success": True, "cleaned_count": cleaned}
            
        except Exception as e:
            error_msg = f"Erro no cleanup: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    def health_check(self) -> Dict[str, Any]:
        """Verifica a saúde do cluster"""
        docker_available = self.docker_client is not None
        try:
            redis_available = self.redis_client is not None and self.redis_client.ping()
        except:
            redis_available = False
        
        return {
            "docker_available": docker_available,
            "redis_available": redis_available,
            "worker_count": len(self.workers),
            "status": "healthy" if docker_available else "degraded"
        }

# Instância global para uso em toda a aplicação
compute_cluster = ComputeCluster(
    redis_url=os.getenv('REDIS_URL', 'redis://localhost:6379')
)
