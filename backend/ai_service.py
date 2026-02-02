import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Multiple Gemini API keys for fallback (comma-separated)
GEMINI_API_KEYS = [key.strip() for key in os.getenv("GEMINI_API_KEYS", "").split(",") if key.strip()]

if not GEMINI_API_KEYS:
    print("WARNING: No GEMINI_API_KEYS set!")

# Track current key index for round-robin
_current_key_index = 0


def get_gemini_client(api_key: str):
    """Configure and return Gemini model with given API key."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def generate_precision_roadmap(user_profile: str) -> dict:
    """Generate career roadmap using Google Gemini with multi-key fallback."""
    global _current_key_index
    
    if not GEMINI_API_KEYS:
        return {"error": "No Gemini API keys configured"}
    
    prompt = f"""User: {user_profile}

Return JSON career roadmap with 6 steps:
{{"career_role":"Title","summary":"2 sentences","roadmap":[{{"step_name":"Step 1: X","official_docs_url":"url or null","paid_course_recommendation":"Course on Udemy","youtube_search_query":"X tutorial"}}]}}"""

    # Try each key starting from current index
    tried_keys = 0
    max_tries = len(GEMINI_API_KEYS)
    
    while tried_keys < max_tries:
        current_key = GEMINI_API_KEYS[_current_key_index]
        
        try:
            model = get_gemini_client(current_key)
            
            response = model.generate_content(
                f"You are a career advisor. Respond with JSON only.\n\n{prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1500,
                    temperature=0.7
                )
            )
            
            response_text = response.text.strip()
            
            # Clean markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            result = json.loads(response_text.strip())
            
            # Success! Rotate to next key for load balancing
            _current_key_index = (_current_key_index + 1) % len(GEMINI_API_KEYS)
            return result
        
        except json.JSONDecodeError as e:
            print(f"JSON error with Gemini key {_current_key_index + 1}: {e}")
            # Don't rotate key for JSON errors - it's a response issue, not key issue
            return {"error": "Failed to parse response. Try again."}
        
        except Exception as e:
            error_msg = str(e).lower()
            print(f"Gemini key {_current_key_index + 1} failed: {e}")
            
            # Check if it's a rate limit or auth error - try next key
            if any(keyword in error_msg for keyword in ['quota', 'rate', 'limit', 'unauthorized', 'invalid', 'api_key', '429', '401', '403']):
                _current_key_index = (_current_key_index + 1) % len(GEMINI_API_KEYS)
                tried_keys += 1
                print(f"Trying next Gemini key ({tried_keys}/{max_tries})...")
                continue
            else:
                # Other errors - don't cycle through all keys
                return {"error": f"AI error: {str(e)}"}
    
    return {"error": "All Gemini API keys exhausted. Please try again later."}
