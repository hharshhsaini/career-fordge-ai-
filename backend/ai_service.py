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
        return get_fallback_roadmap(user_profile)
    except Exception as e:
        print(f"Azure OpenAI error: {e}")
        return get_fallback_roadmap(user_profile)


def get_fallback_roadmap(user_profile: str) -> dict:
    """Return verified fallback data when API fails."""
    profile_lower = user_profile.lower()
    
    if any(word in profile_lower for word in ["data", "analysis", "excel", "statistics", "numbers", "analyst"]):
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
    elif any(word in profile_lower for word in ["ai", "ml", "machine learning", "deep learning", "artificial intelligence"]):
        return {
            "career_role": "AI/ML Engineer",
            "summary": "AI/ML Engineering is at the forefront of technology. Your interest in AI makes this an exciting and high-paying career path.",
            "roadmap": [
                {"step_name": "Step 1: Python & Math Foundations", "official_docs_url": "https://docs.python.org/3/tutorial/", "paid_course_recommendation": "Python for Data Science and Machine Learning Bootcamp by Jose Portilla on Udemy", "youtube_search_query": "Python for machine learning complete course 2024"},
                {"step_name": "Step 2: Machine Learning Fundamentals", "official_docs_url": "https://scikit-learn.org/stable/user_guide.html", "paid_course_recommendation": "Machine Learning A-Z by Kirill Eremenko on Udemy", "youtube_search_query": "Machine learning full course beginners freeCodeCamp"},
                {"step_name": "Step 3: Deep Learning & Neural Networks", "official_docs_url": "https://www.tensorflow.org/tutorials", "paid_course_recommendation": "Deep Learning Specialization by Andrew Ng on Coursera", "youtube_search_query": "Deep learning complete course neural networks"},
                {"step_name": "Step 4: Natural Language Processing", "official_docs_url": "https://huggingface.co/docs", "paid_course_recommendation": "NLP with Transformers by Hugging Face on Coursera", "youtube_search_query": "NLP natural language processing complete course"},
                {"step_name": "Step 5: Computer Vision", "official_docs_url": "https://pytorch.org/tutorials/", "paid_course_recommendation": "PyTorch for Deep Learning by Daniel Bourke on Udemy", "youtube_search_query": "Computer vision deep learning complete course"},
                {"step_name": "Step 6: MLOps & Interview Prep", "official_docs_url": "https://mlflow.org/docs/latest/index.html", "paid_course_recommendation": "MLOps Specialization by DeepLearning.AI on Coursera", "youtube_search_query": "AI ML engineer interview preparation projects"}
            ]
        }
    elif any(word in profile_lower for word in ["web", "frontend", "html", "css", "javascript", "react", "ui", "ux"]):
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
    elif any(word in profile_lower for word in ["cloud", "aws", "azure", "devops", "kubernetes", "docker"]):
        return {
            "career_role": "Cloud/DevOps Engineer",
            "summary": "Cloud and DevOps skills are essential in modern tech. Your interest in infrastructure makes this a high-demand, well-paying career.",
            "roadmap": [
                {"step_name": "Step 1: Linux & Networking Basics", "official_docs_url": "https://linuxjourney.com/", "paid_course_recommendation": "Linux Mastery by Ziyad Yehia on Udemy", "youtube_search_query": "Linux complete course for beginners 2024"},
                {"step_name": "Step 2: AWS Cloud Fundamentals", "official_docs_url": "https://docs.aws.amazon.com/", "paid_course_recommendation": "AWS Certified Solutions Architect by Stephane Maarek on Udemy", "youtube_search_query": "AWS complete course beginners to advanced"},
                {"step_name": "Step 3: Docker Containerization", "official_docs_url": "https://docs.docker.com/get-started/", "paid_course_recommendation": "Docker and Kubernetes: The Complete Guide by Stephen Grider on Udemy", "youtube_search_query": "Docker complete course tutorial 2024"},
                {"step_name": "Step 4: Kubernetes Orchestration", "official_docs_url": "https://kubernetes.io/docs/home/", "paid_course_recommendation": "Kubernetes for Developers by Mumshad Mannambeth on Udemy", "youtube_search_query": "Kubernetes complete course beginners"},
                {"step_name": "Step 5: CI/CD & Infrastructure as Code", "official_docs_url": "https://www.terraform.io/docs", "paid_course_recommendation": "Terraform for AWS by Zeal Vora on Udemy", "youtube_search_query": "CI CD pipeline complete course Jenkins GitHub Actions"},
                {"step_name": "Step 6: Monitoring & Interview Prep", "official_docs_url": "https://prometheus.io/docs/", "paid_course_recommendation": "DevOps Beginners to Advanced by Imran Teli on Udemy", "youtube_search_query": "DevOps engineer interview preparation projects"}
            ]
        }
    elif any(word in profile_lower for word in ["cyber", "security", "hacking", "penetration", "network security"]):
        return {
            "career_role": "Cybersecurity Analyst",
            "summary": "Cybersecurity is critical in today's digital world. Your interest in security makes this a rewarding and in-demand career.",
            "roadmap": [
                {"step_name": "Step 1: Networking Fundamentals", "official_docs_url": "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html", "paid_course_recommendation": "CompTIA Network+ by Mike Meyers on Udemy", "youtube_search_query": "Networking fundamentals complete course 2024"},
                {"step_name": "Step 2: Linux & System Administration", "official_docs_url": "https://linuxjourney.com/", "paid_course_recommendation": "Linux for Cybersecurity by Jason Dion on Udemy", "youtube_search_query": "Linux for cybersecurity complete course"},
                {"step_name": "Step 3: Security Fundamentals (CompTIA Security+)", "official_docs_url": "https://www.comptia.org/certifications/security", "paid_course_recommendation": "CompTIA Security+ by Jason Dion on Udemy", "youtube_search_query": "CompTIA Security+ complete course 2024"},
                {"step_name": "Step 4: Ethical Hacking & Penetration Testing", "official_docs_url": "https://www.kali.org/docs/", "paid_course_recommendation": "Learn Ethical Hacking From Scratch by Zaid Sabih on Udemy", "youtube_search_query": "Ethical hacking complete course beginners"},
                {"step_name": "Step 5: Security Tools & SIEM", "official_docs_url": "https://www.splunk.com/en_us/training.html", "paid_course_recommendation": "Splunk Fundamentals by Splunk on Coursera", "youtube_search_query": "SIEM security tools complete course"},
                {"step_name": "Step 6: Incident Response & Interview Prep", "official_docs_url": None, "paid_course_recommendation": "Cybersecurity Career Path by StationX on Udemy", "youtube_search_query": "Cybersecurity analyst interview preparation"}
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
