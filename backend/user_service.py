import logging
from canvas_client import CanvasClient

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, canvas_client: CanvasClient):
        self.canvas_client = canvas_client

    async def get_user_profile(self):
        try:
            profile_data = await self.canvas_client.get_user_profile()
            if profile_data:
                return {
                    "first_name": profile_data.get("first_name"),
                    "avatar_url": profile_data.get("avatar_url"),
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching user profile: {e}")
            return None 