"""
Chat Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import logging
from services.llm_service import llm_service

logger = logging.getLogger(__name__)
router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    mode: str = "standard"

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tokens_used: int

@router.post("/message", response_model=ChatResponse)
async def send_message(chat_message: ChatMessage):
    try:
        response = await llm_service.process_message(
            chat_message.message,
            chat_message.conversation_id,
            chat_message.mode
        )
        return ChatResponse(
            response=response["message"],
            conversation_id=response["conversation_id"],
            tokens_used=response.get("tokens_used", 0)
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            response = await llm_service.process_message(
                message_data["message"],
                message_data.get("conversation_id"),
                message_data.get("mode", "standard")
            )
            
            await websocket.send_text(json.dumps(response))
            
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=1011)

@router.get("/conversations")
async def get_conversations():
    try:
        # Implementar lógica de listagem de conversas
        return {"conversations": []}
    except Exception as e:
        logger.error(f"Conversations error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
