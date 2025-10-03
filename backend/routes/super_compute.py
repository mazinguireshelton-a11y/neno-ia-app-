"""
Super Compute Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import logging
from services.compute_cluster import compute_cluster
from plugins.super_ia_module import super_ia_instance as super_ia
from plugins.viz_engine import viz_engine

logger = logging.getLogger(__name__)
router = APIRouter()

class ComputeRequest(BaseModel):
    command: str
    parameters: Dict[str, Any] = {}
    optimize: bool = True
    generate_visualization: bool = False

@router.post("/api/super-compute")
async async def super_compute_endpoint(request: ComputeRequest):
    try:
        if request.optimize:
            from services.smart_optimizer import smart_optimizer
            result = smart_optimizer.optimize_computation(request.command, request.parameters)
        else:
            result = super_ia.execute(request.command, request.parameters)

        if request.generate_visualization:
            viz_result = viz_engine.execute(f"{request.command}_viz", {
                **request.parameters,
                **result
            })
            result['visualization'] = viz_result

        return {
            "success": True,
            "result": result,
            "metadata": {
                "command": request.command,
                "optimized": request.optimize,
            }
        }
    except Exception as e:
        logger.error(f"Super compute error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
