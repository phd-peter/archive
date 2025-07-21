from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict
import requests
import base64
from io import BytesIO
from PIL import Image
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드 및 OpenAI 클라이언트 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def create_dynamic_tool(labels: List[str]) -> Dict:
    """사용자가 제공한 labels를 기반으로 동적으로 tool calling 구조 생성"""
    properties = {}
    
    for label in labels:
        properties[label] = {
            "type": "string",
            "description": f"Extract {label} information from the image"
        }
    
    tool = [{
        "type": "function",
        "name": "extract_image_data",
        "description": "Extract specified data fields from the image",
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": labels,
            "additionalProperties": False
        }
    }]
    
    return tool

def call_openai_vision(image_b64: str, labels: List[str]) -> Dict:
    """OpenAI Vision API를 호출하여 이미지에서 데이터 추출"""
    
    # 동적으로 tool 생성
    tool = create_dynamic_tool(labels)
    print(f"🔧 Generated Tool: {json.dumps(tool, indent=2, ensure_ascii=False)}")
    
    # 이미지 입력 구성
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts structured data from images. Please analyze the image carefully and extract the requested information."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{image_b64}"
                }
            ]
        }
    ]
    
    print(f"📨 Messages structure: {json.dumps([{'role': msg['role'], 'content_type': type(msg['content']).__name__, 'content_keys': list(msg['content'][0].keys()) if isinstance(msg['content'], list) else 'string'} for msg in messages], indent=2, ensure_ascii=False)}")
    
    try:
        print("🚀 Calling OpenAI API...")
        print(f"📋 Labels: {labels}")
        print(f"🖼️ Image base64 length: {len(image_b64)} characters")
        
        response = client.responses.create(
            model="gpt-4o",
            input=messages,
            tools=tool
        )
        
        print(f"✅ OpenAI API Response received")
        print(f"📄 Response type: {type(response)}")
        print(f"📄 Response attributes: {dir(response)}")
        
        # Tool call 결과 파싱
        print(f"🔍 Trying to parse: response.output[0].arguments")
        extracted_data = json.loads(response.output[0].arguments)
        print(f"✅ Successfully extracted data: {extracted_data}")
        return extracted_data
        
    except AttributeError as e:
        error_msg = f"OpenAI API 응답 구조 오류: {str(e)} | Available attributes: {dir(response) if 'response' in locals() else 'No response object'}"
        print(f"❌ AttributeError: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
    except json.JSONDecodeError as e:
        error_msg = f"JSON 파싱 오류: {str(e)} | Raw response: {response if 'response' in locals() else 'No response'}"
        print(f"❌ JSONDecodeError: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
    except Exception as e:
        error_msg = f"OpenAI Vision API 호출 실패: {str(e)} | Error type: {type(e).__name__}"
        print(f"❌ Exception: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )

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

    # 2) Base64 변환
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # 3) OpenAI Vision API를 사용하여 데이터 추출
    try:
        extracted_data = call_openai_vision(image_b64, req.labels)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 분석 실패: {str(e)}"
        )

    # 4) 결과를 OCRResult 형태로 변환
    results: List[OCRResult] = []
    for label in req.labels:
        text_value = extracted_data.get(label, "정보를 찾을 수 없습니다")
        # 숫자인 경우 문자열로 변환
        if isinstance(text_value, (int, float)):
            text_value = str(text_value)
        results.append(OCRResult(label=label, text=text_value))

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