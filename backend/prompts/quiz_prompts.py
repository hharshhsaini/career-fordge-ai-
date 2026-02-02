"""
CareerForge AI - Quiz Generation Prompts
Templates for generating knowledge assessment quizzes.
"""

# JSON schema for quiz output
QUIZ_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["questions"],
    "properties": {
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "question", "options", "correct", "explanation", "difficulty"],
                "properties": {
                    "id": {"type": "integer"},
                    "question": {"type": "string"},
                    "code_snippet": {"type": "string"},
                    "options": {
                        "type": "object",
                        "properties": {
                            "A": {"type": "string"},
                            "B": {"type": "string"},
                            "C": {"type": "string"},
                            "D": {"type": "string"}
                        }
                    },
                    "correct": {"type": "string", "enum": ["A", "B", "C", "D"]},
                    "explanation": {"type": "string"},
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
                    "topic_tag": {"type": "string"}
                }
            }
        }
    }
}


def get_quiz_prompt(
    topic: str,
    step_name: str,
    num_questions: int = 15,
    difficulty_mix: dict = None
) -> str:
    """
    Generate the quiz generation prompt.
    
    Args:
        topic: The career/technology topic (e.g., "Full-Stack Development")
        step_name: The specific step being tested (e.g., "React Fundamentals")
        num_questions: Number of questions to generate
        difficulty_mix: Dict with easy/medium/hard percentages
    
    Returns:
        Complete prompt for quiz generation
    """
    
    if difficulty_mix is None:
        difficulty_mix = {"easy": 30, "medium": 50, "hard": 20}
    
    easy_count = int(num_questions * difficulty_mix["easy"] / 100)
    medium_count = int(num_questions * difficulty_mix["medium"] / 100)
    hard_count = num_questions - easy_count - medium_count
    
    prompt = f"""## Quiz Generation Task

**Topic**: {topic}
**Specific Focus**: {step_name}
**Total Questions**: {num_questions}
**Difficulty Distribution**: {easy_count} easy, {medium_count} medium, {hard_count} hard

## Question Quality Requirements

### For EASY Questions (Difficulty: "easy")
- Test basic terminology and concepts
- Straightforward, no trick questions
- Should be answerable by someone who completed the topic

### For MEDIUM Questions (Difficulty: "medium")  
- Test practical application of concepts
- May include simple code snippets
- Require understanding, not just memorization

### For HARD Questions (Difficulty: "hard")
- Test deep understanding or edge cases
- Include realistic code scenarios
- May require combining multiple concepts

## Code Snippet Guidelines
- Use proper formatting with clear indentation
- Keep snippets concise but realistic
- Include relevant context (variable declarations, etc.)
- For JavaScript/Python, show actual runnable code

## Required Output Format
Return ONLY valid JSON with this exact structure:

{{
    "questions": [
        {{
            "id": 1,
            "question": "What is the correct way to declare a constant in JavaScript?",
            "code_snippet": null,
            "options": {{
                "A": "var PI = 3.14;",
                "B": "let PI = 3.14;",
                "C": "const PI = 3.14;",
                "D": "constant PI = 3.14;"
            }},
            "correct": "C",
            "explanation": "The 'const' keyword is used to declare constants in JavaScript (ES6+). Unlike 'var' and 'let', const creates a read-only reference that cannot be reassigned.",
            "difficulty": "easy",
            "topic_tag": "JavaScript Basics"
        }},
        {{
            "id": 2,
            "question": "What will be the output of this code?",
            "code_snippet": "const arr = [1, 2, 3];\\nconst doubled = arr.map(x => x * 2);\\nconsole.log(doubled);",
            "options": {{
                "A": "[2, 4, 6]",
                "B": "[1, 2, 3, 1, 2, 3]",
                "C": "undefined",
                "D": "Error: map is not a function"
            }},
            "correct": "A",
            "explanation": "Array.map() creates a new array by calling a function on every element. Here, each element is multiplied by 2, resulting in [2, 4, 6].",
            "difficulty": "medium",
            "topic_tag": "Array Methods"
        }}
    ]
}}

## Critical Rules
1. Generate exactly {num_questions} questions
2. IDs must be sequential starting from 1
3. Each question must have exactly 4 options (A, B, C, D)
4. Only one correct answer per question
5. Explanations must be educational (50-100 words)
6. code_snippet should be null if no code is needed
7. Questions must be relevant to "{step_name}" specifically
8. No duplicate or near-duplicate questions
9. Avoid ambiguous wording that could have multiple correct interpretations

RETURN ONLY THE JSON OBJECT. NO MARKDOWN FORMATTING. NO ADDITIONAL TEXT."""

    return prompt


