from typing import Dict, List, Any, Optional
import asyncio
from loguru import logger
from canvas_client import CanvasClient


class CanvasModuleService:
    """
    Service for fetching and mapping Canvas module items to lesson data.
    Implements the proper API flow: Announcement → Courses → Modules → Module Items
    """
    
    def __init__(self, canvas_client: CanvasClient):
        self.canvas_client = canvas_client
        self._course_cache: Dict[str, int] = {}  # subject_name -> course_id
        self._module_cache: Dict[int, List[Dict]] = {}  # course_id -> modules
        self._items_cache: Dict[str, List[Dict]] = {}  # "{course_id}_{module_id}" -> items
    
    async def enhance_classwork_with_canvas_data(self, classwork: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance classwork data with proper Canvas URLs and metadata following fixlinksanddata.md flow.
        
        Args:
            classwork: List of subject data from AI parsing (announcement payload)
            
        Returns:
            Enhanced classwork with canvas_urls, completion_status, and lesson_api_urls
        """
        try:
            logger.info("🔄 Starting Canvas data enhancement following fixlinksanddata.md flow")
            
            # Step 1: Get all courses to match subjects to course IDs
            logger.info("📚 Step 1: Fetching all courses for subject matching")
            courses = await self.canvas_client.get_courses()
            course_map = self._build_course_map(courses)
            
            # Step 2: Process each subject in classwork
            enhanced_classwork = []
            
            for subject_data in classwork:
                logger.info(f"🎯 Processing subject: {subject_data.get('subject')}")
                enhanced_subject = await self._enhance_subject_data(subject_data, course_map)
                enhanced_classwork.append(enhanced_subject)
            
            logger.info(f"✅ Canvas data enhancement complete for {len(enhanced_classwork)} subjects")
            return enhanced_classwork
            
        except Exception as e:
            logger.error(f"❌ Failed to enhance classwork with Canvas data: {e}")
            # Return original data with fallback URLs
            return self._add_fallback_urls(classwork)
    
    def _build_course_map(self, courses: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Build a mapping from subject names to course IDs.
        Matches "subject" from announcement to "name" in course payload.
        """
        course_map = {}
        
        logger.info(f"🗺️  Building course map from {len(courses)} courses")
        
        for course in courses:
            course_name = course.get('name', '').strip()
            course_id = course.get('id')
            
            if course_name and course_id:
                # Store exact name match
                course_map[course_name] = course_id
                
                # Also store lowercase version for case-insensitive matching
                course_map[course_name.lower()] = course_id
                
                logger.debug(f"   📋 Mapped course: '{course_name}' → {course_id}")
        
        logger.info(f"📊 Course map built with {len(course_map)} entries")
        return course_map
    
    async def _enhance_subject_data(self, subject_data: Dict[str, Any], course_map: Dict[str, int]) -> Dict[str, Any]:
        """
        Enhance a single subject's data with Canvas URLs and metadata.
        """
        enhanced = subject_data.copy()
        subject_name = subject_data.get('subject', '')
        unit = subject_data.get('unit', '')
        topic = subject_data.get('topic', '')
        lessons = subject_data.get('lessons', [])
        
        # Step 2A: Match subject to course ID
        course_id = self._find_course_id(subject_name, course_map)
        
        if not course_id:
            logger.warning(f"⚠️  No course found for subject '{subject_name}' - using fallback URLs")
            enhanced['canvas_urls'] = {}
            enhanced['completion_status'] = {}
            enhanced['lesson_api_urls'] = {}
            
            # Add fallback URLs for all lessons
            for lesson in lessons:
                enhanced['canvas_urls'][lesson] = "https://learning.acc.edu.au/courses/20564/modules"
                enhanced['completion_status'][lesson] = False  # Default to not completed
                enhanced['lesson_api_urls'][lesson] = f"https://learning.acc.edu.au/api/v1/courses/20564/modules"
            
            return enhanced
        
        logger.info(f"🎯 Found course {course_id} for subject '{subject_name}'")
        
        # Step 2B: Get modules for this course
        modules = await self._get_course_modules(course_id)
        
        # Step 2C: Match unit/topic to module ID
        module_id = self._find_module_id(unit, topic, modules)
        
        if not module_id:
            logger.warning(f"⚠️  No module found for unit '{unit}' or topic '{topic}' in course {course_id}")
            enhanced['canvas_urls'] = {}
            enhanced['completion_status'] = {}
            enhanced['lesson_api_urls'] = {}
            
            # Add fallback URLs for all lessons
            for lesson in lessons:
                enhanced['canvas_urls'][lesson] = f"https://learning.acc.edu.au/courses/{course_id}/modules"
                enhanced['completion_status'][lesson] = False
                enhanced['lesson_api_urls'][lesson] = f"https://learning.acc.edu.au/api/v1/courses/{course_id}/modules"
            
            return enhanced
        
        logger.info(f"🎯 Found module {module_id} for unit '{unit}' / topic '{topic}'")
        
        # Step 2D: Get module items and match lessons
        items = await self._get_module_items(course_id, module_id)
        
        # Step 2E: Match lessons to module items
        lesson_data = self._match_lessons_to_items(lessons, items, course_id, module_id)
        
        # Add the enhanced data
        enhanced['canvas_urls'] = lesson_data['canvas_urls']
        enhanced['completion_status'] = lesson_data['completion_status']
        enhanced['lesson_api_urls'] = lesson_data['lesson_api_urls']
        enhanced['course_id'] = course_id
        enhanced['module_id'] = module_id
        
        return enhanced
    
    def _find_course_id(self, subject_name: str, course_map: Dict[str, int]) -> Optional[int]:
        """
        Find course ID by matching subject name to course name.
        """
        # Define specific subject mappings for cases where simple matching fails
        subject_mappings = {
            "Spiritual and Physical Fitness": "2025 Year 6 Spiritual & Physical Fitness (MPDE)",
            "Health": "2025 Year 6 HPE (MPDE)",  # Health is part of HPE
            "Maths": "2025 Year 6 Maths (MPDE)",
            "Mathematics": "2025 Year 6 Maths (MPDE)",
            "English": "2025 Year 6 English (MPDE)",
            "English Literature": "2025 Year 6 English Literature (MPDE)",
            "PE": "2025 Year 6 HPE (MPDE)",
            "Physical Education": "2025 Year 6 HPE (MPDE)",
            "HPE": "2025 Year 6 HPE (MPDE)",
            "PDHPE": "2025 Year 6 HPE (MPDE)",
            "Science": "2025 Year 6 Science (MPDE)",
            "HASS": "2025 Year 6 HASS (MPDE)",
            "Humanities": "2025 Year 6 HASS (MPDE)",
            "History": "2025 Year 6 HASS (MPDE)",
            "Geography": "2025 Year 6 HASS (MPDE)",
            "Social Studies": "2025 Year 6 HASS (MPDE)",
            "Arts": "2025 Year 6 Arts (MPDE)",
            "Art": "2025 Year 6 Arts (MPDE)",
            "Creative Arts": "2025 Year 6 Arts (MPDE)",
            "Visual Arts": "2025 Year 6 Arts (MPDE)",
            # Common abbreviations and alternatives
            "Lit": "2025 Year 6 English Literature (MPDE)",
            "Literature": "2025 Year 6 English Literature (MPDE)",
            "Math": "2025 Year 6 Maths (MPDE)",
            "Technology": "2025 Year 6 Science (MPDE)",  # Technology often falls under Science
            "Tech": "2025 Year 6 Science (MPDE)",
            # Additional courses that might appear in announcements
            "Communication": "2025 Communication Hub (MPDE)",
            "Communication Hub": "2025 Communication Hub (MPDE)",
            "Orientation": "2025 Primary Orientation Course (MPDE)",
            "Primary Orientation": "2025 Primary Orientation Course (MPDE)",
        }
        
        # Try specific mapping first
        if subject_name in subject_mappings:
            mapped_course_name = subject_mappings[subject_name]
            if mapped_course_name in course_map:
                logger.info(f"🎯 Specific mapping: '{subject_name}' → course '{mapped_course_name}' (ID: {course_map[mapped_course_name]})")
                return course_map[mapped_course_name]
        
        # Try exact match
        if subject_name in course_map:
            return course_map[subject_name]
        
        # Try case-insensitive match
        if subject_name.lower() in course_map:
            return course_map[subject_name.lower()]
        
        # Try partial matching for common variations
        subject_lower = subject_name.lower()
        for course_name, course_id in course_map.items():
            course_lower = course_name.lower()
            
            # Check if subject is contained in course name or vice versa
            if subject_lower in course_lower or course_lower in subject_lower:
                logger.info(f"🔍 Partial match: '{subject_name}' matched to course '{course_name}'")
                return course_id
        
        # Try more flexible matching for subjects like "Maths" -> "Year 6 Maths"
        for course_name, course_id in course_map.items():
            course_lower = course_name.lower()
            
            # Check if the subject appears as a word in the course name
            if f" {subject_lower} " in f" {course_lower} ":
                logger.info(f"🔍 Word match: '{subject_name}' matched to course '{course_name}'")
                return course_id
        
        return None
    
    async def _get_course_modules(self, course_id: int) -> List[Dict[str, Any]]:
        """
        Get modules for a course, with caching.
        """
        if course_id in self._module_cache:
            return self._module_cache[course_id]
        
        try:
            modules = await self.canvas_client.get_course_modules(course_id)
            self._module_cache[course_id] = modules
            logger.info(f"📦 Fetched {len(modules)} modules for course {course_id}")
            return modules
        except Exception as e:
            logger.error(f"❌ Failed to fetch modules for course {course_id}: {e}")
            return []
    
    def _find_module_id(self, unit: str, topic: str, modules: List[Dict[str, Any]]) -> Optional[int]:
        """
        Find module ID by matching unit or topic to module name.
        """
        search_terms = []
        
        if unit:
            search_terms.append(unit.strip())
        if topic:
            search_terms.append(topic.strip())
            
            # Handle topic ranges like "Topic 9 and 10" 
            if " and " in topic.lower():
                # Split topic ranges and extract individual topics
                parts = topic.lower().replace(" and ", ",").split(",")
                for part in parts:
                    part = part.strip()
                    if "topic" in part:
                        search_terms.append(part)
                    elif part.isdigit():
                        search_terms.append(f"topic {part}")
        
        if not search_terms:
            logger.warning("⚠️  No unit or topic to match against modules")
            return None
        
        logger.debug(f"🔍 Searching for terms: {search_terms}")
        
        for module in modules:
            module_name = module.get('name', '')
            module_id = module.get('id')
            
            if not module_name or not module_id:
                continue
            
            # Try exact matches first
            for term in search_terms:
                if term.lower() == module_name.lower():
                    logger.info(f"🎯 Exact match: '{term}' → module '{module_name}' (ID: {module_id})")
                    return module_id
            
            # Try partial matches
            for term in search_terms:
                if term.lower() in module_name.lower() or module_name.lower() in term.lower():
                    logger.info(f"🔍 Partial match: '{term}' → module '{module_name}' (ID: {module_id})")
                    return module_id
            
            # Try topic number matching for cases like "Topic 9 and 10" -> "Topic 9"
            for term in search_terms:
                term_lower = term.lower()
                module_lower = module_name.lower()
                
                # Extract topic numbers from both term and module name
                if "topic" in term_lower and "topic" in module_lower:
                    import re
                    term_numbers = re.findall(r'\btopic\s*(\d+)', term_lower)
                    module_numbers = re.findall(r'\btopic\s*(\d+)', module_lower)
                    
                    if term_numbers and module_numbers:
                        # If term contains a number that matches module number
                        if term_numbers[0] in module_numbers:
                            logger.info(f"🔢 Topic number match: '{term}' (topic {term_numbers[0]}) → module '{module_name}' (topic {module_numbers[0]})")
                            return module_id
        
        logger.warning(f"⚠️  No module found for unit '{unit}' or topic '{topic}'")
        return None
    
    async def _get_module_items(self, course_id: int, module_id: int) -> List[Dict[str, Any]]:
        """
        Get module items, with caching.
        """
        cache_key = f"{course_id}_{module_id}"
        
        if cache_key in self._items_cache:
            return self._items_cache[cache_key]
        
        try:
            items = await self.canvas_client.get_module_items(course_id, module_id)
            self._items_cache[cache_key] = items
            logger.info(f"📝 Fetched {len(items)} items for module {module_id} in course {course_id}")
            return items
        except Exception as e:
            logger.error(f"❌ Failed to fetch items for module {module_id} in course {course_id}: {e}")
            return []
    
    def _match_lessons_to_items(self, lessons: List[str], items: List[Dict[str, Any]], 
                               course_id: int, module_id: int) -> Dict[str, Dict[str, str]]:
        """
        Match lessons from announcement to module items.
        Returns canvas_urls, completion_status, and lesson_api_urls.
        """
        result = {
            'canvas_urls': {},
            'completion_status': {},
            'lesson_api_urls': {}
        }
        
        logger.info(f"🔗 Matching {len(lessons)} lessons to {len(items)} module items")
        
        for lesson in lessons:
            matched_item = self._find_matching_item(lesson, items)
            
            if matched_item:
                # Extract data as specified in fixlinksanddata.md
                html_url = matched_item.get('html_url', '')
                completion_data = matched_item.get('completion_requirement', {})
                completed = completion_data.get('completed', False)
                api_url = matched_item.get('url', '')
                
                result['canvas_urls'][lesson] = html_url
                result['completion_status'][lesson] = completed
                result['lesson_api_urls'][lesson] = api_url
                
                logger.info(f"✅ Matched lesson '{lesson}' → '{matched_item.get('title')}'")
                logger.debug(f"   🔗 Canvas URL: {html_url}")
                logger.debug(f"   ✔️  Completed: {completed}")
                logger.debug(f"   🔌 API URL: {api_url}")
            else:
                # Fallback URLs
                result['canvas_urls'][lesson] = f"https://learning.acc.edu.au/courses/{course_id}/modules/{module_id}"
                result['completion_status'][lesson] = False
                result['lesson_api_urls'][lesson] = f"https://learning.acc.edu.au/api/v1/courses/{course_id}/modules/{module_id}/items"
                
                logger.warning(f"⚠️  No match found for lesson '{lesson}' - using fallback URLs")
        
        return result
    
    def _find_matching_item(self, lesson: str, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Find module item that matches the lesson ID/title.
        """
        lesson_lower = lesson.lower().strip()
        
        # Log available items for debugging
        logger.debug(f"🔍 Looking for lesson '{lesson}' in {len(items)} items:")
        for item in items[:5]:  # Log first 5 for debugging
            logger.debug(f"   📄 Item: '{item.get('title', 'No title')}'")
        
        for item in items:
            title = item.get('title', '').lower().strip()
            
            if not title:
                continue
            
            # Try various matching patterns
            if self._lesson_matches_title(lesson_lower, title):
                return item
        
        return None
    
    def _lesson_matches_title(self, lesson: str, title: str) -> bool:
        """
        Check if a lesson matches a module item title using various patterns.
        """
        # Exact match
        if lesson == title:
            return True
        
        # Common patterns to try
        patterns = [
            lesson,  # Direct match
            f"lesson {lesson}",  # "lesson 1"
            f"lesson-{lesson}",  # "lesson-1"  
            f"lesson_{lesson}",  # "lesson_1"
            f"lesson{lesson}",   # "lesson1"
            f"l{lesson}",        # "l1"
            f" {lesson} ",       # " 1 " (surrounded by spaces)
            f"-{lesson}-",       # "-1-" (surrounded by dashes)
            f"_{lesson}_",       # "_1_" (surrounded by underscores)
        ]
        
        # For lessons like "B1", also try just "1"
        if lesson.startswith('b') and len(lesson) > 1:
            patterns.append(lesson[1:])
        
        # For lessons like "1", also try "01"
        if lesson.isdigit() and len(lesson) == 1:
            patterns.append(f"0{lesson}")
        
        for pattern in patterns:
            if pattern in title:
                logger.debug(f"✅ Pattern match: lesson '{lesson}' matched title '{title}' using pattern '{pattern}'")
                return True
        
        return False
    
    def _add_fallback_urls(self, classwork: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add fallback URLs when Canvas API calls fail.
        """
        enhanced_classwork = []
        
        for subject_data in classwork:
            enhanced = subject_data.copy()
            lessons = subject_data.get('lessons', [])
            
            enhanced['canvas_urls'] = {}
            enhanced['completion_status'] = {}
            enhanced['lesson_api_urls'] = {}
            
            for lesson in lessons:
                enhanced['canvas_urls'][lesson] = "https://learning.acc.edu.au/courses/20564/modules"
                enhanced['completion_status'][lesson] = False
                enhanced['lesson_api_urls'][lesson] = "https://learning.acc.edu.au/api/v1/courses/20564/modules"
            
            enhanced_classwork.append(enhanced)
        
        logger.warning("⚠️  Using fallback URLs for all lessons due to API errors")
        return enhanced_classwork 