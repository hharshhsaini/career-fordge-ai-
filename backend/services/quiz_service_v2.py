"""
CareerForge AI - Quiz Service V2 (Open-Source LLM)
Generates knowledge assessment quizzes using self-hosted LLMs.
Optimized for faster responses with smaller models.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, Optional
from services.llm_service import LLMService, get_llm_service

# Use simplified prompts for faster responses
try:
    from prompts.quiz_prompts_simple import get_simple_quiz_prompt
    USE_SIMPLE_PROMPTS = True
except ImportError:
    from prompts.quiz_prompts import get_quiz_prompt, get_quiz_batch_prompt
    USE_SIMPLE_PROMPTS = False

print(f"[QuizService] Using {'simple' if USE_SIMPLE_PROMPTS else 'detailed'} prompts")


class QuizService:
    """Service for generating knowledge assessment quizzes."""
    
    def __init__(self, llm_service: LLMService = None):
        self.llm = llm_service or get_llm_service()
    
    def generate_quiz(
        self,
        topic: str,
        step_name: str,
        num_questions: int = 15,
        difficulty_mix: Dict[str, int] = None
    ) -> Dict[str, Any]:
        """Generate a full quiz for a roadmap step."""
        
        if not topic or not step_name:
            return {"error": "Topic and step_name are required"}
        
        prompt = get_quiz_prompt(topic, step_name, num_questions, difficulty_mix)
        system_prompt = f"{CAREERFORGE_SYSTEM_PROMPT}\n\n{QUIZ_GENERATION_CONTEXT}"
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=4000,
            expect_json=True
        )
        
        if not response.success:
            return {"error": response.error or "Failed to generate quiz"}
        
        quiz_data = response.parsed_json
        if "questions" not in quiz_data:
            quiz_data = {"questions": []}
        
        quiz_data["meta"] = {
            "model": response.model,
            "latency_ms": response.latency_ms,
            "tokens_used": response.tokens_used
        }
        
        return quiz_data
    
    def generate_quiz_batch(
        self,
        topic: str,
        step_name: str,
        count: int = 5,
        start_id: int = 1,
        difficulty: str = "mixed"
    ) -> Dict[str, Any]:
        """Generate a batch of quiz questions optimized for speed."""
        
        if not topic or not step_name:
            return {"error": "Topic and step_name are required"}
        
        # Use simple prompts for faster responses
        if USE_SIMPLE_PROMPTS:
            prompt = get_simple_quiz_prompt(topic, step_name, count, start_id)
        else:
            from prompts.quiz_prompts import get_quiz_batch_prompt
            prompt = get_quiz_batch_prompt(topic, step_name, count, start_id, difficulty)
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are a quiz generator. Return only valid JSON.",
            temperature=0.5,
            max_tokens=1000,  # Reduced for faster responses
            expect_json=True
        )
        
        if not response.success:
            return {"error": response.error or "Failed to generate quiz batch"}
        
        return response.parsed_json or {"questions": []}


# Backward compatibility functions
def generate_quiz_openai(topic: str, step_name: str) -> Dict[str, Any]:
    """Generate quiz (backward compatible)."""
    service = QuizService()
    return service.generate_quiz(topic, step_name)


def generate_quiz_batch(
    topic: str,
    step_name: str,
    count: int = 5,
    start_id: int = 1
) -> Dict[str, Any]:
    """Generate quiz batch (backward compatible)."""
    service = QuizService()
    return service.generate_quiz_batch(topic, step_name, count, start_id)
