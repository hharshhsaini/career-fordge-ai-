"""
CareerForge AI - API Request Schemas
Pydantic models for request validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class UserProfile(BaseModel):
    """User profile for roadmap generation."""
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="User's background, skills, interests, and career goals"
    )
    hours_per_week: Optional[int] = Field(
        default=15,
        ge=1,
        le=60,
        description="Available study hours per week"
    )
    max_months: Optional[int] = Field(
        default=6,
        ge=1,
        le=24,
        description="Target timeline in months"
    )
    budget: Optional[str] = Field(
        default="free resources preferred",
        description="Budget for learning resources"
    )


class SkillsAnalysisRequest(BaseModel):
    """Request for skills analysis."""
    background: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="User's education, experience, current skills"
    )
    target_role: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Target career role"
    )
    interests: Optional[List[str]] = Field(
        default=None,
        description="List of interests"
    )


class TrendingSkillsRequest(BaseModel):
    """Request for trending skills in a domain."""
    domain: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Career domain to analyze"
    )


class InterviewPrepRequest(BaseModel):
    """Request for interview preparation guide."""
    role: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Target job role"
    )
    experience_level: Optional[str] = Field(
        default="mid",
        description="Experience level: entry, mid, or senior"
    )
    company: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Optional target company"
    )
    focus_areas: Optional[List[str]] = Field(
        default=None,
        description="Specific areas to focus on"
    )


class MockQuestionsRequest(BaseModel):
    """Request for mock interview questions."""
    role: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Target job role"
    )
    question_type: Optional[str] = Field(
        default="mixed",
        description="Question type: technical, behavioral, or mixed"
    )
    count: Optional[int] = Field(
        default=10,
        ge=1,
        le=25,
        description="Number of questions"
    )


class AnswerAnalysisRequest(BaseModel):
    """Request for interview answer analysis."""
    question: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The interview question"
    )
    answer: str = Field(
        ...,
        min_length=20,
        max_length=5000,
        description="User's answer to evaluate"
    )
    role: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Target role for context"
    )


class QuizRequest(BaseModel):
    """Request for quiz generation."""
    topic: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Career or technology topic"
    )
    step_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Specific step or topic to test"
    )
    num_questions: Optional[int] = Field(
        default=15,
        ge=1,
        le=30,
        description="Number of questions"
    )
    difficulty_mix: Optional[Dict[str, int]] = Field(
        default=None,
        description="Difficulty distribution: {easy: 30, medium: 50, hard: 20}"
    )


class QuizBatchRequest(BaseModel):
    """Request for quiz batch generation."""
    topic: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Career or technology topic"
    )
    step_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
        description="Specific step being tested"
    )
    count: Optional[int] = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of questions in batch"
    )
    start_id: Optional[int] = Field(
        default=1,
        ge=1,
        description="Starting ID for questions"
    )
    difficulty: Optional[str] = Field(
        default="mixed",
        description="Difficulty level: easy, medium, hard, or mixed"
    )
