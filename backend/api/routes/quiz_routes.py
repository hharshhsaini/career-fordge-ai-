"""
CareerForge AI - Quiz Routes
Quiz generation endpoints.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, HTTPException
import sys
import os
os.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append('../..')
from api.schemas import QuizRequest, QuizBatchRequest
from services.quiz_service_v2 import QuizService

router = APIRouter(prefix="/quiz", tags=["Quiz"])

# Thread pool for parallel execution
executor = ThreadPoolExecutor(max_workers=8)


@router.post("")
async def generate_quiz(request: QuizRequest):
    """
    Generate a full quiz for a roadmap step.
    
    Creates a set of MCQ questions with varying difficulty,
    explanations, and optional code snippets.
    """
    loop = asyncio.get_event_loop()
    
    service = QuizService()
    result = await loop.run_in_executor(
        executor,
        service.generate_quiz,
        request.topic,
        request.step_name,
        request.num_questions,
        request.difficulty_mix
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )
    
    return result


@router.post("/batch")
async def generate_quiz_batch(request: QuizBatchRequest):
    """
    Generate a batch of quiz questions.
    
    Useful for progressive loading or generating
    additional questions for a step.
    """
    loop = asyncio.get_event_loop()
    
    service = QuizService()
    result = await loop.run_in_executor(
        executor,
        service.generate_quiz_batch,
        request.topic,
        request.step_name,
        request.count,
        request.start_id,
        request.difficulty
    )
    
    if "error" in result:
        raise HTTPException(
            status_code=500,
            detail=result["error"]
        )
    
    return result
