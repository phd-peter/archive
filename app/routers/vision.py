from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os
from pathlib import Path

router = APIRouter(
    prefix="/api/v1/vision",
    tags=["vision"]
)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    이미지 업로드 엔드포인트 (추후 GPT Vision 처리를 위해)
    현재는 업로드만 처리하고, 추후 GPT Vision API 호출 추가 예정
    """
    # 파일 확장자 검증
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일명이 없습니다.")
    
    file_extension = Path(file.filename).suffix.lower().lstrip('.')
    allowed_extensions = ["jpg", "jpeg", "png", "gif", "webp"]
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"지원하지 않는 파일 형식입니다. 허용된 형식: {', '.join(allowed_extensions)}"
        )
    
    # 파일 크기 검증 (10MB 제한)
    contents = await file.read()
    if len(contents) > 10485760:  # 10MB
        raise HTTPException(status_code=400, detail="파일 크기가 10MB를 초과합니다.")
    
    # 현재는 업로드된 파일 정보만 반환
    # 추후 여기에 GPT Vision API 호출 로직 추가 예정
    return JSONResponse(content={
        "message": "이미지 업로드 완료",
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
        "status": "ready_for_processing"
    })

@router.get("/test")
async def test_vision_endpoint():
    """GPT Vision 라우터 테스트 엔드포인트"""
    return {"message": "GPT Vision router is working!"} 