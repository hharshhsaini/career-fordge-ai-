"""
CareerForge AI - AI Routes
Main AI-powered endpoints for career guidance.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
import sys
import os
os.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('../..')
from api.schemas import (
    UserProfile,
    SkillsAnalysisRequest,
    TrendingSkillsRequest,
    InterviewPrepRequest,
    MockQuestionsRequest,
    AnswerAnalysisRequest,
)
from services.roadmap_service import RoadmapService
from services.skills_service import SkillsService
from services.interview_service import InterviewService
from services.youtube_service import get_curated_videos

router = APIRouter(prefix="/ai", tags=["AI"])

# Thread pool for parallel execution
executor = ThreadPoolExecutor(max_workers=12)


@router.post("/roadmap")
async def generate_roadmap(profile: UserProfile):
    """
    Generate a comprehensive career roadmap.
    
    Accepts user profile with background, skills, interests, and goals.
    Returns a structured 6-month roadmap with weekly breakdowns,
    projects, resources, and checkpoints.
    """
    loop = asyncio.get_event_loop()
    
    # Generate roadmap
    service = RoadmapService()
    result = await loop.run_in_executor(
        executor,
        service.generate_roadmap,
        profile.description,
        profile.hours_per_week,
        profile.max_months,
        profile.budget
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to generate roadmap")
        )
    
    # Fetch YouTube videos for roadmap steps in parallel
    roadmap = result.get("data", {}).get("roadmap", [])
    
    async def fetch_videos_for_step(step):
        """Fetch YouTube videos for a roadmap step."""
        # Build search query from step title and focus areas
        title = step.get("title", "")
        focus_areas = step.get("focus_areas", [])
        
        if focus_areas:
            query = f"{focus_areas[0]} tutorial for beginners"
        elif title:
            query = f"{title} tutorial"
        else:
            return step
        
        try:
            videos = await loop.run_in_executor(executor, get_curated_videos, query)
            step["video_results"] = videos
        except Exception as e:
            print(f"[AI Routes] YouTube fetch error: {e}")
            step["video_results"] = []
        
        return step
    
    # Fetch videos for all steps in parallel
    await asyncio.gather(*[fetch_videos_for_step(step) for step in roadmap])
    
    return result


@router.post("/skills")
async def analyze_skills(request: SkillsAnalysisRequest):
    """
    Analyze user's skills and provide recommendations.
    
    Identifies transferable skills, recommends new skills to learn,
    and provides a prioritized skill learning path.
    """
    loop = asyncio.get_event_loop()
    
    service = SkillsService()
    result = await loop.run_in_executor(
        executor,
        service.analyze_skills,
        request.background,
        request.target_role,
        request.interests
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to analyze skills")
        )
    
    return result


@router.post("/skills/trending")
async def get_trending_skills(request: TrendingSkillsRequest):
    """
    Get trending skills for a specific domain.
    
    Returns currently in-demand skills, emerging skills,
    and declining skills to avoid for the specified domain.
    """
    loop = asyncio.get_event_loop()
    
    service = SkillsService()
    result = await loop.run_in_executor(
        executor,
        service.get_trending_skills,
        request.domain
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to get trending skills")
        )
    
    return result


@router.post("/interview-prep")
async def generate_interview_prep(request: InterviewPrepRequest):
    """
    Generate interview preparation guide.
    
    Provides technical questions, behavioral questions,
    company research tips, and red flags to avoid.
    """
    loop = asyncio.get_event_loop()
    
    service = InterviewService()
    result = await loop.run_in_executor(
        executor,
        service.generate_prep_guide,
        request.role,
        request.experience_level,
        request.company,
        request.focus_areas
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to generate interview prep")
        )
    
    return result


@router.post("/interview-prep/questions")
async def generate_mock_questions(request: MockQuestionsRequest):
    """
    Generate mock interview questions for practice.
    
    Creates realistic interview questions with answer frameworks,
    key points to cover, and common mistakes to avoid.
    """
    loop = asyncio.get_event_loop()
    
    service = InterviewService()
    result = await loop.run_in_executor(
        executor,
        service.generate_mock_questions,
        request.role,
        request.question_type,
        request.count
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to generate mock questions")
        )
    
    return result


@router.post("/interview-prep/analyze")
async def analyze_interview_answer(request: AnswerAnalysisRequest):
    """
    Analyze a mock interview answer.
    
    Provides feedback on the answer including strengths,
    areas for improvement, and an improved version.
    """
    loop = asyncio.get_event_loop()
    
    service = InterviewService()
    result = await loop.run_in_executor(
        executor,
        service.analyze_answer,
        request.question,
        request.answer,
        request.role
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Failed to analyze answer")
        )
    
    return result
