from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_service import generate_precision_roadmap
from youtube_service import get_curated_videos

app = FastAPI(title="Career Forge API", version="2.0.0")

# CORS middleware - allowing frontend at localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    
    # Enrich each roadmap step with YouTube videos
    for step in result.get("roadmap", []):
        youtube_query = step.get("youtube_search_query")
        if youtube_query:
            step["video_results"] = get_curated_videos(youtube_query)
        else:
            step["video_results"] = []
    
    return result
