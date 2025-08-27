# backend/services/file_service.py
import os
import fitz  # PyMuPDF para PDF
import docx
from pathlib import Path

def extract_text_from_file(path: Path) -> str:
    """
    Extrai texto de diferentes tipos de arquivos.
    """
    ext = path.suffix.lower()

    try:
        if ext == ".txt":
            return Path(path).read_text(encoding="utf-8", errors="ignore")

        elif ext == ".pdf":
            text = ""
            doc = fitz.open(path)
            for page in doc:
                text += page.get_text()
            return text

        elif ext == ".docx":
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif ext in [".jpg", ".jpeg", ".png"]:
            import pytesseract
            from PIL import Image
            return pytesseract.image_to_string(Image.open(path))

        elif ext in [".mp3", ".wav"]:
            # Aqui podemos mandar para Whisper
            return "[Áudio enviado: use modo voz para transcrição]"

        else:
            return "[Formato não suportado para extração]"
    except Exception as e:
        return f"[Erro ao extrair texto: {e}]"
