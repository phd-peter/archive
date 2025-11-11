from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import vision

app = FastAPI(
    title="GPT Vision Backend",
    description="A FastAPI backend for GPT Vision processing",
    version="1.0.0"
)

# CORS 미들웨어 설정 (프론트엔드 연결을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(vision.router)

@app.get("/")
async def root():
    """Hello World 엔드포인트"""
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    """서버 상태 확인 엔드포인트"""
    return {"status": "healthy"}

@app.get("/api/v1/info")
async def get_info():
    """API 정보 반환"""
    return {
        "name": "GPT Vision Backend",
        "version": "1.0.0",
        "description": "백엔드 API for image processing with GPT Vision"
    } 