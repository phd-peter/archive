# MergeRepos.ps1 수정 버전
$Org      = "phd-peter"
$MonoRepo = "archive"
$Repos    = @(
  "n8n-google-calendar"
)

function Get-DefaultBranch($remoteName) {
  $line = git remote show $remoteName | Select-String "HEAD branch"
  if ($line) {
    return ($line.ToString().Split(":")[-1]).Trim()
  } else {
    return "main"
  }
}

foreach ($repo in $Repos) {
  Write-Host "=== Merging $repo ===" -ForegroundColor Cyan
  $remoteUrl = "https://github.com/$Org/$repo.git"

  git remote remove $repo 2>$null
  git remote add $repo $remoteUrl
  git fetch $repo --tags

  $branch = Get-DefaultBranch $repo
  if (-not (git ls-remote --heads $repo $branch)) { $branch = "master" }

  # 병합 시 README.md 자동 무시
  git merge "$repo/$branch" --allow-unrelated-histories -m "Merge $repo" --strategy-option ours --no-edit

  # README.md 충돌 제거 (혹시 남았을 경우)
  if (Test-Path "README.md") {
    git checkout --ours README.md 2>$null
    git add README.md 2>$null
  }

  $dest = Join-Path "projects" $repo
  New-Item -ItemType Directory -Path $dest -Force | Out-Null

  $exclude = @("projects", ".git")

  Get-ChildItem -Force | Where-Object { $_.Name -notin $exclude } | ForEach-Object {
    git mv $_.Name $dest 2>$null
  }

  git commit -m "Move $repo into $dest" 2>$null
  git remote remove $repo
}

Write-Host "All repos merged into $MonoRepo" -ForegroundColor Green
