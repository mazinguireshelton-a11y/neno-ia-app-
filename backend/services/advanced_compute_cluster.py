import docker
import requests
import json
import time
from typing import Dict, List, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedComputeCluster:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.workers = {}
        self.worker_image = "python:3.9-slim"
        
    def create_worker(self, worker_id: str) -> Dict:
        """Cria worker com API para execução de código"""
        try:
            # Container com servidor Flask para executar código
            container = self.docker_client.containers.run(
                self.worker_image,
                command=[
                    "sh", "-c", 
                    "pip install flask numpy scipy && python -c \""
                    "from flask import Flask, request, jsonify; "
                    "app = Flask(__name__); "
                    "@app.route('/execute', methods=['POST']); "
                    "def execute(): "
                    "    data = request.json; "
                    "    try: "
                    "        result = eval(data['code']); "
                    "        return jsonify({'success': True, 'result': result}); "
                    "    except Exception as e: "
                    "        return jsonify({'success': False, 'error': str(e)}); "
                    "app.run(host='0.0.0.0', port=8000); "
                    "\""
                ],
                detach=True,
                ports={'8000/tcp': None},
                mem_limit='512m',
                cpu_period=100000,
                cpu_quota=50000,
                network_mode='none'
            )
            
            # Obter porta mapeada
            container.reload()
            port = container.ports['8000/tcp'][0]['HostPort']
            
            self.workers[worker_id] = {
                'container': container,
                'port': port,
                'status': 'running',
                'created_at': time.time()
            }
            
            return {
                'worker_id': worker_id,
                'endpoint': f'http://localhost:{port}',
                'status': 'created'
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar worker: {e}")
            raise
            
    def execute_code(self, worker_id: str, code: str, timeout: int = 30) -> Dict:
        """Executa código no worker específico"""
        if worker_id not in self.workers:
            return {'error': 'Worker não encontrado'}
            
        worker = self.workers[worker_id]
        try:
            response = requests.post(
                f"{worker['endpoint']}/execute",
                json={'code': code},
                timeout=timeout
            )
            return response.json()
        except Exception as e:
            return {'error': f'Erro na execução: {str(e)}'}
            
    def cleanup(self):
        """Limpa todos os workers"""
        for worker_id, worker_info in list(self.workers.items()):
            try:
                worker_info['container'].stop()
                worker_info['container'].remove()
                del self.workers[worker_id]
            except Exception as e:
                logger.error(f"Erro ao limpar worker {worker_id}: {e}")

# Instância global
compute_cluster = AdvancedComputeCluster()
