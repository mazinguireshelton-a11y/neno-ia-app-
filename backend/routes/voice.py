# backend/routes/voice.py
from __future__ import annotations

import base64
import os
import uuid
import json
import logging
import tempfile
from typing import Optional, Dict, Any, List
import requests
from flask import Blueprint, request, jsonify, current_app

# Import das constantes atualizadas
from backend.utils.constants import SUPPORTED_LANGUAGES, MODES, DEFAULT_MODE_CONFIGS

voice_bp = Blueprint("voice_bp", __name__)

# Configurações
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "whisper-1")
VOICE_TIMEOUT = int(os.getenv("VOICE_TIMEOUT", "30"))

# -----------------------------
# Helpers Aprimorados
# -----------------------------
def _detect_language_from_audio(audio_path: str) -> str:
    """
    Detecta automaticamente o idioma do áudio usando Whisper.
    Retorna código de idioma (ex: 'pt-BR', 'en-US')
    """
    try:
        if not OPENAI_API_KEY:
            return "pt-BR"  # Fallback
        
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": WHISPER_MODEL,
                "response_format": "verbose_json",
                "language": "auto"  # Permite detecção automática
            }
            
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=VOICE_TIMEOUT)
            if resp.status_code == 200:
                result = resp.json()
                detected_lang = result.get("language", "pt-BR")
                
                # Mapeia códigos simples para completos (ex: 'pt' → 'pt-BR')
                lang_mapping = {
                    "pt": "pt-BR", "en": "en-US", "es": "es-ES",
                    "fr": "fr-FR", "de": "de-DE", "it": "it-IT",
                    "ja": "ja-JP", "zh": "zh-CN", "ru": "ru-RU",
                    "ar": "ar-SA"
                }
                
                return lang_mapping.get(detected_lang, detected_lang)
        
        return "pt-BR"  # Fallback seguro
        
    except Exception as e:
        current_app.logger.warning(f"Falha na detecção de idioma: {e}")
        return "pt-BR"

def _transcribe_with_openai(audio_path: str, lang: Optional[str] = None) -> Dict[str, Any]:
    """
    Usa OpenAI Whisper API para transcrever áudio com metadados completos.
    Retorna dict com texto, confiança e idioma detectado.
    """
    try:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY não configurada")

        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "model": WHISPER_MODEL,
                "response_format": "verbose_json",  # Para obter metadados
                "temperature": 0.0,  # Mais determinístico
            }
            
            if lang and lang != "auto":
                data["language"] = lang

            resp = requests.post(url, headers=headers, files=files, data=data, timeout=VOICE_TIMEOUT)
            
            if resp.status_code >= 400:
                error_msg = resp.text[:200] if resp.text else "Erro desconhecido"
                raise RuntimeError(f"Whisper falhou {resp.status_code}: {error_msg}")

            result = resp.json()
            
            return {
                "text": result.get("text", "").strip(),
                "language": result.get("language", lang or "pt-BR"),
                "confidence": _calculate_confidence(result),
                "duration": result.get("duration", 0)
            }
            
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout na transcrição de áudio")
    except Exception as e:
        current_app.logger.error(f"Erro na transcrição: {e}")
        raise

def _calculate_confidence(result: Dict) -> float:
    """
    Calcula confiança aproximada baseada nos metadados do Whisper.
    """
    # Implementação simplificada - pode ser aprimorada
    segments = result.get("segments", [])
    if not segments:
        return 0.8  # Confiança padrão
    
    # Média das confianças dos segmentos
    confidences = [seg.get("confidence", 0.7) for seg in segments if seg.get("confidence")]
    return sum(confidences) / len(confidences) if confidences else 0.7

