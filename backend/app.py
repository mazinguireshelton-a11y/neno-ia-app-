# backend/app.py
from __future__ import annotations

import os
import logging
import uuid
from pathlib import Path
from datetime import timedelta

from flask import (
    Flask, request, redirect, url_for, session,
    send_from_directory, jsonify, render_template
)
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

# .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# ---------------------------
# Caminhos e Config do App
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent              # /neno-ia-app
BACKEND_DIR = BASE_DIR / "backend"                             # /neno-ia-app/backend
FRONTEND_DIR = BASE_DIR / "frontend"                           # /neno-ia-app/frontend
STATIC_ROOT = BASE_DIR / "static"                              # /neno-ia-app/static
ASSETS_DIR = STATIC_ROOT / "assets"                            # /neno-ia-app/static/assets
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", STATIC_ROOT / "uploads"))
DATA_DIR = BASE_DIR / "data"                                   # /neno-ia-app/data

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    
    # ADICIONAR ESTAS LINHAS:
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / "logs"
    UPLOAD_DIR = BASE_DIR / "uploads" 
    DATA_DIR = BASE_DIR / "data"
    
    
    # Segredo / sessão
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or os.getenv("SECRET_KEY") or os.urandom(32)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("DEBUG", "false").lower() not in ("1", "true")  # True em produção (HTTPS)
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)

    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", os.getenv("DEBUG", "false")).lower() in ("1", "true")
    JSON_AS_ASCII = False
    TEMPLATES_AUTO_RELOAD = True if DEBUG else False
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024  # 50MB padrão

    # CORS
    CORS_ORIGINS = [
        os.getenv("BASE_URL", "http://localhost:5000"),
        os.getenv("FRONTEND_URL", "http://localhost:5000"),
        "http://127.0.0.1:5000",
        "http://localhost",
        "http://127.0.0.1",
    ]
    CORS_SUPPORTS_CREDENTIALS = True

