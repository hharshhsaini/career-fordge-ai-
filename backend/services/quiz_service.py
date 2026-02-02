import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Multiple OpenAI API keys for fallback (comma-separated)
OPENAI_API_KEYS = [key.strip() for key in os.getenv("OPENAI_API_KEYS", "").split(",") if key.strip()]

# Model to use (gpt-4o-mini is fast and cost-effective for quizzes)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEYS:
    print("WARNING: No OPENAI_API_KEYS set!")

# Track current key index for round-robin
_current_key_index = 0


def get_openai_client(api_key: str) -> OpenAI:
    """Create OpenAI client with given API key."""
    return OpenAI(api_key=api_key)


def _call_openai_with_fallback(messages: list, max_tokens: int) -> dict:
    """Call OpenAI API with multi-key fallback."""
    global _current_key_index
    
    if not OPENAI_API_KEYS:
        return {"error": "No OpenAI API keys configured"}
    
    tried_keys = 0
    max_tries = len(OPENAI_API_KEYS)
    
    while tried_keys < max_tries:
        current_key = OPENAI_API_KEYS[_current_key_index]
        
        try:
            client = get_openai_client(current_key)
            
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Clean markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            
            # Success! Rotate to next key for load balancing
            _current_key_index = (_current_key_index + 1) % len(OPENAI_API_KEYS)
            return result
        
        except json.JSONDecodeError as e:
            print(f"JSON error with OpenAI key {_current_key_index + 1}: {e}")
            return {"error": "Failed to parse quiz response. Please try again."}
        
        except Exception as e:
            error_msg = str(e).lower()
            print(f"OpenAI key {_current_key_index + 1} failed: {e}")
            
            # Check if it's a rate limit or auth error - try next key
            if any(keyword in error_msg for keyword in ['quota', 'rate', 'limit', 'unauthorized', 'invalid', 'api_key', '429', '401', '403', 'insufficient']):
                _current_key_index = (_current_key_index + 1) % len(OPENAI_API_KEYS)
                tried_keys += 1
                print(f"Trying next OpenAI key ({tried_keys}/{max_tries})...")
                continue
            else:
                return {"error": f"Quiz error: {str(e)}"}
    
    return {"error": "All OpenAI API keys exhausted. Please try again later."}


def generate_quiz_batch(topic: str, step_name: str, count: int, start_id: int = 1) -> dict:
    """Generate a batch of quiz questions using OpenAI ChatGPT."""
    prompt = f"""Generate {count} technical MCQ for: {step_name} ({topic})
Start id from {start_id}. 4 options, 1 correct, code snippets, mix difficulty.
JSON only: {{"questions":[{{"id":{start_id},"question":"Q?","options":{{"A":"","B":"","C":"","D":""}},"correct":"A","explanation":"Why","difficulty":"easy"}}]}}"""

    messages = [
        {"role": "system", "content": "Quiz generator. JSON only."},
        {"role": "user", "content": prompt}
    ]
    
    max_tokens = 1500 if count <= 5 else 3000
    result = _call_openai_with_fallback(messages, max_tokens)
    
    if "error" in result:
        return result
    
    return result if "questions" in result else {"questions": []}


def generate_quiz_openai(topic: str, step_name: str) -> dict:
    """Generate full 15 question quiz using OpenAI ChatGPT."""
    prompt = f"""Generate 15 technical MCQ for: {step_name} ({topic})
4 options each, 1 correct, code snippets, mix easy/medium/hard.
JSON: {{"questions":[{{"id":1,"question":"Q?","options":{{"A":"","B":"","C":"","D":""}},"correct":"A","explanation":"Why","difficulty":"easy"}}]}}"""

    messages = [
        {"role": "system", "content": "Quiz generator. JSON only."},
        {"role": "user", "content": prompt}
    ]
    
    result = _call_openai_with_fallback(messages, 4000)
    
    if "error" in result:
        return result
    
    if "questions" in result and len(result["questions"]) > 0:
        return result
    
    return {"error": "Failed to generate quiz. Please try again."}
