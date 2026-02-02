"""
CareerForge AI - Simplified Quiz Prompts
Optimized for smaller/faster LLMs.
"""


def get_simple_quiz_prompt(topic: str, step_name: str, count: int = 3, start_id: int = 1) -> str:
    """Generate a simple quiz prompt optimized for smaller LLMs."""
    
    return f"""Create {count} multiple choice questions about {step_name} for {topic}.

Return JSON:
{{
    "questions": [
        {{
            "id": {start_id},
            "question": "Your question here?",
            "code_snippet": null,
            "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
            "correct": "A",
            "explanation": "Brief explanation why A is correct",
            "difficulty": "medium",
            "topic_tag": "{step_name}"
        }}
    ]
}}

Requirements:
- Create exactly {count} questions
- IDs start from {start_id}
- Each has 4 options (A,B,C,D)
- One CLEAR correct answer
- Short, educational explanation
- Questions MUST test understanding of "{step_name}"
- NO trick questions or ambiguity
- NO generic questions unrelated to the topic

ONLY return valid JSON, no other text."""
