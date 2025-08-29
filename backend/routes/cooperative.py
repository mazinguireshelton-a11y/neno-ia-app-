from services.compute.cluster import compute_cluster
from flask import Blueprint, request, jsonify
from services import llm_service
import asyncio

cooperative_bp = Blueprint('cooperative_bp', __name__)

@cooperative_bp.route('/api/cooperative/analyze', methods=['POST'])
def analyze_complexity():
    """Analisa complexidade de uma tarefa"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({"error": "Prompt é obrigatório"}), 400
    
    complexity = llm_service.cooperative_orchestrator.analyze_complexity(prompt)
    
    return jsonify({
        "prompt": prompt,
        "analysis": complexity,
        "recommendation": "cooperative" if complexity["needs_cooperation"] else "single"
    })

@cooperative_bp.route('/api/cooperative/execute', methods=['POST'])
def execute_cooperative():
    """Executa tarefa com cooperação forçada"""
    data = request.get_json()
    prompt = data.get('prompt', '')
    num_workers = data.get('workers', None)
    
    if not prompt:
        return jsonify({"error": "Prompt é obrigatório"}), 400
    
    try:
        # Forçar divisão de tarefa
        if num_workers:
            subtasks = llm_service.cooperative_orchestrator.divide_task(prompt, num_workers)
        else:
            complexity = llm_service.cooperative_orchestrator.analyze_complexity(prompt)
            subtasks = llm_service.cooperative_orchestrator.divide_task(
                prompt, complexity["recommended_workers"]
            )
        
        # Executar cooperativamente
        result = asyncio.run(
            llm_service.cooperative_orchestrator.execute_cooperative_task(prompt, False)
        )
        
        return jsonify({
            "success": True,
            "cooperative": True,
            "subtasks": subtasks,
            "result": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "cooperative": False
        }), 500

@cooperative_bp.route('/api/cooperative/status', methods=['GET'])
def cooperative_status():
    """Retorna status do sistema cooperativo"""
    status = llm_service.cooperative_orchestrator.get_cooperation_status()
    return jsonify(status)
