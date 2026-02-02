"""
CareerForge AI - Main Application (Open-Source Version)
Production-ready FastAPI backend with self-hosted LLM support.

Run with: uvicorn main_v2:app --reload --port 8000
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from concurrent.futures import ThreadPoolExecutor

from config import api_config, print_config
from services.llm_service import get_llm_service
from services.roadmap_service import RoadmapService
from services.quiz_service_v2 import QuizService, generate_quiz_openai, generate_quiz_batch
from services.youtube_service import get_curated_videos

# Print configuration on startup
print_config()

# Initialize FastAPI application
app = FastAPI(
    title="CareerForge AI",
    description="🚀 AI-Powered Career Guidance - 100% Open-Source, Zero API Costs",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Thread pool for parallel execution
executor = ThreadPoolExecutor(max_workers=12)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

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


# ============================================================
# Health Endpoints
# ============================================================

@app.get("/")
async def root():
    """Root endpoint - API status check."""
    return {
        "message": "CareerForge AI is running",
        "version": "3.0.0",
        "engine": "open-source-llm",
        "docs_url": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """System health check."""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "engine": "open-source-llm"
    }


@app.get("/api/health/llm")
async def llm_health_check():
    """LLM service health check."""
    llm_service = get_llm_service()
    is_healthy, status_message = llm_service.check_health()
    
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "message": status_message,
        "model": llm_service.model,
        "base_url": llm_service.base_url
    }


@app.get("/api/health/models")
async def list_models():
    """List available models."""
    llm_service = get_llm_service()
    models = llm_service.list_models()
    
    return {
        "available_models": models,
        "primary_model": llm_service.model
    }


# ============================================================
# AI Endpoints
# ============================================================

@app.post("/api/ai/roadmap")
async def generate_roadmap_endpoint(profile: UserProfile):
    """Generate a comprehensive career roadmap."""
    loop = asyncio.get_event_loop()
    
    service = RoadmapService()
    result = await loop.run_in_executor(
        executor,
        service.generate_roadmap,
        profile.description
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to generate roadmap")
        )
    
    return result


@app.post("/api/ai/quiz")
async def generate_quiz_endpoint(request: QuizRequest):
    """Generate a knowledge quiz."""
    loop = asyncio.get_event_loop()
    
    service = QuizService()
    result = await loop.run_in_executor(
        executor,
        service.generate_quiz,
        request.topic,
        request.step_name
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


# ============================================================
# Legacy Endpoints (backward compatibility)
# ============================================================

@app.post("/generate-path")
async def generate_path(profile: UserProfile):
    """Legacy endpoint for roadmap generation."""
    loop = asyncio.get_event_loop()
    
    service = RoadmapService()
    result = await loop.run_in_executor(
        executor,
        service.generate_roadmap,
        profile.description
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    # Extract roadmap data
    roadmap_data = result.get("data", {})
    roadmap = roadmap_data.get("roadmap", [])
    
    # Fetch YouTube videos for each step
    async def fetch_videos(step):
        title = step.get("title", step.get("step_name", ""))
        focus_areas = step.get("focus_areas", [])
        query = focus_areas[0] if focus_areas else title
        
        if query:
            try:
                videos = await loop.run_in_executor(executor, get_curated_videos, f"{query} tutorial")
                step["video_results"] = videos
            except Exception:
                step["video_results"] = []
        else:
            step["video_results"] = []
        return step
    
    await asyncio.gather(*[fetch_videos(step) for step in roadmap])
    
    return roadmap_data


@app.post("/generate-quiz")
async def generate_quiz_legacy(request: QuizRequest):
    """Legacy endpoint for quiz generation."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        generate_quiz_openai,
        request.topic,
        request.step_name
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@app.post("/generate-quiz-batch")
async def generate_quiz_batch_legacy(request: QuizBatchRequest):
    """Legacy endpoint for batch quiz generation."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        generate_quiz_batch,
        request.topic,
        request.step_name,
        request.count,
        request.start_id
    )
    
    return result


# ============================================================
# Startup Event
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("\n" + "=" * 60)
    print("🚀 CareerForge AI - Open Source Edition")
    print("=" * 60)
    print("Engine: Self-hosted LLM via Ollama")
    print("Cost: $0 / Zero API usage fees")
    print("=" * 60)
    
    llm = get_llm_service()
    is_healthy, status = llm.check_health()
    
    if is_healthy:
        print(f"✅ LLM Service: {status}")
    else:
        print(f"⚠️  LLM Service: {status}")
    
    print("=" * 60)
    print(f"📚 API Docs: http://localhost:{api_config.port}/docs")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_v2:app", host="0.0.0.0", port=8000, reload=True)
