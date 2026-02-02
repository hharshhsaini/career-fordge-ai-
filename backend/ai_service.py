import os
import json
from dotenv import load_dotenv

load_dotenv()

# Multiple Gemini API keys for fallback (comma-separated)
GEMINI_API_KEYS = [key.strip() for key in os.getenv("GEMINI_API_KEYS", "").split(",") if key.strip()]

print(f"[AI Service] Loaded {len(GEMINI_API_KEYS)} Gemini API keys")

if not GEMINI_API_KEYS:
    print("WARNING: No GEMINI_API_KEYS set!")

# Track current key index for round-robin
_current_key_index = 0


def generate_precision_roadmap(user_profile: str) -> dict:
    """Generate career roadmap using Google Gemini with multi-key fallback."""
    global _current_key_index
    
    # Late import to avoid startup issues
    try:
        from google import genai
        from google.genai import types
    except ImportError as e:
        print(f"[AI Service] Failed to import google-genai: {e}")
        return {"error": f"SDK import error: {str(e)}"}
    
    if not GEMINI_API_KEYS:
        print("[AI Service] No API keys configured")
        return {"error": "No Gemini API keys configured"}
    
    prompt = f"""You are a career advisor. User: {user_profile}

Return ONLY valid JSON career roadmap with 6 steps in this exact format:
{{"career_role":"Title","summary":"2 sentences","roadmap":[{{"step_name":"Step 1: X","official_docs_url":"url or null","paid_course_recommendation":"Course on Udemy","youtube_search_query":"X tutorial"}}]}}

Important: Return ONLY the JSON object, no markdown, no extra text."""

    # Try each key starting from current index
    tried_keys = 0
    max_tries = len(GEMINI_API_KEYS)
    last_error = None
    
    while tried_keys < max_tries:
        current_key = GEMINI_API_KEYS[_current_key_index]
        key_preview = f"{current_key[:8]}...{current_key[-4:]}" if len(current_key) > 12 else "***"
        print(f"[AI Service] Trying key {_current_key_index + 1}/{max_tries}: {key_preview}")
        
        try:
            # Create client with current API key
            client = genai.Client(api_key=current_key)
            
            response = client.models.generate_content(
                model="models/gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=2000,
                    temperature=0.7
                )
            )
            
            response_text = response.text.strip()
            print(f"[AI Service] Got response, length: {len(response_text)}")
            
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
            print(f"[AI Service] Success! Generated roadmap for: {result.get('career_role', 'Unknown')}")
            return result
        
        except json.JSONDecodeError as e:
            print(f"[AI Service] JSON parse error: {e}")
            print(f"[AI Service] Raw response: {response_text[:500] if 'response_text' in dir() else 'N/A'}")
            return {"error": "Failed to parse AI response. Please try again."}
        
        except Exception as e:
            error_msg = str(e).lower()
            last_error = str(e)
            print(f"[AI Service] Key {_current_key_index + 1} error: {e}")
            
            # Check if it's a rate limit or auth error - try next key
            if any(keyword in error_msg for keyword in ['quota', 'rate', 'limit', 'unauthorized', 'invalid', 'api_key', '429', '401', '403', 'resource_exhausted', 'permission']):
                _current_key_index = (_current_key_index + 1) % len(GEMINI_API_KEYS)
                tried_keys += 1
                print(f"[AI Service] Rotating to next key ({tried_keys}/{max_tries})...")
                continue
            else:
                # Other errors - return immediately
                return {"error": f"AI error: {str(e)}"}
    
    print(f"[AI Service] All {max_tries} keys exhausted. Last error: {last_error}")
    return {"error": "All Gemini API keys exhausted. Please try again later."}
