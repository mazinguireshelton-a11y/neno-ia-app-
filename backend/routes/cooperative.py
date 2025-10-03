"""
Cooperative Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
router = APIRouter()
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class CooperativeRequest(BaseModel):
    task: str
    parameters: Dict[str, Any] = {}
    agents: List[str] = []

@router.post("/execute")
async async def execute_cooperative_task(request: CooperativeRequest):
    try:
        result = await cooperative_orchestrator.orchestrate_task(
            request.task,
            request.parameters,
            request.agents
        )
        return {
            "success": True,
            "result": result,
            "agents_used": request.agents
        }
    except Exception as e:
        logger.error(f"Cooperative task error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/agents")
async async def get_available_agents():
    try:
        agents = await cooperative_orchestrator.get_available_agents()
        return {"agents": agents}
    except Exception as e:
        logger.error(f"Agents error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
