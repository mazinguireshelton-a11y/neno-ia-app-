# backend/routes/chat.py
from __future__ import annotations

import os
import json
import time
import uuid
import html
import logging
from typing import Dict, Any, Generator, List, Optional

import requests
from flask import Blueprint, request, Response, current_app, jsonify, stream_with_context

# Opcional: se você já tiver um serviço central de LLM, usamos.
# Caso não exista, seguimos com as funções locais deste arquivo.
try:
    from services.llm_service import build_system_prompt  # opcional
except Exception:
    build_system_prompt = None  # type: ignore

# -----------------------------
# Config / Providers
# -----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Detecção de idioma server-side (fallback, opcional)
try:
    from langdetect import detect  # pip install langdetect
except Exception:
    detect = None  # type: ignore

chat_bp = Blueprint("chat_bp", __name__)

# -----------------------------
# Helpers
# -----------------------------
def _detect_lang(text: str, default: str = "auto") -> str:
    lang = default
    # prioridade ao header do browser (front deve mandar navigator.language)
    if request.headers.get("X-User-Lang"):
        return request.headers["X-User-Lang"]
    if detect:
        try:
            lang = detect(text)  # ex: 'pt', 'en'
        except Exception:
            pass
    return lang or "auto"


def _sanitize_text(s: str, max_len: int = 10000) -> str:
    s = s.strip()
    if len(s) > max_len:
        s = s[:max_len]
    return html.escape(s)


def _system_for_mode(mode: str, user_lang: str) -> str:
    """
    System prompt por modo. Mantém sua filosofia:
    - programador: respostas técnicas, trechos de código com explicação.
    - criativo: ideias, histórias, brainstorming.
    - padrão: assistente geral multilíngue.
    """
    base = (
        "Você é a NENO IA, uma assistente multimodal de nível mundial. "
        "Responda no mesmo idioma do usuário. Seja clara, objetiva e útil. "
        "Se houver arquivos/imagens no contexto, use-os de forma precisa."
    )
    if mode == "programador":
        return (
            f"{base} Modo Programador: use linguagem técnica quando necessário, "
            "explique decisões de design e mostre exemplos de código bem formatados. "
            "Inclua passos reproduzíveis e considerações de segurança/performance."
        )
    if mode == "criativo":
        return (
            f"{base} Modo Criativo: pense fora da caixa, proponha variações, "
            "estilos e tons diferentes. Mantenha coerência com o pedido."
        )
    return base


def _build_messages(user_text: str, mode: str, user_lang: str, context: Optional[str]) -> List[Dict[str, str]]:
    # system
    if build_system_prompt:
        system_content = build_system_prompt(mode=mode, lang=user_lang)
    else:
        system_content = _system_for_mode(mode, user_lang)

    msgs: List[Dict[str, str]] = [{"role": "system", "content": system_content}]

    if context:
        msgs.append({
            "role": "system",
            "content": f"Contexto fornecido pelo usuário (resumido):\n{context[:4000]}"
        })

    msgs.append({"role": "user", "content": user_text})
    return msgs


def _call_openrouter(messages: List[Dict[str, str]], stream: bool = False) -> requests.Response:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("BASE_URL", "http://localhost:5000"),
        "X-Title": "NENO IA",
    }
    payload = {"model": OPENROUTER_MODEL, "messages": messages, "stream": stream}
    return requests.post(url, headers=headers, json=payload, timeout=60, stream=stream)


def _call_openai(messages: List[Dict[str, str]], stream: bool = False) -> requests.Response:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODEL, "messages": messages, "stream": stream}
    return requests.post(url, headers=headers, json=payload, timeout=60, stream=stream)


def _call_groq(messages: List[Dict[str, str]], stream: bool = False) -> requests.Response:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": GROQ_MODEL, "messages": messages, "stream": stream}
    return requests.post(url, headers=headers, json=payload, timeout=60, stream=stream)


def _llm_fallback(messages: List[Dict[str, str]], stream: bool = False) -> requests.Response:
    """
    Fallback: OpenRouter -> OpenAI -> Groq
    Levanta Exception se tudo falhar.
    """
    last_err = None

    if OPENROUTER_API_KEY:
        try:
            resp = _call_openrouter(messages, stream=stream)
            if resp.status_code < 500:
                return resp
            last_err = f"OpenRouter {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_err = f"OpenRouter err: {e}"

    if OPENAI_API_KEY:
        try:
            resp = _call_openai(messages, stream=stream)
            if resp.status_code < 500:
                return resp
            last_err = f"OpenAI {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_err = f"OpenAI err: {e}"

    if GROQ_API_KEY:
        try:
            resp = _call_groq(messages, stream=stream)
            if resp.status_code < 500:
                return resp
            last_err = f"Groq {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_err = f"Groq err: {e}"

    raise RuntimeError(last_err or "Nenhum provedor LLM disponível")


# -----------------------------
# Supabase (histórico)
# -----------------------------
def _supabase_client():
    if not (SUPABASE_URL and SUPABASE_KEY):
        return None
    try:
        from supabase import create_client  # pip install supabase
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        current_app.logger.warning("Supabase indisponível: %s", e)
        return None


