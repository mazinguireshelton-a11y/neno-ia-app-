"""
Authentication Routes - FastAPI Version
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    authenticated: bool

@router.post("/login", response_model=UserResponse)
async async def login(credentials: LoginRequest):
    try:
        if credentials.username == "admin" and credentials.password == "admin":
            return UserResponse(username=credentials.username, authenticated=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/me", response_model=UserResponse)
async async def get_current_user():
    return UserResponse(username="admin", authenticated=True)

@router.post("/logout")
async async def logout():
    return {"message": "Logged out successfully"}
