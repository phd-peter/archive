# Personal Jekyll Theme Portfolio

이 프로젝트는 [Personal Jekyll Theme](https://github.com/le4ker/personal-jekyll-theme)을 기반으로 한 개인 포트폴리오 사이트입니다.

## 특징

- **1페이지 스크롤 디자인**: About, Blog, Timeline, Contact 섹션
- **반응형 디자인**: 모바일 친화적
- **타임라인**: 경력/프로젝트 히스토리 표시
- **블로그 기능**: Jekyll 기반 블로그 포스팅
- **소셜 미디어 연동**: GitHub, LinkedIn, Twitter 등

## 로컬 개발 환경 설정

### 필요한 도구
- Ruby (2.7 이상)
- Bundler

### 설치 및 실행

1. 의존성 설치:
```bash
bundle install
```

2. 로컬 서버 실행:
```bash
bundle exec jekyll serve
```

3. 브라우저에서 `http://localhost:4000` 접속

## 커스터마이징

### 기본 정보 수정
`_config.yml` 파일에서 다음 항목들을 수정하세요:

- `author`: 이름
- `title`: 사이트 제목
- `description`: 사이트 설명
- `email`: 이메일 주소
- `quote`: 헤더에 표시될 인용구
- `social`: 소셜 미디어 링크들

### 타임라인 수정
`_config.yml`의 `events` 섹션에서 경력/프로젝트 정보를 수정하세요.

### 프로필 이미지 변경
- `me-img`: 헤더 프로필 이미지
- `author_blurb_image`: 블로그 포스트 하단 프로필 이미지

## 새 포스트 작성

`_posts` 디렉토리에 `YYYY-MM-DD-title.md` 형식으로 파일을 생성:

```markdown
---
layout: post
section-type: post
title: "포스트 제목"
date: 2025-07-17
category: tech
tags: [ 'tag1', 'tag2' ]
---

포스트 내용을 여기에 작성하세요.
```

## GitHub Pages 배포

1. GitHub 저장소 생성
2. 코드 푸시
3. 저장소 Settings > Pages에서 Source를 "GitHub Actions"로 설정
4. 자동으로 배포됩니다