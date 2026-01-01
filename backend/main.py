from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import generate_precision_roadmap
from youtube_service import get_curated_videos
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI(title="Career Forge API", version="2.0.0")

# Thread pool for parallel YouTube API calls
executor = ThreadPoolExecutor(max_workers=6)

# CORS middleware - allowing frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.netlify.app", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserProfile(BaseModel):
    description: str


@app.get("/")
async def root():
    return {"message": "Career Forge API is running"}


@app.post("/generate-path")
async def generate_path(profile: UserProfile):
    """
    Generate a precision career path with curated resources.
    """
    # Generate career roadmap from AI
    result = generate_precision_roadmap(profile.description)
    
    # Check for errors
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    # Fetch YouTube videos in PARALLEL for all steps
    loop = asyncio.get_event_loop()
    roadmap = result.get("roadmap", [])
    
    # Create tasks for all YouTube searches
    async def fetch_videos(step):
        query = step.get("youtube_search_query")
        if query:
            videos = await loop.run_in_executor(executor, get_curated_videos, query)
            step["video_results"] = videos
        else:
            step["video_results"] = []
        return step
    
    # Run all YouTube fetches in parallel
    await asyncio.gather(*[fetch_videos(step) for step in roadmap])
    
    return result
