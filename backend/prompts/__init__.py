"""
CareerForge AI - Prompt Templates Module
Centralized prompt engineering for consistent AI behavior.
"""

from .system_prompts import CAREERFORGE_SYSTEM_PROMPT, get_system_prompt
from .roadmap_prompts import get_roadmap_prompt, ROADMAP_OUTPUT_SCHEMA
from .quiz_prompts import get_quiz_prompt, QUIZ_OUTPUT_SCHEMA

__all__ = [
    "CAREERFORGE_SYSTEM_PROMPT",
    "get_system_prompt",
    "get_roadmap_prompt",
    "ROADMAP_OUTPUT_SCHEMA",
    "get_quiz_prompt",
    "QUIZ_OUTPUT_SCHEMA",
]
