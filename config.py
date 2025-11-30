from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    service_name: str = "Student Grouping Microservice"
    version: str = "1.0.0"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    log_level: str = "INFO"
    
    database_url: str = "sqlite:///./groupement_microservice.db"
    default_group_size: int = 5
    
    class Config:
        env_file = ".env"
        extra = "ignore"


def get_settings():
    return Settings()


# For backward compatibility with existing code
settings = get_settings()
DEFAULT_GROUP_SIZE = settings.default_group_size
DATABASE_URL = settings.database_url