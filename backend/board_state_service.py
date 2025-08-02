import logging
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import BoardState, WeeklyPlan
from database import get_db

logger = logging.getLogger(__name__)

class BoardStateService:
    """
    Service for managing Kanban board state persistence.
    Handles saving and loading board states for users across sessions.
    """
    
    def __init__(self):
        pass
    
    def generate_session_id(self) -> str:
        """
        Generate a unique session ID for a user.
        In a production app, this would be tied to user authentication.
        
        Returns:
            Unique session identifier
        """
        return str(uuid.uuid4())
    
    def ensure_weekly_plan_exists(self, db: Session, weekly_plan_id: int) -> WeeklyPlan:
        """
        Ensure a weekly plan exists, creating a default one if needed.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan to check/create
            
        Returns:
            WeeklyPlan instance
        """
        existing_plan = db.query(WeeklyPlan).filter(WeeklyPlan.id == weekly_plan_id).first()
        
        if existing_plan:
            return existing_plan
        
        # Create a default weekly plan for persistence
        logger.info(f"Creating default weekly plan with ID {weekly_plan_id}")
        
        default_plan = WeeklyPlan(
            id=weekly_plan_id,
            week_starting=datetime.now(),
            processed_json={
                "week_starting": datetime.now().strftime("%Y-%m-%d"),
                "title": "Default Weekly Plan",
                "teacher": {"name": "Default Teacher", "role": "Instructor"},
                "classwork": []
            },
            created_at=datetime.now()
        )
        
        db.add(default_plan)
        db.commit()
        db.refresh(default_plan)
        
        logger.info(f"Created default weekly plan with ID {weekly_plan_id}")
        return default_plan
    
    async def save_board_state(self, db: Session, weekly_plan_id: int, 
                             user_session: str, board_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save or update the board state for a user and weekly plan.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            user_session: User session identifier
            board_data: Current state of the Kanban board
            
        Returns:
            Result dictionary with success status
            
        Raises:
            Exception: If save operation fails
        """
        
        try:
            logger.info(f"Saving board state for session {user_session} and plan {weekly_plan_id}")
            
            # Ensure the weekly plan exists
            self.ensure_weekly_plan_exists(db, weekly_plan_id)
            
            # Check if board state already exists for this user/plan combination
            existing_state = db.query(BoardState).filter(
                and_(
                    BoardState.weekly_plan_id == weekly_plan_id,
                    BoardState.user_session == user_session
                )
            ).first()
            
            if existing_state:
                # Update existing board state
                existing_state.board_data = board_data
                existing_state.last_updated = datetime.now()
                logger.info(f"Updated existing board state with ID {existing_state.id}")
            else:
                # Create new board state
                new_state = BoardState(
                    weekly_plan_id=weekly_plan_id,
                    user_session=user_session,
                    board_data=board_data,
                    last_updated=datetime.now(),
                    created_at=datetime.now()
                )
                db.add(new_state)
                logger.info(f"Created new board state for session {user_session}")
            
            db.commit()
            
            return {
                "status": "success",
                "message": "Board state saved successfully",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to save board state: {e}")
            db.rollback()
            raise Exception(f"Unable to save board state: {e}")
    
    async def load_board_state(self, db: Session, weekly_plan_id: int, 
                             user_session: str) -> Optional[Dict[str, Any]]:
        """
        Load the saved board state for a user and weekly plan.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            user_session: User session identifier
            
        Returns:
            Board state data if found, None otherwise
        """
        
        try:
            logger.info(f"Loading board state for session {user_session} and plan {weekly_plan_id}")
            
            board_state = db.query(BoardState).filter(
                and_(
                    BoardState.weekly_plan_id == weekly_plan_id,
                    BoardState.user_session == user_session
                )
            ).first()
            
            if board_state:
                logger.info(f"Found saved board state from {board_state.last_updated}")
                return {
                    "board_data": board_state.board_data,
                    "last_updated": board_state.last_updated.isoformat(),
                    "created_at": board_state.created_at.isoformat()
                }
            
            logger.info(f"No saved board state found for session {user_session}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to load board state: {e}")
            return None
    
    async def get_or_create_session_board_state(self, db: Session, weekly_plan_id: int, 
                                              user_session: str, default_board_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get existing board state or create with default data if none exists.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            user_session: User session identifier
            default_board_data: Default board state to use if none exists
            
        Returns:
            Board state data (either saved or default)
        """
        
        # Try to load existing state
        saved_state = await self.load_board_state(db, weekly_plan_id, user_session)
        
        if saved_state:
            return saved_state["board_data"]
        
        # No saved state found, save the default and return it
        logger.info(f"No saved state found, creating default board state for session {user_session}")
        await self.save_board_state(db, weekly_plan_id, user_session, default_board_data)
        
        return default_board_data
    
    async def clear_board_state(self, db: Session, weekly_plan_id: int, 
                              user_session: str) -> Dict[str, Any]:
        """
        Clear/reset the board state for a user and weekly plan.
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            user_session: User session identifier
            
        Returns:
            Result dictionary with success status
        """
        
        try:
            logger.info(f"Clearing board state for session {user_session} and plan {weekly_plan_id}")
            
            board_state = db.query(BoardState).filter(
                and_(
                    BoardState.weekly_plan_id == weekly_plan_id,
                    BoardState.user_session == user_session
                )
            ).first()
            
            if board_state:
                db.delete(board_state)
                db.commit()
                logger.info(f"Cleared board state for session {user_session}")
                
                return {
                    "status": "success",
                    "message": "Board state cleared successfully"
                }
            
            return {
                "status": "info",
                "message": "No board state found to clear"
            }
            
        except Exception as e:
            logger.error(f"Failed to clear board state: {e}")
            db.rollback()
            raise Exception(f"Unable to clear board state: {e}")
    
    def get_board_state_summary(self, db: Session, weekly_plan_id: int) -> Dict[str, Any]:
        """
        Get summary of all board states for a weekly plan (for debugging/admin).
        
        Args:
            db: Database session
            weekly_plan_id: ID of the weekly plan
            
        Returns:
            Summary of board states
        """
        
        try:
            board_states = db.query(BoardState).filter(
                BoardState.weekly_plan_id == weekly_plan_id
            ).all()
            
            summary = {
                "weekly_plan_id": weekly_plan_id,
                "total_sessions": len(board_states),
                "sessions": []
            }
            
            for state in board_states:
                summary["sessions"].append({
                    "user_session": state.user_session,
                    "last_updated": state.last_updated.isoformat(),
                    "created_at": state.created_at.isoformat(),
                    "board_data_keys": list(state.board_data.keys()) if state.board_data else []
                })
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get board state summary: {e}")
            return {
                "error": f"Unable to get summary: {e}",
                "weekly_plan_id": weekly_plan_id
            }


# Singleton instance for use throughout the application
board_state_service = BoardStateService() 