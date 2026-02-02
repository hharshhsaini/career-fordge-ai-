"""
CareerForge AI - Roadmap Generation Prompts
Templates for generating structured career roadmaps.
"""

# JSON schema that the LLM must follow
ROADMAP_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["career_role", "overview", "timeline_months", "roadmap", "final_outcome"],
    "properties": {
        "career_role": {"type": "string"},
        "overview": {"type": "string"},
        "timeline_months": {"type": "integer"},
        "roadmap": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["month", "title", "focus_areas", "weeks", "tools", "projects", "checkpoint"],
                "properties": {
                    "month": {"type": "integer"},
                    "title": {"type": "string"},
                    "focus_areas": {"type": "array", "items": {"type": "string"}},
                    "weeks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "week": {"type": "integer"},
                                "focus": {"type": "string"},
                                "hours": {"type": "integer"},
                                "tasks": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "tools": {"type": "array", "items": {"type": "string"}},
                    "projects": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "description": {"type": "string"},
                                "difficulty": {"type": "string", "enum": ["beginner", "intermediate", "advanced"]},
                                "estimated_hours": {"type": "integer"},
                                "skills_practiced": {"type": "array", "items": {"type": "string"}}
                            }
                        }
                    },
                    "checkpoint": {"type": "string"}
                }
            }
        },
        "final_outcome": {"type": "string"},
        "resources": {
            "type": "object",
            "properties": {
                "official_docs": {"type": "array", "items": {"type": "string"}},
                "recommended_courses": {"type": "array", "items": {"type": "string"}},
                "youtube_channels": {"type": "array", "items": {"type": "string"}},
                "books": {"type": "array", "items": {"type": "string"}},
                "communities": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
}


def get_roadmap_prompt(user_profile: str, constraints: dict = None) -> str:
    """
    Generate the roadmap generation prompt.
    
    Args:
        user_profile: User's background, skills, interests, and goals
        constraints: Optional constraints like available hours per week, timeline, etc.
    
    Returns:
        Complete prompt for roadmap generation
    """
    
    # Extract constraints with defaults
    if constraints is None:
        constraints = {}
    
    hours_per_week = constraints.get("hours_per_week", 15)
    max_months = constraints.get("max_months", 6)
    budget = constraints.get("budget", "free resources preferred")
    
    prompt = f"""## User Profile
{user_profile}

## Constraints
- Available time: {hours_per_week} hours per week
- Target timeline: {max_months} months maximum
- Budget: {budget}

## Your Task
Generate a comprehensive, actionable career roadmap for this person.

## Required Output Format
You MUST return ONLY valid JSON matching this exact structure (no markdown, no explanations outside JSON):

{{
    "career_role": "The recommended career role/title",
    "overview": "2-3 sentence summary of why this career fits them and the overall approach",
    "timeline_months": 6,
    "roadmap": [
        {{
            "month": 1,
            "title": "Phase 1: Foundation Building",
            "focus_areas": ["HTML/CSS", "Git Basics", "Terminal Commands"],
            "weeks": [
                {{
                    "week": 1,
                    "focus": "HTML5 Semantic Elements & Structure",
                    "hours": 15,
                    "tasks": [
                        "Complete MDN HTML tutorial",
                        "Build 3 basic webpage layouts",
                        "Learn VS Code shortcuts"
                    ]
                }},
                {{
                    "week": 2,
                    "focus": "CSS Fundamentals & Flexbox",
                    "hours": 15,
                    "tasks": [
                        "Master CSS selectors and specificity",
                        "Complete Flexbox Froggy game",
                        "Style your HTML pages"
                    ]
                }}
            ],
            "tools": ["VS Code", "Chrome DevTools", "Git"],
            "projects": [
                {{
                    "name": "Personal Portfolio Website",
                    "description": "A responsive portfolio showcasing your work",
                    "difficulty": "beginner",
                    "estimated_hours": 10,
                    "skills_practiced": ["HTML5", "CSS3", "Responsive Design"]
                }}
            ],
            "checkpoint": "Can build a responsive multi-page website from scratch without tutorials"
        }}
    ],
    "final_outcome": "After completing this roadmap, you will be able to [specific outcomes with measurable results]",
    "resources": {{
        "official_docs": ["https://developer.mozilla.org/en-US/docs/Learn"],
        "recommended_courses": ["The Odin Project (Free)", "CS50x (Free)", "Udemy: Complete Web Developer"],
        "youtube_channels": ["Traversy Media", "Fireship", "The Coding Train"],
        "books": ["Eloquent JavaScript (Free Online)"],
        "communities": ["r/learnprogramming", "freeCodeCamp Forum"]
    }}
}}

## Critical Requirements
1. Generate exactly 6 months of content (or adjust based on timeline constraint)
2. Each month must have specific weekly breakdowns
3. Projects must have clear difficulty levels and hour estimates
4. Checkpoints must be measurable/demonstrable skills
5. Tools must be industry-standard and currently relevant
6. Resources must include free options
7. Tasks must be specific and actionable (not vague like "practice coding")

RETURN ONLY THE JSON OBJECT. NO ADDITIONAL TEXT."""

    return prompt


def get_skills_gap_prompt(current_skills: list, target_role: str) -> str:
    """
    Generate prompt for analyzing skills gap.
    
    Args:
        current_skills: List of skills the user already has
        target_role: The career role they're aiming for
    
    Returns:
        Prompt for skills gap analysis
    """
    
    skills_str = ", ".join(current_skills) if current_skills else "None specified"
    
    return f"""## Current Skills
{skills_str}

## Target Role
{target_role}

## Your Task
Analyze the gap between current skills and required skills for the target role.

## Required Output Format
Return ONLY valid JSON:

{{
    "target_role": "{target_role}",
    "required_skills": [
        {{
            "skill": "JavaScript",
            "importance": "critical",
            "current_level": "none|beginner|intermediate|advanced",
            "target_level": "intermediate",
            "learning_hours": 80,
            "priority_rank": 1
        }}
    ],
    "transferable_skills": [
        {{
            "existing_skill": "Problem Solving",
            "applies_to": "Debugging and algorithm design",
            "leverage_rating": "high"
        }}
    ],
    "recommended_learning_order": ["Skill1", "Skill2", "Skill3"],
    "quick_wins": ["Skills that can be learned in under 1 week"],
    "long_term_investments": ["Skills requiring 3+ months to develop"]
}}

RETURN ONLY THE JSON OBJECT."""
