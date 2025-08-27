# backend/services/compute_cluster.py
import redis
import docker
from typing import Dict, Any, List
import json
import os
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ComputeCluster:
    def __init__(self):
        # Configuração Redis
        self.redis_client = redis.Redis(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
        
        # Configuração Docker
        docker_host = os.getenv('DOCKER_HOST', 'unix:///var/run/docker.sock')
        self.docker_client = docker.DockerClient(base_url=docker_host)
        
        self.active_containers = {}
        self.worker_stats = {}
        
        logger.info(f"ComputeCluster inicializado em modo {os.getenv('COMPUTE_MODE', 'balanced')}")

    def get_compute_mode_config(self):
        """Retorna configuração baseada no modo selecionado"""
        mode = os.getenv('COMPUTE_MODE', 'balanced')
        
        configs = {
            'economy': {'mem': '1g', 'cpu': 25000, 'workers': 2},
            'balanced': {'mem': '2g', 'cpu': 50000, 'workers': 4},
            'performance': {'mem': '4g', 'cpu': 100000, 'workers': 8}
        }
        
        return configs.get(mode, configs['balanced'])

    def start_worker_container(self, image: str = None) -> str:
        """Inicia container worker com configurações otimizadas"""
        image = image or os.getenv('WORKER_IMAGE', 'python:3.9')
        config = self.get_compute_mode_config()
        
        try:
            container = self.docker_client.containers.run(
                image,
                command="python -m http.server 8000",
                detach=True,
                ports={'8000/tcp': None},
                mem_limit=config['mem'],
                cpu_period=100000,
                cpu_quota=config['cpu'],
                environment={
                    'PYTHONUNBUFFERED': '1',
                    'OMP_NUM_THREADS': '2',
                    'MKL_NUM_THREADS': '2'
                },
                name=f"super_worker_{int(time.time())}_{len(self.active_containers)}"
            )
            
            container_id = container.id
            self.active_containers[container_id] = container
            
            # Aguarda container estar pronto
            time.sleep(0.5)
            container.reload()
            
            # Recupera porta mapeada
            port = container.ports['8000/tcp'][0]['HostPort']
            endpoint = f"http://localhost:{port}"
            
            # Registra estatísticas
            self.worker_stats[container_id] = {
                'start_time': datetime.now().isoformat(),
                'endpoint': endpoint,
                'config': config
            }
            
            logger.info(f"Worker iniciado: {endpoint}")
            return endpoint
            
        except Exception as e:
            logger.error(f"Erro ao iniciar container: {str(e)}")
            raise Exception(f"Erro ao iniciar container: {str(e)}")
    
    def scale_workers(self, n_workers: int = None) -> List[str]:
        """Escala número de workers inteligentemente"""
        if n_workers is None:
            config = self.get_compute_mode_config()
            n_workers = config['workers']
        
        max_workers = int(os.getenv('MAX_WORKERS', 8))
        n_workers = min(n_workers, max_workers)
        
        endpoints = []
        current_count = len(self.active_containers)
        
        # Se precisar reduzir workers
        if n_workers < current_count:
            return self.reduce_workers(current_count - n_workers)
        
        # Adiciona workers
        for i in range(n_workers - current_count):
            try:
                endpoint = self.start_worker_container()
                endpoints.append(endpoint)
            except Exception as e:
                logger.error(f"Erro ao iniciar worker {i}: {e}")
                continue
        
        # Atualiza endpoints no Redis
        all_endpoints = list(self.active_containers.values())
        self.redis_client.set('worker_endpoints', json.dumps(all_endpoints))
        self.redis_client.set('last_scale_time', datetime.now().isoformat())
                
        return endpoints
    
    def reduce_workers(self, count: int) -> List[str]:
        """Reduz número de workers mantendo os mais recentes"""
        if count <= 0:
            return list(self.worker_stats.keys())
        
        # Ordena containers por tempo de criação (mais antigos primeiro)
        sorted_containers = sorted(
            self.active_containers.items(),
            key=lambda x: self.worker_stats[x[0]]['start_time']
        )
        
        removed = []
        for i in range(min(count, len(sorted_containers))):
            container_id, container = sorted_containers[i]
            try:
                container.stop(timeout=5)
                container.remove()
                removed.append(container_id)
            except Exception as e:
                logger.error(f"Erro ao remover container {container_id}: {e}")
        
        # Remove dos registros
        for container_id in removed:
            self.active_containers.pop(container_id, None)
            self.worker_stats.pop(container_id, None)
        
        remaining_endpoints = [
            stats['endpoint'] for stats in self.worker_stats.values()
        ]
        
        self.redis_client.set('worker_endpoints', json.dumps(remaining_endpoints))
        return remaining_endpoints
    
    def get_worker_endpoints(self) -> List[str]:
        """Recupera endpoints dos workers"""
        # Tenta do Redis primeiro
        endpoints_json = self.redis_client.get('worker_endpoints')
        if endpoints_json:
            try:
                return json.loads(endpoints_json)
            except json.JSONDecodeError:
                pass
        
        # Fallback para containers ativos
        endpoints = []
        for container_id, container in self.active_containers.items():
            try:
                container.reload()
                if container.status == 'running':
                    port = container.ports['8000/tcp'][0]['HostPort']
                    endpoints.append(f"http://localhost:{port}")
            except:
                continue
        
        return endpoints
    
    def get_cluster_stats(self) -> Dict:
        """Retorna estatísticas do cluster"""
        return {
            'total_workers': len(self.active_containers),
            'active_containers': list(self.active_containers.keys()),
            'worker_stats': self.worker_stats,
            'compute_mode': os.getenv('COMPUTE_MODE', 'balanced'),
            'auto_scale': os.getenv('AUTO_SCALE', 'true').lower() == 'true'
        }
    
    def cleanup_containers(self):
        """Limpa todos os containers ativos"""
        logger.info("Limpando containers...")
        for container_id, container in self.active_containers.items():
            try:
                container.stop(timeout=5)
                container.remove()
                logger.info(f"Container {container_id} removido")
            except Exception as e:
                logger.error(f"Erro ao limpar container {container_id}: {e}")
        
        self.active_containers.clear()
        self.worker_stats.clear()
        self.redis_client.delete('worker_endpoints')
        
        logger.info("Todos os containers foram limpos")

# Instância global
compute_cluster = ComputeCluster()
