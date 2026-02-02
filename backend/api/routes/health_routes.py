"""
CareerForge AI - Health Routes
System health check endpoints.
"""

from fastapi import APIRouter
import sys
import os
os.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('../..')
from services.llm_service import get_llm_service

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health_check():
    """
    Basic health check endpoint.
    Returns overall system status.
    """
    return {
        "status": "healthy",
        "version": "3.0.0",
        "engine": "open-source-llm"
    }


@router.get("/llm")
async def llm_health_check():
    """
    Check LLM service health.
    Verifies Ollama is running and model is available.
    """
    llm_service = get_llm_service()
    is_healthy, status_message = llm_service.check_health()
    
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "message": status_message,
        "model": llm_service.model,
        "base_url": llm_service.base_url
    }


@router.get("/models")
async def list_available_models():
    """
    List available models in Ollama.
    """
    llm_service = get_llm_service()
    models = llm_service.list_models()
    
    return {
        "available_models": models,
        "primary_model": llm_service.model,
        "fallback_model": llm_service.fallback_model
    }