def _init_services(app: Flask) -> None:
    """Inicializa serviços globais de forma organizada e robusta"""
    try:
        # ==================== SERVIÇOS PRINCIPAIS ====================
        app.logger.info("🔄 Inicializando serviços principais...")
        
        # Serviço de memória
        from backend.services.memory_service import MemoryService
        memory_path = DATA_DIR / "memories.json"
        app.memory_service = MemoryService(memory_path)
        app.logger.info("✅ MemoryService inicializado")
        
        # Serviço de plugins
        from backend.services.plugin_service import PluginService
        app.plugin_service = PluginService()
        app.logger.info("✅ PluginService inicializado")
        
        # Serviço de feedback
        from backend.services.feedback_service import FeedbackService
        feedback_path = DATA_DIR / "feedback.json"
        app.feedback_service = FeedbackService(feedback_path)
        app.logger.info("✅ FeedbackService inicializado")
        
        # ==================== SERVIÇOS DE IA ====================
        app.logger.info("🔄 Inicializando serviços de IA...")
        
        # Serviço de LLM (AGORA USANDO LLMService COOPERATIVO)
        from backend.services.llm_service import llm_service, LLMService
        app.llm_service = llm_service  # ✅ MUDANÇA: usar llm_service global
        app.logger.info(f"✅ LLMService inicializado com {len(app.llm_service.providers)} provedores")
        
        # LLM Router (para compatibilidade)
        try:
            from backend.services.llm_router import LLMRouter
            app.llm_router = LLMRouter()
            app.logger.info("✅ LLMRouter inicializado")
        except Exception as e:
            app.logger.warning(f"⚠️ LLMRouter não disponível: {e}")
            app.llm_router = None
        
        # ==================== SISTEMA COOPERATIVO ====================
        app.logger.info("🔄 Inicializando sistema cooperativo...")
        
        from backend.services.cooperative_orchestrator import init_cooperative_orchestrator
        app.cooperative_orchestrator = init_cooperative_orchestrator(app.llm_service)  # ✅ CORRIGIDO
        app.logger.info("✅ Sistema cooperativo inicializado")
        
        # ==================== INFRAESTRUTURA AVANÇADA ====================
        app.logger.info("🔄 Inicializando infraestrutura avançada...")
        
        # Banco Vetorial
        try:
            from backend.services.vector_db import VectorDBService
            app.vector_db = VectorDBService()
            app.logger.info("✅ VectorDBService inicializado")
        except Exception as e:
            app.logger.warning(f"⚠️ VectorDBService não disponível: {e}")
            app.vector_db = None
        
        # Cache Service
        try:
            from backend.services.cache_service import CacheService
            app.cache_service = CacheService()
            app.logger.info("✅ CacheService inicializado")
        except Exception as e:
            app.logger.warning(f"⚠️ CacheService não disponível: {e}")
            app.cache_service = None
        
        # Cluster de Computação
        try:
            from backend.services.advanced_compute_cluster import compute_cluster, AdvancedComputeCluster
            app.compute_cluster = compute_cluster
            app.logger.info("✅ ComputeCluster inicializado")
        except Exception as e:
            app.logger.warning(f"⚠️ ComputeCluster não disponível: {e}")
            app.compute_cluster = None
        
        # ==================== GERENCIADOR DE MODOS ====================
        app.logger.info("🔄 Inicializando gerenciador de modos...")
        
        # ✅ CORRIGIDO: Agora usando app.llm_service em vez de app.llm_router
        from backend.services.mode_manager import ModeManager
        app.mode_manager = ModeManager(app.plugin_service, app.llm_service)
        app.logger.info("✅ ModeManager inicializado")
        
        # ==================== MONITORAMENTO ====================
        app.logger.info("🔄 Inicializando monitoramento...")
        
        try:
            from backend.utils.monitoring import init_monitoring
            init_monitoring(app)
            app.logger.info("✅ Monitoramento inicializado")
        except Exception as e:
            app.logger.warning(f"⚠️ Monitoramento não disponível: {e}")
        
        # ==================== CONFIGURAÇÕES GLOBAIS ====================
        app.logger.info("🔄 Carregando configurações globais...")
        
        from backend.utils.constants import MODES, MODE_CAPABILITIES, DEFAULT_MODE_CONFIGS
        app.config['MODES'] = MODES
        app.config['MODE_CAPABILITIES'] = MODE_CAPABILITIES
        app.config['DEFAULT_MODE_CONFIGS'] = DEFAULT_MODE_CONFIGS
        app.logger.info(f"✅ {len(MODES)} modos carregados")
        
        # ==================== VERIFICAÇÃO DE SAÚDE ====================
        app.logger.info("🔍 Verificando saúde dos serviços...")
        
        services_health = {
            'llm_service': bool(app.llm_service and app.llm_service.providers),
            'plugin_service': bool(app.plugin_service),
            'cooperative_orchestrator': bool(app.cooperative_orchestrator),
            'mode_manager': bool(app.mode_manager),
            'vector_db': bool(app.vector_db),
            'cache_service': bool(app.cache_service),
            'compute_cluster': bool(app.compute_cluster)
        }
        
        healthy_services = sum(services_health.values())
        total_services = len(services_health)
        
        app.logger.info(f"📊 Saúde dos serviços: {healthy_services}/{total_services}")
        
        for service, status in services_health.items():
            status_icon = "✅" if status else "❌"
            app.logger.info(f"   {status_icon} {service}: {'OK' if status else 'FALHA'}")
        
        if healthy_services == total_services:
            app.logger.info("🎉 Todos os serviços inicializados com sucesso!")
        else:
            app.logger.warning(f"⚠️  Alguns serviços não inicializaram: {total_services - healthy_services} falhas")
        
    except ImportError as e:
        app.logger.error(f"❌ Erro de importação: {e}")
        raise
    except Exception as e:
        app.logger.error(f"❌ Erro crítico na inicialização: {e}")
        raise

