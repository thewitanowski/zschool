import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from canvas_client import canvas_client
from ai_service import ai_service
from models import WeeklyPlan
from database import get_db
from canvas_module_service import CanvasModuleService
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeekPlanService:
    """
    Service for managing weekly plans - fetching, parsing, and storing.
    Orchestrates Canvas API calls, AI parsing, and database operations.
    """
    
    def __init__(self):
        self.canvas_client = canvas_client
        self.ai_service = ai_service
        self.canvas_module_service = CanvasModuleService(canvas_client)
        
    async def get_latest_week_plan(self, db: Session, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Get the latest weekly plan - either from database or by fetching/parsing new data.
        
        Args:
            db: Database session
            force_refresh: If True, always fetch new data from Canvas
            
        Returns:
            Latest weekly plan JSON object
            
        Raises:
            Exception: If unable to fetch or parse weekly plan
        """
        
        # Check database for existing plans first (unless force refresh)
        if not force_refresh:
            logger.info("Checking database for latest weekly plan")
            latest_plan = db.query(WeeklyPlan).order_by(desc(WeeklyPlan.created_at)).first()
            
            if latest_plan:
                logger.info(f"Found existing weekly plan from {latest_plan.created_at}")
                return latest_plan.processed_json
        
        # Fetch and parse new data from Canvas
        logger.info("Fetching new weekly plan from Canvas")
        return await self._fetch_and_parse_latest_plan(db)
    
    async def _fetch_and_parse_latest_plan(self, db: Session) -> Dict[str, Any]:
        """
        Fetch the latest announcement from Canvas and parse it with AI.
        
        Args:
            db: Database session
            
        Returns:
            Parsed weekly plan JSON object
            
        Raises:
            Exception: If unable to fetch or parse data
        """
        
        try:
            # Step 1: Fetch latest announcement from Canvas
            logger.info("Fetching latest announcement from Canvas")
            
            # Use course ID 20564 as specified in the project brief
            course_id = 20564
            announcement = await self.canvas_client.get_latest_announcement(course_id)
            
            if not announcement:
                raise Exception("No announcements found in the specified course")
            
            # Extract HTML content
            html_content = announcement.get('message', '')
            if not html_content:
                raise Exception("Announcement has no content")
            
            logger.info(f"Retrieved announcement: {announcement.get('title', 'Untitled')}")
            logger.debug(f"HTML content length: {len(html_content)} characters")
            
            # Step 2: Parse with AI
            logger.info("Parsing announcement with AI service")
            parsed_json = self.ai_service.parse_announcement_to_json(html_content)
            
            # Step 3: Enhance with Canvas URLs
            logger.info("Fetching Canvas URLs for lessons")
            try:
                # Default course ID - this should be configurable in the future
                course_id = 20564
                classwork = parsed_json.get('classwork', [])
                
                if classwork:
                    lesson_urls = await self.canvas_module_service.get_lesson_urls_for_subjects(course_id, classwork)
                    
                    # Add Canvas URLs to each lesson in classwork
                    for subject_data in classwork:
                        subject_name = subject_data.get('subject', '').lower().replace(' ', '_')
                        lessons = subject_data.get('lessons', [])
                        
                        # Add canvas_urls field to each subject
                        subject_data['canvas_urls'] = {}
                        
                        for lesson in lessons:
                            lesson_key = f"{subject_name}_{lesson.lower()}"
                            canvas_url = lesson_urls.get(lesson_key)
                            
                            if canvas_url:
                                subject_data['canvas_urls'][lesson] = canvas_url
                            else:
                                # Fallback to course modules page
                                subject_data['canvas_urls'][lesson] = f"https://learning.acc.edu.au/courses/{course_id}/modules"
                    
                    logger.info(f"Added Canvas URLs for {len(lesson_urls)} lessons")
                else:
                    logger.warning("No classwork found in parsed data")
                    
            except Exception as e:
                logger.error(f"Failed to fetch Canvas URLs: {e}")
                # Continue without Canvas URLs - frontend will use fallbacks
            
            # Step 4: Fetch weekly assignments
            logger.info("Fetching weekly assignments")
            try:
                # Calculate current week's Monday to Sunday
                now = datetime.now()
                # Find Monday of current week (weekday 0=Monday, 6=Sunday)
                days_since_monday = now.weekday()
                monday = now - timedelta(days=days_since_monday)
                sunday = monday + timedelta(days=6)
                
                start_date = monday.strftime('%Y-%m-%d')
                end_date = sunday.strftime('%Y-%m-%d')
                
                # Course IDs to fetch assignments from
                course_ids = [20564, 20354]  # Add more course IDs as needed
                
                assignments = await self.canvas_client.get_weekly_assignments(start_date, end_date, course_ids)
                
                # Add assignments to the parsed data
                parsed_json['assignments'] = assignments
                parsed_json['assignment_period'] = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'total_assignments': len(assignments)
                }
                
                logger.info(f"Added {len(assignments)} assignments for week {start_date} to {end_date}")
                
            except Exception as e:
                logger.error(f"Failed to fetch weekly assignments: {e}")
                # Continue without assignments
                parsed_json['assignments'] = []
                parsed_json['assignment_period'] = {
                    'start_date': '',
                    'end_date': '',
                    'total_assignments': 0
                }
            
            # Step 5: Save to database
            logger.info("Saving parsed plan to database")
            
            # Extract week starting date for the database
            week_starting_str = parsed_json.get('week_starting', '')
            week_starting = None
            
            if week_starting_str:
                try:
                    week_starting = datetime.fromisoformat(week_starting_str)
                except ValueError:
                    logger.warning(f"Unable to parse week_starting date: {week_starting_str}")
                    week_starting = datetime.now()
            else:
                week_starting = datetime.now()
            
            # Check if a plan already exists for this week
            existing_plan = db.query(WeeklyPlan).filter(
                WeeklyPlan.week_starting == week_starting.date()
            ).first()
            
            if existing_plan:
                # Update existing plan
                existing_plan.processed_json = parsed_json
                existing_plan.created_at = datetime.now()
                weekly_plan = existing_plan
                logger.info(f"Updated existing weekly plan with ID {weekly_plan.id}")
            else:
                # Create new WeeklyPlan record
                weekly_plan = WeeklyPlan(
                    week_starting=week_starting,
                    processed_json=parsed_json,
                    created_at=datetime.now()
                )
                db.add(weekly_plan)
                logger.info("Created new weekly plan")
            
            db.commit()
            db.refresh(weekly_plan)
            
            logger.info(f"Successfully saved weekly plan with ID {weekly_plan.id}")
            
            return parsed_json
            
        except Exception as e:
            logger.error(f"Failed to fetch and parse weekly plan: {e}")
            db.rollback()
            raise Exception(f"Unable to process weekly plan: {e}")
    
    async def get_week_plan_by_date(self, db: Session, week_starting: datetime) -> Optional[Dict[str, Any]]:
        """
        Get a specific weekly plan by its starting date.
        
        Args:
            db: Database session
            week_starting: The starting date of the week
            
        Returns:
            Weekly plan JSON object if found, None otherwise
        """
        
        logger.info(f"Looking for weekly plan for week starting {week_starting}")
        
        plan = db.query(WeeklyPlan).filter(
            WeeklyPlan.week_starting == week_starting
        ).first()
        
        if plan:
            logger.info(f"Found weekly plan for {week_starting}")
            return plan.processed_json
        
        logger.info(f"No weekly plan found for {week_starting}")
        return None
    
    async def get_all_week_plans(self, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get all weekly plans, ordered by most recent first.
        
        Args:
            db: Database session
            limit: Maximum number of plans to return
            
        Returns:
            List of weekly plan JSON objects
        """
        
        logger.info(f"Fetching up to {limit} weekly plans")
        
        plans = db.query(WeeklyPlan).order_by(
            desc(WeeklyPlan.created_at)
        ).limit(limit).all()
        
        result = []
        for plan in plans:
            plan_data = plan.processed_json.copy()
            plan_data['id'] = plan.id
            plan_data['created_at'] = plan.created_at.isoformat()
            result.append(plan_data)
        
        logger.info(f"Found {len(result)} weekly plans")
        return result
    
    def test_integration(self, db: Session) -> Dict[str, Any]:
        """
        Test the complete integration - Canvas API + AI parsing + Database.
        
        Args:
            db: Database session
            
        Returns:
            Test result dictionary
        """
        
        test_result = {
            "canvas_client": "not_tested",
            "ai_service": "not_tested",
            "database": "not_tested",
            "overall_status": "pending"
        }
        
        try:
            # Test Canvas client
            logger.info("Testing Canvas client connection")
            canvas_test = self.canvas_client.test_connection()
            test_result["canvas_client"] = "success" if canvas_test["status"] == "success" else "failed"
            
            # Test AI service
            logger.info("Testing AI service connection")
            ai_test = self.ai_service.test_connection()
            test_result["ai_service"] = "success" if ai_test["status"] == "success" else "failed"
            
            # Test database
            logger.info("Testing database connection")
            try:
                # Simple database query
                count = db.query(WeeklyPlan).count()
                test_result["database"] = "success"
                test_result["db_plan_count"] = count
            except Exception as e:
                logger.error(f"Database test failed: {e}")
                test_result["database"] = "failed"
                test_result["db_error"] = str(e)
            
            # Overall status
            if all(status == "success" for status in [
                test_result["canvas_client"], 
                test_result["ai_service"], 
                test_result["database"]
            ]):
                test_result["overall_status"] = "success"
                test_result["message"] = "All integrations working correctly"
            else:
                test_result["overall_status"] = "partial_failure"
                test_result["message"] = "Some integrations failed"
            
        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            test_result["overall_status"] = "error"
            test_result["message"] = f"Integration test error: {e}"
        
        return test_result


# Singleton instance for use throughout the application
week_plan_service = WeekPlanService() 