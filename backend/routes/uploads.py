"""
Uploads Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional
router = APIRouter()
router = APIRouter()
import logging
from pathlib import Path
import tempfile
import os

logger = logging.getLogger(__name__)
router = APIRouter()

class UploadResponse(BaseModel):
    success: bool
    message: str
    content: Optional[str] = None
    file_type: Optional[str] = None

@router.post("/file", response_model=UploadResponse)
async async def upload_file(file: UploadFile = File(...)):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Extract text
            text_content = extract_text_from_file(Path(tmp_path))
            
            return UploadResponse(
                success=True,
                message="File processed successfully",
                content=text_content,
                file_type=file.content_type
            )
        finally:
            # Cleanup
            os.unlink(tmp_path)

    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/supported-formats")
async async def get_supported_formats():
    try:
        formats = [".txt", ".pdf", ".docx", ".csv", ".json"]
        return {"supported_formats": formats}
    except Exception as e:
        logger.error(f"Formats error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
