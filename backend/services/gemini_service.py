import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")


async def generate_career_roadmap(skills: str, interests: str) -> dict:
    prompt = f"""You are Career Forge, an AI career advisor. Based on the user's skills and interests, generate a personalized career path and learning roadmap.

User Skills: {skills}
User Interests: {interests}

Respond in this exact JSON format:
{{
    "career_title": "Recommended career title",
    "career_description": "Brief description of this career path",
    "roadmap": [
        {{
            "step": 1,
            "title": "Step title",
            "description": "What to learn/do",
            "duration": "Estimated time",
            "search_query": "YouTube search query for learning resources"
        }}
    ],
    "skills_to_develop": ["skill1", "skill2"],
    "potential_salary_range": "Salary range estimate"
}}

Generate 5-6 roadmap steps. Make search_query specific for finding educational YouTube videos."""

    response = model.generate_content(prompt)
    
    import json
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return {"error": "Failed to parse AI response", "raw": response.text}
