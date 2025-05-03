# vibe-coding

## Jekyll + Minimal Mistakes 블로그 세팅 및 문제 해결 기록

### 1. 목표
- 마크다운으로 글을 쓰는 블로그를 만들고 싶었음
- Jekyll + Minimal Mistakes 테마 + GitHub Pages 조합을 선택

### 2. 진행 과정
1. Jekyll 설치 및 블로그 초기화 (Ruby, Jekyll, Bundler)
2. 기존 git 레포지토리에 Jekyll 파일 구조 추가
3. Minimal Mistakes 테마 적용 (remote_theme)
4. 필수 플러그인 추가 (jekyll-remote-theme, jekyll-include-cache)
5. 레이아웃(front matter) 수정 (layout: single 등)
6. 로컬 서버 실행 (bundle exec jekyll serve)

### 3. 문제점 및 해결
- **Sass Deprecation Warning**: 최신 Sass와 테마의 문법 차이로 경고 다수 발생
  - Gemfile에 `gem "sass-embedded", "~> 1.58.3"` 추가로 대부분 해결
- **Ruby 3.4+ bigdecimal 에러**: Gemfile에 `gem "bigdecimal"` 추가로 해결
- **Minimal Mistakes 최신 개발 버전 사용**: `_config.yml`에서 `remote_theme: "mmistakes/minimal-mistakes@master"`로 지정

### 4. 남은 경고
- 일부 Sass 경고는 테마가 최신 Sass 문법을 완전히 지원하지 않아서 남아있음
- 사이트 동작에는 영향 없음 (단순 경고)

### 5. 경고를 완전히 없애고 싶다면?
- Minimal Mistakes 테마를 직접 포크해서, Sass 파일을 모두 최신 문법으로 고치면 경고가 완전히 사라짐
- 단, 테마 업데이트 시 직접 관리해야 하고, 수정량이 많음

### 6. 실전 추천
- 개인 블로그/실사용: 경고는 무시하고, 공식 테마 + Sass 버전 다운그레이드로 충분히 사용 가능
- 경고가 정말 신경 쓰이거나, 회사/팀 프로젝트: 테마를 포크해서 직접 고치는 것도 가능

### 7. 추가로 할 수 있는 것
- favicon.ico 추가(404 방지)
- 프로필, 메뉴, 카테고리 등 커스터마이즈
- GitHub Pages로 배포

---

이 기록은 블로그 개발 및 유지보수에 참고용으로 남깁니다.

---

## 블로그 글 작성 및 배포(실전 사용법)

### 1. 글 작성
- `_posts/` 폴더에 마크다운(`.md`) 파일로 글을 작성
- 파일명은 `YYYY-MM-DD-title.md` 형식
- 예시:
  ```
  _posts/2024-06-10-my-first-post.md
  ```
- 파일 맨 위에는 아래와 같은 front matter 필요:
  ```markdown
  ---
  layout: single
  title: "나의 첫 글"
  date: 2024-06-10
  categories: [카테고리1, 카테고리2]
  ---
  여기에 본문을 작성하세요!
  ```

### 2. 로컬에서 미리보기 (선택)
```sh
bundle exec jekyll serve
```
- 브라우저에서 `http://localhost:4000` 접속

### 3. 배포(publish)
- **GitHub Pages를 사용한다면 반드시 git push가 필요!**
  1. 변경사항을 커밋
     ```sh
     git add .
     git commit -m "새 글 추가"
     ```
  2. 원격 저장소로 푸시
     ```sh
     git push
     ```
  3. 잠시 후(수십 초~수 분 내) GitHub Pages가 자동으로 배포
     - 블로그 주소: `https://phd-peter.github.io/vibe-coding/`

---

- 커밋/푸시만 잘 해주면, 별도의 "배포" 명령은 필요 없음
- 블로그 설정이나 테마를 바꿔도, push만 하면 자동 반영
