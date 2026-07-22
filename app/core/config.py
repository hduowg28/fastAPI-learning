from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL:str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Bỏ qua nếu trong file .env có thừa biến không khai báo ở trên
    )
    SECRET_KEY="abc123"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
settings = Settings()