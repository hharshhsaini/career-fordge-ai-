"""
CareerForge AI - Input Validation Utilities
Sanitization and validation for user inputs.
"""

import re
from typing import Tuple


def validate_user_profile(description: str) -> Tuple[bool, str]:
    """
    Validate user profile description.
    
    Args:
        description: User's profile description
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not description:
        return False, "Description is required"
    
    if not isinstance(description, str):
        return False, "Description must be a string"
    
    description = description.strip()
    
    if len(description) < 10:
        return False, "Please provide more details (at least 10 characters)"
    
    if len(description) > 5000:
        return False, "Description is too long (maximum 5000 characters)"
    
    # Check for minimum word count
    words = description.split()
    if len(words) < 3:
        return False, "Please provide at least a few words describing your background"
    
    return True, ""


def sanitize_input(text: str, max_length: int = 5000) -> str:
    """
    Sanitize user input to prevent prompt injection.
    
    Args:
        text: User input text
        max_length: Maximum allowed length
    
    Returns:
        Sanitized text
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Truncate to max length
    text = text[:max_length]
    
    # Remove potential prompt injection patterns
    # These are common patterns used to try to override system prompts
    injection_patterns = [
        r'ignore (all )?previous instructions',
        r'disregard (all )?(previous|above) (instructions|prompts)',
        r'forget (everything|all)',
        r'system prompt:',
        r'new instructions:',
        r'\[INST\]',
        r'\[/INST\]',
        r'<\|.*?\|>',
        r'<<SYS>>',
        r'<</SYS>>',
    ]
    
    for pattern in injection_patterns:
        text = re.sub(pattern, '[FILTERED]', text, flags=re.IGNORECASE)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def validate_role_name(role: str) -> Tuple[bool, str]:
    """
    Validate a role/job title name.
    
    Args:
        role: The role name to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not role:
        return False, "Role is required"
    
    role = role.strip()
    
    if len(role) < 2:
        return False, "Role name is too short"
    
    if len(role) > 200:
        return False, "Role name is too long"
    
    # Only allow reasonable characters
    if not re.match(r'^[\w\s\-\./&]+$', role):
        return False, "Role name contains invalid characters"
    
    return True, ""


def validate_experience_level(level: str) -> str:
    """
    Validate and normalize experience level.
    
    Args:
        level: Experience level string
    
    Returns:
        Normalized level (entry/mid/senior) or 'mid' as default
    """
    if not level:
        return "mid"
    
    level = level.lower().strip()
    
    # Normalize various inputs
    entry_synonyms = ['entry', 'junior', 'beginner', 'fresher', 'new grad', 'intern']
    mid_synonyms = ['mid', 'middle', 'intermediate', 'regular']
    senior_synonyms = ['senior', 'lead', 'principal', 'staff', 'expert', 'advanced']
    
    for synonym in entry_synonyms:
        if synonym in level:
            return "entry"
    
    for synonym in senior_synonyms:
        if synonym in level:
            return "senior"
    
    for synonym in mid_synonyms:
        if synonym in level:
            return "mid"
    
    return "mid"


def validate_difficulty(difficulty: str) -> str:
    """
    Validate and normalize difficulty level.
    
    Args:
        difficulty: Difficulty string
    
    Returns:
        Normalized difficulty (easy/medium/hard/mixed)
    """
    if not difficulty:
        return "mixed"
    
    difficulty = difficulty.lower().strip()
    
    if difficulty in ['easy', 'beginner', 'simple']:
        return "easy"
    if difficulty in ['medium', 'intermediate', 'moderate']:
        return "medium"
    if difficulty in ['hard', 'difficult', 'advanced', 'expert']:
        return "hard"
    
    return "mixed"
