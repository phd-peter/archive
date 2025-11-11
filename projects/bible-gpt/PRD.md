# PRD: 말씀 길잡이 – 성경 Q&A ChatGPT 원페이지 웹사이트

## 1. 목적(Purpose)
- 사용자가 성경에 대해 궁금한 점을 자유롭게 질문하고, ChatGPT API를 통해 신속하고 정확하게 답변을 받을 수 있는 원페이지(One Page) 웹사이트 "말씀 길잡이"를 개발한다.
- Next.js의 최신 권장사항과 접근성, 성능, 확장성을 고려한다.

## 2. 주요 기능(Features)
1. **채팅 인터페이스**
   - 사용자가 질문을 입력할 수 있는 입력창
   - 이전 대화 내역이 스크롤 형태로 표시
   - 답변이 실시간으로 표시됨(로딩 인디케이터 포함)
2. **ChatGPT API 연동**
   - 사용자의 질문을 OpenAI ChatGPT API로 전송
   - API로부터 받은 답변을 사용자에게 표시
   - 성경 관련 질문임을 명확히 전달하는 프롬프트 엔지니어링 적용
3. **반응형 디자인**
   - 모바일, 태블릿, 데스크탑 등 다양한 기기에서 사용 가능
4. **심플한 UI/UX**
   - 불필요한 메뉴/기능 없이 채팅에 집중
   - "말씀 길잡이" 로고, 간단한 소개문구, 푸터(저작권 등)만 포함
5. **에러 처리**
   - API 오류, 네트워크 오류 발생 시 사용자에게 안내 메시지 표시
6. **접근성(Accessibility)**
   - Next.js 공식 문서의 접근성 가이드 준수
   - 스크린리더, 키보드 네비게이션, 명확한 대비 등 기본 접근성 보장
7. **PWA(Progressive Web App) 지원(선택)**
   - 홈 화면 추가, 오프라인 메시지 안내 등 PWA 기능 고려

## 3. 비기능 요구사항(Non-functional Requirements)
- **성능**: 빠른 응답 속도, 최소한의 로딩 시간, Next.js의 자동 최적화 활용
- **보안**: API Key 등 민감 정보는 클라이언트에 노출되지 않도록 처리(서버리스 함수 활용)
- **접근성**: 시각장애인 등도 사용할 수 있도록 Next.js 접근성 가이드라인 준수
- **배포**: Vercel, Netlify 등으로 손쉽게 배포 가능
- **SEO**: Next.js의 사전 렌더링(Static Generation) 및 메타 태그 활용

## 4. 기술 스택(Tech Stack)
- **프론트엔드**: Next.js (App Router), React, TypeScript, Tailwind CSS
- **API 연동**: OpenAI ChatGPT API (서버리스 함수 또는 백엔드 프록시 활용)
- **배포**: Vercel (권장)
- **PWA**: next-pwa 등 라이브러리 활용 가능

## 5. 렌더링 전략(Rendering Strategy)
- **메인 페이지**: Static Generation(정적 생성) 또는 Server-side Rendering(SSR) 적용
- **채팅 기능**: 클라이언트 사이드 렌더링(Client-side Rendering, CSR)로 실시간 인터랙션 구현
- **API 연동**: Next.js API Route 또는 서버리스 함수 활용

## 6. 화면 설계(UI Sketch)
- 상단: "말씀 길잡이" 로고 및 간단한 소개문구
- 중앙: 채팅창(대화 내역, 입력창, 전송 버튼)
- 하단: 푸터(저작권, 문의 이메일 등)

## 7. 사용자 시나리오(User Flow)
1. 사용자가 "말씀 길잡이" 웹사이트에 접속한다.
2. 성경에 대해 궁금한 점을 입력창에 작성한다.
3. 전송 버튼을 누른다.
4. ChatGPT API로 질문이 전달된다.
5. 답변이 실시간으로 채팅창에 표시된다.
6. 사용자는 추가 질문을 하거나 대화를 이어갈 수 있다.
7. 새로고침/재접속 시 채팅 기록은 사라진다(비회원, 익명 사용 기준).

## 8. 확장성 및 추가 고려사항
- 답변이 성경 본문 인용이나 참고 구절을 포함할 수 있도록 프롬프트 설계
- 개인정보 수집 없음(비회원, 익명 사용)
- 추후 다국어 지원 가능성 고려(1차는 한국어)
- 로컬 스토리지 활용 시, 같은 브라우저/기기에서만 대화 기록 임시 저장 가능
- PWA 기능 확장 시, 오프라인 안내 및 홈화면 추가 지원

## 9. 운영/보안 정책
- Abuse(악용) 방지: API 사용량 제한, 비정상 요청 차단
- API Key 보호: 서버리스 함수/백엔드에서만 API Key 사용
- 에러/로그 모니터링: Sentry 등 도구 연동 고려
- HTTPS 적용, 서비스워커 보안 설정(PWA 적용 시)

## 10. 참고 문서
- [Next.js 공식 문서](https://nextjs.org/docs)
- [Next.js Progressive Web Apps](https://nextjs.org/docs/canary/app/building-your-application/configuring/progressive-web-apps)
- [OpenAI API 문서](https://platform.openai.com/docs) 