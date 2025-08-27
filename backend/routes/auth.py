# backend/routes/auth.py
from __future__ import annotations

import os
import uuid
import time
from typing import Optional, Dict, Any

from flask import (
    Blueprint, request, jsonify, session, current_app
)

auth_bp = Blueprint("auth_bp", __name__)

# -----------------------------
# Config
# -----------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # para auth real, use a anon key (pública) em produção
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

DEBUG = os.getenv("FLASK_DEBUG", os.getenv("DEBUG", "false")).lower() in ("1", "true")


# -----------------------------
# Supabase client (lazy)
# -----------------------------
def _supabase_client():
    """
    Cria cliente Supabase se variáveis estiverem configuradas.
    Retorna None se indisponível (permite fallback DEV).
    """
    if not (SUPABASE_URL and SUPABASE_KEY):
        return None
    try:
        from supabase import create_client, Client  # pip install supabase
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        current_app.logger.warning("Supabase indisponível: %s", e)
        return None


# -----------------------------
# Helpers
# -----------------------------
def _set_user_session(user: Dict[str, Any], access_token: Optional[str] = None, refresh_token: Optional[str] = None):
    """
    Salva informações mínimas na sessão Flask (cookie).
    Não armazene tokens sensíveis além do necessário.
    """
    session.permanent = True
    session["user"] = {
        "id": user.get("id") or user.get("user", {}).get("id") or str(uuid.uuid4()),
        "email": user.get("email") or user.get("user", {}).get("email"),
        "name": user.get("user_metadata", {}).get("full_name")
                or user.get("user", {}).get("user_metadata", {}).get("full_name")
                or user.get("name"),
        "avatar_url": user.get("user_metadata", {}).get("avatar_url")
                      or user.get("user", {}).get("user_metadata", {}).get("avatar_url"),
        "providers": user.get("identities") or user.get("app_metadata", {}).get("providers"),
    }
    # Tokens: mantenha só se realmente precisar chamar APIs do lado do servidor
    if access_token:
        session["access_token"] = access_token
    if refresh_token:
        session["refresh_token"] = refresh_token


def _clear_session():
    for k in list(session.keys()):
        session.pop(k, None)


def _require_json(fields: list[str]) -> Optional[tuple]:
    data = request.get_json(silent=True) or {}
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    if missing:
        return jsonify({"ok": False, "error": f"Campos faltando: {', '.join(missing)}"}), 400
    return None


# -----------------------------
# Rotas
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login_email_password():
    """
    Login com e-mail/senha via Supabase.
    Body JSON: { "email": "...", "password": "..." }
    """
    err = _require_json(["email", "password"])
    if err:
        return err

    data = request.get_json(silent=True) or {}
    email = data["email"].strip()
    password = data["password"].strip()

    client = _supabase_client()
    if not client:
        # Fallback DEV (apenas para desenvolvimento local)
        if DEBUG:
            fake_user = {"id": "dev-user-123", "email": email, "name": "Dev User"}
            _set_user_session(fake_user, access_token="dev-token", refresh_token="dev-refresh")
            return jsonify({"ok": True, "user": session["user"], "dev": True})
        return jsonify({"ok": False, "error": "Supabase não configurado"}), 503

    try:
        # supabase-py v2
        # https://supabase.com/docs/reference/python/auth-signinwithpassword
        res = client.auth.sign_in_with_password({"email": email, "password": password})
        # res.session, res.user
        if not getattr(res, "user", None):
            return jsonify({"ok": False, "error": "Credenciais inválidas"}), 401

        access_token = getattr(res.session, "access_token", None) if getattr(res, "session", None) else None
        refresh_token = getattr(res.session, "refresh_token", None) if getattr(res, "session", None) else None
        user_obj = {
            "id": res.user.id,
            "email": res.user.email,
            "user_metadata": getattr(res.user, "user_metadata", {}) or {},
            "app_metadata": getattr(res.user, "app_metadata", {}) or {},
        }

        _set_user_session(user_obj, access_token=access_token, refresh_token=refresh_token)
        return jsonify({"ok": True, "user": session["user"]})
    except Exception as e:
        current_app.logger.warning("Login falhou: %s", e)
        return jsonify({"ok": False, "error": "Falha no login"}), 401


