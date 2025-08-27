"""
Utilitários de segurança para a aplicação NENO IA
"""
import re
import html
import uuid
from functools import wraps
from flask import request, jsonify, current_app

def sanitize_input(text: str, max_length: int = 4000) -> str:
    """
    Sanitiza entrada de texto para prevenir XSS e outros ataques
    
    Args:
        text: Texto a ser sanitizado
        max_length: Comprimento máximo permitido
    
    Returns:
        str: Texto sanitizado
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Limita o comprimento
    text = text.strip()[:max_length]
    
    # Escapa HTML para prevenir XSS
    text = html.escape(text)
    
    # Remove caracteres potencialmente perigosos
    text = re.sub(r'[<>"\'();\\]', '', text)
    
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def require_auth(f):
    """
    Decorator para exigir autenticação
    
    Usage:
        @require_auth
        def minha_rota():
            return "Acesso permitido"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user') or not request.user:
            return jsonify({
                "ok": False, 
                "error": "Autenticação necessária",
                "code": 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def generate_secure_token() -> str:
    """
    Gera um token seguro usando UUID4
    
    Returns:
        str: Token seguro
    """
    return str(uuid.uuid4())

def validate_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args:
        email: Email a ser validado
    
    Returns:
        bool: True se o email for válido
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> tuple:
    """
    Valida força da senha
    
    Args:
        password: Senha a ser validada
    
    Returns:
        tuple: (bool, str) - (é válida, mensagem de erro)
    """
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"
    
    if not re.search(r'[A-Z]', password):
        return False, "A senha deve conter pelo menos uma letra maiúscula"
    
    if not re.search(r'[a-z]', password):
        return False, "A senha deve conter pelo menos uma letra minúscula"
    
    if not re.search(r'[0-9]', password):
        return False, "A senha deve conter pelo menos um número"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "A senha deve conter pelo menos um caractere especial"
    
    return True, "Senha válida"

def rate_limit(max_requests: int = 100, window: int = 900):
    """
    Decorator para limitar taxa de requisições
    
    Args:
        max_requests: Número máximo de requisições
        window: Janela de tempo em segundos (padrão: 15 minutos)
    
    Returns:
        function: Decorator
    """
    from datetime import datetime, timedelta
    
    requests = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            now = datetime.now()
            ip = request.remote_addr
            
            # Limpa requisições antigas
            for ip_addr, timestamps in list(requests.items()):
                requests[ip_addr] = [
                    ts for ts in timestamps 
                    if now - ts < timedelta(seconds=window)
                ]
                if not requests[ip_addr]:
                    del requests[ip_addr]
            
            # Verifica limite
            if ip in requests and len(requests[ip]) >= max_requests:
                return jsonify({
                    "ok": False,
                    "error": "Limite de requisições excedido",
                    "retry_after": window
                }), 429
            
            # Registra requisição
            if ip not in requests:
                requests[ip] = []
            requests[ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def validate_file_upload(file_stream, filename, max_size):
    """Validação completa de upload de arquivos"""
    if not allowed_file(filename):
        return False, "Tipo de arquivo não permitido"
    
    # Verificar tamanho
    file_stream.seek(0, 2)  # Ir para o final
    size = file_stream.tell()
    file_stream.seek(0)  # Voltar ao início
    
    if size > max_size:
        return False, f"Arquivo muito grande. Máximo: {max_size} bytes"
    
    # Verificar conteúdo (opcional)
    if filename.endswith(('.exe', '.bat', '.sh')):
        return False, "Tipo de arquivo potencialmente perigoso"
    
    return True, "OK"

def sanitize_sql_input(input_str):
    """Prevenir SQL injection"""
    if not input_str:
        return ""
    
    # Remover caracteres perigosos
    dangerous = [';', "'", '"', '--', '/*', '*/', 'xp_']
    for char in dangerous:
        input_str = input_str.replace(char, '')
    
    return input_str.strip()
