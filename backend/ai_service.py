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
    
    prompt = f"""Career advisor. User: {user_profile}

Generate 6-step career roadmap. JSON only:
{{"career_role":"Job Title","summary":"Why this career fits","roadmap":[{{"step_name":"Step 1: Topic","official_docs_url":"https://docs.example.com or null","paid_course_recommendation":"Course by Instructor on Udemy/Coursera","youtube_search_query":"topic full course tutorial 2024"}}]}}

Rules: 6 steps (beginner to advanced), real courses, specific youtube queries. Pick BEST career for user skills."""

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Career advisor. JSON only. Pick best career for user, not always Full Stack."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
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