@auth_bp.route("/register", methods=["POST"])
def register_email_password():
    """
    Registro por e-mail/senha. Opcional — desabilite no .env se não quiser.
    Body JSON: { "email": "...", "password": "..." }
    """
    if os.getenv("ALLOW_REGISTER", "true").lower() not in ("1", "true"):
        return jsonify({"ok": False, "error": "Registro desativado"}), 403

    err = _require_json(["email", "password"])
    if err:
        return err

    data = request.get_json(silent=True) or {}
    email = data["email"].strip()
    password = data["password"].strip()

    client = _supabase_client()
    if not client:
        if DEBUG:
            # simula criação e login em DEV
            fake_user = {"id": "dev-user-123", "email": email, "name": "Dev User"}
            _set_user_session(fake_user, access_token="dev-token", refresh_token="dev-refresh")
            return jsonify({"ok": True, "user": session["user"], "dev": True})
        return jsonify({"ok": False, "error": "Supabase não configurado"}), 503

    try:
        # https://supabase.com/docs/reference/python/auth-signup
        res = client.auth.sign_up({"email": email, "password": password})
        if not getattr(res, "user", None):
            return jsonify({"ok": False, "error": "Não foi possível registrar"}), 400

        # dependendo das config do projeto, pode exigir confirmação por e-mail
        needs_confirm = True
        try:
            needs_confirm = not bool(getattr(res.user, "confirmed_at", None))
        except Exception:
            pass

        return jsonify({
            "ok": True,
            "user": {
                "id": res.user.id,
                "email": res.user.email,
            },
            "needs_email_confirmation": needs_confirm
        })
    except Exception as e:
        current_app.logger.warning("Registro falhou: %s", e)
        return jsonify({"ok": False, "error": "Falha no registro"}), 400


@auth_bp.route("/refresh", methods=["POST"])
def refresh_session():
    """
    Atualiza tokens usando refresh_token que está na sessão.
    """
    client = _supabase_client()
    if not client:
        if DEBUG:
            # mantemos a sessão dev viva
            return jsonify({"ok": True, "user": session.get("user"), "dev": True})
        return jsonify({"ok": False, "error": "Supabase não configurado"}), 503

    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return jsonify({"ok": False, "error": "Sem refresh_token na sessão"}), 401

    try:
        # https://supabase.com/docs/reference/python/auth-refreshsession
        res = client.auth.refresh_session({"refresh_token": refresh_token})
        if not getattr(res, "session", None):
            return jsonify({"ok": False, "error": "Falha ao atualizar a sessão"}), 401

        access_token = getattr(res.session, "access_token", None)
        refresh_token = getattr(res.session, "refresh_token", None)
        # res.user pode vir None — mantenha user atual da sessão
        user_obj = {
            "id": getattr(getattr(res, "user", None), "id", session.get("user", {}).get("id")),
            "email": getattr(getattr(res, "user", None), "email", session.get("user", {}).get("email")),
            "user_metadata": getattr(getattr(res, "user", None), "user_metadata", {}) or {},
        }
        _set_user_session(user_obj, access_token=access_token, refresh_token=refresh_token)

        return jsonify({"ok": True, "user": session.get("user")})
    except Exception as e:
        current_app.logger.warning("Refresh falhou: %s", e)
        return jsonify({"ok": False, "error": "Falha ao renovar a sessão"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Limpa a sessão. Opcionalmente informa o Supabase para revogar o token.
    """
    client = _supabase_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception as e:
            current_app.logger.debug("sign_out supabase: %s", e)

    _clear_session()
    return jsonify({"ok": True})


@auth_bp.route("/me", methods=["GET"])
def me():
    """
    Retorna informações básicas do usuário logado (da sessão).
    """
    user = session.get("user")
    if not user:
        return jsonify({"ok": False, "authenticated": False}), 401
    return jsonify({"ok": True, "authenticated": True, "user": user})


# -----------------------------
# (Opcional) OAuth server-side
# -----------------------------
@auth_bp.route("/oauth/<provider>/start", methods=["GET"])
def oauth_start(provider: str):
    """
    START de OAuth: retorna uma URL de autorização do Supabase para o browser.
    Recomendação: em produção, use o supabase-js no frontend (melhor UX).
    Aqui, entregamos a URL para o cliente redirecionar.
    """
    provider = provider.lower()
    if provider not in ("google", "github"):
        return jsonify({"ok": False, "error": "Provider inválido"}), 400

    if not (SUPABASE_URL and SUPABASE_KEY):
        if DEBUG:
            return jsonify({"ok": True, "dev": True, "notice": "Configure SUPABASE_URL/KEY para OAuth"})
        return jsonify({"ok": False, "error": "Supabase não configurado"}), 503

    # URL de autorização do GoTrue (Supabase Auth)
    # Doc: https://supabase.com/docs/guides/auth#third-party-oauth-providers
    # Em muitos setups o JS lida com apikey/header. Aqui só devolvemos a rota-base para o front redirecionar.
    auth_url = f"{SUPABASE_URL}/auth/v1/authorize?provider={provider}&redirect_to={BASE_URL}/login"
    state = str(uuid.uuid4())
    return jsonify({"ok": True, "url": auth_url, "state": state})
