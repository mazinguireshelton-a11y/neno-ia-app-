# backend/routes/imax_render.py
from fastapi import APIRouter, request, jsonify
from backend.services.imax_service import imax_service

imax_router = APIRouter('imax', __name__)

@imax_bp.route('/imax/render', methods=['POST'])
async def start_imax_render():
    """Inicia uma renderização IMAX"""
    try:
        config = await request.json()
        if not config:
            return {'status': 'error', 'message': 'Configuração não fornecida'}, 400
        
        result = imax_service.start_render(config)
        return result, 200
        
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@imax_bp.route('/imax/status/<render_id>', methods=['GET'])
async def get_render_status(render_id):
    """Obtém o status de uma renderização"""
    status = imax_service.get_render_status(render_id)
    if status:
        return status, 200
    return {'status': 'error', 'message': 'Renderização não encontrada'}, 404

@imax_bp.route('/imax/stop/<render_id>', methods=['POST'])
async def stop_render(render_id):
    """Para uma renderização"""
    result = imax_service.stop_render(render_id)
    return result, 200

@imax_bp.route('/imax/history', methods=['GET'])
async def get_render_history():
    """Obtém o histórico de renderizações"""
    history = imax_service.get_render_history()
    return history, 200
