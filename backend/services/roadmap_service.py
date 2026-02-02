"""
CareerForge AI - Roadmap Service
Generates personalized career roadmaps using the LLM.
Optimized for faster responses with smaller models.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, Dict, Any
from services.llm_service import LLMService, get_llm_service
from prompts.system_prompts import CAREERFORGE_SYSTEM_PROMPT

# Use simplified prompts for faster responses
try:
    from prompts.roadmap_prompts_simple import get_simple_roadmap_prompt, get_simple_skills_gap_prompt
    USE_SIMPLE_PROMPTS = True
except ImportError:
    from prompts.roadmap_prompts import get_roadmap_prompt, get_skills_gap_prompt
    USE_SIMPLE_PROMPTS = False


class RoadmapService:
    """
    Service for generating career roadmaps.
    Optimized for fast responses with smaller LLMs.
    """
    
    def __init__(self, llm_service: LLMService = None):
        self.llm = llm_service or get_llm_service()
        print(f"[RoadmapService] Using {'simple' if USE_SIMPLE_PROMPTS else 'detailed'} prompts")
    
    def generate_roadmap(
        self,
        user_profile: str,
        hours_per_week: int = 15,
        max_months: int = 6,
        budget: str = "free resources preferred"
    ) -> Dict[str, Any]:
        """Generate a career roadmap optimized for speed."""
        
        if not user_profile or len(user_profile.strip()) < 10:
            return {
                "success": False,
                "error": "Please provide more details about your background and goals"
            }
        
        constraints = {
            "hours_per_week": hours_per_week,
            "max_months": max_months,
            "budget": budget
        }
        
        # Use simple prompt for faster generation
        if USE_SIMPLE_PROMPTS:
            prompt = get_simple_roadmap_prompt(user_profile, constraints)
        else:
            from prompts.roadmap_prompts import get_roadmap_prompt
            prompt = get_roadmap_prompt(user_profile, constraints)
        
        print(f"[RoadmapService] Generating roadmap for: {user_profile[:50]}...")
        
        response = self.llm.generate(
            prompt=prompt,
            system_prompt="You are a career expert. Return only valid JSON.",
            temperature=0.5,
            max_tokens=1500,  # Optimized for speed with shorter descriptions
            expect_json=True
        )
        
        if not response.success:
            print(f"[RoadmapService] LLM Error: {response.error}")
            return {
                "success": False,
                "error": response.error or "Failed to generate roadmap. Please try again."
            }
        
        roadmap_data = response.parsed_json
        if not self._validate_roadmap(roadmap_data):
            # Return what we got anyway - partial data is better than nothing
            print(f"[RoadmapService] Warning: Roadmap validation failed, returning raw data")
            return {
                "success": True,  # Still return as success if we have some data
                "data": roadmap_data if roadmap_data else {"error": "Incomplete response"},
                "meta": {
                    "model": response.model,
                    "latency_ms": response.latency_ms,
                    "tokens_used": response.tokens_used,
                    "note": "Response may be incomplete"
                }
            }
        
        return {
            "success": True,
            "data": roadmap_data,
            "meta": {
                "model": response.model,
                "latency_ms": response.latency_ms,
                "tokens_used": response.tokens_used
            }
        }
    
    def _validate_roadmap(self, data: Optional[Dict]) -> bool:
        """Validate roadmap structure - flexible to accept various formats."""
        if not data or not isinstance(data, dict):
            return False
        
        # Accept any response that looks like a roadmap
        valid_keys = {"career_role", "roadmap", "career", "months", "path", 
                      "skills", "overview", "plan", "steps"}
        
        return bool(set(data.keys()) & valid_keys)


def generate_roadmap(user_profile: str, **kwargs) -> Dict[str, Any]:
    """Convenience function for roadmap generation."""
    service = RoadmapService()
    return service.generate_roadmap(user_profile, **kwargs)
