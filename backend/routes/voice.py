"""
Voice Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
router = APIRouter()
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class VoiceResponse(BaseModel):
    text: str
    duration: float
    language: Optional[str] = None

@router.post("/speech-to-text", response_model=VoiceResponse)
async def speech_to_text(file: UploadFile = File(...)):
    try:
        result = await voice_service.speech_to_text(file)
        return VoiceResponse(
            text=result["text"],
            duration=result.get("duration", 0),
            language=result.get("language")
        )
    except Exception as e:
        logger.error(f"Speech-to-text error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/text-to-speech")
async def text_to_speech(text: str, voice: str = "default"):
    try:
        result = await voice_service.text_to_speech(text, voice)
        return result
    except Exception as e:
        logger.error(f"Text-to-speech error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/voices")
async def get_available_voices():
    try:
        voices = await voice_service.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        logger.error(f"Voices error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
