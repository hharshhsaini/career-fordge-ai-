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


def generate_quiz_batch(topic: str, step_name: str, count: int, start_id: int = 1) -> dict:
    """Generate a batch of quiz questions."""
    prompt = f"""Generate {count} technical MCQ for: {step_name} ({topic})
Start id from {start_id}. 4 options, 1 correct, code snippets, mix difficulty.
JSON only: {{"questions":[{{"id":{start_id},"question":"Q?","options":{{"A":"","B":"","C":"","D":""}},"correct":"A","explanation":"Why","difficulty":"easy"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=QUIZ_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Quiz generator. JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500 if count <= 5 else 3000
        )
        
        response_text = response.choices[0].message.content.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        result = json.loads(response_text.strip())
        return result if "questions" in result else {"questions": []}
    except:
        return {"questions": []}


def generate_quiz_openai(topic: str, step_name: str) -> dict:
    """Generate full 15 question quiz."""
    prompt = f"""Generate 15 technical MCQ for: {step_name} ({topic})
4 options each, 1 correct, code snippets, mix easy/medium/hard.
JSON: {{"questions":[{{"id":1,"question":"Q?","options":{{"A":"","B":"","C":"","D":""}},"correct":"A","explanation":"Why","difficulty":"easy"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=QUIZ_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "Quiz generator. JSON only."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4000
        )
        
        response_text = response.choices[0].message.content.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        result = json.loads(response_text.strip())
        
        if "questions" in result and len(result["questions"]) > 0:
            return result
        return {"error": "Failed to generate quiz. Please try again."}
    
    except json.JSONDecodeError:
        return {"error": "Failed to parse quiz response. Please try again."}
    except Exception as e:
        return {"error": f"Quiz error: {str(e)}"}
