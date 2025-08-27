# backend/routes/super_compute.py
from flask import Blueprint, request, jsonify
from backend.services.compute_cluster import compute_cluster
from backend.services.smart_optimizer import smart_optimizer
from backend.plugins.super_ai_module import SuperAIModule
from backend.plugins.viz_engine import VisualizationEngine
import time
import os
import logging

logger = logging.getLogger(__name__)

super_compute_bp = Blueprint('super_compute_bp', __name__)

# Instâncias globais
super_ai = SuperAIModule()
viz_engine = VisualizationEngine()

@super_compute_bp.route('/api/super-compute', methods=['POST'])
def super_compute():
    """Endpoint principal para computação avançada"""
    try:
        data = request.json
        command = data.get('command')
        params = data.get('parameters', {})
        
        # Verifica modo de otimização
        use_optimization = params.get('optimize', True)
        
        if use_optimization:
            # Usa otimizador inteligente
            result = smart_optimizer.optimize_computation(command, params)
        else:
            # Execução direta
            result = super_ai.execute(command, params)
        
        # Adiciona visualização se solicitado
        if params.get('generate_visualization', False):
            viz_result = viz_engine.execute(f"{command}_viz", {
                **params,
                **result
            })
            result['visualization'] = viz_result
        
        return jsonify({
            "success": True,
            "result": result,
            "metadata": {
                "command": command,
                "timestamp": time.time(),
                "optimized": use_optimization,
                "compute_mode": os.getenv('COMPUTE_MODE', 'balanced')
            }
        })
        
    except Exception as e:
        logger.error(f"Erro em super-compute: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@super_compute_bp.route('/api/scale-cluster', methods=['POST'])
def scale_cluster():
    """Escala o cluster de computação"""
    try:
        data = request.json
        n_workers = data.get('workers')
        
        endpoints = compute_cluster.scale_workers(n_workers)
        
        # Atualiza endpoints do super_ai
        super_ai.cloud_endpoints = endpoints
        
        return jsonify({
            "success": True,
            "endpoints": endpoints,
            "total_workers": len(endpoints),
            "compute_mode": os.getenv('COMPUTE_MODE', 'balanced')
        })
        
    except Exception as e:
        logger.error(f"Erro ao escalar cluster: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@super_compute_bp.route('/api/cluster-info', methods=['GET'])
def cluster_info():
    """Retorna informações sobre o cluster"""
    try:
        endpoints = compute_cluster.get_worker_endpoints()
        stats = compute_cluster.get_cluster_stats()
        
        return jsonify({
            "success": True,
            "cluster_stats": stats,
            "total_workers": len(endpoints),
            "endpoints": endpoints,
            "compute_mode": os.getenv('COMPUTE_MODE', 'balanced'),
            "auto_scale": os.getenv('AUTO_SCALE', 'true').lower() == 'true'
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter info do cluster: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@super_compute_bp.route('/api/set-compute-mode', methods=['POST'])
def set_compute_mode():
    """Define o modo de computação"""
    try:
        data = request.json
        mode = data.get('mode', 'balanced')
        
        # Modos válidos
        valid_modes = ['economy', 'balanced', 'performance']
        if mode not in valid_modes:
            return jsonify({
                "success": False,
                "error": f"Modo inválido. Use: {valid_modes}"
            }), 400
        
        # Atualiza variável de ambiente
        os.environ['COMPUTE_MODE'] = mode
        
        # Reconfigura cluster
        compute_cluster.scale_workers()
        
        return jsonify({
            "success": True,
            "message": f"Modo de computação alterado para {mode}",
            "new_mode": mode
        })
        
    except Exception as e:
        logger.error(f"Erro ao alterar modo: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@super_compute_bp.route('/api/cleanup', methods=['POST'])
def cleanup_cluster():
    """Limpa todos os containers do cluster"""
    try:
        compute_cluster.cleanup_containers()
        
        return jsonify({
            "success": True,
            "message": "Cluster limpo com sucesso"
        })
        
    except Exception as e:
        logger.error(f"Erro ao limpar cluster: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@super_compute_bp.route('/api/performance-stats', methods=['GET'])
def performance_stats():
    """Retorna estatísticas de performance"""
    try:
        stats = smart_optimizer.get_performance_stats()
        
        return jsonify({
            "success": True,
            "performance_stats": stats
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter stats: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
