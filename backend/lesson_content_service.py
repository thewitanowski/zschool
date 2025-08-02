import logging
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import LessonContent, WeeklyPlanLesson, WeeklyPlan
from canvas_client import canvas_client
from ai_service import ai_service

logger = logging.getLogger(__name__)

class LessonContentService:
    def __init__(self):
        """Initialize the lesson content service."""
        self.cache_duration_hours = 24  # Cache content for 24 hours
        
    def _generate_content_hash(self, content: str) -> str:
        """Generate a hash of the content to detect changes."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    async def get_lesson_content(self, db: Session, course_id: int, module_item_id: int, 
                               force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get lesson content, using cache when available or fetching from Canvas.
        
        Args:
            db: Database session
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            force_refresh: Force refresh from Canvas even if cached
            
        Returns:
            Dict containing the lesson content and metadata
        """
        try:
            logger.info(f"Getting lesson content for course {course_id}, item {module_item_id}")
            
            # Check if we have cached content
            cached_content = None
            if not force_refresh:
                cached_content = self._get_cached_content(db, course_id, module_item_id)
                
                if cached_content and self._is_cache_valid(cached_content):
                    logger.info(f"Using cached content for item {module_item_id}")
                    return {
                        "success": True,
                        "content": cached_content.transformed_content,
                        "cached": True,
                        "last_updated": cached_content.last_transformed.isoformat(),
                        "lesson_id": cached_content.id
                    }
            
            # Fetch fresh content from Canvas
            logger.info(f"Fetching fresh content from Canvas for item {module_item_id}")
            canvas_content = await canvas_client.get_module_item_content(course_id, module_item_id)
            
            if not canvas_content:
                raise Exception("No content returned from Canvas")
            
            # Transform content using AI
            raw_html = canvas_content.get("content", "") or canvas_content.get("body", "")
            lesson_title = canvas_content.get("title", "")
            lesson_type = canvas_content.get("type", "")
            
            transformation_result = await ai_service.transform_lesson_content(
                raw_html, lesson_title, lesson_type
            )
            
            # Save or update cached content
            lesson_content = self._save_lesson_content(
                db, course_id, module_item_id, canvas_content, transformation_result
            )
            
            return {
                "success": True,
                "content": lesson_content.transformed_content,
                "cached": False,
                "last_updated": lesson_content.last_transformed.isoformat(),
                "lesson_id": lesson_content.id,
                "transformation_success": lesson_content.transformation_success
            }
            
        except Exception as e:
            logger.error(f"Error getting lesson content for item {module_item_id}: {e}")
            
            # Try to return cached content even if it's stale
            cached_content = self._get_cached_content(db, course_id, module_item_id)
            if cached_content:
                logger.warning(f"Returning stale cached content for item {module_item_id}")
                return {
                    "success": False,
                    "error": str(e),
                    "content": cached_content.transformed_content,
                    "cached": True,
                    "stale": True,
                    "last_updated": cached_content.last_transformed.isoformat(),
                    "lesson_id": cached_content.id
                }
            
            # Return error with fallback content
            return {
                "success": False,
                "error": str(e),
                "content": {
                    "title": "Content Unavailable",
                    "summary": f"Unable to load lesson content: {str(e)}",
                    "sections": [
                        {
                            "heading": "Error",
                            "content": "This lesson content could not be loaded at this time. Please try again later or access it directly in Canvas.",
                            "type": "text"
                        }
                    ]
                }
            }
    
    def _get_cached_content(self, db: Session, course_id: int, module_item_id: int) -> Optional[LessonContent]:
        """Get cached lesson content from database."""
        return db.query(LessonContent).filter(
            and_(
                LessonContent.course_id == course_id,
                LessonContent.module_item_id == module_item_id
            )
        ).first()
    
    def _is_cache_valid(self, cached_content: LessonContent) -> bool:
        """Check if cached content is still valid."""
        if not cached_content.last_fetched:
            return False
            
        cache_expiry = cached_content.last_fetched + timedelta(hours=self.cache_duration_hours)
        return datetime.now() < cache_expiry
    
    def _save_lesson_content(self, db: Session, course_id: int, module_item_id: int,
                           canvas_content: Dict, transformation_result: Dict) -> LessonContent:
        """Save or update lesson content in database."""
        try:
            raw_content = canvas_content.get("content", "") or canvas_content.get("body", "")
            content_hash = self._generate_content_hash(raw_content)
            
            # Check if we already have this content
            existing_content = self._get_cached_content(db, course_id, module_item_id)
            
            if existing_content:
                # Update existing content
                existing_content.lesson_title = canvas_content.get("title", "")
                existing_content.lesson_type = canvas_content.get("type", "")
                existing_content.raw_content = raw_content
                existing_content.canvas_url = canvas_content.get("html_url", "")
                existing_content.transformed_content = transformation_result.get("content", {})
                existing_content.transformation_success = transformation_result.get("success", False)
                existing_content.transformation_error = transformation_result.get("error")
                existing_content.last_fetched = datetime.now()
                existing_content.last_transformed = datetime.now()
                existing_content.content_hash = content_hash
                
                lesson_content = existing_content
                logger.info(f"Updated existing lesson content {existing_content.id}")
            else:
                # Create new content
                lesson_content = LessonContent(
                    course_id=course_id,
                    module_item_id=module_item_id,
                    lesson_title=canvas_content.get("title", ""),
                    lesson_type=canvas_content.get("type", ""),
                    raw_content=raw_content,
                    canvas_url=canvas_content.get("html_url", ""),
                    transformed_content=transformation_result.get("content", {}),
                    transformation_success=transformation_result.get("success", False),
                    transformation_error=transformation_result.get("error"),
                    last_fetched=datetime.now(),
                    last_transformed=datetime.now(),
                    content_hash=content_hash
                )
                
                db.add(lesson_content)
                logger.info(f"Created new lesson content for item {module_item_id}")
            
            db.commit()
            db.refresh(lesson_content)
            
            return lesson_content
            
        except Exception as e:
            logger.error(f"Error saving lesson content: {e}")
            db.rollback()
            raise
    
    async def get_lesson_content_by_id(self, db: Session, lesson_id: int) -> Dict[str, Any]:
        """
        Get lesson content by its database ID.
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            
        Returns:
            Dict containing the lesson content
        """
        try:
            lesson_content = db.query(LessonContent).filter(LessonContent.id == lesson_id).first()
            
            if not lesson_content:
                return {
                    "success": False,
                    "error": "Lesson content not found"
                }
            
            return {
                "success": True,
                "content": lesson_content.transformed_content,
                "lesson_id": lesson_content.id,
                "last_updated": lesson_content.last_transformed.isoformat(),
                "transformation_success": lesson_content.transformation_success
            }
            
        except Exception as e:
            logger.error(f"Error getting lesson content by ID {lesson_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_lessons_for_weekly_plan(self, db: Session, weekly_plan_id: int) -> List[Dict[str, Any]]:
        """
        Get all lessons associated with a weekly plan.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            
        Returns:
            List of lesson content dictionaries
        """
        try:
            lessons = db.query(WeeklyPlanLesson).filter(
                WeeklyPlanLesson.weekly_plan_id == weekly_plan_id
            ).all()
            
            result = []
            for lesson_plan in lessons:
                if lesson_plan.lesson_content:
                    result.append({
                        "lesson_id": lesson_plan.lesson_content.id,
                        "title": lesson_plan.lesson_content.lesson_title,
                        "type": lesson_plan.lesson_content.lesson_type,
                        "subject": lesson_plan.subject,
                        "order": lesson_plan.lesson_order,
                        "completed": lesson_plan.user_completed,
                        "content": lesson_plan.lesson_content.transformed_content
                    })
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting lessons for weekly plan {weekly_plan_id}: {e}")
            return []
    
    def mark_lesson_completed(self, db: Session, lesson_id: int, user_session: str, 
                            completed: bool = True) -> Dict[str, Any]:
        """
        Mark a lesson as completed or incomplete.
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            user_session: User session ID
            completed: Whether to mark as completed
            
        Returns:
            Dict with success status
        """
        try:
            # For now, we'll use a simple approach without user-specific tracking
            # In a full implementation, you'd want to track completion per user
            
            lesson_content = db.query(LessonContent).filter(LessonContent.id == lesson_id).first()
            
            if not lesson_content:
                return {
                    "success": False,
                    "error": "Lesson not found"
                }
            
            # Update any weekly plan lessons associated with this content
            weekly_plan_lessons = db.query(WeeklyPlanLesson).filter(
                WeeklyPlanLesson.lesson_content_id == lesson_id
            ).all()
            
            for wpl in weekly_plan_lessons:
                wpl.user_completed = completed
                wpl.completion_date = datetime.now() if completed else None
            
            db.commit()
            
            return {
                "success": True,
                "lesson_id": lesson_id,
                "completed": completed,
                "updated_count": len(weekly_plan_lessons)
            }
            
        except Exception as e:
            logger.error(f"Error marking lesson {lesson_id} as completed: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    async def mark_lesson_complete_in_canvas(self, db: Session, lesson_id: int, 
                                           course_id: int, module_item_id: int,
                                           user_session: str, completed: bool = True) -> Dict[str, Any]:
        """
        Mark a lesson as complete both in our database and in Canvas LMS.
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            user_session: User session ID
            completed: Whether to mark as completed
            
        Returns:
            Dict with success status and Canvas response
        """
        try:
            logger.info(f"Marking lesson {lesson_id} as {'complete' if completed else 'incomplete'} in Canvas and database")
            
            # First, mark in Canvas LMS
            canvas_result = await canvas_client.mark_lesson_complete(
                course_id, module_item_id, completed
            )
            
            # Then update our local database
            db_result = self.mark_lesson_completed(db, lesson_id, user_session, completed)
            
            if not db_result.get("success"):
                logger.warning(f"Canvas update succeeded but database update failed: {db_result.get('error')}")
            
            return {
                "success": canvas_result.get("success", False),
                "lesson_id": lesson_id,
                "module_item_id": module_item_id,
                "completed": completed,
                "canvas_response": canvas_result,
                "database_response": db_result,
                "synced": canvas_result.get("success") and db_result.get("success")
            }
            
        except Exception as e:
            logger.error(f"Error marking lesson {lesson_id} as complete: {e}")
            return {
                "success": False,
                "error": str(e),
                "lesson_id": lesson_id,
                "completed": completed
            }

    async def get_lesson_progress_from_canvas(self, db: Session, course_id: int, 
                                            module_item_id: int) -> Dict[str, Any]:
        """
        Get lesson completion status from Canvas and sync with local database.
        
        Args:
            db: Database session
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            
        Returns:
            Dict containing lesson progress information
        """
        try:
            logger.info(f"Getting lesson progress from Canvas for item {module_item_id}")
            
            # Get completion status from Canvas
            canvas_status = await canvas_client.get_lesson_completion_status(
                course_id, module_item_id
            )
            
            if not canvas_status.get("success"):
                return canvas_status
            
            # Find corresponding lesson in our database
            lesson_content = db.query(LessonContent).filter(
                and_(
                    LessonContent.course_id == course_id,
                    LessonContent.module_item_id == module_item_id
                )
            ).first()
            
            if not lesson_content:
                logger.warning(f"Lesson not found in database for Canvas item {module_item_id}")
                return {
                    "success": False,
                    "error": "Lesson not found in local database",
                    "canvas_status": canvas_status
                }
            
            # Sync completion status with database if needed
            canvas_completed = canvas_status.get("completed", False)
            
            # Update all weekly plan lessons for this content
            weekly_plan_lessons = db.query(WeeklyPlanLesson).filter(
                WeeklyPlanLesson.lesson_content_id == lesson_content.id
            ).all()
            
            for wpl in weekly_plan_lessons:
                if wpl.user_completed != canvas_completed:
                    wpl.user_completed = canvas_completed
                    wpl.completion_date = datetime.now() if canvas_completed else None
                    logger.info(f"Synced lesson {lesson_content.id} completion status from Canvas")
            
            db.commit()
            
            return {
                "success": True,
                "lesson_id": lesson_content.id,
                "module_item_id": module_item_id,
                "completed": canvas_completed,
                "completion_requirement": canvas_status.get("completion_requirement"),
                "title": canvas_status.get("title"),
                "type": canvas_status.get("type"),
                "synced": True
            }
            
        except Exception as e:
            logger.error(f"Error getting lesson progress from Canvas: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e),
                "module_item_id": module_item_id
            }

    def update_lesson_status_in_board(self, db: Session, lesson_id: int, 
                                    new_status: str, user_session: str) -> Dict[str, Any]:
        """
        Update lesson status and trigger Kanban board update.
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            new_status: New status (to-do, in-progress, done)
            user_session: User session ID
            
        Returns:
            Dict with success status and updated board state
        """
        try:
            logger.info(f"Updating lesson {lesson_id} status to {new_status}")
            
            # Mark lesson as completed if status is 'done'
            completed = new_status == 'done'
            lesson_result = self.mark_lesson_completed(db, lesson_id, user_session, completed)
            
            if not lesson_result.get("success"):
                return lesson_result
            
            # This would integrate with board_state_service to update the Kanban board
            # For now, we'll return the lesson update result
            # In a full implementation, this would trigger board state updates
            
            return {
                "success": True,
                "lesson_id": lesson_id,
                "new_status": new_status,
                "completed": completed,
                "board_update_needed": True,
                "message": f"Lesson marked as {new_status}"
            }
            
        except Exception as e:
            logger.error(f"Error updating lesson status in board: {e}")
            return {
                "success": False,
                "error": str(e),
                "lesson_id": lesson_id,
                "new_status": new_status
            }

    async def mark_lesson_as_read(self, db: Session, lesson_id: int, 
                                user_session: str) -> Dict[str, Any]:
        """
        Mark a lesson as read (viewed but not necessarily completed).
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            user_session: User session ID
            
        Returns:
            Dict with success status
        """
        try:
            logger.info(f"Marking lesson {lesson_id} as read")
            
            # For now, we'll track this as metadata in the lesson content
            lesson_content = db.query(LessonContent).filter(LessonContent.id == lesson_id).first()
            
            if not lesson_content:
                return {
                    "success": False,
                    "error": "Lesson not found"
                }
            
            # Update last_fetched to indicate it was viewed
            lesson_content.last_fetched = datetime.now()
            
            # Update weekly plan lessons to track read status
            weekly_plan_lessons = db.query(WeeklyPlanLesson).filter(
                WeeklyPlanLesson.lesson_content_id == lesson_id
            ).all()
            
            for wpl in weekly_plan_lessons:
                # Add a note that it was read (if not already completed)
                if not wpl.user_completed:
                    current_notes = wpl.user_notes or ""
                    read_marker = f"[Read on {datetime.now().strftime('%Y-%m-%d %H:%M')}]"
                    if read_marker not in current_notes:
                        wpl.user_notes = f"{current_notes}\n{read_marker}".strip()
            
            db.commit()
            
            return {
                "success": True,
                "lesson_id": lesson_id,
                "marked_as_read": True,
                "timestamp": datetime.now().isoformat(),
                "updated_count": len(weekly_plan_lessons)
            }
            
        except Exception as e:
            logger.error(f"Error marking lesson {lesson_id} as read: {e}")
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }

    async def get_lesson_with_canvas_status(self, db: Session, lesson_id: int) -> Dict[str, Any]:
        """
        Get lesson content with real-time Canvas completion status.
        
        Args:
            db: Database session
            lesson_id: Database ID of the lesson content
            
        Returns:
            Dict containing lesson content and Canvas status
        """
        try:
            lesson_content = db.query(LessonContent).filter(LessonContent.id == lesson_id).first()
            
            if not lesson_content:
                return {
                    "success": False,
                    "error": "Lesson not found"
                }
            
            # Get current status from Canvas if we have the required IDs
            canvas_status = None
            if lesson_content.course_id and lesson_content.module_item_id:
                canvas_status = await self.get_lesson_progress_from_canvas(
                    db, lesson_content.course_id, lesson_content.module_item_id
                )
            
            return {
                "success": True,
                "lesson_id": lesson_id,
                "content": lesson_content.transformed_content,
                "last_updated": lesson_content.last_transformed.isoformat(),
                "transformation_success": lesson_content.transformation_success,
                "canvas_status": canvas_status,
                "course_id": lesson_content.course_id,
                "module_item_id": lesson_content.module_item_id
            }
            
        except Exception as e:
            logger.error(f"Error getting lesson with Canvas status: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Singleton instance for use throughout the application
lesson_content_service = LessonContentService() 