"""
CareerForge AI - API Routes Module
"""

from .health_routes import router as health_router
from .ai_routes import router as ai_router
from .quiz_routes import router as quiz_router

__all__ = [
    "health_router",
    "ai_router",
    "quiz_router",
]
