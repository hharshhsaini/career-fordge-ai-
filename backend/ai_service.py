import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    print("WARNING: GEMINI_API_KEY not set!")
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")  # Faster model


def generate_precision_roadmap(user_profile: str) -> dict:
    """
    Generate a precision career roadmap with verified, high-quality resources.
    """
    prompt = f"""You are Career Forge, a precision career advisor. Analyze the user profile and provide EXACT, VERIFIED resources.

User Profile: {user_profile}

STRICT RULES:
1. Only provide official_docs_url if you are 100% CERTAIN it is the correct official documentation URL
2. If unsure about a URL, use null instead of guessing
3. paid_course_recommendation must be a REAL, FAMOUS course that actually exists on Udemy/Coursera
4. youtube_search_query must be SPECIFIC enough to find full courses/playlists (not shorts or random videos)
5. Provide exactly 6 steps covering Beginner to Advanced

Respond with RAW JSON only. No markdown, no code blocks, no explanation.

{{"career_role": "Exact Job Title","summary": "2-3 sentences explaining why this career fits the user","roadmap": [{{"step_name": "Step 1: Foundation Topic Name","official_docs_url": "https://exact-official-docs-url.com or null if unsure","paid_course_recommendation": "Exact Course Name by Instructor Name on Platform","youtube_search_query": "very specific full course tutorial query 2024"}},{{"step_name": "Step 2: Next Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name by Instructor on Platform","youtube_search_query": "specific search query"}},{{"step_name": "Step 3: Intermediate Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 4: Intermediate Topic 2","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 5: Advanced Topic","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "query"}},{{"step_name": "Step 6: Projects & Interview Prep","official_docs_url": "URL or null","paid_course_recommendation": "Course Name","youtube_search_query": "career role interview preparation projects"}}]}}"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean markdown formatting if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        return json.loads(response_text)
    
    except json.JSONDecodeError:
        return get_fallback_roadmap(user_profile)
    except Exception:
        return get_fallback_roadmap(user_profile)


def get_fallback_roadmap(user_profile: str) -> dict:
    """Return verified fallback data when API fails."""
    profile_lower = user_profile.lower()
    
    if any(word in profile_lower for word in ["data", "analysis", "excel", "statistics", "numbers"]):
        return {
            "career_role": "Data Analyst",
            "summary": "Data Analyst combines analytical thinking with business impact. Your interest in data and numbers makes this an ideal path with strong job demand.",
            "roadmap": [
                {"step_name": "Step 1: Python Programming Fundamentals", "official_docs_url": "https://docs.python.org/3/tutorial/", "paid_course_recommendation": "100 Days of Code: The Complete Python Pro Bootcamp by Dr. Angela Yu on Udemy", "youtube_search_query": "Python full course for beginners 2024 freeCodeCamp"},
                {"step_name": "Step 2: Data Analysis with Pandas & NumPy", "official_docs_url": "https://pandas.pydata.org/docs/getting_started/", "paid_course_recommendation": "Python for Data Science and Machine Learning Bootcamp by Jose Portilla on Udemy", "youtube_search_query": "Pandas complete tutorial data analysis Python"},
                {"step_name": "Step 3: SQL & Database Querying", "official_docs_url": "https://www.postgresql.org/docs/", "paid_course_recommendation": "The Complete SQL Bootcamp: Go from Zero to Hero by Jose Portilla on Udemy", "youtube_search_query": "SQL full course for data analysts beginners to advanced"},
                {"step_name": "Step 4: Data Visualization with Python", "official_docs_url": "https://matplotlib.org/stable/tutorials/index.html", "paid_course_recommendation": "Data Visualization with Python by IBM on Coursera", "youtube_search_query": "Matplotlib Seaborn complete tutorial data visualization"},
                {"step_name": "Step 5: Statistics for Data Analysis", "official_docs_url": "https://docs.scipy.org/doc/scipy/reference/stats.html", "paid_course_recommendation": "Statistics for Data Science and Business Analysis by 365 Careers on Udemy", "youtube_search_query": "Statistics for data science complete course"},
                {"step_name": "Step 6: Power BI & Portfolio Projects", "official_docs_url": "https://learn.microsoft.com/en-us/power-bi/", "paid_course_recommendation": "Microsoft Power BI Desktop for Business Intelligence by Maven Analytics on Udemy", "youtube_search_query": "Data Analyst interview preparation portfolio projects"}
            ]
        }
    elif any(word in profile_lower for word in ["web", "frontend", "html", "css", "javascript", "react"]):
        return {
            "career_role": "Frontend Developer",
            "summary": "Frontend Development is creative and highly in-demand. Your web skills provide a strong foundation for building modern user interfaces.",
            "roadmap": [
                {"step_name": "Step 1: HTML5 & CSS3 Mastery", "official_docs_url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "paid_course_recommendation": "Build Responsive Real-World Websites with HTML and CSS by Jonas Schmedtmann on Udemy", "youtube_search_query": "HTML CSS complete course responsive design 2024"},
                {"step_name": "Step 2: JavaScript Fundamentals", "official_docs_url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "paid_course_recommendation": "The Complete JavaScript Course 2024 by Jonas Schmedtmann on Udemy", "youtube_search_query": "JavaScript full course beginners to advanced 2024"},
                {"step_name": "Step 3: React.js Framework", "official_docs_url": "https://react.dev/learn", "paid_course_recommendation": "React - The Complete Guide 2024 by Maximilian Schwarzmuller on Udemy", "youtube_search_query": "React JS complete course 2024 hooks projects"},
                {"step_name": "Step 4: Tailwind CSS & Modern Styling", "official_docs_url": "https://tailwindcss.com/docs", "paid_course_recommendation": "Tailwind CSS From Scratch by Brad Traversy on Udemy", "youtube_search_query": "Tailwind CSS complete course tutorial 2024"},
                {"step_name": "Step 5: TypeScript & Next.js", "official_docs_url": "https://nextjs.org/docs", "paid_course_recommendation": "Next.js 14 & React - The Complete Guide by Maximilian Schwarzmuller on Udemy", "youtube_search_query": "Next.js 14 complete course TypeScript tutorial"},
                {"step_name": "Step 6: Testing & Interview Prep", "official_docs_url": "https://testing-library.com/docs/", "paid_course_recommendation": "React Testing Library and Jest by Stephen Grider on Udemy", "youtube_search_query": "Frontend developer interview preparation JavaScript React"}
            ]
        }
    else:
        return {
            "career_role": "Full Stack Developer",
            "summary": "Full Stack Development offers versatile skills and excellent job opportunities. It's a comprehensive path that makes you valuable to any tech team.",
            "roadmap": [
                {"step_name": "Step 1: HTML, CSS & JavaScript", "official_docs_url": "https://developer.mozilla.org/en-US/docs/Learn", "paid_course_recommendation": "The Web Developer Bootcamp 2024 by Colt Steele on Udemy", "youtube_search_query": "Web development full course HTML CSS JavaScript 2024"},
                {"step_name": "Step 2: React.js Frontend", "official_docs_url": "https://react.dev/learn", "paid_course_recommendation": "React - The Complete Guide 2024 by Maximilian Schwarzmuller on Udemy", "youtube_search_query": "React JS complete course for beginners 2024"},
                {"step_name": "Step 3: Node.js & Express Backend", "official_docs_url": "https://expressjs.com/en/guide/routing.html", "paid_course_recommendation": "Node.js, Express, MongoDB & More by Jonas Schmedtmann on Udemy", "youtube_search_query": "Node.js Express REST API complete course"},
                {"step_name": "Step 4: Databases - MongoDB & SQL", "official_docs_url": "https://www.mongodb.com/docs/manual/", "paid_course_recommendation": "The Complete SQL Bootcamp by Jose Portilla on Udemy", "youtube_search_query": "MongoDB complete course Node.js tutorial"},
                {"step_name": "Step 5: DevOps & Deployment", "official_docs_url": "https://docs.docker.com/get-started/", "paid_course_recommendation": "Docker and Kubernetes: The Complete Guide by Stephen Grider on Udemy", "youtube_search_query": "DevOps for developers Docker deployment complete course"},
                {"step_name": "Step 6: System Design & Interview Prep", "official_docs_url": None, "paid_course_recommendation": "Master the Coding Interview by Andrei Neagoie on Udemy", "youtube_search_query": "Full stack developer interview preparation system design"}
            ]
        }