def _synthesize_speech(text: str, lang: str, voice_model: str = None) -> Optional[bytes]:
    """
    Sintetiza fala usando TTS (implementação básica - pode ser expandida).
    """
    try:
        # Configurações baseadas no idioma
        voice_config = SUPPORTED_LANGUAGES.get(lang, {})
        available_voices = voice_config.get("voice_models", [])
        
        if not voice_model and available_voices:
            voice_model = available_voices[0]  # Voz padrão do idioma
        
        # Aqui integraria com API de TTS (Google, Azure, ElevenLabs, etc.)
        # Por enquanto retorna None - o frontend pode usar TTS do navegador
        
        return None
        
    except Exception as e:
        current_app.logger.error(f"Erro na síntese de voz: {e}")
        return None

def _forward_to_chat(transcript: str, mode: str, lang: str, user_id: str, voice_context: Dict = None) -> dict:
    """
    Encaminha transcrição para o /chat com contexto de voz.
    """
    try:
        # Prepara contexto adicional para o modo voz
        chat_payload = {
            "text": transcript, 
            "mode": mode, 
            "lang": lang, 
            "user_id": user_id,
            "voice_context": voice_context or {}
        }
        
        # Usa requests para chamar internamente o endpoint de chat
        # (Melhor que test_request_context para produção)
        service_url = os.getenv("SERVICE_URL", "http://localhost:5000")
        chat_url = f"{service_url}/chat"
        
        resp = requests.post(
            chat_url, 
            json=chat_payload,
            timeout=30,
            headers={"Content-Type": "application/json"}
        )
        
        if resp.status_code == 200:
            return resp.json()
        else:
            raise RuntimeError(f"Erro no serviço de chat: {resp.status_code}")
            
    except requests.exceptions.Timeout:
        raise RuntimeError("Timeout no serviço de chat")
    except Exception as e:
        current_app.logger.error(f"Erro ao encaminhar para chat: {e}")
        raise

def _validate_voice_mode(mode: str) -> bool:
    """
    Valida se o modo suporta funcionalidades de voz.
    """
    mode_config = MODES.get(mode, {})
    return mode_config.get("multilingual", False) or mode == "voice"

def _get_voice_config(lang: str) -> Dict[str, Any]:
    """
    Retorna configurações de voz para o idioma especificado.
    """
    lang_config = SUPPORTED_LANGUAGES.get(lang, {})
    voice_config = DEFAULT_MODE_CONFIGS.get("voice", {})
    
    return {
        "language": lang,
        "voice_models": lang_config.get("voice_models", []),
        "stt_accuracy": lang_config.get("stt_accuracy", 0.9),
        "tts_quality": lang_config.get("tts_quality", 0.9),
        "auto_detect": voice_config.get("auto_detect_language", True),
        "fallback_language": voice_config.get("fallback_language", "pt-BR"),
        "voice_speed": voice_config.get("voice_speed", "normal"),
        "voice_style": voice_config.get("voice_style", "natural")
    }

