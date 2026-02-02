"""
CareerForge AI - Interview Service
Generates interview preparation content.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from services.llm_service import LLMService, get_llm_service
from prompts.system_prompts import CAREERFORGE_SYSTEM_PROMPT


class InterviewService:
    """Service for interview preparation."""
    
    def __init__(self, llm_service: LLMService = None):
        self.llm = llm_service or get_llm_service()
    
    def generate_prep_guide(
        self,
        role: str,
        experience_level: str = "mid",
        company: str = None,
        focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """Generate interview preparation guide."""
        
        if not role:
            return {"success": False, "error": "Please specify the target role"}
        
        prompt = f"""Generate interview prep for: {role}
Experience Level: {experience_level}
Company: {company or "Not specified"}

Return JSON with: technical_questions (list), behavioral_questions (list), tips (list)"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=CAREERFORGE_SYSTEM_PROMPT,
            temperature=0.7,
            expect_json=True
        )
        
        if not response.success:
            return {"success": False, "error": response.error}
        
        return {
            "success": True,
            "data": response.parsed_json,
            "meta": {"model": response.model, "latency_ms": response.latency_ms}
        }
    
    def generate_mock_questions(
        self,
        role: str,
        question_type: str = "mixed",
        count: int = 10
    ) -> Dict[str, Any]:
        """Generate mock interview questions."""
        
        prompt = f"""Generate {count} {question_type} interview questions for: {role}

Return JSON with: questions (list of objects with question, type, difficulty)"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=CAREERFORGE_SYSTEM_PROMPT,
            temperature=0.7,
            expect_json=True
        )
        
        if not response.success:
            return {"success": False, "error": response.error}
        
        return {
            "success": True,
            "data": response.parsed_json,
            "meta": {"model": response.model, "latency_ms": response.latency_ms}
        }
    
    def analyze_answer(
        self,
        question: str,
        answer: str,
        role: str
    ) -> Dict[str, Any]:
        """Analyze interview answer and provide feedback."""
        
        if not answer or len(answer.strip()) < 20:
            return {"success": False, "error": "Please provide a more complete answer"}
        
        prompt = f"""Analyze this interview answer for {role}:
Question: {question}
Answer: {answer}

Return JSON with: score (1-10), strengths (list), improvements (list), improved_answer"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=CAREERFORGE_SYSTEM_PROMPT,
            temperature=0.6,
            expect_json=True
        )
        
        if not response.success:
            return {"success": False, "error": response.error}
        
        return {
            "success": True,
            "data": response.parsed_json,
            "meta": {"model": response.model, "latency_ms": response.latency_ms}
        }
