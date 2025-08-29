from __future__ import annotations

import os
import uuid
import logging
from pathlib import Path
from typing import List

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from services.file_service import extract_text_from_file

uploads_bp = Blueprint("uploads_bp", __name__)

# Config
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
ALLOWED_EXTS = {"txt", "pdf", "docx", "jpg", "jpeg", "png", "mp3", "wav"}
MAX_FILE_SIZE_MB = 25  # limite de 25MB


# -----------------------------
# Helpers
# -----------------------------
def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTS


def _check_size(f) -> bool:
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    return size <= MAX_FILE_SIZE_MB * 1024 * 1024


# -----------------------------
# Upload de arquivos
# -----------------------------
@uploads_bp.route("/upload", methods=["POST"])
def upload_file():
    """
    Upload de arquivos para contexto da IA.
    - Salva em ./uploads
    - Extrai texto (quando possível)
    - Retorna ID único para referência no chat
    """
    try:
        if "file" not in request.files:
            return jsonify({"ok": False, "error": "Nenhum arquivo enviado"}), 400

        f = request.files["file"]

        if f.filename == "":
            return jsonify({"ok": False, "error": "Arquivo sem nome"}), 400

        if not _allowed_file(f.filename):
            return jsonify({"ok": False, "error": "Tipo de arquivo não permitido"}), 400

        if not _check_size(f):
            return jsonify({"ok": False, "error": f"Tamanho máximo {MAX_FILE_SIZE_MB}MB excedido"}), 400

        # Criar diretório se não existir
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        # Nome seguro
        ext = f.filename.rsplit(".", 1)[1].lower()
        file_id = str(uuid.uuid4())
        filename = secure_filename(f"{file_id}.{ext}")
        save_path = UPLOAD_DIR / filename
        f.save(save_path)

        # Extrair texto
        extracted_text = extract_text_from_file(save_path)

        return jsonify({
            "ok": True,
            "file_id": file_id,
            "filename": filename,
            "extracted_text": extracted_text[:2000],  # limita preview
        })
    except Exception as e:
        current_app.logger.exception("Erro no upload: %s", e)
        return jsonify({"ok": False, "error": str(e)}), 500