# -----------------------------
# Rotas Principais
# -----------------------------
@voice_bp.route("/voice", methods=["POST"])
def voice_entry():
    """
    Endpoint principal para modo voz com suporte multilíngue completo.
    
    Parâmetros esperados (multipart/form-data ou JSON):
    - audio: arquivo de áudio (opcional se text for fornecido)
    - text: transcrição prévia (opcional)
    - mode: modo de operação (default: "voice")
    - lang: idioma preferido (default: "auto" para detecção)
    - user_id: identificador do usuário
    - voice_model: modelo de voz preferido para TTS
    """
    try:
        # Obter parâmetros da requisição
        user_id = request.form.get("user_id", request.json.get("user_id", "anon"))
        mode = request.form.get("mode", request.json.get("mode", "voice"))
        lang = request.form.get("lang", request.json.get("lang", "auto"))
        voice_model = request.form.get("voice_model", request.json.get("voice_model"))
        
        # Validar modo
        if not _validate_voice_mode(mode):
            return jsonify({
                "ok": False, 
                "error": f"Modo '{mode}' não suporta funcionalidades de voz"
            }), 400

        # Obter transcrição (áudio ou texto direto)
        transcript_data = None
        
        if request.form.get("text") or (request.json and "text" in request.json):
            # Texto direto do frontend
            transcript = request.form.get("text") or request.json.get("text", "")
            transcript_data = {
                "text": transcript.strip(),
                "language": lang if lang != "auto" else "pt-BR",
                "confidence": 0.95,  # Alta confiança para texto direto
                "duration": 0
            }
        else:
            # Processar áudio
            if "audio" not in request.files:
                return jsonify({
                    "ok": False, 
                    "error": "Faltando áudio ou texto para processamento"
                }), 400

            audio_file = request.files["audio"]
            if audio_file.filename == "":
                return jsonify({"ok": False, "error": "Arquivo de áudio inválido"}), 400

            # Salvar áudio temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio_file.save(tmp.name)
                tmp_path = tmp.name

            try:
                # Detectar idioma se automático
                if lang == "auto":
                    detected_lang = _detect_language_from_audio(tmp_path)
                    current_app.logger.info(f"Idioma detectado: {detected_lang}")
                    lang = detected_lang
                
                # Transcrever áudio
                transcript_data = _transcribe_with_openai(tmp_path, lang)
                
            finally:
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass

        if not transcript_data or not transcript_data["text"]:
            return jsonify({
                "ok": False, 
                "error": "Transcrição vazia ou falha no processamento"
            }), 400

        # Preparar contexto de voz
        voice_context = {
            "transcription_confidence": transcript_data["confidence"],
            "detected_language": transcript_data["language"],
            "audio_duration": transcript_data["duration"],
            "voice_config": _get_voice_config(lang)
        }

        # Encaminhar para serviço de chat
        chat_resp = _forward_to_chat(
            transcript_data["text"], 
            mode, 
            lang, 
            user_id, 
            voice_context
        )

        # Sintetizar resposta em áudio se solicitado
        audio_response = None
        if request.args.get("tts", "false").lower() == "true":
            response_text = chat_resp.get("response", "")
            if response_text:
                audio_response = _synthesize_speech(response_text, lang, voice_model)

        # Montar resposta completa
        response_data = {
            "ok": True,
            "transcription": transcript_data,
            "chat_response": chat_resp,
            "voice_context": voice_context,
            "mode": mode,
            "language": lang
        }

        # Adicionar áudio se disponível
        if audio_response:
            response_data["audio_response"] = {
                "format": "audio/wav",
                "data": base64.b64encode(audio_response).decode('utf-8') if audio_response else None
            }

        return jsonify(response_data)

    except RuntimeError as e:
        current_app.logger.warning(f"Erro de runtime em /voice: {e}")
        return jsonify({"ok": False, "error": str(e)}), 400
        
    except Exception as e:
        current_app.logger.exception("Erro não esperado no /voice: %s", e)
        return jsonify({
            "ok": False, 
            "error": "Erro interno no processamento de voz"
        }), 500

@voice_bp.route("/voice/languages", methods=["GET"])
def get_supported_languages():
    """
    Retorna lista de idiomas suportados pelo sistema de voz.
    """
    try:
        languages = []
        for lang_code, config in SUPPORTED_LANGUAGES.items():
            languages.append({
                "code": lang_code,
                "name": config["name"],
                "native_name": config["native_name"],
                "flag": config["flag"],
                "voice_models": config.get("voice_models", []),
                "stt_accuracy": config.get("stt_accuracy", 0.9),
                "tts_quality": config.get("tts_quality", 0.9)
            })
        
        return jsonify({
            "ok": True,
            "languages": sorted(languages, key=lambda x: x["name"]),
            "default_language": "pt-BR"
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter idiomas: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@voice_bp.route("/voice/config", methods=["GET"])
def get_voice_config():
    """
    Retorna configurações atuais do sistema de voz.
    """
    try:
        lang = request.args.get("lang", "pt-BR")
        
        return jsonify({
            "ok": True,
            "config": _get_voice_config(lang),
            "supported_modes": [mode for mode, config in MODES.items() 
                               if config.get("multilingual") or mode == "voice"]
        })
        
    except Exception as e:
        current_app.logger.error(f"Erro ao obter configuração de voz: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500
