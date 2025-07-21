from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import List
import requests
import base64
from io import BytesIO
from PIL import Image
# from pytesseract import image_to_string  # OCR 라이브러리 예시
import os

app = FastAPI(title="Image OCR Service")

class ImageRequest(BaseModel):
    web_content_link: HttpUrl = Field(
        ...,
        description="Google Drive의 webContentLink 형태로, anyone-with-link 상태여야 합니다."
    )
    labels: List[str] = Field(
        ...,
        min_items=1,
        description="최소 1개 이상의 라벨을 문자열 리스트로 전달합니다."
    )

class OCRResult(BaseModel):
    label: str
    text: str

class ImageResponse(BaseModel):
    results: List[OCRResult]

@app.post("/process", response_model=ImageResponse)
def process_image(req: ImageRequest):
    # 1) 이미지 다운로드
    try:
        resp = requests.get(req.web_content_link)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail=f"이미지 다운로드 실패: {e}"
        )
    
    image_bytes = resp.content

    # 2) Base64 변환 (필요시)
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # 3) OCR 수행 (여기선 스텁)
    # image = Image.open(BytesIO(image_bytes))
    # full_text = image_to_string(image, lang="eng")  # 실제 OCR 로직 예시
    full_text = "여기에 OCR로 추출된 전체 텍스트가 들어갑니다."

    # 4) 라벨별 매칭/필터링 예시
    results: List[OCRResult] = []
    for label in req.labels:
        # TODO: label 기반 필터링 로직 구현
        matched = full_text  # 예시로 전체 텍스트를 그대로 사용
        results.append(OCRResult(label=label, text=matched))

    return ImageResponse(results=results)

@app.get("/")
async def root():
    """Hello World 엔드포인트"""
    return {"message": "Hello World"}

@app.get("/health")
async def health_check():
    """서버 상태 확인 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)