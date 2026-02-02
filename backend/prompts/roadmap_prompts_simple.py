"""
CareerForge AI - Simplified Roadmap Prompts
Faster, more concise prompts for smaller LLMs.
"""


def get_simple_roadmap_prompt(user_profile: str, constraints: dict = None) -> str:
    """
    Generate a simplified roadmap prompt optimized for smaller/faster LLMs.
    
    Args:
        user_profile: User's background, skills, interests, and goals
        constraints: Optional constraints
    
    Returns:
        Concise prompt for roadmap generation
    """
    
    if constraints is None:
        constraints = {}
    
    months = constraints.get("max_months", 3)
    
    prompt = f"""Create a {months}-month career roadmap for:
"{user_profile}"

Return JSON:
{{
    "career_role": "recommended job title",
    "overview": "why this fits you",
    "months": [
        {{
            "month": 1,
            "title": "Month title",
            "skills": ["skill1", "skill2"],
            "project": "one project to build",
            "goal": "measurable outcome"
        }}
    ],
    "resources": ["top 3 learning resources"]
}}

ONLY return valid JSON, no other text."""

    return prompt


def get_simple_skills_gap_prompt(current_skills: list, target_role: str) -> str:
    """Simplified skills gap analysis prompt."""
    
    skills_str = ", ".join(current_skills) if current_skills else "None"
    
    return f"""Analyze skills gap.
Current: {skills_str}
Target: {target_role}

Return JSON:
{{
    "missing_skills": ["skill1", "skill2", "skill3"],
    "priority_order": ["learn first", "learn second", "learn third"],
    "estimated_months": 6,
    "quick_wins": ["skill learnable in 1 week"]
}}

ONLY return valid JSON."""
