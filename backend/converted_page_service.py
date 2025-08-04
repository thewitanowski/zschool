"""
Service for managing AI-converted Canvas page storage and caching.
Handles persistence, retrieval, and cache invalidation.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from models import ConvertedCanvasPage
from ai_service import AIService
import logging

logger = logging.getLogger(__name__)

class ConvertedPageService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def get_content_hash(self, html_content: str) -> str:
        """Generate SHA-256 hash of HTML content for change detection."""
        return hashlib.sha256(html_content.encode('utf-8')).hexdigest()

    def get_converted_page(
        self, 
        db: Session, 
        course_id: int, 
        page_slug: str,
        force_refresh: bool = False
    ) -> Optional[ConvertedCanvasPage]:
        """
        Get a converted page from cache, optionally forcing refresh.
        
        Args:
            db: Database session
            course_id: Canvas course ID
            page_slug: Canvas page slug
            force_refresh: If True, ignore cache and return None
            
        Returns:
            ConvertedCanvasPage if found and valid, None otherwise
        """
        if force_refresh:
            return None
            
        converted_page = db.query(ConvertedCanvasPage).filter(
            ConvertedCanvasPage.course_id == course_id,
            ConvertedCanvasPage.page_slug == page_slug
        ).first()
        
        if converted_page:
            # Update last accessed timestamp
            converted_page.last_accessed_at = datetime.now()
            db.commit()
            logger.info(f"Found cached converted page: {course_id}/{page_slug}")
            
        return converted_page

    def save_converted_page(
        self,
        db: Session,
        course_id: int,
        page_slug: str,
        canvas_data: Dict,
        ai_components: List[Dict],
        processing_info: Dict,
        conversion_time_ms: int,
        raw_html_body: str
    ) -> ConvertedCanvasPage:
        """
        Save or update a converted page in the database.
        
        Args:
            db: Database session
            course_id: Canvas course ID  
            page_slug: Canvas page slug
            canvas_data: Original Canvas page data
            ai_components: AI-converted components
            processing_info: AI processing metadata
            conversion_time_ms: Time taken for conversion
            raw_html_body: Original HTML content
            
        Returns:
            ConvertedCanvasPage: Saved database record
        """
        content_hash = self.get_content_hash(raw_html_body)
        
        # Check if page already exists
        existing_page = db.query(ConvertedCanvasPage).filter(
            ConvertedCanvasPage.course_id == course_id,
            ConvertedCanvasPage.page_slug == page_slug
        ).first()
        
        if existing_page:
            # Update existing record
            existing_page.page_title = canvas_data.get('title', 'Untitled')
            existing_page.page_id = canvas_data.get('page_id')
            existing_page.canvas_url = canvas_data.get('html_url')
            existing_page.raw_html_body = raw_html_body
            existing_page.ai_components = ai_components
            existing_page.processing_info = processing_info
            existing_page.content_hash = content_hash
            existing_page.canvas_updated_at = datetime.fromisoformat(
                canvas_data.get('updated_at', datetime.now().isoformat()).replace('Z', '+00:00')
            ) if canvas_data.get('updated_at') else datetime.now()
            existing_page.last_accessed_at = datetime.now()
            existing_page.conversion_time_ms = conversion_time_ms
            existing_page.component_count = len(ai_components)
            existing_page.conversion_success = True
            existing_page.conversion_error = None
            
            converted_page = existing_page
            logger.info(f"Updated cached converted page: {course_id}/{page_slug}")
        else:
            # Create new record
            converted_page = ConvertedCanvasPage(
                course_id=course_id,
                page_slug=page_slug,
                page_title=canvas_data.get('title', 'Untitled'),
                page_id=canvas_data.get('page_id'),
                canvas_url=canvas_data.get('html_url'),
                raw_html_body=raw_html_body,
                ai_components=ai_components,
                processing_info=processing_info,
                content_hash=content_hash,
                canvas_updated_at=datetime.fromisoformat(
                    canvas_data.get('updated_at', datetime.now().isoformat()).replace('Z', '+00:00')
                ) if canvas_data.get('updated_at') else datetime.now(),
                conversion_time_ms=conversion_time_ms,
                component_count=len(ai_components),
                conversion_success=True
            )
            
            db.add(converted_page)
            logger.info(f"Saved new converted page: {course_id}/{page_slug}")
        
        db.commit()
        db.refresh(converted_page)
        return converted_page

    def save_conversion_error(
        self,
        db: Session,
        course_id: int,
        page_slug: str,
        canvas_data: Dict,
        error_message: str,
        raw_html_body: str
    ) -> ConvertedCanvasPage:
        """
        Save a failed conversion attempt for debugging and fallback.
        
        Args:
            db: Database session
            course_id: Canvas course ID
            page_slug: Canvas page slug  
            canvas_data: Original Canvas page data
            error_message: Error that occurred during conversion
            raw_html_body: Original HTML content
            
        Returns:
            ConvertedCanvasPage: Saved error record
        """
        content_hash = self.get_content_hash(raw_html_body)
        
        # Check if page already exists
        existing_page = db.query(ConvertedCanvasPage).filter(
            ConvertedCanvasPage.course_id == course_id,
            ConvertedCanvasPage.page_slug == page_slug
        ).first()
        
        if existing_page:
            # Update with error info
            existing_page.conversion_success = False
            existing_page.conversion_error = error_message
            existing_page.content_hash = content_hash
            existing_page.last_accessed_at = datetime.now()
            converted_page = existing_page
        else:
            # Create new error record
            converted_page = ConvertedCanvasPage(
                course_id=course_id,
                page_slug=page_slug,
                page_title=canvas_data.get('title', 'Untitled'),
                page_id=canvas_data.get('page_id'),
                canvas_url=canvas_data.get('html_url'),
                raw_html_body=raw_html_body,
                ai_components=[],  # Empty components for failed conversion
                processing_info={'status': 'error', 'message': error_message},
                content_hash=content_hash,
                canvas_updated_at=datetime.fromisoformat(
                    canvas_data.get('updated_at', datetime.now().isoformat()).replace('Z', '+00:00')
                ) if canvas_data.get('updated_at') else datetime.now(),
                conversion_success=False,
                conversion_error=error_message,
                component_count=0
            )
            db.add(converted_page)
        
        db.commit()
        db.refresh(converted_page)
        logger.warning(f"Saved conversion error for {course_id}/{page_slug}: {error_message}")
        return converted_page

    def is_content_changed(
        self, 
        cached_page: ConvertedCanvasPage, 
        current_html: str,
        canvas_updated_at: Optional[str] = None
    ) -> bool:
        """
        Check if the Canvas content has changed since last conversion.
        
        Args:
            cached_page: Existing cached page
            current_html: Current HTML content from Canvas
            canvas_updated_at: Canvas-reported last update time
            
        Returns:
            True if content has changed and needs re-conversion
        """
        # Check content hash
        current_hash = self.get_content_hash(current_html)
        if cached_page.content_hash != current_hash:
            logger.info(f"Content hash changed for {cached_page.course_id}/{cached_page.page_slug}")
            return True
            
        # Check Canvas updated timestamp if available
        if canvas_updated_at and cached_page.canvas_updated_at:
            try:
                current_updated = datetime.fromisoformat(
                    canvas_updated_at.replace('Z', '+00:00')
                )
                if current_updated > cached_page.canvas_updated_at:
                    logger.info(f"Canvas timestamp newer for {cached_page.course_id}/{cached_page.page_slug}")
                    return True
            except (ValueError, TypeError) as e:
                logger.warning(f"Failed to parse Canvas timestamp: {e}")
        
        return False

    def get_conversion_status(
        self,
        db: Session,
        course_id: int,
        page_slug: str
    ) -> Dict:
        """
        Get the conversion status for a specific page.
        
        Args:
            db: Database session
            course_id: Canvas course ID
            page_slug: Canvas page slug
            
        Returns:
            Dict with conversion status information
        """
        converted_page = db.query(ConvertedCanvasPage).filter(
            ConvertedCanvasPage.course_id == course_id,
            ConvertedCanvasPage.page_slug == page_slug
        ).first()
        
        if not converted_page:
            return {
                'is_converted': False,
                'exists': False
            }
        
        return {
            'is_converted': True,
            'exists': True,
            'success': converted_page.conversion_success,
            'component_count': converted_page.component_count,
            'last_converted': converted_page.first_converted_at.isoformat(),
            'last_accessed': converted_page.last_accessed_at.isoformat(),
            'error': converted_page.conversion_error
        } 