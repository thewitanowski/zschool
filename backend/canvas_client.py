import os
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class CanvasClient:
    """
    Canvas LMS API client for handling all Canvas API interactions.
    Encapsulates authentication, headers, and common API patterns.
    """
    
    def __init__(self):
        self.base_url = "https://learning.acc.edu.au"
        self.bearer_token = os.getenv("CANVAS_BEARER_TOKEN")
        
        if not self.bearer_token:
            raise ValueError("CANVAS_BEARER_TOKEN environment variable is required")
        
        # Standard headers for all Canvas API requests
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Create async HTTP client with proper configuration
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers=self.headers
        )
        
        logger.info("Canvas client initialized")
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build complete URL for Canvas API endpoint.
        
        Args:
            endpoint: API endpoint path (without leading slash)
            
        Returns:
            Complete URL for the endpoint
        """
        return f"{self.base_url}/api/v1/{endpoint}"
    
    async def get_latest_announcement(self, course_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch the latest announcement for a specific course.
        
        Args:
            course_id: Canvas course ID
            
        Returns:
            Latest announcement object or None if not found
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url("announcements")
        
        # Parameters for the latest announcement
        params = {
            "context_codes[]": f"course_{course_id}",
            "active_only": "true",
            "per_page": "1",
            "page": "1"
        }
        
        try:
            logger.info(f"Fetching latest announcement for course {course_id}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            announcements = response.json()
            
            if announcements and len(announcements) > 0:
                logger.info(f"Found announcement: {announcements[0].get('title', 'Untitled')}")
                return announcements[0]
            
            logger.warning(f"No announcements found for course {course_id}")
            return None
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching announcement: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching latest announcement: {e}")
            raise Exception(f"Failed to fetch announcement: {e}")
    
    async def get_courses(self) -> List[Dict[str, Any]]:
        """
        Fetch all courses for the authenticated user.
        
        Returns:
            List of course objects
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url("courses")
        
        params = {
            "enrollment_state": "active",
            "per_page": "100"
        }
        
        try:
            logger.info("Fetching user courses")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            courses = response.json()
            logger.info(f"Found {len(courses)} courses")
            
            return courses
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching courses: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching courses: {e}")
            raise Exception(f"Failed to fetch courses: {e}")
    
    async def get_course_modules(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Fetch all modules for a specific course.
        
        Args:
            course_id: Canvas course ID
            
        Returns:
            List of module objects
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url(f"courses/{course_id}/modules")
        
        params = {
            "include[]": ["items"],
            "per_page": "100"
        }
        
        try:
            logger.info(f"Fetching modules for course {course_id}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            modules = response.json()
            logger.info(f"Found {len(modules)} modules")
            
            return modules
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching modules: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching course modules: {e}")
            raise Exception(f"Failed to fetch course modules: {e}")
    
    async def get_module_items(self, course_id: int, module_id: int) -> List[Dict[str, Any]]:
        """
        Fetch all items for a specific module.
        
        Args:
            course_id: Canvas course ID
            module_id: Canvas module ID
            
        Returns:
            List of module item objects
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url(f"courses/{course_id}/modules/{module_id}/items")
        
        params = {
            "include[]": ["content_details", "mastery_paths"],
            "per_page": "100"
        }
        
        try:
            logger.info(f"Fetching items for module {module_id} in course {course_id}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            items = response.json()
            logger.info(f"Found {len(items)} module items")
            
            return items
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching module items: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching module items: {e}")
            raise Exception(f"Failed to fetch module items: {e}")
    
    async def get_calendar_events(self, start_date: datetime, end_date: datetime, 
                                  course_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """
        Fetch calendar events (assignments) within a date range.
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            course_ids: Optional list of course IDs to filter by
            
        Returns:
            List of calendar event objects
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url("calendar_events")
        
        params = {
            "type": "assignment",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "per_page": "100"
        }
        
        # Add course context codes if specified
        if course_ids:
            params["context_codes[]"] = [f"course_{cid}" for cid in course_ids]
        
        try:
            logger.info(f"Fetching calendar events from {start_date} to {end_date}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            events = response.json()
            logger.info(f"Found {len(events)} calendar events")
            
            return events
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching calendar events: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching calendar events: {e}")
            raise Exception(f"Failed to fetch calendar events: {e}")
    
    async def get_page_content(self, course_id: int, page_url: str) -> Dict[str, Any]:
        """
        Fetch content for a specific page.
        
        Args:
            course_id: Canvas course ID
            page_url: Page URL slug
            
        Returns:
            Page object with content
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url(f"courses/{course_id}/pages/{page_url}")
        
        try:
            logger.info(f"Fetching page content for {page_url} in course {course_id}")
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            page = response.json()
            logger.info(f"Retrieved page: {page.get('title', 'Untitled')}")
            
            return page
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching page: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching page content: {e}")
            raise Exception(f"Failed to fetch page content: {e}")
    
    async def mark_item_done(self, course_id: int, module_id: int, item_id: int) -> bool:
        """
        Mark a module item as done.
        
        Args:
            course_id: Canvas course ID
            module_id: Canvas module ID
            item_id: Canvas module item ID
            
        Returns:
            True if successful
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url(f"courses/{course_id}/modules/{module_id}/items/{item_id}/done")
        
        try:
            logger.info(f"Marking item {item_id} as done")
            
            response = await self.client.put(url)
            response.raise_for_status()
            
            logger.info(f"Successfully marked item {item_id} as done")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error marking item done: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error marking item done: {e}")
            raise Exception(f"Failed to mark item done: {e}")
    
    async def mark_item_read(self, course_id: int, module_id: int, item_id: int) -> bool:
        """
        Mark a module item as read.
        
        Args:
            course_id: Canvas course ID
            module_id: Canvas module ID
            item_id: Canvas module item ID
            
        Returns:
            True if successful
            
        Raises:
            Exception: If API call fails
        """
        
        url = self._build_url(f"courses/{course_id}/modules/{module_id}/items/{item_id}/mark_read")
        
        try:
            logger.info(f"Marking item {item_id} as read")
            
            response = await self.client.post(url)
            response.raise_for_status()
            
            logger.info(f"Successfully marked item {item_id} as read")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error marking item read: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error marking item read: {e}")
            raise Exception(f"Failed to mark item read: {e}")
    
    def get_current_week_dates(self) -> Dict[str, str]:
        """
        Get current week date range for Canvas API queries.
        
        Returns:
            Dictionary with start and end dates
        """
        
        today = datetime.now()
        # Get Monday of current week
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        week_end = week_start + timedelta(days=6)
        
        return {
            "start_date": week_start.strftime("%Y-%m-%d"),
            "end_date": week_end.strftime("%Y-%m-%d")
        }
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the Canvas client connection and configuration.
        
        Returns:
            Test result dictionary
        """
        try:
            # Check configuration
            config_status = {
                "base_url": self.base_url,
                "bearer_token_configured": bool(self.bearer_token),
                "headers_configured": bool(self.headers),
                "client_initialized": self.client is not None
            }
            
            return {
                "status": "success",
                "message": "Canvas client is properly configured",
                "configuration": config_status
            }
            
        except Exception as e:
            logger.error(f"Canvas client test failed: {e}")
            return {
                "status": "error",
                "message": f"Canvas client test failed: {e}"
            }
    
    def get_test_urls(self) -> Dict[str, Any]:
        """
        Get test URLs for Canvas API endpoints.
        
        Returns:
            Dictionary with test URLs
        """
        try:
            # Test course IDs from the project brief
            course_id = 20564  # Course from project brief
            module_id = 253389  # Example module ID
            item_id = 2567723   # Example item ID
            
            urls = {
                "get_announcements": self._build_url("announcements"),
                "get_courses": self._build_url("courses"),
                "get_course_modules": self._build_url(f"courses/{course_id}/modules"),
                "get_module_items": self._build_url(f"courses/{course_id}/modules/{module_id}/items"),
                "get_calendar_events": self._build_url("calendar_events"),
                "get_page_content": self._build_url(f"courses/{course_id}/pages/example-page"),
                "mark_item_done": self._build_url(f"courses/{course_id}/modules/{module_id}/items/{item_id}/done"),
                "mark_item_read": self._build_url(f"courses/{course_id}/modules/{module_id}/items/{item_id}/mark_read")
            }
            
            return {
                "status": "success",
                "base_url": self.base_url,
                "urls": urls
            }
            
        except Exception as e:
            logger.error(f"Failed to generate test URLs: {e}")
            return {
                "status": "error",
                "message": f"Failed to generate test URLs: {e}"
            }
    
    async def get_course_modules(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get all modules for a course.
        
        Args:
            course_id: Canvas course ID
            
        Returns:
            List of module objects
            
        Raises:
            Exception: If API call fails
        """
        url = self._build_url(f"courses/{course_id}/modules")
        
        params = {
            "per_page": "100",
            "include[]": ["items"]
        }
        
        try:
            logger.info(f"Fetching modules for course {course_id}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            modules = response.json()
            logger.info(f"Found {len(modules)} modules")
            
            return modules
            
        except Exception as e:
            logger.error(f"Failed to fetch modules for course {course_id}: {e}")
            raise Exception(f"Canvas modules API error: {e}")
    
    async def get_module_items(self, course_id: int, module_id: int) -> List[Dict[str, Any]]:
        """
        Get all items (lessons) in a specific module.
        
        Args:
            course_id: Canvas course ID
            module_id: Canvas module ID
            
        Returns:
            List of module item objects with html_url for each lesson
            
        Raises:
            Exception: If API call fails
        """
        url = self._build_url(f"courses/{course_id}/modules/{module_id}/items")
        
        params = {
            "per_page": "50"
        }
        
        try:
            logger.info(f"Fetching items for module {module_id} in course {course_id}")
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            items = response.json()
            logger.info(f"Found {len(items)} items in module {module_id}")
            
            return items
            
        except Exception as e:
            logger.error(f"Failed to fetch items for module {module_id}: {e}")
            raise Exception(f"Canvas module items API error: {e}")
    
    async def get_weekly_assignments(self, start_date: str, end_date: str, course_ids: List[int]) -> List[Dict[str, Any]]:
        """
        Get assignments for the current week across multiple courses.
        
        Args:
            start_date: Start date in format 'YYYY-MM-DD' (Monday of current week)
            end_date: End date in format 'YYYY-MM-DD' (Sunday of current week)
            course_ids: List of course IDs to fetch assignments from
            
        Returns:
            List of assignment objects from calendar events
            
        Raises:
            Exception: If API call fails
        """
        all_assignments = []
        
        for course_id in course_ids:
            url = self._build_url("calendar_events")
            
            params = {
                "start_date": start_date,
                "end_date": end_date,
                "type": "assignment",
                "context_codes[]": f"course_{course_id}",
                "per_page": "50"
            }
            
            try:
                logger.info(f"Fetching weekly assignments for course {course_id} from {start_date} to {end_date}")
                
                response = await self.client.get(url, params=params)
                response.raise_for_status()
                
                assignments = response.json()
                
                # Add course_id to each assignment for reference
                for assignment in assignments:
                    assignment['course_id'] = course_id
                    
                all_assignments.extend(assignments)
                logger.info(f"Found {len(assignments)} assignments for course {course_id}")
                
            except Exception as e:
                logger.error(f"Failed to fetch assignments for course {course_id}: {e}")
                # Continue with other courses even if one fails
                continue
        
        logger.info(f"Total assignments fetched: {len(all_assignments)}")
        return all_assignments
    
    async def close(self):
        """Close the HTTP client connection."""
        if self.client:
            await self.client.aclose()
            logger.info("Canvas client connection closed")

    async def get_module_item_content(self, course_id: int, module_item_id: int) -> dict:
        """
        Get the content of a specific module item (lesson).
        
        Args:
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            
        Returns:
            Dict containing the module item content and metadata
        """
        try:
            logger.info(f"Fetching content for module item {module_item_id} in course {course_id}")
            
            # First get the module item details to understand its type
            item_url = f"{self.base_url}/api/v1/courses/{course_id}/modules/items/{module_item_id}"
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.bearer_token}"}
                
                # Get module item metadata
                response = await client.get(item_url, headers=headers)
                response.raise_for_status()
                module_item = response.json()
                
                content_result = {
                    "item_id": module_item_id,
                    "title": module_item.get("title", ""),
                    "type": module_item.get("type", ""),
                    "html_url": module_item.get("html_url", ""),
                    "content_id": module_item.get("content_id"),
                    "url": module_item.get("url"),
                    "content": None,
                    "body": None
                }
                
                # Handle different types of content
                if module_item.get("type") == "Page":
                    # Fetch page content
                    page_url = module_item.get("page_url")
                    if page_url:
                        page_content_url = f"{self.base_url}/api/v1/courses/{course_id}/pages/{page_url}"
                        page_response = await client.get(page_content_url, headers=headers)
                        page_response.raise_for_status()
                        page_data = page_response.json()
                        content_result["content"] = page_data.get("body", "")
                        content_result["body"] = page_data.get("body", "")
                        
                elif module_item.get("type") == "Assignment":
                    # Fetch assignment details
                    assignment_id = module_item.get("content_id")
                    if assignment_id:
                        assignment_url = f"{self.base_url}/api/v1/courses/{course_id}/assignments/{assignment_id}"
                        assignment_response = await client.get(assignment_url, headers=headers)
                        assignment_response.raise_for_status()
                        assignment_data = assignment_response.json()
                        content_result["content"] = assignment_data.get("description", "")
                        content_result["body"] = assignment_data.get("description", "")
                        content_result["due_date"] = assignment_data.get("due_at")
                        content_result["points_possible"] = assignment_data.get("points_possible")
                        
                elif module_item.get("type") == "Discussion":
                    # Fetch discussion topic
                    discussion_id = module_item.get("content_id")
                    if discussion_id:
                        discussion_url = f"{self.base_url}/api/v1/courses/{course_id}/discussion_topics/{discussion_id}"
                        discussion_response = await client.get(discussion_url, headers=headers)
                        discussion_response.raise_for_status()
                        discussion_data = discussion_response.json()
                        content_result["content"] = discussion_data.get("message", "")
                        content_result["body"] = discussion_data.get("message", "")
                        
                elif module_item.get("type") == "ExternalUrl":
                    # External URL - just provide the URL
                    content_result["content"] = f"External link: {module_item.get('external_url', '')}"
                    content_result["external_url"] = module_item.get("external_url", "")
                    
                elif module_item.get("type") == "File":
                    # File - provide download information
                    file_id = module_item.get("content_id")
                    if file_id:
                        file_url = f"{self.base_url}/api/v1/courses/{course_id}/files/{file_id}"
                        file_response = await client.get(file_url, headers=headers)
                        file_response.raise_for_status()
                        file_data = file_response.json()
                        content_result["content"] = f"File: {file_data.get('display_name', '')} ({file_data.get('content-type', '')})"
                        content_result["file_url"] = file_data.get("url", "")
                        content_result["filename"] = file_data.get("display_name", "")
                        content_result["size"] = file_data.get("size", 0)
                        
                else:
                    # Generic content - try to fetch from URL if available
                    item_url = module_item.get("url")
                    if item_url:
                        try:
                            item_response = await client.get(item_url, headers=headers)
                            item_response.raise_for_status()
                            item_data = item_response.json()
                            content_result["content"] = str(item_data)
                        except Exception as e:
                            logger.warning(f"Could not fetch generic content for item {module_item_id}: {e}")
                            content_result["content"] = f"Content type '{module_item.get('type')}' not directly viewable."
                
                logger.info(f"Successfully fetched content for module item {module_item_id}")
                return content_result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching module item content {module_item_id}: {e}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching module item content {module_item_id}: {e}")
            raise Exception(f"Failed to fetch lesson content: {e}")

    async def get_course_pages(self, course_id: int) -> list:
        """
        Get all pages for a course.
        
        Args:
            course_id: Canvas course ID
            
        Returns:
            List of page objects
        """
        try:
            logger.info(f"Fetching pages for course {course_id}")
            
            url = f"{self.base_url}/api/v1/courses/{course_id}/pages"
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.bearer_token}"}
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                pages = response.json()
                logger.info(f"Found {len(pages)} pages for course {course_id}")
                return pages
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching course pages: {e}")
            raise Exception(f"Canvas API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error fetching course pages: {e}")
            raise Exception(f"Failed to fetch course pages: {e}")

    async def mark_lesson_complete(self, course_id: int, module_item_id: int, completed: bool = True) -> dict:
        """
        Mark a module item (lesson) as complete or incomplete in Canvas.
        
        Args:
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            completed: Whether to mark as completed
            
        Returns:
            Dict containing the completion status and response
        """
        try:
            logger.info(f"Marking lesson {module_item_id} as {'complete' if completed else 'incomplete'} in Canvas")
            
            # Canvas API endpoint for module item completion
            url = f"{self.base_url}/api/v1/courses/{course_id}/modules/items/{module_item_id}/done"
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.bearer_token}"}
                
                if completed:
                    # PUT request to mark as done
                    response = await client.put(url, headers=headers)
                else:
                    # DELETE request to mark as not done
                    response = await client.delete(url, headers=headers)
                
                response.raise_for_status()
                
                logger.info(f"Successfully marked lesson {module_item_id} as {'complete' if completed else 'incomplete'}")
                
                return {
                    "success": True,
                    "module_item_id": module_item_id,
                    "completed": completed,
                    "canvas_response": response.status_code
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error marking lesson completion: {e}")
            return {
                "success": False,
                "error": f"Canvas API error: {e.response.status_code}",
                "module_item_id": module_item_id,
                "completed": completed
            }
        except Exception as e:
            logger.error(f"Error marking lesson completion: {e}")
            return {
                "success": False,
                "error": str(e),
                "module_item_id": module_item_id,
                "completed": completed
            }

    async def get_lesson_completion_status(self, course_id: int, module_item_id: int) -> dict:
        """
        Get the completion status of a specific lesson from Canvas.
        
        Args:
            course_id: Canvas course ID
            module_item_id: Canvas module item ID
            
        Returns:
            Dict containing completion status information
        """
        try:
            logger.info(f"Getting completion status for lesson {module_item_id}")
            
            # Get module item details which includes completion info
            url = f"{self.base_url}/api/v1/courses/{course_id}/modules/items/{module_item_id}"
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.bearer_token}"}
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                module_item = response.json()
                
                # Check completion requirements and status
                completion_requirement = module_item.get("completion_requirement", {})
                completed = module_item.get("completed", False)
                
                return {
                    "success": True,
                    "module_item_id": module_item_id,
                    "completed": completed,
                    "completion_requirement": completion_requirement.get("type"),
                    "title": module_item.get("title", ""),
                    "type": module_item.get("type", "")
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting completion status: {e}")
            return {
                "success": False,
                "error": f"Canvas API error: {e.response.status_code}",
                "module_item_id": module_item_id
            }
        except Exception as e:
            logger.error(f"Error getting completion status: {e}")
            return {
                "success": False,
                "error": str(e),
                "module_item_id": module_item_id
            }

    async def mark_assignment_complete(self, course_id: int, assignment_id: int, user_id: int = None) -> dict:
        """
        Submit or mark an assignment as complete in Canvas.
        
        Args:
            course_id: Canvas course ID
            assignment_id: Canvas assignment ID
            user_id: User ID (optional, defaults to current user)
            
        Returns:
            Dict containing submission status
        """
        try:
            logger.info(f"Marking assignment {assignment_id} as complete")
            
            # For assignments, we typically need to create a submission
            url = f"{self.base_url}/api/v1/courses/{course_id}/assignments/{assignment_id}/submissions"
            
            # Basic submission data
            submission_data = {
                "submission": {
                    "submission_type": "online_text_entry",
                    "body": "Completed via ZSchool interface"
                }
            }
            
            if user_id:
                submission_data["submission"]["user_id"] = user_id
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.bearer_token}",
                    "Content-Type": "application/json"
                }
                response = await client.post(url, headers=headers, json=submission_data)
                response.raise_for_status()
                
                submission = response.json()
                
                logger.info(f"Successfully submitted assignment {assignment_id}")
                
                return {
                    "success": True,
                    "assignment_id": assignment_id,
                    "submission_id": submission.get("id"),
                    "submitted_at": submission.get("submitted_at"),
                    "workflow_state": submission.get("workflow_state")
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error submitting assignment: {e}")
            return {
                "success": False,
                "error": f"Canvas API error: {e.response.status_code}",
                "assignment_id": assignment_id
            }
        except Exception as e:
            logger.error(f"Error submitting assignment: {e}")
            return {
                "success": False,
                "error": str(e),
                "assignment_id": assignment_id
            }

    async def get_user_progress(self, course_id: int, user_id: int = None) -> dict:
        """
        Get user progress for a course, including module completion.
        
        Args:
            course_id: Canvas course ID
            user_id: User ID (optional, defaults to current user)
            
        Returns:
            Dict containing user progress information
        """
        try:
            logger.info(f"Getting user progress for course {course_id}")
            
            # Get course progress
            if user_id:
                url = f"{self.base_url}/api/v1/courses/{course_id}/users/{user_id}/progress"
            else:
                url = f"{self.base_url}/api/v1/courses/{course_id}/users/self/progress"
            
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.bearer_token}"}
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                progress_data = response.json()
                
                logger.info(f"Successfully retrieved user progress for course {course_id}")
                
                return {
                    "success": True,
                    "course_id": course_id,
                    "progress": progress_data
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting user progress: {e}")
            return {
                "success": False,
                "error": f"Canvas API error: {e.response.status_code}",
                "course_id": course_id
            }
        except Exception as e:
            logger.error(f"Error getting user progress: {e}")
            return {
                "success": False,
                "error": str(e),
                "course_id": course_id
            }


# Singleton instance for use throughout the application
canvas_client = CanvasClient() 