def create_app() -> Flask:
    # Servimos arquivos estáticos **da pasta FRONTEND** para manter
    # referências como <link href="neno.css"> funcionando.
    # Assets/Uploads ganham rotas dedicadas abaixo.
    app = Flask(
        __name__,
        template_folder=str(FRONTEND_DIR),
        static_folder=str(FRONTEND_DIR),
        static_url_path=""  # permite /neno.css, /script.js direto na raiz
    )
    app.config.from_object(Config)

    # Proxy fix (caso rode atrás de Nginx/Ingress)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # CORS
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=app.config["CORS_SUPPORTS_CREDENTIALS"],
    )

    # Logging estruturado
    _init_logging(app)

    # Inicializar serviços
    _init_services(app)

    # ID de requisição para rastreio
    @app.before_request
    def _attach_request_id():
        request.id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # log básico de início
        app.logger.info(
            "REQ %s %s %s ip=%s ua=%s",
            request.id, request.method, request.path,
            request.headers.get("X-Forwarded-For", request.remote_addr),
            request.user_agent.string if request.user_agent else "-",
        )

    @app.after_request
    def _security_headers(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        resp.headers.setdefault("X-XSS-Protection", "1; mode=block")
        csp = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:;"
            "img-src 'self' data: blob: https:;"
            "media-src 'self' blob:;"
            "connect-src 'self' https: http:;"
        )
        resp.headers.setdefault("Content-Security-Policy", csp)
        return resp

    # ---------------------------
    # Rotas de Arquivos Estáticos
    # ---------------------------
    # /assets/* → static/assets
    @app.route("/assets/<path:filename>")
    def assets(filename):
        return send_from_directory(ASSETS_DIR, filename)

    # /uploads/* → static/uploads
    @app.route("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)

    # ---------------------------
    # Páginas (Templates)
    # ---------------------------
    # Observação: como template_folder = FRONTEND_DIR,
    # render_template("login.html") / ("index.html") funciona.
    @app.route("/")
    def home():
        # Se quiser forçar login:
        if not session.get("user"):
            return redirect(url_for("login_page"))
        return render_template("index.html")

    @app.route("/login")
    def login_page():
        return render_template("login.html")

    @app.route("/voice")
    def voice_page():
        return render_template("voice.html")

    # Healthcheck
    @app.route("/healthz")
    def healthz():
        return jsonify({"status": "ok"})

    # ---------------------------
    # Blueprints (API)
    # ---------------------------
    _register_blueprints(app)

    # ---------------------------
    # Tratamento de Erros
    # ---------------------------
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"ok": False, "error": "Rota não encontrada", "code": 404}), 404
        # fallback para login ou index
        try:
            return render_template("index.html"), 404
        except Exception:
            return "404 Not Found", 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"ok": False, "error": "Arquivo muito grande", "code": 413}), 413

    @app.errorhandler(Exception)
    def on_error(e):
        app.logger.exception("Unhandled error: %s", e)
        if request.path.startswith("/api/"):
            return jsonify({"ok": False, "error": str(e), "code": 500}), 500
        # Em páginas HTML, mostramos erro simples
        return render_template("login.html"), 500

    return app


def _register_blueprints(app: Flask):
    """
    Importa e registra os blueprints. Mantém o app rodando
    mesmo se algum módulo opcional não estiver instalado durante dev.
    """
    # /api/auth
    try:
        from backend.routes.auth import auth_bp  # ✅ CORRIGIDO: backend.routes
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
    except Exception as e:
        app.logger.warning("Auth blueprint não carregado: %s", e)

    # /api/chat (streaming SSE e chat normal)
    try:
        from backend.routes.chat import chat_bp  # ✅ CORRIGIDO: backend.routes
        app.register_blueprint(chat_bp, url_prefix="/api")
    except Exception as e:
        app.logger.warning("Chat blueprint não carregado: %s", e)

    # /api/uploads
    try:
        from backend.routes.uploads import uploads_bp  # ✅ CORRIGIDO: backend.routes
        app.register_blueprint(uploads_bp, url_prefix="/api")
    except Exception as e:
        app.logger.warning("Uploads blueprint não carregado: %s", e)

    # /api/voice
    try:
        from backend.routes.voice import voice_bp  # ✅ CORRIGIDO: backend.routes
        app.register_blueprint(voice_bp, url_prefix="/api")
    except Exception as e:
        app.logger.warning("Voice blueprint não carregado: %s", e)

    # ✅ NOVO: Modos
    try:
        from backend.routes.modes import modes_bp
        app.register_blueprint(modes_bp, url_prefix="/api")
    except Exception as e:
        app.logger.warning("Modes blueprint não carregado: %s", e)

def _init_logging(app: Flask):
    """Configuração avançada de logging"""
    log_dir = Config.LOG_DIR
    log_dir.mkdir(exist_ok=True)

    # Formato detalhado
    formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)

    # Handler para arquivo
    file_handler = logging.FileHandler(log_dir / 'app.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)

    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    # ✅ REMOVER handlers existentes primeiro
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Filter para adicionar contexto
'''
    class ContextFilter(logging.Filter):
        def filter(self, record):
            record.client_ip = request.remote_addr if hasattr(request, 'remote_addr') else 'unknown'
            record.user_id = session.get('user', {}).get('id', 'anonymous') if hasattr(session, 'get') else 'anonymous'
            record.request_id = getattr(request, 'id', 'unknown')
            return True '''

    # ✅✅✅ ESTA LINHA DEVE ESTAR AQUI DENTRO DA FUNÇÃO!
   # root_logger.addFilter(ContextFilter())
# ---------------------------
# CLI
# ---------------------------
app = create_app()

if __name__ == "__main__":
    # Em dev/Termux: python backend/app.py
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    app.run(host=host, port=port, debug=app.config["DEBUG"])
