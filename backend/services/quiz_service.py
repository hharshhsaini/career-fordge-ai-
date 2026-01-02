import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not set!")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_quiz_openai(topic: str, step_name: str) -> dict:
    """
    Generate a technical quiz with coding and concept questions using OpenAI.
    """
    prompt = f"""You are a technical interview quiz generator for developers.

Generate 15 multiple choice questions to test REAL technical knowledge of: {step_name}
Topic: {topic}

CRITICAL REQUIREMENTS:
1. Questions MUST be technical and specific to the topic
2. Include these question types:
   - Code output questions (What will this code print?)
   - Concept questions (What is the purpose of X?)
   - Best practice questions (Which approach is recommended for Y?)
   - Debugging questions (What's wrong with this code?)
   - Comparison questions (What's the difference between A and B?)
3. For coding questions, include actual code snippets in the question
4. Each question must have exactly 4 options (A, B, C, D)
5. Only ONE option should be correct
6. Explanation must teach WHY the answer is correct
7. Difficulty mix: 5 easy, 6 medium, 4 hard

EXAMPLE GOOD QUESTIONS:
- "What will console.log(typeof null) output in JavaScript?" 
- "In React, what hook is used to perform side effects?"
- "What is the time complexity of binary search?"
- "Which SQL keyword is used to filter grouped results?"

DO NOT ask generic questions like "Why is learning important?" or "What is the best approach to learn?"

Respond with valid JSON only:

{{"questions": [{{"id": 1,"question": "Technical question with code if applicable?","options": {{"A": "Option A","B": "Option B","C": "Option C","D": "Option D"}},"correct": "A","explanation": "Technical explanation of why A is correct","difficulty": "easy"}}]}}

Generate exactly 15 technical questions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior technical interviewer. Generate challenging, real-world technical questions that test actual coding knowledge and concepts. Always include code snippets where relevant. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
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
        result = json.loads(response_text)
        
        # Validate we got questions
        if "questions" in result and len(result["questions"]) > 0:
            return result
        else:
            return {"error": "Failed to generate quiz questions. Please try again."}
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return {"error": f"Failed to parse quiz response. Please try again."}
    except Exception as e:
        print(f"OpenAI quiz generation error: {e}")
        return {"error": f"Quiz service error: {str(e)}. Please try again later."}

