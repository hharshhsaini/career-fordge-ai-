from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import generate_precision_roadmap
from services.quiz_service import generate_quiz_openai
from services.youtube_service import get_curated_videos
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="Career Forge API", version="2.0.0")

# Thread pool for parallel execution - more workers for speed
executor = ThreadPoolExecutor(max_workers=12)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    description: str


class QuizRequest(BaseModel):
    topic: str
    step_name: str


@app.get("/")
async def root():
    return {"message": "Career Forge API is running"}


@app.post("/generate-path")
async def generate_path(profile: UserProfile):
    """
    Generate career path - AI roadmap + parallel YouTube searches.
    """
    loop = asyncio.get_event_loop()
    
    # Run AI generation in thread pool
    result = await loop.run_in_executor(executor, generate_precision_roadmap, profile.description)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    roadmap = result.get("roadmap", [])
    
    # Fetch ALL YouTube videos in parallel (6 searches at once)
    async def fetch_videos(step):
        query = step.get("youtube_search_query")
        if query:
            videos = await loop.run_in_executor(executor, get_curated_videos, query)
            step["video_results"] = videos
        else:
            step["video_results"] = []
        return step
    
    # All 6 YouTube searches run simultaneously
    await asyncio.gather(*[fetch_videos(step) for step in roadmap])
    
    return result


@app.post("/generate-quiz")
async def generate_quiz_endpoint(request: QuizRequest):
    """
    Generate quiz - runs in thread pool for non-blocking.
    """
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, generate_quiz_openai, request.topic, request.step_name)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
