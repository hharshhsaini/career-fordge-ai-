import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Use same fast endpoint as quiz (gpt-4.1-nano)
AZURE_ENDPOINT = os.getenv("QUIZ_ENDPOINT", os.getenv("AZURE_OPENAI_ENDPOINT"))
AZURE_API_KEY = os.getenv("QUIZ_API_KEY", os.getenv("AZURE_OPENAI_API_KEY"))
AZURE_DEPLOYMENT = os.getenv("QUIZ_DEPLOYMENT", os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-nano"))
AZURE_API_VERSION = os.getenv("QUIZ_API_VERSION", os.getenv("AZURE_OPENAI_API_VERSION", "2024-05-01-preview"))

if not AZURE_API_KEY:
    print("WARNING: API KEY not set!")

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION
)


def generate_precision_roadmap(user_profile: str) -> dict:
    """Generate career roadmap using fast GPT-4.1-nano."""
    
    prompt = f"""User: {user_profile}

Return JSON career roadmap with 6 steps:
{{"career_role":"Title","summary":"2 sentences","roadmap":[{{"step_name":"Step 1: X","official_docs_url":"url or null","paid_course_recommendation":"Course on Udemy","youtube_search_query":"X tutorial"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Career advisor. JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        return json.loads(response_text.strip())
    
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        return {"error": "Failed to parse response. Try again."}
    except Exception as e:
        print(f"AI error: {e}")
        return {"error": f"AI error: {str(e)}"}
