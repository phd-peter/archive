# 구조공학+AI 팀 협업 폴더 구조 (간결 가이드)

2~4인 팀이 바로 적용할 수 있는, 실전 중심의 협업 폴더 구조 예시입니다.

---

## 첫 셋팅가이드

1. **리포지토리 클론**
   ```bash
   git clone [이 저장소 주소]
   cd [저장소 폴더명]
   ```
2. **Python 3.11.8 버전 설치**
   - (pyenv 등으로 설치 권장, 이미 있다면 생략)
3. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. **필수 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```
5. **(선택) VSCode 등에서 Python 인터프리터를 venv로 지정**
6. **코드 작성/실행/협업 시작!**
   - 실습, 노트, 프로젝트 등 각 폴더에 맞게 파일을 추가/수정

> venv/ 폴더는 깃허브에 올리지 않습니다. 패키지 추가 시 requirements.txt도 꼭 업데이트하세요.

---

## 폴더 구조 예시

```
AI_Python_스터디/
├─ 0_공통/            # 전체 공지, 로드맵, 참고자료
│   ├─ 로드맵_240520.pdf
│   ├─ 주차계획표.xlsx
│   └─ 참고자료/
│       └─ OpenAI_API_가이드.md
│
├─ 1_주차별학습/       # 주차별 실습, 공통노트, 팀원별 실습파일
│   ├─ Week01/
│   │    ├─ 광원_변수실습.py
│   │    ├─ 준영_변수실습.py
│   ├─ Week02/
│   │    ├─ 광원_조건문.py
│   │    └─ 준영_조건문.py
│
├─ 2_개인노트/         # 팀원별 개인 정리, 질문, 느낀점 등
│   ├─ 광원/
│   │    ├─ 느낀점.md
│   │    ├─ 질문모음.md
│   ├─ 준영/
│   │    ├─ 아이디어정리.docx
│
└─ 3_프로젝트/         # 실전 프로젝트별 폴더
    ├─ proj_구조설계자동화/
    │    ├─ README.md
    │    ├─ main.py
    │    ├─ 발표자료.pptx
    └─ proj_재료시험AI/
```

---

## 폴더별 용도

- **0_공통/**: 전체 공지, 로드맵, 참고자료 등 팀원 모두가 참고
- **1_주차별학습/**: 주차별 실습, 공통노트, 팀원별 실습파일 정리
- **2_개인노트/**: 팀원별 개인 정리, 질문, 느낀점 등 기록
- **3_프로젝트/**: 실전 프로젝트별 폴더, 결과물 및 발표자료 관리

---

## 개발 환경 세팅 방법 (팀원 공통)

1. Python 3.11.8 버전 설치 (pyenv 권장)
2. (선택) 가상환경 생성 및 활성화
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```
4. (처음 세팅 시) `.gitignore`에 `venv/`가 포함되어 있는지 확인

> 가상환경(venv)은 각자 로컬에서만 생성/사용하며, 깃허브에는 올리지 않습니다.

- 팀원이 늘어나면 `2_개인노트/`에 새 폴더, `1_주차별학습/`의 각 Week 폴더에 새 실습 파일만 추가하면 됩니다.
- 각 폴더/파일명은 팀 상황에 맞게 자유롭게 조정하세요.

---

## AI API 연동 및 helper_functions 사용법

### 1. .env 파일에 OpenAI API 키 설정
프로젝트 루트에 `.env` 파일을 만들고 아래처럼 본인의 OpenAI API 키를 입력하세요:

```
OPENAI_API_KEY=sk-xxxxxxx
```

### 2. 공통 LLM 함수 사용법
`common/helper_functions.py`의 함수를 import하여 쉽게 OpenAI 챗봇을 사용할 수 있습니다.

#### 예시 (어느 Week 폴더에서든 사용 가능)
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.helper_functions import print_llm_response, get_llm_response

print_llm_response("Hello, world!")
print(get_llm_response("Tell me a good joke."))

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the weather today?"}
]
print_llm_response(messages)
```
- 문자열만 넣어도 자동으로 챗 메시지로 변환되어 동작합니다.
- 리스트 형태로 직접 넘겨도 됩니다.

---

## Appendix (참고)

- 이 구조는 진도, 개인 성장, 실전 프로젝트를 명확히 분리하여 협업과 관리가 쉬움.
- 팀원/주차/프로젝트가 늘어나도 구조 변경 없이 확장 가능함