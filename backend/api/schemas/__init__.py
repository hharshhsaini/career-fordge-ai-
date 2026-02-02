"""
CareerForge AI - API Schemas Module
"""

from .requests import (
    UserProfile,
    SkillsAnalysisRequest,
    TrendingSkillsRequest,
    InterviewPrepRequest,
    MockQuestionsRequest,
    AnswerAnalysisRequest,
    QuizRequest,
    QuizBatchRequest,
)

from .responses import (
    MetaInfo,
    SuccessResponse,
    ErrorResponse,
    HealthResponse,
    QuizResponse,
)

__all__ = [
    # Request schemas
    "UserProfile",
    "SkillsAnalysisRequest",
    "TrendingSkillsRequest",
    "InterviewPrepRequest",
    "MockQuestionsRequest",
    "AnswerAnalysisRequest",
    "QuizRequest",
    "QuizBatchRequest",
    # Response schemas
    "MetaInfo",
    "SuccessResponse",
    "ErrorResponse",
    "HealthResponse",
    "QuizResponse",
]
