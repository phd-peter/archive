from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # FastAPI 설정
    app_name: str = "GPT Vision Backend"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # OpenAI API 설정 (추후 GPT Vision 사용시 필요)
    openai_api_key: str = ""
    openai_model: str = "gpt-4-vision-preview"
    
    # 파일 업로드 설정
    max_file_size: int = 10485760  # 10MB in bytes
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 설정 인스턴스 생성
settings = Settings()

# uploads 디렉토리 생성
if not os.path.exists(settings.upload_dir):
    os.makedirs(settings.upload_dir) 