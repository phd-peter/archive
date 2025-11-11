#!/bin/bash
set -e

MONOREPO="archive"

repos=(
  "bible-gpt"
  "Youtube-script-use1"
  "n8n-google-calendar"
  "SMW2025"
  "gemini-extractor"
  "insightatech"
  "backend-GPTvision-2"
  "phdpeter_guides"
  # ...여기에 나머지 15개 repo 이름을 추가
)

for repo in "${repos[@]}"; do
  echo "Merging $repo ..."
  git remote add $repo https://github.com/phd-peter/$repo.git
  git fetch $repo
  git merge $repo/main --allow-unrelated-histories -m "Merge $repo"
  mkdir -p projects/$repo
  shopt -s extglob
  git mv !(projects|.git|README.md) projects/$repo/ 2>/dev/null || true
  git commit -am "Move $repo into projects/$repo/"
  git remote remove $repo
done

git add .
git commit -m "All repos merged into monorepo structure"