def _save_history(user_id: str, title: str, user_text: str, ai_text: str, mode: str, lang: str) -> None:
    client = _supabase_client()
    if not client:
        return
    try:
        # Tabelas esperadas:
        # conversations(id, user_id, title, mode, lang, created_at)
        # messages(id, conversation_id, role, content, created_at)
        conv = client.table("conversations").insert({
            "user_id": user_id,
            "title": title[:120] if title else (user_text[:60] or "Nova conversa"),
            "mode": mode,
            "lang": lang,
        }).execute()
        conv_id = conv.data[0]["id"]
        client.table("messages").insert([
            {"conversation_id": conv_id, "role": "user", "content": user_text},
            {"conversation_id": conv_id, "role": "assistant", "content": ai_text},
        ]).execute()
    except Exception as e:
        current_app.logger.warning("Falha ao salvar histórico: %s", e)


# -----------------------------
# Rotas
# -----------------------------
@chat_bp.route("/chat", methods=["POST"])
def chat_once() -> Response:
    """
    Resposta única (não stream). Ideal para o modo voz e mobile.
    Body JSON:
      {
        "text": "...",
        "mode": "padrao|programador|criativo",
        "lang": "pt-BR" (opcional),
        "context": "trechos de arquivos, resumos, etc" (opcional),
        "user_id": "uuid" (opcional)
      }
    """
    data = request.get_json(silent=True) or {}
    user_text: str = _sanitize_text(str(data.get("text", "")))
    if not user_text:
        return jsonify({"ok": False, "error": "Texto vazio"}), 400

    mode: str = str(data.get("mode", "padrao")).lower()
    user_lang: str = str(data.get("lang") or _detect_lang(user_text))
    context: Optional[str] = data.get("context")
    user_id: str = str(data.get("user_id") or "anon")

    messages = _build_messages(user_text, mode, user_lang, context)

    try:
        resp = _llm_fallback(messages, stream=False)
        if resp.status_code >= 400:
            return jsonify({"ok": False, "error": resp.text, "code": resp.status_code}), resp.status_code

        payload = resp.json()
        ai_text = (
            payload.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        # salva histórico (apenas user_text + ai_text)
        _save_history(user_id=user_id, title=user_text, user_text=user_text, ai_text=ai_text, mode=mode, lang=user_lang)

        return jsonify({
            "ok": True,
            "mode": mode,
            "lang": user_lang,
            "request_id": getattr(request, "id", str(uuid.uuid4())),
            "answer": ai_text,
        })
    except Exception as e:
        current_app.logger.exception("chat_once error: %s", e)
        return jsonify({"ok": False, "error": str(e)}), 500


@chat_bp.route("/chat/stream", methods=["POST"])
def chat_stream() -> Response:
    """
    SSE (Server-Sent Events) streaming, estilo ChatGPT.
    Body JSON:
      {
        "text": "...",
        "mode": "padrao|programador|criativo",
        "lang": "pt-BR" (opcional),
        "context": "..." (opcional),
        "user_id": "uuid" (opcional)
      }
    """
    data = request.get_json(silent=True) or {}
    user_text: str = _sanitize_text(str(data.get("text", "")))
    if not user_text:
        return jsonify({"ok": False, "error": "Texto vazio"}), 400

    mode: str = str(data.get("mode", "padrao")).lower()
    user_lang: str = str(data.get("lang") or _detect_lang(user_text))
    context: Optional[str] = data.get("context")
    user_id: str = str(data.get("user_id") or "anon")
    messages = _build_messages(user_text, mode, user_lang, context)

    def _event_stream() -> Generator[str, None, None]:
        request_id = getattr(request, "id", str(uuid.uuid4()))
        yield f"event: meta\ndata: {json.dumps({'request_id': request_id, 'lang': user_lang, 'mode': mode})}\n\n"

        ai_accum = ""

        try:
            # Preferimos OpenRouter/OpenAI/Groq no modo streaming
            resp = _llm_fallback(messages, stream=True)
            if resp.status_code >= 400:
                err = resp.text[:500]
                yield f"event: error\ndata: {json.dumps({'error': err})}\n\n"
                return

            # Stream do provedor
            for raw in resp.iter_lines(decode_unicode=True):
                if not raw:
                    continue

                # OpenAI-like stream envia linhas "data: {...}"
                if raw.startswith("data: "):
                    chunk = raw[6:]
                else:
                    chunk = raw

                if chunk.strip() == "[DONE]":
                    break

                try:
                    obj = json.loads(chunk)
                except Exception:
                    # Alguns provedores mandam JSON parcial — ignore
                    continue

                # Conteúdo incremental
                delta = ""
                # OpenAI style
                if "choices" in obj and obj["choices"]:
                    delta = (
                        obj["choices"][0]
                        .get("delta", {})
                        .get("content", "")
                    ) or obj["choices"][0].get("message", {}).get("content", "")

                # OpenRouter pode embutir em "choices[].delta.content"
                if delta:
                    ai_accum += delta
                    yield f"data: {json.dumps({'delta': delta})}\n\n"

            # fim
            yield f"event: done\ndata: {json.dumps({'final': True})}\n\n"

            # Salvar histórico no fim (apenas texto final)
            if ai_accum.strip():
                _save_history(user_id=user_id, title=user_text, user_text=user_text, ai_text=ai_accum, mode=mode, lang=user_lang)

        except Exception as e:
            current_app.logger.exception("chat_stream error: %s", e)
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return Response(stream_with_context(_event_stream()), mimetype="text/event-stream")
