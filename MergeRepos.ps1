# MergeRepos.ps1
# 사용 전 아래 세 변수만 수정하세요.
$Org      = "phd-peter"           # <- GitHub 사용자명 또는 org
$MonoRepo = "archive"            # <- 만들 모노레포 이름
$Repos    = @(
  "bible-gpt",
  "Youtube-script-use1",
  "n8n-google-calendar",
  "SMW2025",
  "gemini-extractor",
  "insightatech",
  "backend-GPTvision-2",
  "phdpeter_guides"
  # ... 나머지 repo 이름 추가
)

# PowerShell 실행 권한(현재 세션만) - 필요 시 주석 해제
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force


function Get-DefaultBranch($remoteName) {
  $line = git remote show $remoteName | Select-String "HEAD branch"
  if ($line) {
    return ($line.ToString().Split(":")[-1]).Trim()
  } else {
    return "main"  # fallback
  }
}

foreach ($repo in $Repos) {
  Write-Host "=== Merging $repo ===" -ForegroundColor Cyan
  $remoteUrl = "https://github.com/$Org/$repo.git"

  # 2) 리모트 추가 & 페치
  git remote remove $repo 2>$null
  git remote add $repo $remoteUrl
  git fetch $repo --tags

  # 3) 기본 브랜치 감지 (main/master 대응)
  $branch = Get-DefaultBranch $repo
  if (-not (git ls-remote --heads $repo $branch)) {
    $branch = "master"
  }

  # 4) 병합 (히스토리 유지)
  git merge "$repo/$branch" --allow-unrelated-histories -m "Merge $repo"

  # 5) 폴더 이동 (projects/<repo>/ 로 정리)
  $dest = Join-Path "projects" $repo
  New-Item -ItemType Directory -Path $dest -Force | Out-Null

  # 이동 제외 목록
  $exclude = @("projects", ".git")

  Get-ChildItem -Force | Where-Object {
    $_.Name -notin $exclude
  } | ForEach-Object {
    git mv $_.Name $dest 2>$null
  }

  git commit -m "Move $repo into $dest" 2>$null

  # 6) 리모트 정리
  git remote remove $repo
}

Write-Host "All repos merged into $MonoRepo" -ForegroundColor Green
