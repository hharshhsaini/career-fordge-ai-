from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import generate_precision_roadmap
from services.quiz_service import generate_quiz_openai, generate_quiz_batch
from services.youtube_service import get_curated_videos
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="Career Forge API", version="2.0.0")

# Thread pool for parallel execution
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


class QuizBatchRequest(BaseModel):
    topic: str
    step_name: str
    count: int = 5
    start_id: int = 1


@app.get("/")
async def root():
    return {"message": "Career Forge API is running"}


@app.post("/generate-path")
async def generate_path(profile: UserProfile):
    """Generate career roadmap (fast, no YouTube wait)."""
    loop = asyncio.get_event_loop()
    
    # Generate roadmap with fast model
    result = await loop.run_in_executor(executor, generate_precision_roadmap, profile.description)

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Return immediately - frontend will fetch videos separately
    for step in result.get("roadmap", []):
        step["video_results"] = []
    
    return result


@app.post("/fetch-videos")
async def fetch_videos_endpoint(profile: UserProfile):
    """Fetch YouTube videos for a search query."""
    loop = asyncio.get_event_loop()
    videos = await loop.run_in_executor(executor, get_curated_videos, profile.description)
    return {"videos": videos}


@app.post("/generate-quiz")
async def generate_quiz_endpoint(request: QuizRequest):
    """Generate full quiz (15 questions)."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, generate_quiz_openai, request.topic, request.step_name)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@app.post("/generate-quiz-batch")
async def generate_quiz_batch_endpoint(request: QuizBatchRequest):
    """Generate batch of questions (for progressive loading)."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor, generate_quiz_batch, request.topic, request.step_name, request.count, request.start_id
    )
    return result
