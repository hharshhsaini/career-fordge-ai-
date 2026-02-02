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
    
    months = constraints.get("max_months", 6)
    
    prompt = f"""You are a career expert. Create a detailed 6-step learning roadmap for: "{user_profile}".

You MUST return a JSON object with exactly 6 steps in the "roadmap" array.
Structure each step exactly like the example below.
KEEP DESCRIPTIONS SHORT (max 15 words) for speed.

Example JSON Structure:
{{
    "career_role": "Python Developer",
    "summary": "6-month plan to master Python.",
    "roadmap": [
        {{
            "step_name": "Month 1: Python Basics",
            "description": "Master variables, loops, functions, and data structures.",
            "official_docs_url": "https://docs.python.org/3/",
            "paid_course_recommendation": "Complete Python Bootcamp"
        }},
        // ... generate exactly 6 steps
    ]
}}

Requirements:
1. "roadmap" array MUST have exactly 6 items.
2. "step_name" must start with "Month 1:", "Month 2:", etc.
3. Content must be specific to the user's goal.
4. "official_docs_url" must be a real URL.
5. Order MUST follow logical dependency (Beginner -> Advanced).
6. NO FLUFF. Every step must be justifiable and industry-relevant.

RETURN ONLY VALID JSON."""

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
