import os
from typing import List

class Settings:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins based on environment"""
        if self.environment == "production":
            # Add your production frontend URLs here
            return [
                "https://zschool.up.railway.app/",  # Railway frontend
                "https://your-frontend-domain.vercel.app",   # Vercel frontend
                "https://your-frontend-domain.netlify.app",  # Netlify frontend
                # Add your custom domain when you have one
                # "https://yourdomain.com",
            ]
        else:
            # Development origins
            return [
                "http://localhost:3000", 
                "http://localhost:3001", 
                "http://frontend:3000"
            ]
    
    @property
    def database_url(self) -> str:
        """Get database URL from environment"""
        return os.getenv("DATABASE_URL", "postgresql://zschool_user:zschool_password@localhost:5433/zschool")
    
    @property
    def debug(self) -> bool:
        """Enable debug mode in development"""
        return self.environment == "development"

settings = Settings() 