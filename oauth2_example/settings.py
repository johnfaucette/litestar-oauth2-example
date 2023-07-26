from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(case_sensitive=True)

    DEBUG: bool = False

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str


load_dotenv()
settings = Settings()