from typing import Dict, List, Any, Optional
import asyncio
from loguru import logger
from canvas_client import CanvasClient


class CanvasModuleService:
    """
    Service for fetching and mapping Canvas module items to lesson data.
    """
    
    def __init__(self, canvas_client: CanvasClient):
        self.canvas_client = canvas_client
        self._module_cache: Dict[int, List[Dict]] = {}
        self._lesson_url_cache: Dict[str, str] = {}
    
    async def get_lesson_urls_for_subjects(self, course_id: int, subjects_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Get Canvas URLs for all lessons across subjects.
        
        Args:
            course_id: Canvas course ID
            subjects_data: List of subject data from AI parsing (classwork)
            
        Returns:
            Dict mapping lesson keys to Canvas URLs
            Example: {
                "maths_b1": "https://learning.acc.edu.au/courses/20564/modules/items/123",
                "english_1": "https://learning.acc.edu.au/courses/20564/modules/items/456"
            }
        """
        lesson_urls = {}
        
        try:
            # Get all modules for the course
            modules = await self.canvas_client.get_course_modules(course_id)
            logger.info(f"Found {len(modules)} modules for course {course_id}")
            
            # Process each subject to find matching modules
            for subject_data in subjects_data:
                subject_name = subject_data.get('subject', '').lower()
                lessons = subject_data.get('lessons', [])
                unit = subject_data.get('unit', '').lower()
                topic = subject_data.get('topic', '').lower()
                
                logger.info(f"Processing {subject_name} with {len(lessons)} lessons")
                
                # Find modules that might match this subject
                matching_modules = self._find_matching_modules(modules, subject_name, unit, topic)
                
                for module in matching_modules:
                    module_id = module.get('id')
                    if module_id:
                        # Get items for this module
                        try:
                            items = await self.canvas_client.get_module_items(course_id, module_id)
                            
                            # Map lessons to URLs
                            for lesson in lessons:
                                lesson_key = f"{subject_name.replace(' ', '_')}_{lesson.lower()}"
                                canvas_url = self._find_lesson_url(items, lesson, unit, topic)
                                
                                if canvas_url:
                                    lesson_urls[lesson_key] = canvas_url
                                    logger.info(f"Mapped {lesson_key} → {canvas_url}")
                                else:
                                    # Fallback to module page if specific lesson not found
                                    lesson_urls[lesson_key] = f"https://learning.acc.edu.au/courses/{course_id}/modules/{module_id}"
                                    logger.warning(f"No specific URL found for {lesson_key}, using module page")
                                    
                        except Exception as e:
                            logger.error(f"Failed to get items for module {module_id}: {e}")
                            # Fallback URL
                            for lesson in lessons:
                                lesson_key = f"{subject_name.replace(' ', '_')}_{lesson.lower()}"
                                lesson_urls[lesson_key] = f"https://learning.acc.edu.au/courses/{course_id}/modules"
            
            logger.info(f"Successfully mapped {len(lesson_urls)} lesson URLs")
            return lesson_urls
            
        except Exception as e:
            logger.error(f"Failed to get lesson URLs: {e}")
            # Return empty dict - frontend will use fallback URLs
            return {}
    
    def _find_matching_modules(self, modules: List[Dict], subject_name: str, unit: str, topic: str) -> List[Dict]:
        """
        Find Canvas modules that match the given subject/unit/topic.
        """
        matching = []
        
        # Keywords to look for in module names
        subject_keywords = self._get_subject_keywords(subject_name)
        
        for module in modules:
            module_name = module.get('name', '').lower()
            
            # Check if module name contains subject keywords
            if any(keyword in module_name for keyword in subject_keywords):
                matching.append(module)
                logger.debug(f"Module '{module.get('name')}' matches subject '{subject_name}'")
            
            # Also check unit/topic matching
            elif unit and unit in module_name:
                matching.append(module)
                logger.debug(f"Module '{module.get('name')}' matches unit '{unit}'")
            
            elif topic and topic in module_name:
                matching.append(module)
                logger.debug(f"Module '{module.get('name')}' matches topic '{topic}'")
        
        return matching
    
    def _get_subject_keywords(self, subject_name: str) -> List[str]:
        """
        Get keywords to search for in Canvas module names based on subject.
        """
        subject_lower = subject_name.lower()
        
        keyword_map = {
            'maths': ['math', 'maths', 'mathematics', 'topic', 'unit', 'number', 'algebra', 'geometry'],
            'english': ['english', 'literacy', 'writing', 'reading', 'language', 'comprehension', 'unit'],
            'technology': ['technology', 'tech', 'digital', 'ict', 'computer', 'coding'],
            'health': ['health', 'wellbeing', 'personal development', 'pdhpe'],
            'pe': ['pe', 'physical education', 'sport', 'fitness', 'pdhpe'],
            'spiritual and physical fitness': ['spiritual', 'physical', 'fitness', 'sport', 'pdhpe'],
            'science': ['science', 'biology', 'chemistry', 'physics'],
            'history': ['history', 'hass', 'social studies'],
            'geography': ['geography', 'hass', 'social studies']
        }
        
        # Find matching keywords
        for key, keywords in keyword_map.items():
            if key in subject_lower or subject_lower in key:
                logger.debug(f"📚 Subject '{subject_name}' matched to keywords: {keywords}")
                return keywords + [subject_lower]
        
        # Default: use subject name and common terms
        default_keywords = [subject_lower, 'unit', 'topic', 'lesson']
        logger.debug(f"📚 Subject '{subject_name}' using default keywords: {default_keywords}")
        return default_keywords
    
    def _find_lesson_url(self, items: List[Dict], lesson: str, unit: str, topic: str) -> Optional[str]:
        """
        Find the Canvas URL for a specific lesson within module items.
        """
        lesson_lower = lesson.lower()
        logger.debug(f"🔍 Looking for lesson '{lesson}' in {len(items)} Canvas items")
        
        # Log available items for debugging
        for item in items[:5]:  # Log first 5 items
            logger.debug(f"   Canvas item: '{item.get('title', 'No title')}'")
        
        for item in items:
            title = item.get('title', '').lower()
            html_url = item.get('html_url')
            
            if not html_url:
                continue
            
            # Enhanced matching patterns
            matching_patterns = [
                # Direct lesson number/code match
                lesson_lower,
                # Lesson with spaces
                f"lesson {lesson_lower}",
                f"lesson-{lesson_lower}",
                f"lesson_{lesson_lower}",
                # With unit
                f"unit {unit.lower()} lesson {lesson_lower}" if unit else None,
                f"{unit.lower()} lesson {lesson_lower}" if unit else None,
                f"unit-{unit.lower()}-lesson-{lesson_lower}" if unit else None,
                # With topic  
                f"topic {topic.lower()} lesson {lesson_lower}" if topic else None,
                f"{topic.lower()} lesson {lesson_lower}" if topic else None,
                # Common Canvas patterns
                f"lesson{lesson_lower}",
                f"l{lesson_lower}",
                f" {lesson_lower} ",  # Surrounded by spaces
                f"-{lesson_lower}-",  # Surrounded by dashes
                f"_{lesson_lower}_",  # Surrounded by underscores
                # For lessons like "B1", also try just "1"
                lesson_lower[1:] if lesson_lower.startswith('b') and len(lesson_lower) > 1 else None,
                # For lessons like "1", also try "01"
                f"0{lesson_lower}" if lesson_lower.isdigit() and len(lesson_lower) == 1 else None,
            ]
            
            # Remove None values
            matching_patterns = [p for p in matching_patterns if p]
            
            for pattern in matching_patterns:
                if pattern in title:
                    logger.info(f"✅ Found lesson '{lesson}' → '{item.get('title')}' using pattern '{pattern}'")
                    return html_url
        
        # If no specific match, log the failure
        logger.warning(f"❌ No specific URL found for lesson '{lesson}' in {len(items)} items")
        logger.debug(f"   Available titles: {[item.get('title', 'No title') for item in items[:10]]}")
        
        # Return the first lesson-like item as fallback
        for item in items:
            title = item.get('title', '').lower()
            html_url = item.get('html_url')
            
            if 'lesson' in title and html_url:
                logger.info(f"📋 Using fallback lesson URL for '{lesson}' → '{item.get('title')}'")
                return html_url
        
        return None 