# backend/routes/imax_render.py
from flask import Blueprint, request, jsonify
from backend.services.imax_service import imax_service

imax_bp = Blueprint('imax', __name__)

@imax_bp.route('/imax/render', methods=['POST'])
def start_imax_render():
    """Inicia uma renderização IMAX"""
    try:
        config = request.get_json()
        if not config:
            return jsonify({'status': 'error', 'message': 'Configuração não fornecida'}), 400
        
        result = imax_service.start_render(config)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@imax_bp.route('/imax/status/<render_id>', methods=['GET'])
def get_render_status(render_id):
    """Obtém o status de uma renderização"""
    status = imax_service.get_render_status(render_id)
    if status:
        return jsonify(status), 200
    return jsonify({'status': 'error', 'message': 'Renderização não encontrada'}), 404

@imax_bp.route('/imax/stop/<render_id>', methods=['POST'])
def stop_render(render_id):
    """Para uma renderização"""
    result = imax_service.stop_render(render_id)
    return jsonify(result), 200

@imax_bp.route('/imax/history', methods=['GET'])
def get_render_history():
    """Obtém o histórico de renderizações"""
    history = imax_service.get_render_history()
    return jsonify(history), 200
