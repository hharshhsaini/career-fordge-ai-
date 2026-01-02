import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure Azure OpenAI
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "career_fordge")

if not AZURE_API_KEY:
    print("WARNING: AZURE_OPENAI_API_KEY not set!")

AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version=AZURE_API_VERSION
)


def generate_precision_roadmap(user_profile: str) -> dict:
    """
    Generate a precision career roadmap using Azure OpenAI GPT-4.
    """
    prompt = f"""You are Career Forge, a precision career advisor. Analyze the user profile and provide EXACT, VERIFIED resources.

User Profile: {user_profile}

STRICT RULES:
1. Only provide official_docs_url if you are 100% CERTAIN it is the correct official documentation URL
2. If unsure about a URL, use null instead of guessing
3. paid_course_recommendation must be a REAL, FAMOUS course that actually exists on Udemy/Coursera
4. youtube_search_query must be SPECIFIC enough to find full courses/playlists (not shorts or random videos)
5. Provide exactly 6 steps covering Beginner to Advanced
6. Choose the BEST career based on user's skills and interests - NOT always Full Stack Developer

Respond with RAW JSON only. No markdown, no code blocks, no explanation.

{{"career_role": "Exact Job Title","summary": "2-3 sentences explaining why this career fits the user","roadmap": [{{"step_name": "Step 1: Foundation Topic Name","official_docs_url": "https://exact-official-docs-url.com or null if unsure","paid_course_recommendation": "Exact Course Name by Instructor Name on Platform","youtube_search_query": "very specific full course tutorial query 2024"}},{{"step_name": "Step 2: Next Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name by Instructor on Platform","youtube_search_query": "specific search query"}},{{"step_name": "Step 3: Intermediate Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 4: Intermediate Topic 2","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 5: Advanced Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 6: Projects & Interview Prep","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "career role interview preparation projects"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a career advisor AI. Always respond with valid JSON only. Analyze user skills carefully and recommend the most suitable career - not always Full Stack Developer."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=2000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean markdown formatting if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        return json.loads(response_text)
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"error": f"Failed to parse AI response. Please try again."}
    except Exception as e:
        print(f"Azure OpenAI error: {e}")
        return {"error": f"AI service error: {str(e)}. Please try again later."}
