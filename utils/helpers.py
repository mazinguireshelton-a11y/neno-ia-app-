"""
Funções auxiliares para a aplicação NENO IA
"""
import uuid
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

def generate_id() -> str:
    """
    Gera um ID único usando UUID4
    
    Returns:
        str: ID único
    """
    return str(uuid.uuid4())

def format_timestamp(timestamp: Optional[datetime] = None, 
                    format_str: str = "%H:%M") -> str:
    """
    Formata timestamp para exibição amigável
    
    Args:
        timestamp: Timestamp a ser formatado (None para agora)
        format_str: Formato desejado
    
    Returns:
        str: Timestamp formatado
    """
    if not timestamp:
        timestamp = datetime.now()
    return timestamp.strftime(format_str)

def format_relative_time(timestamp: datetime) -> str:
    """
    Formata tempo relativo (ex: "há 2 minutos")
    
    Args:
        timestamp: Timestamp de referência
    
    Returns:
        str: Tempo relativo formatado
    """
    now = datetime.now()
    diff = now - timestamp
    
    if diff < timedelta(minutes=1):
        return "agora mesmo"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"há {minutes} minuto{'s' if minutes > 1 else ''}"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"há {hours} hora{'s' if hours > 1 else ''}"
    elif diff < timedelta(days=30):
        days = diff.days
        return f"há {days} dia{'s' if days > 1 else ''}"
    else:
        return timestamp.strftime("%d/%m/%Y")

def truncate_text(text: str, max_length: int = 100, 
                 ellipsis: str = "...") -> str:
    """
    Trunca texto com elipses se muito longo
    
    Args:
        text: Texto a ser truncado
        max_length: Comprimento máximo
        ellipsis: String de elipse
    
    Returns:
        str: Texto truncado
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(ellipsis)] + ellipsis

def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em bytes para formato legível
    
    Args:
        size_bytes: Tamanho em bytes
    
    Returns:
        str: Tamanho formatado (ex: "2.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.1f} {units[unit_index]}"

def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """
    Faz merge profundo de dois dicionários
    
    Args:
        dict1: Primeiro dicionário
        dict2: Segundo dicionário
    
    Returns:
        Dict: Dicionário mergeado
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if (key in result and isinstance(result[key], dict) 
            and isinstance(value, dict)):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result

def retry_operation(operation, max_attempts: int = 3, 
                   delay: float = 1.0, backoff: float = 2.0):
    """
    Tenta executar uma operação com retry automático
    
    Args:
        operation: Função a ser executada
        max_attempts: Número máximo de tentativas
        delay: Delay inicial entre tentativas
        backoff: Fator de backoff exponencial
    
    Returns:
        Any: Resultado da operação
    
    Raises:
        Exception: Se todas as tentativas falharem
    """
    attempt = 1
    current_delay = delay
    
    while attempt <= max_attempts:
        try:
            return operation()
        except Exception as e:
            if attempt == max_attempts:
                raise e
            
            time.sleep(current_delay)
            current_delay *= backoff
            attempt += 1

def is_valid_url(url: str) -> bool:
    """
    Verifica se uma string é uma URL válida
    
    Args:
        url: String a ser verificada
    
    Returns:
        bool: True se for uma URL válida
    """
    import re
    pattern = re.compile(
        r'^(https?|ftp)://'  # protocolo
        r'([A-Z0-9]([A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}'  # domínio
        r'(:\d+)?'  # porta
        r'(/.*)?$',  # caminho
        re.IGNORECASE
    )
    return bool(pattern.match(url))

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divide uma lista em chunks menores
    
    Args:
        lst: Lista a ser dividida
        chunk_size: Tamanho de cada chunk
    
    Returns:
        List[List[Any]]: Lista de chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
