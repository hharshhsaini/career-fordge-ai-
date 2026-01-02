import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

# GPT-4.1-nano on Azure for fast quiz generation
QUIZ_ENDPOINT = os.getenv("QUIZ_ENDPOINT", "https://career-fordge-resource.cognitiveservices.azure.com/")
QUIZ_API_KEY = os.getenv("QUIZ_API_KEY")
QUIZ_DEPLOYMENT = os.getenv("QUIZ_DEPLOYMENT", "gpt-4.1-nano")
QUIZ_API_VERSION = os.getenv("QUIZ_API_VERSION", "2024-05-01-preview")

if not QUIZ_API_KEY:
    print("WARNING: QUIZ_API_KEY not set!")

client = AzureOpenAI(
    azure_endpoint=QUIZ_ENDPOINT,
    api_key=QUIZ_API_KEY,
    api_version=QUIZ_API_VERSION
)


def generate_quiz_openai(topic: str, step_name: str) -> dict:
    """
    Generate a technical quiz using GPT-4.1-nano on Azure (fast).
    """
    prompt = f"""Generate 15 technical MCQ questions for: {step_name}
Topic: {topic}

Requirements:
- Include code output, concept, debugging, and comparison questions
- 4 options (A,B,C,D) per question, only 1 correct
- Mix: 5 easy, 6 medium, 4 hard
- Include code snippets where relevant

Return JSON only:
{{"questions":[{{"id":1,"question":"Question?","options":{{"A":"","B":"","C":"","D":""}},"correct":"A","explanation":"Why","difficulty":"easy"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=QUIZ_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Technical quiz generator. Return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000
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
        
        if "questions" in result and len(result["questions"]) > 0:
            return result
        else:
            return {"error": "Failed to generate quiz questions. Please try again."}
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"error": "Failed to parse quiz response. Please try again."}
    except Exception as e:
        print(f"Quiz generation error: {e}")
        return {"error": f"Quiz service error: {str(e)}. Please try again later."}
