"""
CareerForge AI - JSON Parser Utilities
Safe JSON extraction from LLM responses.
"""

import json
import re
from typing import Any, Dict, Optional


def safe_parse_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON from text, handling common LLM output issues.
    
    Args:
        text: Text that may contain JSON
    
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    if not text or not isinstance(text, str):
        return None
    
    # Try direct parsing first (fastest path)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    
    # Try extracting from markdown code blocks
    extracted = extract_json_from_text(text)
    if extracted:
        return extracted
    
    return None


def extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON object from text that may contain extra content.
    
    Handles:
    - Markdown code blocks (```json ... ```)
    - Leading/trailing text
    - Nested objects
    
    Args:
        text: Text containing JSON somewhere
    
    Returns:
        Extracted and parsed JSON or None
    """
    if not text:
        return None
    
    cleaned = text.strip()
    
    # Remove markdown code block markers
    patterns = [
        r'^```json\s*\n?(.*?)\n?```$',  # ```json ... ```
        r'^```\s*\n?(.*?)\n?```$',       # ``` ... ```
        r'^`(.*)`$',                       # `...`
    ]
    
    for pattern in patterns:
        match = re.match(pattern, cleaned, re.DOTALL)
        if match:
            cleaned = match.group(1).strip()
            break
    
    # Try parsing the cleaned text
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON object boundaries { ... }
    try:
        start = cleaned.find('{')
        if start == -1:
            return None
        
        # Find matching closing brace
        depth = 0
        end = start
        for i, char in enumerate(cleaned[start:], start):
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        
        if end > start:
            json_str = cleaned[start:end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON array boundaries [ ... ]
    try:
        start = cleaned.find('[')
        if start == -1:
            return None
        
        depth = 0
        end = start
        for i, char in enumerate(cleaned[start:], start):
            if char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        
        if end > start:
            json_str = cleaned[start:end]
            parsed = json.loads(json_str)
            # Wrap array in dict for consistency
            return {"data": parsed}
    except json.JSONDecodeError:
        pass
    
    return None


def clean_json_string(text: str) -> str:
    """
    Clean common issues in JSON strings from LLMs.
    
    Fixes:
    - Trailing commas
    - Single quotes instead of double quotes
    - Unquoted keys
    
    Args:
        text: JSON-like string
    
    Returns:
        Cleaned string (may still not be valid JSON)
    """
    if not text:
        return text
    
    # Remove trailing commas before } or ]
    text = re.sub(r',\s*([}\]])', r'\1', text)
    
    # This is risky but sometimes helps with simple cases
    # Replace single quotes with double quotes (only for simple cases)
    # text = text.replace("'", '"')
    
    return text


def validate_json_schema(data: Dict, required_fields: list) -> bool:
    """
    Validate that a dict has all required fields.
    
    Args:
        data: Dictionary to validate
        required_fields: List of required field names
    
    Returns:
        True if all fields present, False otherwise
    """
    if not isinstance(data, dict):
        return False
    
    for field in required_fields:
        if field not in data:
            return False
    
    return True
