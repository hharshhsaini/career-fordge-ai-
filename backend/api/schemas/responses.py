"""
CareerForge AI - API Response Schemas
Pydantic models for response formatting.
"""

from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class MetaInfo(BaseModel):
    """Metadata about the response."""
    model: str
    latency_ms: int
    tokens_used: int


class SuccessResponse(BaseModel):
    """Standard success response wrapper."""
    success: bool = True
    data: Dict[str, Any]
    meta: Optional[MetaInfo] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    services: Dict[str, str]


class QuizResponse(BaseModel):
    """Quiz generation response."""
    questions: List[Dict[str, Any]]
    meta: Optional[MetaInfo] = None
