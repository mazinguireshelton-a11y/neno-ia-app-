"""
Serviço de processamento de voz para transcrição e síntese
"""
import os
import tempfile
import logging
from typing import Optional, Tuple
import requests

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        self.whisper_model = os.getenv("WHISPER_MODEL", "whisper-1")
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
    def transcribe_audio(self, audio_data: bytes, language: Optional[str] = None) -> str:
        """
        Transcreve áudio para texto usando Whisper
        """
        try:
            # Salva temporariamente o áudio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name
            
            try:
                # Usa OpenAI Whisper
                if self.openai_api_key:
                    return self._transcribe_with_openai(tmp_path, language)
                
                # Fallback para OpenRouter se disponível
                openrouter_key = os.getenv("OPENROUTER_API_KEY")
                if openrouter_key:
                    return self._transcribe_with_openrouter(tmp_path, language)
                    
                raise Exception("Nenhum serviço de transcrição configurado")
                    
            finally:
                # Limpa arquivo temporário
                try:
                    os.unlink(tmp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            raise
    
    def _transcribe_with_openai(self, audio_path: str, language: Optional[str]) -> str:
        """Transcrição usando OpenAI Whisper"""
        import openai
        
        client = openai.OpenAI(api_key=self.openai_api_key)
        
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=self.whisper_model,
                file=audio_file,
                language=language if language != "auto" else None,
                response_format="text"
            )
            
        return transcript
    
    def _transcribe_with_openrouter(self, audio_path: str, language: Optional[str]) -> str:
        """Transcrição usando OpenRouter (fallback)"""
        url = "https://openrouter.ai/api/v1/audio/transcriptions"
        
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {"model": "openai/whisper-1"}
            
            if language and language != "auto":
                data["language"] = language
                
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            }
            
            response = requests.post(url, files=files, data=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.json().get("text", "")
            else:
                raise Exception(f"OpenRouter error: {response.status_code} - {response.text}")
    
    def text_to_speech(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> Optional[bytes]:
        """
        Converte texto em fala usando ElevenLabs
        """
        if not self.elevenlabs_api_key:
            logger.warning("ElevenLabs API key não configurada")
            return None
            
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"ElevenLabs error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erro no TTS: {e}")
            return None
    
    def get_available_voices(self) -> list:
        """Retorna vozes disponíveis do ElevenLabs"""
        if not self.elevenlabs_api_key:
            return []
            
        try:
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": self.elevenlabs_api_key}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("voices", [])
            return []
            
        except Exception as e:
            logger.error(f"Erro ao buscar vozes: {e}")
            return []

# Instância global do serviço
voice_service = VoiceService()
