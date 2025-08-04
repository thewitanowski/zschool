import os
from fastapi import FastAPI, HTTPException, Depends, Query, Body, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from database import engine, Base, get_db
from models import Course, WeeklyPlan, Module, ModuleItem, Assignment, BoardState, LessonContent, WeeklyPlanLesson, ConvertedCanvasPage
from canvas_client import canvas_client
from ai_service import ai_service
from week_plan_service import week_plan_service
from board_state_service import board_state_service
from lesson_content_service import lesson_content_service
from sqlalchemy import and_
from sqlalchemy.orm import Session
from user_service import UserService
from converted_page_service import ConvertedPageService
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency injection functions
def get_user_service() -> UserService:
    return UserService(canvas_client)

def get_converted_page_service() -> ConvertedPageService:
    return ConvertedPageService(ai_service)

# Create FastAPI app
app = FastAPI(
    title="ZSchool API",
    description="A display layer over Canvas LMS API for better student access",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001", 
        "http://frontend:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers and monitoring.
    Returns service status and basic diagnostics.
    """
    try:
        # Test database connection
        db = next(get_db())
        try:
            # Simple query to verify database connectivity
            db.execute("SELECT 1")
            db_status = "healthy"
        except Exception as db_error:
            db_status = f"unhealthy: {str(db_error)}"
        finally:
            db.close()
            
        # Test AI service
        try:
            # Simple AI service check (without actually calling external API)
            ai_status = "healthy" if ai_service else "unhealthy"
        except Exception as ai_error:
            ai_status = f"unhealthy: {str(ai_error)}"
            
        # Test Canvas client
        try:
            canvas_status = "healthy" if canvas_client else "unhealthy"
        except Exception as canvas_error:
            canvas_status = f"unhealthy: {str(canvas_error)}"
        
        overall_status = "healthy" if all([
            "healthy" in db_status,
            "healthy" in ai_status, 
            "healthy" in canvas_status
        ]) else "degraded"
        
        return {
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": db_status,
                "ai_service": ai_status,
                "canvas_client": canvas_status
            },
            "version": "1.0.0"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "version": "1.0.0"
        }

# API status endpoint
@app.get("/api/v1/status")
async def api_status():
    """API status endpoint with service information."""
    return {
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "canvas_api": "enabled",
            "ai_service": "enabled",
            "database": "enabled",
            "board_persistence": "enabled",
            "lesson_viewer": "enabled",
            "content_transformation": "enabled",
            "lesson_actions": "enabled",
            "canvas_sync": "enabled"
        }
    }

# Canvas API test endpoints
@app.get("/api/v1/canvas/test")
async def test_canvas_connection():
    """Test Canvas API connection."""
    try:
        result = canvas_client.test_connection()
        return result
    except Exception as e:
        logger.error(f"Canvas connection test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Canvas API test failed: {e}")

@app.get("/api/v1/canvas/urls")
async def get_canvas_urls():
    """Get Canvas API URLs for verification."""
    try:
        return canvas_client.get_test_urls()
    except Exception as e:
        logger.error(f"Failed to get Canvas URLs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get Canvas URLs: {e}")

# Phase 1.1 & 1.3 & Persistence: Canvas Page Content Endpoint with AI Processing and Caching
@app.get("/api/v1/courses/{course_id}/pages/{page_slug}")
async def get_canvas_page_content(
    course_id: int,
    page_slug: str,
    raw: bool = Query(False, description="Return raw Canvas data instead of processed components"),
    force_refresh: bool = Query(False, description="Force refresh of cached content"),
    db: Session = Depends(get_db),
    converted_page_service: ConvertedPageService = Depends(get_converted_page_service)
):
    """
    Get Canvas page content converted to structured JSON components with caching.
    
    - **course_id**: Canvas course ID
    - **page_slug**: Canvas page URL slug  
    - **raw**: Return raw Canvas data instead of AI-processed components
    - **force_refresh**: Force refresh of cached AI-converted content
    """
    start_time = time.time()
    
    try:
        logger.info(f"Fetching Canvas page content: course {course_id}, page {page_slug}")
        
        # Always fetch fresh Canvas data to check for updates
        page_content = await canvas_client.get_page_content(course_id, page_slug)
        logger.info(f"Successfully retrieved page: {page_content.get('title', 'Untitled')}")

        if raw:
            logger.info("Returning raw Canvas data as requested")
            return page_content

        html_body = page_content.get('body', '')
        if not html_body:
            logger.warning("No HTML body content found in Canvas response")
            return {
                "title": page_content.get('title', 'Untitled'),
                "page_id": page_content.get('page_id'),
                "updated_at": page_content.get('updated_at'),
                "url": page_content.get('url'),
                "components": [],
                "processed": True,
                "cached": False,
                "processing_info": {
                    "status": "no_content",
                    "message": "No HTML body content found"
                }
            }

        # Check for cached converted content
        cached_page = converted_page_service.get_converted_page(
            db, course_id, page_slug, force_refresh
        )
        
        # Determine if we need to re-convert
        needs_conversion = (
            cached_page is None or
            force_refresh or
            not cached_page.conversion_success or
            converted_page_service.is_content_changed(
                cached_page, 
                html_body,
                page_content.get('updated_at')
            )
        )
        
        if not needs_conversion and cached_page:
            # Return cached content
            logger.info(f"Returning cached converted content ({cached_page.component_count} components)")
            cached_page.last_accessed_at = datetime.now()
            db.commit()
            
            return {
                "title": cached_page.page_title,
                "page_id": cached_page.page_id,
                "updated_at": page_content.get('updated_at'),
                "url": page_content.get('url'),
                "course_id": course_id,
                "components": cached_page.ai_components,
                "processed": True,
                "cached": True,
                "processing_info": {
                    **cached_page.processing_info,
                    "cached_at": cached_page.first_converted_at.isoformat(),
                    "last_accessed": cached_page.last_accessed_at.isoformat()
                }
            }

        # Convert with AI (new conversion or refresh)
        conversion_start = time.time()
        logger.info(f"Converting HTML content ({len(html_body)} chars) to structured components")
        
        try:
            components = ai_service.convert_html_to_components(html_body)
            conversion_time_ms = int((time.time() - conversion_start) * 1000)
            
            logger.info(f"Successfully converted to {len(components)} components in {conversion_time_ms}ms")
            
            # Save converted content to cache
            processing_info = {
                "status": "success",
                "components_count": len(components),
                "original_html_length": len(html_body),
                "conversion_time_ms": conversion_time_ms,
                "cached": True
            }
            
            converted_page_service.save_converted_page(
                db=db,
                course_id=course_id,
                page_slug=page_slug,
                canvas_data=page_content,
                ai_components=components,
                processing_info=processing_info,
                conversion_time_ms=conversion_time_ms,
                raw_html_body=html_body
            )

            total_time_ms = int((time.time() - start_time) * 1000)
            
            return {
                "title": page_content.get('title', 'Untitled'),
                "page_id": page_content.get('page_id'),
                "updated_at": page_content.get('updated_at'),
                "url": page_content.get('url'),
                "course_id": course_id,
                "components": components,
                "processed": True,
                "cached": False,  # Just converted, not from cache
                "processing_info": {
                    **processing_info,
                    "total_time_ms": total_time_ms
                }
            }
            
        except Exception as ai_error:
            # Save conversion error for debugging
            logger.error(f"AI conversion failed: {ai_error}")
            conversion_time_ms = int((time.time() - conversion_start) * 1000)
            
            converted_page_service.save_conversion_error(
                db=db,
                course_id=course_id,
                page_slug=page_slug,
                canvas_data=page_content,
                error_message=str(ai_error),
                raw_html_body=html_body
            )
            
            # Return fallback response
            return {
                "title": page_content.get('title', 'Untitled'),
                "page_id": page_content.get('page_id'),
                "updated_at": page_content.get('updated_at'),
                "url": page_content.get('url'),
                "course_id": course_id,
                "components": [],
                "processed": False,
                "cached": False,
                "processing_info": {
                    "status": "ai_error",
                    "message": str(ai_error),
                    "fallback": "raw_html_available",
                    "conversion_time_ms": conversion_time_ms
                },
                "raw_html_body": html_body
            }

    except Exception as e:
        logger.error(f"Failed to process Canvas page content: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve or process page content: {e}"
        )

# New endpoint: Check conversion status for multiple pages
@app.get("/api/v1/courses/{course_id}/pages/{page_slug}/status")
async def get_page_conversion_status(
    course_id: int,
    page_slug: str,
    db: Session = Depends(get_db),
    converted_page_service: ConvertedPageService = Depends(get_converted_page_service)
):
    """
    Check if a specific Canvas page has been AI-converted and cached.
    
    - **course_id**: Canvas course ID
    - **page_slug**: Canvas page URL slug
    
    Returns conversion status and metadata.
    """
    try:
        status = converted_page_service.get_conversion_status(db, course_id, page_slug)
        return {
            "course_id": course_id,
            "page_slug": page_slug,
            **status
        }
    except Exception as e:
        logger.error(f"Failed to get conversion status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to check conversion status: {e}"
        )

# New endpoint: Batch check conversion status for multiple pages
@app.post("/api/v1/conversion-status/batch")
async def get_batch_conversion_status(
    pages: list[dict],
    db: Session = Depends(get_db),
    converted_page_service: ConvertedPageService = Depends(get_converted_page_service)
):
    """
    Check conversion status for multiple pages at once.
    
    Request body should be a list of objects with 'course_id' and 'page_slug':
    [
        {"course_id": 123, "page_slug": "lesson-1"},
        {"course_id": 123, "page_slug": "lesson-2"}
    ]
    """
    try:
        results = []
        for page_info in pages:
            course_id = page_info.get('course_id')
            page_slug = page_info.get('page_slug')
            
            if not course_id or not page_slug:
                continue
                
            status = converted_page_service.get_conversion_status(db, course_id, page_slug)
            results.append({
                "course_id": course_id,
                "page_slug": page_slug,
                **status
            })
        
        return {"results": results}
    except Exception as e:
        logger.error(f"Failed to get batch conversion status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to check batch conversion status: {e}"
        )

# AI Service test endpoints
@app.get("/api/v1/ai/test")
async def test_ai_connection():
    """Test AI service connection."""
    try:
        result = ai_service.test_connection()
        return result
    except Exception as e:
        logger.error(f"AI service test failed: {e}")
        raise HTTPException(status_code=500, detail=f"AI service test failed: {e}")

# Week Plan endpoints - The main functionality
@app.get("/api/v1/week-plan/latest")
async def get_latest_week_plan(
    request: Request,
    force_refresh: bool = False,
    db=Depends(get_db)
):
    user_session = request.headers.get('user-session')
    try:
        logger.info(f"Getting latest week plan (force_refresh: {force_refresh}, user_session: {user_session})")
        
        result = await week_plan_service.get_latest_week_plan(db, force_refresh)
        
        response = {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
            "source": "canvas_api" if force_refresh else "database_cache"
        }
        
        # If user session provided, try to load saved board state
        if user_session:
            # Get the weekly plan ID from database
            # For simplicity, we'll use a default ID of 1 for mock data
            weekly_plan_id = 1
            
            saved_board_state = await board_state_service.load_board_state(
                db, weekly_plan_id, user_session
            )
            
            if saved_board_state:
                response["saved_board_state"] = saved_board_state
                response["board_state_loaded"] = True
                logger.info(f"Loaded saved board state for session {user_session}")
            else:
                response["board_state_loaded"] = False
                logger.info(f"No saved board state found for session {user_session}")
        
        return response
        
    except Exception as e:
        logger.error(f"Failed to get latest week plan: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Unable to retrieve weekly plan: {e}"
        )

@app.get("/api/v1/week-plan/mock")
async def get_mock_week_plan():
    """
    Get a mock weekly plan demonstrating the expected JSON structure.
    This endpoint shows the target format for Phase 1, Step 1.3 testing.
    
    Returns:
        Mock structured weekly plan JSON object
    """
    try:
        logger.info("Returning mock weekly plan data")
        
        mock_data = {
            "week_starting": "2025-07-28",
            "title": "Week starting Monday 28 July",
            "teacher": {
                "name": "Norm Fitzgerald",
                "role": "Stage 3 Teacher"
            },
            "classwork": [
                {
                    "subject": "Spiritual and Physical Fitness",
                    "unit": "Unit 3",
                    "topic": "",
                    "lessons": ["11", "12", "13", "14", "15"],
                    "days": [],
                    "notes": []
                },
                {
                    "subject": "Maths",
                    "unit": "",
                    "topic": "Topic 9",
                    "lessons": ["B1", "B2", "B3", "B4", "B5"],
                    "days": [],
                    "notes": []
                },
                {
                    "subject": "English",
                    "unit": "Unit 11",
                    "topic": "",
                    "lessons": ["1", "2", "3", "4", "5"],
                    "days": [],
                    "notes": [
                        "Please submit your Informative, Imaginative and Persuasive Sentences"
                    ]
                },
                {
                    "subject": "Technology",
                    "unit": "Unit 3",
                    "topic": "",
                    "lessons": ["1", "2", "3", "4"],
                    "days": ["Monday", "Tuesday", "Thursday", "Friday"],
                    "notes": [
                        "Please submit your Binary Image assessment",
                        "Digital Design Project due on Sunday, 17 August (not end of term as mentioned in lessons)"
                    ]
                },
                {
                    "subject": "Health",
                    "unit": "Unit 3",
                    "topic": "",
                    "lessons": ["3"],
                    "days": ["Wednesday"],
                    "notes": []
                },
                {
                    "subject": "PE",
                    "unit": "Unit 3",
                    "topic": "",
                    "lessons": ["3"],
                    "days": ["Wednesday"],
                    "notes": []
                }
            ],
            "announcements": [
                {
                    "type": "term_start",
                    "message": "Welcome to Term 3"
                },
                {
                    "type": "new_student",
                    "message": "Welcome to our new student joining us this term"
                },
                {
                    "type": "term_index_notice",
                    "message": "The Term Index is no longer available. Use the Canvas Calendar or To Do List."
                },
                {
                    "type": "mark_as_done_tip",
                    "message": "Use 'Mark as Done' to keep track of lesson completion"
                }
            ],
            "assessment_and_quizzes": {
                "due_day": "Sunday",
                "access_window": "1 week before and after lesson appears",
                "exceptions": [
                    "If sick, travelling or in elite sport, use the 2-week window",
                    "If unable to complete, use the Attendance form in the Communication Hub and submit a Doctor's Certificate"
                ],
                "guidelines": [
                    "Do not email assessments to teachers",
                    "Plan ahead; no early or late access will be granted"
                ]
            },
            "class_connect": {
                "start_time": "Monday at 9:00",
                "description": "Live class session to meet your teacher and classmates, play games, and get school tips"
            },
            "induction_meeting": {
                "audience": "New DE students and supervisors",
                "datetime": "2025-07-30T09:00:00+10:00",
                "link": "https://meet.google.com/ids-iwku-fud",
                "instructions": "Student should be on their device and logged into Canvas Dashboard"
            }
        }
        
        return {
            "status": "success",
            "data": mock_data,
            "timestamp": datetime.now().isoformat(),
            "source": "mock_data",
            "note": "This is mock data demonstrating the expected JSON structure for Phase 1, Step 1.3"
        }
        
    except Exception as e:
        logger.error(f"Failed to return mock data: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Unable to retrieve mock weekly plan: {e}"
        )

# Board State Persistence Endpoints - Phase 1, Step 1.5
@app.post("/api/v1/board-state/save")
async def save_board_state(
    user_session: str = Header(..., description="User session ID"),
    board_data: Dict[str, Any] = Body(..., description="Current board state to save"),
    weekly_plan_id: int = Body(1, description="Weekly plan ID (default: 1 for mock data)"),
    db=Depends(get_db)
):
    """
    Save the current board state for a user session.
    
    Args:
        user_session: User session identifier from header
        board_data: Current state of the Kanban board
        weekly_plan_id: ID of the weekly plan (defaults to 1 for mock data)
        db: Database session dependency
        
    Returns:
        Save confirmation with timestamp
    """
    try:
        logger.info(f"Saving board state for session {user_session}")
        
        result = await board_state_service.save_board_state(
            db, weekly_plan_id, user_session, board_data
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to save board state: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to save board state: {e}"
        )

@app.get("/api/v1/board-state/load")
async def load_board_state(
    user_session: str = Header(..., description="User session ID"),
    weekly_plan_id: int = Query(1, description="Weekly plan ID (default: 1 for mock data)"),
    db=Depends(get_db)
):
    """
    Load the saved board state for a user session.
    
    Args:
        user_session: User session identifier from header
        weekly_plan_id: ID of the weekly plan (defaults to 1 for mock data)
        db: Database session dependency
        
    Returns:
        Saved board state data or 404 if not found
    """
    try:
        logger.info(f"Loading board state for session {user_session}")
        
        saved_state = await board_state_service.load_board_state(
            db, weekly_plan_id, user_session
        )
        
        if saved_state:
            return {
                "status": "success",
                "data": saved_state,
                "timestamp": datetime.now().isoformat()
            }
        
        raise HTTPException(
            status_code=404,
            detail="No saved board state found for this session"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to load board state: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load board state: {e}"
        )

@app.delete("/api/v1/board-state/clear")
async def clear_board_state(
    user_session: str = Header(..., description="User session ID"),
    weekly_plan_id: int = Query(1, description="Weekly plan ID (default: 1 for mock data)"),
    db=Depends(get_db)
):
    """
    Clear/reset the saved board state for a user session.
    
    Args:
        user_session: User session identifier from header
        weekly_plan_id: ID of the weekly plan (defaults to 1 for mock data)
        db: Database session dependency
        
    Returns:
        Clear confirmation
    """
    try:
        logger.info(f"Clearing board state for session {user_session}")
        
        result = await board_state_service.clear_board_state(
            db, weekly_plan_id, user_session
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to clear board state: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to clear board state: {e}"
        )

@app.get("/api/v1/board-state/session")
async def generate_session_id():
    """
    Generate a new user session ID for board state tracking.
    
    Returns:
        New session ID that can be used for board state persistence
    """
    try:
        session_id = board_state_service.generate_session_id()
        
        return {
            "status": "success",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "note": "Use this session ID in the 'user-session' header for board state persistence"
        }
        
    except Exception as e:
        logger.error(f"Failed to generate session ID: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate session ID: {e}"
        )

@app.get("/api/v1/board-state/summary/{weekly_plan_id}")
async def get_board_state_summary(
    weekly_plan_id: int,
    db=Depends(get_db)
):
    """
    Get summary of all board states for a weekly plan (debugging/admin endpoint).
    
    Args:
        weekly_plan_id: ID of the weekly plan
        db: Database session dependency
        
    Returns:
        Summary of all board states for the weekly plan
    """
    try:
        summary = board_state_service.get_board_state_summary(db, weekly_plan_id)
        
        return {
            "status": "success",
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get board state summary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to get board state summary: {e}"
        )

@app.get("/api/v1/week-plan/all")
async def get_all_week_plans(
    limit: int = Query(10, ge=1, le=50, description="Number of plans to return"),
    db=Depends(get_db)
):
    """
    Get all weekly plans from the database.
    
    Args:
        limit: Maximum number of plans to return (1-50)
        db: Database session dependency
        
    Returns:
        List of weekly plan JSON objects
    """
    try:
        logger.info(f"Getting all week plans (limit: {limit})")
        
        plans = await week_plan_service.get_all_week_plans(db, limit)
        
        return {
            "status": "success",
            "data": plans,
            "count": len(plans),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get week plans: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Unable to retrieve weekly plans: {e}"
        )

@app.get("/api/v1/week-plan/by-date")
async def get_week_plan_by_date(
    week_starting: str = Query(..., description="Week starting date in YYYY-MM-DD format"),
    db=Depends(get_db)
):
    """
    Get a specific weekly plan by its starting date.
    
    Args:
        week_starting: Week starting date in YYYY-MM-DD format
        db: Database session dependency
        
    Returns:
        Weekly plan JSON object if found
    """
    try:
        # Parse the date
        try:
            date_obj = datetime.fromisoformat(week_starting)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid date format. Use YYYY-MM-DD format."
            )
        
        logger.info(f"Getting week plan for {week_starting}")
        
        result = await week_plan_service.get_week_plan_by_date(db, date_obj)
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"No weekly plan found for {week_starting}"
            )
        
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get week plan by date: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Unable to retrieve weekly plan: {e}"
        )

# Integration test endpoint
@app.get("/api/v1/test/integration")
async def test_integration(db=Depends(get_db)):
    """
    Test the complete integration: Canvas API + AI Service + Database.
    
    Args:
        db: Database session dependency
        
    Returns:
        Integration test results
    """
    try:
        logger.info("Running integration test")
        
        result = week_plan_service.test_integration(db)
        
        # Return appropriate HTTP status based on test results
        if result["overall_status"] == "success":
            status_code = 200
        elif result["overall_status"] == "partial_failure":
            status_code = 206  # Partial Content
        else:
            status_code = 500
        
        return result
        
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Integration test error: {e}"
        )

# Canvas announcement endpoint for debugging
@app.get("/api/v1/canvas/announcement/latest")
async def get_latest_announcement():
    """
    Get the latest Canvas announcement (for debugging purposes).
    
    Returns:
        Latest announcement data from Canvas
    """
    try:
        logger.info("Getting latest Canvas announcement")
        
        # Use course ID 20564 as specified in the project brief
        course_id = 20564
        announcement = await canvas_client.get_latest_announcement(course_id)
        
        if not announcement:
            raise HTTPException(
                status_code=404,
                detail="No announcements found in the specified course"
            )
        
        return {
            "status": "success",
            "data": announcement,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get latest announcement: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Unable to retrieve announcement: {e}"
        )

# Lesson Content Endpoints - Phase 2, Step 2.1
@app.get("/api/v1/lessons/{lesson_id}")
async def get_lesson_content_by_id(
    lesson_id: int,
    db=Depends(get_db)
):
    """
    Get lesson content by its database ID.
    
    Args:
        lesson_id: Database ID of the lesson content
    """
    try:
        logger.info(f"Getting lesson content by ID: {lesson_id}")
        
        result = await lesson_content_service.get_lesson_content_by_id(db, lesson_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get("error", "Lesson content not found")
            )
        
        return {
            "status": "success",
            "data": result["content"],
            "lesson_id": lesson_id,
            "last_updated": result.get("last_updated"),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get lesson content by ID {lesson_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve lesson content: {e}"
        )

@app.get("/api/v1/lessons/canvas/{course_id}/{module_item_id}")
async def get_lesson_content_from_canvas(
    course_id: int,
    module_item_id: int,
    force_refresh: bool = Query(False, description="Force refresh from Canvas"),
    db=Depends(get_db)
):
    """
    Get lesson content from Canvas, with caching and AI transformation.
    
    Args:
        course_id: Canvas course ID
        module_item_id: Canvas module item ID
        force_refresh: Force refresh from Canvas even if cached
    """
    try:
        logger.info(f"Getting lesson content from Canvas: course {course_id}, item {module_item_id}")
        
        result = await lesson_content_service.get_lesson_content(
            db, course_id, module_item_id, force_refresh
        )
        
        response_data = {
            "status": "success" if result.get("success") else "partial_success",
            "data": result["content"],
            "cached": result.get("cached", False),
            "last_updated": result.get("last_updated"),
            "lesson_id": result.get("lesson_id"),
            "timestamp": datetime.now().isoformat()
        }
        
        if not result.get("success"):
            response_data["error"] = result.get("error")
            response_data["stale"] = result.get("stale", False)
        
        return response_data
        
    except Exception as e:
        logger.error(f"Failed to get lesson content from Canvas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve lesson content: {e}"
        )

@app.post("/api/v1/lessons/{lesson_id}/complete")
async def mark_lesson_complete(
    lesson_id: int,
    user_session: str = Header(..., description="User session ID"),
    completed: bool = Body(True, description="Whether to mark as completed"),
    db=Depends(get_db)
):
    """
    Mark a lesson as completed or incomplete.
    
    Args:
        lesson_id: Database ID of the lesson content
        user_session: User session ID
        completed: Whether to mark as completed
    """
    try:
        logger.info(f"Marking lesson {lesson_id} as {'completed' if completed else 'incomplete'}")
        
        result = lesson_content_service.mark_lesson_completed(
            db, lesson_id, user_session, completed
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to update lesson status")
            )
        
        return {
            "status": "success",
            "lesson_id": lesson_id,
            "completed": completed,
            "updated_count": result.get("updated_count", 0),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark lesson {lesson_id} as completed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to update lesson status: {e}"
        )

@app.get("/api/v1/weekly-plans/{weekly_plan_id}/lessons")
async def get_weekly_plan_lessons(
    weekly_plan_id: int,
    db=Depends(get_db)
):
    """
    Get all lessons associated with a weekly plan.
    
    Args:
        weekly_plan_id: ID of the weekly plan
    """
    try:
        logger.info(f"Getting lessons for weekly plan {weekly_plan_id}")
        
        lessons = lesson_content_service.get_lessons_for_weekly_plan(db, weekly_plan_id)
        
        return {
            "status": "success",
            "data": lessons,
            "weekly_plan_id": weekly_plan_id,
            "lesson_count": len(lessons),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get lessons for weekly plan {weekly_plan_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve weekly plan lessons: {e}"
        )

# Demo endpoint for lesson content (for testing without real Canvas data)
@app.get("/api/v1/lessons/demo/{lesson_number}")
async def get_demo_lesson_content(
    lesson_number: int,
    db=Depends(get_db)
):
    """
    Get demo lesson content for testing the lesson viewer.
    
    Args:
        lesson_number: Demo lesson number (1-5)
    """
    try:
        logger.info(f"Getting demo lesson content {lesson_number}")
        
        demo_lessons = {
            1: {
                "title": "Introduction to Algebra",
                "type": "Page",
                "summary": "Learn the fundamentals of algebraic expressions and equations in this introductory lesson.",
                "learning_objectives": [
                    "Understand what variables represent in algebra",
                    "Learn to simplify algebraic expressions",
                    "Solve basic linear equations"
                ],
                "sections": [
                    {
                        "heading": "What is Algebra?",
                        "content": "Algebra is a branch of mathematics that uses letters and symbols to represent numbers and quantities in formulas and equations. These letters, called variables, can stand for unknown values that we want to find.",
                        "type": "text"
                    },
                    {
                        "heading": "Key Concepts",
                        "content": "• Variables: Letters that represent unknown numbers\n• Expressions: Combinations of numbers, variables, and operations\n• Equations: Mathematical statements that show two expressions are equal\n• Coefficients: Numbers that multiply variables",
                        "type": "list"
                    },
                    {
                        "heading": "Practice Problems",
                        "content": "Try solving these basic equations:\n1. x + 5 = 12\n2. 2y - 3 = 7\n3. 3z + 4 = 19",
                        "type": "text"
                    }
                ],
                "resources": [
                    {
                        "title": "Algebra Basics Video",
                        "url": "https://example.com/algebra-video",
                        "type": "video"
                    },
                    {
                        "title": "Practice Worksheet",
                        "url": "https://example.com/worksheet.pdf",
                        "type": "file"
                    }
                ],
                "key_points": [
                    "Variables represent unknown numbers",
                    "Algebra helps solve real-world problems",
                    "Practice is essential for mastering concepts"
                ],
                "estimated_time": "15-20 minutes"
            },
            2: {
                "title": "The Water Cycle",
                "type": "Page",
                "summary": "Explore how water moves through Earth's atmosphere, land, and oceans in a continuous cycle.",
                "learning_objectives": [
                    "Identify the stages of the water cycle",
                    "Understand the role of energy in the water cycle",
                    "Explain how the water cycle affects weather patterns"
                ],
                "sections": [
                    {
                        "heading": "Overview",
                        "content": "The water cycle is the continuous movement of water on, above, and below the surface of Earth. This process is powered by energy from the sun and involves several key stages.",
                        "type": "text"
                    },
                    {
                        "heading": "Stages of the Water Cycle",
                        "content": "1. Evaporation: Water changes from liquid to gas\n2. Condensation: Water vapor forms clouds\n3. Precipitation: Rain, snow, or hail falls\n4. Collection: Water gathers in bodies of water\n5. Infiltration: Water soaks into the ground",
                        "type": "list"
                    },
                    {
                        "heading": "Human Impact",
                        "content": "Human activities can affect the water cycle through pollution, deforestation, and urbanization. Understanding these impacts is crucial for environmental conservation.",
                        "type": "text"
                    }
                ],
                "resources": [
                    {
                        "title": "Water Cycle Diagram",
                        "url": "https://example.com/water-cycle.png",
                        "type": "image"
                    }
                ],
                "key_points": [
                    "The sun provides energy for the water cycle",
                    "Water constantly moves between different states",
                    "The water cycle is essential for all life on Earth"
                ],
                "estimated_time": "12-15 minutes"
            },
            3: {
                "title": "Creative Writing: Character Development",
                "type": "Assignment",
                "summary": "Learn techniques for creating compelling, three-dimensional characters in your stories.",
                "learning_objectives": [
                    "Develop realistic character personalities",
                    "Create character backstories and motivations",
                    "Write dialogue that reveals character"
                ],
                "sections": [
                    {
                        "heading": "What Makes a Good Character?",
                        "content": "Great characters feel like real people with their own goals, fears, strengths, and weaknesses. They should be relatable and drive the story forward through their actions and decisions.",
                        "type": "text"
                    },
                    {
                        "heading": "Character Development Techniques",
                        "content": "• Give characters clear motivations\n• Create detailed backstories\n• Develop unique speech patterns\n• Show character growth throughout the story\n• Include both strengths and flaws",
                        "type": "list"
                    },
                    {
                        "heading": "Assignment",
                        "content": "Create a character profile for a protagonist including: name, age, background, personality traits, goals, and fears. Write a 500-word scene that introduces this character.",
                        "type": "text"
                    }
                ],
                "resources": [
                    {
                        "title": "Character Development Worksheet",
                        "url": "https://example.com/character-worksheet.pdf",
                        "type": "file"
                    }
                ],
                "key_points": [
                    "Characters should feel like real people",
                    "Backstory informs present behavior",
                    "Dialogue reveals personality"
                ],
                "estimated_time": "25-30 minutes"
            }
        }
        
        if lesson_number not in demo_lessons:
            lesson_number = 1  # Default to first lesson
        
        return {
            "status": "success",
            "data": demo_lessons[lesson_number],
            "lesson_id": f"demo-{lesson_number}",
            "cached": False,
            "last_updated": datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat(),
            "demo": True
        }
        
    except Exception as e:
        logger.error(f"Failed to get demo lesson content: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve demo lesson content: {e}"
        )

# Lesson Actions Endpoints - Phase 2, Step 2.2
@app.post("/api/v1/lessons/{lesson_id}/mark-done")
async def mark_lesson_done(
    lesson_id: int,
    user_session: str = Header(..., description="User session ID"),
    course_id: int = Body(..., description="Canvas course ID"),
    module_item_id: int = Body(..., description="Canvas module item ID"),
    db=Depends(get_db)
):
    """
    Mark a lesson as done/complete in both Canvas and local database.
    
    Args:
        lesson_id: Database ID of the lesson content
        user_session: User session ID
        course_id: Canvas course ID
        module_item_id: Canvas module item ID
    """
    try:
        logger.info(f"Marking lesson {lesson_id} as done via Canvas integration")
        
        result = await lesson_content_service.mark_lesson_complete_in_canvas(
            db, lesson_id, course_id, module_item_id, user_session, True
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to mark lesson as done")
            )
        
        return {
            "status": "success",
            "message": "Lesson marked as done in Canvas and database",
            "lesson_id": lesson_id,
            "canvas_synced": result.get("synced", False),
            "canvas_response": result.get("canvas_response", {}),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark lesson {lesson_id} as done: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to mark lesson as done: {e}"
        )

@app.post("/api/v1/lessons/{lesson_id}/mark-read")
async def mark_lesson_read(
    lesson_id: int,
    user_session: str = Header(..., description="User session ID"),
    db=Depends(get_db)
):
    """
    Mark a lesson as read (viewed but not necessarily completed).
    
    Args:
        lesson_id: Database ID of the lesson content
        user_session: User session ID
    """
    try:
        logger.info(f"Marking lesson {lesson_id} as read")
        
        result = await lesson_content_service.mark_lesson_as_read(
            db, lesson_id, user_session
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to mark lesson as read")
            )
        
        return {
            "status": "success",
            "message": "Lesson marked as read",
            "lesson_id": lesson_id,
            "marked_as_read": True,
            "timestamp": result.get("timestamp"),
            "updated_count": result.get("updated_count", 0)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark lesson {lesson_id} as read: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to mark lesson as read: {e}"
        )

@app.post("/api/v1/lessons/{lesson_id}/update-board-status")
async def update_lesson_board_status(
    lesson_id: int,
    user_session: str = Header(..., description="User session ID"),
    status: str = Body(..., description="New board status: to-do, in-progress, done"),
    db=Depends(get_db)
):
    """
    Update lesson status in the Kanban board.
    
    Args:
        lesson_id: Database ID of the lesson content
        user_session: User session ID
        status: New status (to-do, in-progress, done)
    """
    try:
        logger.info(f"Updating lesson {lesson_id} board status to {status}")
        
        valid_statuses = ['to-do', 'in-progress', 'done']
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        result = lesson_content_service.update_lesson_status_in_board(
            db, lesson_id, status, user_session
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to update lesson status")
            )
        
        return {
            "status": "success",
            "message": result.get("message", f"Lesson status updated to {status}"),
            "lesson_id": lesson_id,
            "new_status": status,
            "completed": result.get("completed", False),
            "board_update_needed": result.get("board_update_needed", False),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update lesson {lesson_id} board status: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to update lesson status: {e}"
        )

@app.get("/api/v1/lessons/{lesson_id}/canvas-status")
async def get_lesson_canvas_status(
    lesson_id: int,
    db=Depends(get_db)
):
    """
    Get lesson content with real-time Canvas completion status.
    
    Args:
        lesson_id: Database ID of the lesson content
    """
    try:
        logger.info(f"Getting Canvas status for lesson {lesson_id}")
        
        result = await lesson_content_service.get_lesson_with_canvas_status(db, lesson_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=404,
                detail=result.get("error", "Lesson not found")
            )
        
        return {
            "status": "success",
            "lesson_id": lesson_id,
            "canvas_status": result.get("canvas_status"),
            "lesson_content": result.get("content"),
            "course_id": result.get("course_id"),
            "module_item_id": result.get("module_item_id"),
            "last_updated": result.get("last_updated"),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get Canvas status for lesson {lesson_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to get Canvas status: {e}"
        )

@app.post("/api/v1/canvas/lesson/{course_id}/{module_item_id}/complete")
async def mark_canvas_lesson_complete(
    course_id: int,
    module_item_id: int,
    completed: bool = Body(True, description="Whether to mark as completed"),
    db=Depends(get_db)
):
    """
    Mark a Canvas lesson as complete directly via Canvas API.
    
    Args:
        course_id: Canvas course ID
        module_item_id: Canvas module item ID
        completed: Whether to mark as completed
    """
    try:
        logger.info(f"Marking Canvas lesson {module_item_id} as {'complete' if completed else 'incomplete'}")
        
        result = await canvas_client.mark_lesson_complete(course_id, module_item_id, completed)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to update Canvas lesson")
            )
        
        # Sync with local database if lesson exists
        lesson_content = db.query(LessonContent).filter(
            and_(
                LessonContent.course_id == course_id,
                LessonContent.module_item_id == module_item_id
            )
        ).first()
        
        local_sync_result = None
        if lesson_content:
            # Update local status to match Canvas
            weekly_plan_lessons = db.query(WeeklyPlanLesson).filter(
                WeeklyPlanLesson.lesson_content_id == lesson_content.id
            ).all()
            
            for wpl in weekly_plan_lessons:
                wpl.user_completed = completed
                wpl.completion_date = datetime.now() if completed else None
            
            db.commit()
            local_sync_result = {
                "synced": True,
                "lesson_id": lesson_content.id,
                "updated_count": len(weekly_plan_lessons)
            }
        
        return {
            "status": "success",
            "module_item_id": module_item_id,
            "completed": completed,
            "canvas_response": result,
            "local_sync": local_sync_result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to mark Canvas lesson as complete: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to update lesson status: {e}"
        )

@app.get("/api/v1/canvas/lesson-status/{course_id}/{module_id}/{module_item_id}")
async def get_canvas_lesson_status(
    course_id: int,
    module_id: int,
    module_item_id: int
):
    """
    Get Canvas lesson completion status by course_id, module_id, and module_item_id.
    Optimized for targeted status syncing without full data refresh.
    
    Args:
        course_id: Canvas course ID
        module_id: Canvas module ID
        module_item_id: Canvas module item ID
        
    Returns:
        Canvas completion status information
    """
    try:
        logger.debug(f"Getting Canvas status for course {course_id}, module {module_id}, item {module_item_id}")
        
        # Get completion status directly from Canvas
        canvas_status = await canvas_client.get_lesson_completion_status(course_id, module_item_id, module_id)
        
        if not canvas_status.get("success"):
            return {
                "success": False,
                "error": canvas_status.get("error", "Failed to get Canvas status"),
                "course_id": course_id,
                "module_id": module_id,
                "module_item_id": module_item_id
            }
        
        return {
            "success": True,
            "course_id": course_id,
            "module_id": module_id,
            "module_item_id": module_item_id,
            "completed": canvas_status.get("completed", False),
            "completion_requirement": canvas_status.get("completion_requirement"),
            "title": canvas_status.get("title", ""),
            "type": canvas_status.get("type", ""),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get Canvas lesson status for {course_id}/{module_id}/{module_item_id}: {e}")
        return {
            "success": False,
            "error": str(e),
            "course_id": course_id,
            "module_id": module_id,
            "module_item_id": module_item_id
        }

@app.get("/api/v1/canvas/progress/{course_id}")
async def get_canvas_course_progress(
    course_id: int,
    user_id: int = Query(None, description="User ID (optional)")
):
    """
    Get user progress for a Canvas course.
    
    Args:
        course_id: Canvas course ID
        user_id: User ID (optional, defaults to current user)
    """
    try:
        logger.info(f"Getting Canvas course progress for course {course_id}")
        
        result = await canvas_client.get_user_progress(course_id, user_id)
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to get course progress")
            )
        
        return {
            "status": "success",
            "course_id": course_id,
            "user_id": user_id,
            "progress": result.get("progress"),
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get Canvas course progress: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Unable to get course progress: {e}"
        )

@app.get("/api/v1/user/profile")
async def get_user_profile(user_service: UserService = Depends(get_user_service)):
    profile = await user_service.get_user_profile()
    if profile:
        return profile
    raise HTTPException(status_code=404, detail="User profile not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 