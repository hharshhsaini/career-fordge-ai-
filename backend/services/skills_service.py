"""
CareerForge AI - Skills Service
Analyzes user skills and provides recommendations.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List
from services.llm_service import LLMService, get_llm_service
from prompts.system_prompts import CAREERFORGE_SYSTEM_PROMPT


class SkillsService:
    """Service for analyzing and recommending skills."""
    
    def __init__(self, llm_service: LLMService = None):
        self.llm = llm_service or get_llm_service()
    
    def analyze_skills(
        self,
        background: str,
        target_role: str = None,
        interests: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze user's background and recommend skills."""
        
        if not background or len(background.strip()) < 10:
            return {"success": False, "error": "Please provide more details"}
        
        interests_str = ", ".join(interests) if interests else "Not specified"
        target_str = target_role or "Not specified"
        
        prompt = f"""Analyze this person's skills and provide recommendations.
Background: {background}
Target Role: {target_str}
Interests: {interests_str}

Return JSON with: profile_summary, recommended_skills (list), learning_path"""

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
    
    def get_trending_skills(self, domain: str) -> Dict[str, Any]:
        """Get trending skills for a domain."""
        
        prompt = f"""List trending skills for: {domain}
Return JSON with: trending_skills (list with skill, trend, demand_level)"""

        response = self.llm.generate(
            prompt=prompt,
            system_prompt=CAREERFORGE_SYSTEM_PROMPT,
            temperature=0.5,
            expect_json=True
        )
        
        if not response.success:
            return {"success": False, "error": response.error}
        
        return {
            "success": True,
            "data": response.parsed_json,
            "meta": {"model": response.model, "latency_ms": response.latency_ms}
        }
