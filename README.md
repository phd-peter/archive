# GPT Vision Backend

FastAPI를 사용한 GPT Vision 처리 백엔드 API

## 기능

### 현재 구현된 기능 (MVP)
- ✅ Hello World API 엔드포인트
- ✅ 서버 상태 확인 API
- ✅ 기본 API 정보 반환
- ✅ 이미지 업로드 엔드포인트 (기본 구조)

### 추후 구현 예정
- 🔄 GPT Vision API 연동
- 🔄 이미지 처리 및 분석
- 🔄 사용자 요청에 따른 이미지 분석 결과 반환

## 설치 및 실행

### 1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
python run.py
```

또는 직접 uvicorn 사용:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### 기본 엔드포인트
- `GET /` - Hello World 메시지 반환
- `GET /health` - 서버 상태 확인
- `GET /api/v1/info` - API 정보 반환

### GPT Vision 엔드포인트 (준비 중)
- `POST /api/v1/vision/upload` - 이미지 업로드
- `GET /api/v1/vision/test` - Vision 라우터 테스트

## 프로젝트 구조

```
backend-GPTvision-1/
├── main.py                 # FastAPI 애플리케이션 메인 파일
├── config.py              # 설정 관리
├── run.py                 # 서버 실행 스크립트
├── requirements.txt       # Python 의존성
├── README.md              # 프로젝트 문서
├── app/
│   ├── __init__.py
│   └── routers/
│       ├── __init__.py
│       └── vision.py      # GPT Vision 관련 라우터
└── uploads/               # 업로드된 파일 저장 (자동 생성)
```

## 개발 환경 설정

### 환경변수 설정 (추후 필요시)
`.env` 파일을 생성하여 다음 내용을 설정:
```
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-vision-preview
```

## API 문서

서버 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 다음 단계

1. OpenAI API 키 설정
2. GPT Vision API 연동 로직 구현
3. 이미지 처리 및 분석 기능 추가
4. 에러 처리 및 로깅 개선
5. 테스트 코드 작성 