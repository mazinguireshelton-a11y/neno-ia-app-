import os
from pathlib import Path

class Config:
    # Diretórios
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOAD_DIR = BASE_DIR / "uploads"
    DATA_DIR = BASE_DIR / "data"
    LOG_DIR = BASE_DIR / "logs"
    
    # LLM Providers
    LLM_CONFIG = {
        'openai': {
            'api_key': os.getenv('OPENAI_API_KEY'),
            'model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        },
        'openrouter': {
            'api_key': os.getenv('OPENROUTER_API_KEY'),
            'model': os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o-mini')
        },
        'groq': {
            'api_key': os.getenv('GROQ_API_KEY'), 
            'model': os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile')
        }
    }
    
    # Segurança
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'}
