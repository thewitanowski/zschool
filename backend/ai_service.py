import os
import json
import logging
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    """
    AI service for processing Canvas LMS data using Grok model via X.AI.
    Handles announcement parsing and content transformation.
    """
    
    def __init__(self):
        self.xai_token = os.getenv("XAI_TOKEN")
        
        if not self.xai_token:
            raise ValueError("XAI_TOKEN environment variable is required")
        
        # Initialize OpenAI client with X.AI endpoint
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=self.xai_token,
        )
        
        self.model = "grok-3-mini"
        
    def parse_announcement_to_json(self, html_content: str, target_json_structure: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse Canvas announcement HTML into structured JSON using Kimi K2 model.
        
        Args:
            html_content: Raw HTML content from Canvas announcement
            target_json_structure: Optional JSON structure template
            
        Returns:
            Structured JSON object with parsed announcement data
            
        Raises:
            Exception: If AI parsing fails or returns invalid JSON
        """
        
        if not target_json_structure:
            target_json_structure = self._get_default_json_structure()
        
        system_prompt = """
        You are a highly accurate data extraction engine. Your task is to parse the provided HTML from a Canvas LMS announcement and convert it into a valid JSON object that strictly follows the user-provided format.
        
        CRITICAL INSTRUCTIONS:
        - Extract the start date from the title (e.g., "Week starting Monday 28 July" -> "2025-07-28")
        - Extract all lesson numbers into lists of strings (e.g., "Lessons 1-5" -> ["1", "2", "3", "4", "5"])
        - Extract the teacher's name and role from the signature at the end
        - Infer the days of the week for each subject if they are mentioned in parentheses
        - Accurately categorize all other information into the respective keys like 'announcements', 'assessment_and_quizzes', etc.
        - If a value is not found, use an empty string "" or an empty list []
        - For lesson ranges like "11-15", expand them to individual numbers: ["11", "12", "13", "14", "15"]
        - For lesson codes like "B1 to B5", expand them to: ["B1", "B2", "B3", "B4", "B5"]
        - Extract important dates and convert them to ISO format where possible
        - Return ONLY the JSON object and nothing else
        
        LESSON PARSING RULES:
        - "Lessons 1-5" becomes ["1", "2", "3", "4", "5"]
        - "All lesson pages listed as B1 to B5" becomes ["B1", "B2", "B3", "B4", "B5"]
        - "Lessons 11-15" becomes ["11", "12", "13", "14", "15"]
        - "Unit 3 Lessons 1-4" becomes ["1", "2", "3", "4"]
        
        DAYS PARSING RULES:
        - "(Mon, Tue, Thur, Fri)" becomes ["Monday", "Tuesday", "Thursday", "Friday"]
        - "(Wed)" becomes ["Wednesday"]
        - If no days mentioned, leave as empty array []
        """
        
        user_prompt = f"""
        **TARGET JSON FORMAT:**
        ```json
        {target_json_structure}
        ```

        **HTML CONTENT TO PARSE:**
        ```html
        {html_content}
        ```
        """
        
        try:
            logger.info("Sending request to Kimi K2 model for announcement parsing")
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,  # Maximum predictability for data extraction
                response_format={"type": "json_object"},
            )
            
            response_content = completion.choices[0].message.content
            logger.info(f"AI response content: {response_content}")
            logger.info(f"AI response length: {len(response_content) if response_content else 0}")
            
            if not response_content or response_content.strip() == "":
                logger.error("AI returned empty response")
                raise Exception("AI returned empty response")
            
            # Clean the response - remove markdown code blocks if present
            cleaned_content = response_content.strip()
            if cleaned_content.startswith("```json"):
                cleaned_content = cleaned_content[7:]  # Remove ```json
            if cleaned_content.startswith("```"):
                cleaned_content = cleaned_content[3:]   # Remove ```
            if cleaned_content.endswith("```"):
                cleaned_content = cleaned_content[:-3]  # Remove closing ```
            cleaned_content = cleaned_content.strip()
            
            logger.info(f"Cleaned AI response (first 200 chars): {cleaned_content[:200]}")
            
            # Parse and validate JSON
            parsed_json = json.loads(cleaned_content)
            
            # Validate required fields
            self._validate_parsed_json(parsed_json)
            
            logger.info("Successfully parsed announcement to JSON")
            return parsed_json
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            raise Exception(f"AI returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            raise Exception(f"Failed to parse announcement: {e}")
    
    def _get_default_json_structure(self) -> str:
        """
        Get the default JSON structure template for Canvas announcements.
        
        Returns:
            JSON structure string template
        """
        return json.dumps({
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
        }, indent=2)
    
    def _validate_parsed_json(self, parsed_json: Dict[str, Any]) -> None:
        """
        Validate that the parsed JSON contains required fields.
        
        Args:
            parsed_json: The parsed JSON object to validate
            
        Raises:
            Exception: If validation fails
        """
        required_fields = ["week_starting", "title", "teacher", "classwork"]
        
        for field in required_fields:
            if field not in parsed_json:
                raise Exception(f"Missing required field: {field}")
        
        # Validate teacher structure
        if not isinstance(parsed_json["teacher"], dict):
            raise Exception("Teacher field must be an object")
        
        teacher_fields = ["name", "role"]
        for field in teacher_fields:
            if field not in parsed_json["teacher"]:
                raise Exception(f"Missing teacher field: {field}")
        
        # Validate classwork structure
        if not isinstance(parsed_json["classwork"], list):
            raise Exception("Classwork field must be an array")
        
        for i, work in enumerate(parsed_json["classwork"]):
            if not isinstance(work, dict):
                raise Exception(f"Classwork item {i} must be an object")
            
            work_fields = ["subject", "unit", "topic", "lessons", "days", "notes"]
            for field in work_fields:
                if field not in work:
                    raise Exception(f"Missing classwork field: {field} in item {i}")
        
        logger.debug("JSON validation passed")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the AI service connection and functionality.
        
        Returns:
            Test result dictionary
        """
        try:
            # Simple test request
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Return a JSON object with a 'status' field set to 'success' and a 'message' field set to 'AI service is working'."}
                ],
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            
            response_content = completion.choices[0].message.content
            result = json.loads(response_content)
            
            return {
                "status": "success",
                "message": "AI service connection test passed",
                "model": self.model,
                "test_response": result
            }
            
        except Exception as e:
            logger.error(f"AI service test failed: {e}")
            return {
                "status": "error",
                "message": f"AI service test failed: {e}",
                "model": self.model
            }

    async def transform_lesson_content(self, raw_html: str, lesson_title: str = "", lesson_type: str = "") -> dict:
        """
        Transform raw HTML lesson content into clean, structured, readable format.
        
        Args:
            raw_html: Raw HTML content from Canvas
            lesson_title: Title of the lesson
            lesson_type: Type of content (Page, Assignment, Discussion, etc.)
            
        Returns:
            Dict with transformed content including structured sections
        """
        try:
            logger.info(f"Transforming lesson content: '{lesson_title}' (type: {lesson_type})")
            
            if not raw_html or not raw_html.strip():
                return {
                    "success": False,
                    "error": "No content provided",
                    "content": {
                        "title": lesson_title,
                        "type": lesson_type,
                        "sections": [],
                        "summary": "No content available."
                    }
                }
            
            # Prepare the transformation prompt
            system_prompt = """You are an expert educational content formatter. Transform the provided HTML content into a clean, structured, student-friendly format.

Your task:
1. Parse the HTML content and extract the meaningful text and structure
2. Organize the content into logical sections with clear headings
3. Format the content for optimal readability and learning
4. Preserve important links, images, and embedded media references
5. Create a brief summary of the lesson content

Return your response as a JSON object with this structure:
{
  "title": "Clean lesson title",
  "type": "content type",
  "summary": "Brief 2-3 sentence summary of the lesson",
  "learning_objectives": ["objective 1", "objective 2"],
  "sections": [
    {
      "heading": "Section Title",
      "content": "Clean formatted content",
      "type": "text|list|image|video|link|code"
    }
  ],
  "resources": [
    {
      "title": "Resource name",
      "url": "resource URL",
      "type": "link|file|video"
    }
  ],
  "key_points": ["important point 1", "important point 2"],
  "estimated_time": "5-10 minutes"
}

Guidelines:
- Remove unnecessary HTML formatting but preserve structure
- Convert complex nested HTML into simple, readable text
- Extract and organize any lists, steps, or procedures
- Identify and format code snippets appropriately
- Note any embedded videos, images, or external links
- Make the content scannable with clear headings
- Focus on educational value and student comprehension"""
            
            user_prompt = f"""
Transform this Canvas lesson content:

Title: {lesson_title}
Type: {lesson_type}

HTML Content:
{raw_html[:8000]}  # Limit content to avoid token limits

Please transform this into a clean, student-friendly format following the JSON structure specified."""

            # Make API call to Hugging Face
            response = await self._make_api_call(system_prompt, user_prompt)
            
            # Parse the response
            try:
                parsed_content = json.loads(response)
                
                # Validate the response structure
                if not isinstance(parsed_content, dict):
                    raise ValueError("Response is not a valid JSON object")
                
                # Ensure required fields exist
                required_fields = ["title", "summary", "sections"]
                for field in required_fields:
                    if field not in parsed_content:
                        parsed_content[field] = ""
                
                # Ensure sections is a list
                if not isinstance(parsed_content.get("sections", []), list):
                    parsed_content["sections"] = []
                
                # Set defaults for optional fields
                parsed_content.setdefault("type", lesson_type)
                parsed_content.setdefault("learning_objectives", [])
                parsed_content.setdefault("resources", [])
                parsed_content.setdefault("key_points", [])
                parsed_content.setdefault("estimated_time", "5-10 minutes")
                
                logger.info(f"Successfully transformed lesson content: '{lesson_title}'")
                
                return {
                    "success": True,
                    "content": parsed_content,
                    "raw_html": raw_html[:1000]  # Store truncated raw HTML for reference
                }
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                logger.error(f"Raw response: {response[:500]}...")
                
                # Fallback: create basic structured content from raw HTML
                fallback_content = self._create_fallback_content(raw_html, lesson_title, lesson_type)
                
                return {
                    "success": False,
                    "error": f"AI response parsing failed: {e}",
                    "content": fallback_content,
                    "raw_response": response[:500]
                }
                
        except Exception as e:
            logger.error(f"Error transforming lesson content: {e}")
            
            # Create fallback content
            fallback_content = self._create_fallback_content(raw_html, lesson_title, lesson_type)
            
            return {
                "success": False,
                "error": str(e),
                "content": fallback_content
            }

    def _create_fallback_content(self, raw_html: str, title: str, content_type: str) -> dict:
        """
        Create a fallback structured content when AI transformation fails.
        
        Args:
            raw_html: Raw HTML content
            title: Lesson title
            content_type: Type of content
            
        Returns:
            Basic structured content dict
        """
        try:
            # Simple HTML-to-text conversion
            import re
            
            # Remove HTML tags but preserve some structure
            text = re.sub(r'<script[^>]*>.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
            
            # Convert common HTML elements to text
            text = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\n## \1\n', text)
            text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text)
            text = re.sub(r'<br[^>]*>', '\n', text)
            text = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1\n', text)
            text = re.sub(r'<[^>]+>', '', text)  # Remove remaining HTML tags
            
            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)
            text = text.strip()
            
            # Truncate if too long
            if len(text) > 2000:
                text = text[:2000] + "... (content truncated)"
            
            return {
                "title": title or "Lesson Content",
                "type": content_type,
                "summary": f"Content from {content_type}: {title}" if title else f"{content_type} content",
                "sections": [
                    {
                        "heading": "Content",
                        "content": text or "No readable content available.",
                        "type": "text"
                    }
                ],
                "learning_objectives": [],
                "resources": [],
                "key_points": [],
                "estimated_time": "5-10 minutes"
            }
            
        except Exception as e:
            logger.error(f"Error creating fallback content: {e}")
            return {
                "title": title or "Lesson Content",
                "type": content_type,
                "summary": "Content could not be processed.",
                "sections": [
                    {
                        "heading": "Raw Content",
                        "content": "Content is not available in a readable format.",
                        "type": "text"
                    }
                ],
                "learning_objectives": [],
                "resources": [],
                "key_points": [],
                "estimated_time": "Unknown"
            }

# Singleton instance for use throughout the application
ai_service = AIService() 