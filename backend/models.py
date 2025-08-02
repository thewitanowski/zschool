from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, autoincrement=False, comment="Canvas Course ID")
    name = Column(String, nullable=False)
    
    # Relationships
    modules = relationship("Module", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")

class WeeklyPlan(Base):
    __tablename__ = 'weekly_plans'
    
    id = Column(Integer, primary_key=True)
    week_starting = Column(DateTime, nullable=False, index=True)
    processed_json = Column(JSON, nullable=False, comment="The final JSON output from the LLM")
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    board_states = relationship("BoardState", back_populates="weekly_plan")
    weekly_plan_lessons = relationship("WeeklyPlanLesson", back_populates="weekly_plan")

class BoardState(Base):
    __tablename__ = 'board_states'
    
    id = Column(Integer, primary_key=True)
    weekly_plan_id = Column(Integer, ForeignKey('weekly_plans.id'), nullable=False)
    user_session = Column(String(255), nullable=False, comment="Session identifier for the user")
    board_data = Column(JSON, nullable=False, comment="Current state of the Kanban board columns")
    last_updated = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Relationships
    weekly_plan = relationship("WeeklyPlan", back_populates="board_states")
    
    # Unique constraint to ensure one board state per user per week
    __table_args__ = (
        UniqueConstraint('weekly_plan_id', 'user_session', name='unique_user_week_board'),
    )

class Module(Base):
    __tablename__ = 'modules'
    
    id = Column(Integer, primary_key=True, autoincrement=False, comment="Canvas Module ID")
    course_id = Column(Integer, ForeignKey('courses.id'))
    name = Column(String, nullable=False)
    position = Column(Integer)
    
    # Relationships
    course = relationship("Course", back_populates="modules")
    items = relationship("ModuleItem", back_populates="module")

class ModuleItem(Base):
    __tablename__ = 'module_items'
    
    id = Column(Integer, primary_key=True, autoincrement=False, comment="Canvas Module Item ID")
    module_id = Column(Integer, ForeignKey('modules.id'))
    title = Column(String, nullable=False)
    content_type = Column(String)  # Page, Assignment, Discussion, etc.
    position = Column(Integer)
    url = Column(String)
    
    # Progress tracking
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime)
    
    # Relationships
    module = relationship("Module", back_populates="items")

class Assignment(Base):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True, autoincrement=False, comment="Canvas Assignment ID")
    course_id = Column(Integer, ForeignKey('courses.id'))
    name = Column(String, nullable=False)
    due_date = Column(DateTime)
    description = Column(Text)
    points_possible = Column(Integer)
    
    # Relationships
    course = relationship("Course", back_populates="assignments") 

class LessonContent(Base):
    __tablename__ = 'lesson_contents'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, nullable=False, comment="Canvas course ID")
    module_item_id = Column(Integer, nullable=False, comment="Canvas module item ID")
    lesson_title = Column(String(500), nullable=False)
    lesson_type = Column(String(100), nullable=False, comment="Page, Assignment, Discussion, etc.")
    
    # Raw content from Canvas
    raw_content = Column(Text, comment="Raw HTML content from Canvas")
    canvas_url = Column(String(1000), comment="Canvas URL for the content")
    
    # AI-transformed content
    transformed_content = Column(JSON, comment="AI-transformed structured content")
    transformation_success = Column(Boolean, default=False)
    transformation_error = Column(Text, comment="Error message if transformation failed")
    
    # Metadata
    last_fetched = Column(DateTime, default=datetime.datetime.now)
    last_transformed = Column(DateTime, default=datetime.datetime.now)
    content_hash = Column(String(64), comment="Hash of raw content to detect changes")
    
    # Relationship to weekly plans (a lesson can appear in multiple weeks)
    weekly_plan_lessons = relationship("WeeklyPlanLesson", back_populates="lesson_content")
    
    # Indexing for fast lookups
    __table_args__ = (
        UniqueConstraint('course_id', 'module_item_id', name='unique_lesson_content'),
    )

class WeeklyPlanLesson(Base):
    __tablename__ = 'weekly_plan_lessons'
    
    id = Column(Integer, primary_key=True)
    weekly_plan_id = Column(Integer, ForeignKey('weekly_plans.id'), nullable=False)
    lesson_content_id = Column(Integer, ForeignKey('lesson_contents.id'), nullable=False)
    
    # Position in the weekly plan
    subject = Column(String(200), comment="Subject this lesson belongs to in the weekly plan")
    lesson_order = Column(Integer, comment="Order within the subject")
    
    # User-specific data for this lesson in this week
    user_completed = Column(Boolean, default=False)
    user_notes = Column(Text, comment="Student's personal notes for this lesson")
    completion_date = Column(DateTime, comment="When the student marked this as complete")
    
    # Relationships
    weekly_plan = relationship("WeeklyPlan", back_populates="weekly_plan_lessons")
    lesson_content = relationship("LessonContent", back_populates="weekly_plan_lessons")
    
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now) 