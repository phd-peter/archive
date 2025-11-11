<<<<<<< HEAD
기존에 작성했던 Repo들을 보관.
추후에 볼 가능성은 0이지만 버리긴 아쉬워서.
공부해왔던, 코딩해왔던, AI생성해왔던 기록들임.
=======
# 말씀 길잡이 – 성경 Q&A ChatGPT

성경에 대해 궁금한 점을 자유롭게 질문할 수 있는 원페이지 Q&A 챗봇 서비스입니다. OpenAI ChatGPT API를 활용하여 신속하고 정확한 답변을 제공합니다.

## 주요 특징
- **실시간 채팅**: 사용자의 질문에 대해 AI가 실시간으로 답변
- **성경 전문가 프롬프트**: 답변이 성경적으로 친절하고 정확하게 제공됨
- **반응형 UI**: 모바일, 태블릿, 데스크탑 지원
- **접근성**: Next.js 공식 가이드라인 준수
- **에러 처리**: API 오류, 네트워크 오류 안내
- **심플한 디자인**: 불필요한 메뉴 없이 채팅에 집중

## 기술 스택
- **프레임워크**: Next.js (App Router)
- **언어**: TypeScript, React
- **스타일**: Tailwind CSS
- **API 연동**: OpenAI ChatGPT API (서버리스 함수)

## 폴더 구조
```
app/
  page.tsx         # 메인 채팅 UI 및 로직
  layout.tsx       # 글로벌 레이아웃
  globals.css      # 글로벌 스타일(Tailwind)
  api/chat/route.ts# ChatGPT API 연동 서버리스 함수
  components/      # UI 컴포넌트
public/            # 정적 파일 및 아이콘
.next/             # Next.js 빌드 산출물(배포 시 생성)
types/             # 타입 정의 파일
```

## 환경 변수 설정
OpenAI API Key가 필요합니다. 루트에 `.env` 파일을 생성하고 아래와 같이 입력하세요:
```
OPENAI_API_KEY=sk-...
```

## 실행 방법
```bash
npm install
npm run dev
```
로컬에서 [http://localhost:3000](http://localhost:3000) 접속

## 배포
- Vercel 등 Next.js 지원 플랫폼에 손쉽게 배포 가능
- 환경 변수(OPENAI_API_KEY) 설정 필요

## 참고 문서
- [Next.js 공식 문서](https://nextjs.org/docs)
- [OpenAI API 문서](https://platform.openai.com/docs)

---
© 2024 말씀 길잡이 | bible-gpt
>>>>>>> bible-gpt/main