def get_quiz_batch_prompt(
    topic: str,
    step_name: str,
    count: int,
    start_id: int,
    difficulty: str = "mixed"
) -> str:
    """
    Generate prompt for a batch of quiz questions (for progressive loading).
    
    Args:
        topic: The career/technology topic
        step_name: The specific step being tested
        count: Number of questions to generate
        start_id: Starting ID for questions
        difficulty: "easy", "medium", "hard", or "mixed"
    
    Returns:
        Prompt for batch quiz generation
    """
    
    difficulty_instruction = ""
    if difficulty == "mixed":
        difficulty_instruction = "Mix of easy, medium, and hard difficulty"
    else:
        difficulty_instruction = f"All questions should be {difficulty} difficulty"
    
    return f"""Generate {count} technical MCQ questions for: {step_name} ({topic})

Start question IDs from {start_id}.
{difficulty_instruction}

Each question must have:
- 4 options (A, B, C, D)
- Exactly 1 correct answer
- Include code snippets where appropriate
- Educational explanation

Return ONLY valid JSON:
{{
    "questions": [
        {{
            "id": {start_id},
            "question": "Question text?",
            "code_snippet": "Optional code here",
            "options": {{"A": "", "B": "", "C": "", "D": ""}},
            "correct": "A",
            "explanation": "Why this answer is correct",
            "difficulty": "medium",
            "topic_tag": "Specific topic"
        }}
    ]
}}

RETURN ONLY THE JSON OBJECT."""


def get_interview_prep_prompt(role: str, experience_level: str) -> str:
    """
    Generate prompt for interview preparation content.
    
    Args:
        role: Target job role
        experience_level: "entry", "mid", "senior"
    
    Returns:
        Prompt for interview preparation
    """
    
    return f"""## Interview Preparation Request

**Target Role**: {role}
**Experience Level**: {experience_level}

## Your Task
Generate comprehensive interview preparation content for this role.

## Required Output Format
Return ONLY valid JSON:

{{
    "role": "{role}",
    "experience_level": "{experience_level}",
    "technical_questions": [
        {{
            "question": "Explain the difference between REST and GraphQL",
            "category": "System Design",
            "difficulty": "medium",
            "key_points": ["Flexibility", "Over-fetching", "Versioning"],
            "sample_answer": "REST uses fixed endpoints... [150-200 words]",
            "follow_up_questions": ["When would you choose one over the other?"]
        }}
    ],
    "behavioral_questions": [
        {{
            "question": "Tell me about a time you had to deal with a difficult team member",
            "framework": "STAR",
            "what_they_assess": "Conflict resolution, communication skills",
            "sample_answer_structure": {{
                "situation": "Set the context briefly",
                "task": "What was your responsibility",
                "action": "What specific steps you took",
                "result": "Measurable outcome"
            }}
        }}
    ],
    "technical_concepts_to_review": [
        {{
            "concept": "Big O Notation",
            "importance": "high",
            "quick_review": "Brief explanation",
            "common_mistakes": ["Confusing average and worst case"]
        }}
    ],
    "company_research_tips": [
        "Review the engineering blog for tech stack insights",
        "Check Glassdoor for interview process details"
    ],
    "red_flags_to_avoid": [
        "Speaking negatively about previous employers",
        "Not having questions to ask the interviewer"
    ]
}}

RETURN ONLY THE JSON OBJECT."""
