# backend/routes/modes.py
from flask import Blueprint, request, jsonify, current_app

modes_bp = Blueprint("modes_bp", __name__)

@modes_bp.route("/modes", methods=["GET"])
def list_modes():
    """Lista todos os modos disponíveis"""
    try:
        result = current_app.mode_manager.list_modes()
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Erro ao listar modos: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@modes_bp.route("/modes/current", methods=["GET"])
def get_current_mode():
    """Retorna o modo atual"""
    try:
        result = current_app.mode_manager.get_current_mode()
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Erro ao obter modo atual: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@modes_bp.route("/modes/set", methods=["POST"])
def set_mode():
    """Define o modo ativo"""
    try:
        data = request.get_json() or {}
        mode_name = data.get("mode", "default")
        
        result = current_app.mode_manager.set_mode(mode_name)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Erro ao definir modo: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@modes_bp.route("/modes/exec", methods=["POST"])
def execute_mode():
    """Executa uma ação no modo atual"""
    try:
        data = request.get_json() or {}
        message = data.get("message", "")
        params = data.get("params", {})
        
        result = current_app.mode_manager.handle_request(message, params)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Erro ao executar modo: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
