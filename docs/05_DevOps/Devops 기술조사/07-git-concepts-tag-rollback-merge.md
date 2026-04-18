# Git 개념 가이드: 태그, 롤백, 머지 전략

> **목적**: DevOps Workflow 제품 개발을 위한 Git 핵심 개념 심화 학습
> **작성일**: 2024-12-28

---

## 목차

1. [Git 태그 완벽 가이드](#1-git-태그-완벽-가이드)
2. [롤백 전략 및 명령어](#2-롤백-전략-및-명령어)
3. [머지 전략 비교 분석](#3-머지-전략-비교-분석)
4. [DevOps Workflow 구현 시 고려사항](#4-devops-workflow-구현-시-고려사항)

---

# 1. Git 태그 완벽 가이드

## 1.1 태그의 종류

### Lightweight Tag vs Annotated Tag 비교

| 구분 | Lightweight Tag | Annotated Tag |
|------|----------------|---------------|
| **생성 방식** | `git tag v1.0.0` | `git tag -a v1.0.0 -m "message"` |
| **저장 정보** | 커밋 해시만 저장 (포인터) | 태거 정보, 날짜, 메시지, 체크섬 포함 |
| **Git 객체** | 별도 객체 없음 | 별도 Tag 객체 생성 |
| **서명 가능** | ❌ 불가능 | ✅ GPG 서명 가능 |
| **메타데이터** | ❌ 없음 | ✅ 풍부한 메타데이터 |
| **용도** | 임시/로컬 마킹, 북마크 | **릴리즈, CI/CD 트리거** |
| **`git describe`** | 기본 제외 | 기본 포함 |
| **`git push --follow-tags`** | 제외됨 | 포함됨 |

### 내부 구조 차이

```bash
# Lightweight Tag - 단순 참조 파일
cat .git/refs/tags/v1.0.0-light
# abc123def456...  (커밋 해시만)

# Annotated Tag - 별도 Git 객체
git cat-file -t v1.0.0
# tag

git cat-file -p v1.0.0
# object abc123def456...
# type commit
# tag v1.0.0
# tagger John Doe <john@example.com> 1703750400 +0900
#
# Release version 1.0.0
```

---

## 1.2 태그 생성 명령어

### 기본 태그 생성

```bash
# Lightweight 태그 (임시용)
git tag v1.0.0-temp

# Annotated 태그 (권장)
git tag -a v1.0.0 -m "Release version 1.0.0"

# 서명된 태그 (보안 강화)
git tag -s v1.0.0 -m "Signed release v1.0.0"
# GPG 키 필요

# 특정 커밋에 태그 생성
git tag -a v1.0.0 <commit-hash> -m "Release from specific commit"

# 과거 커밋에 태그 (릴리즈 누락 시)
git log --oneline -10
git tag -a v0.9.0 abc1234 -m "Retroactive tag for v0.9.0"
```

### 다양한 태그 패턴

```bash
# ═══════════════════════════════════════
# Semantic Versioning (SemVer)
# ═══════════════════════════════════════
git tag -a v1.2.3 -m "Major.Minor.Patch"
# Major: 호환성 깨지는 변경
# Minor: 하위 호환 기능 추가
# Patch: 하위 호환 버그 수정

# ═══════════════════════════════════════
# Pre-release 태그
# ═══════════════════════════════════════
git tag -a v1.2.3-alpha.1 -m "Alpha release"      # 초기 테스트
git tag -a v1.2.3-beta.2 -m "Beta release"        # 기능 완료, 테스트 중
git tag -a v1.2.3-rc.1 -m "Release candidate"     # 릴리즈 후보

# ═══════════════════════════════════════
# 빌드 메타데이터 포함
# ═══════════════════════════════════════
git tag -a v1.2.3+build.456 -m "With build number"
git tag -a v1.2.3+20241228 -m "With build date"
git tag -a v1.2.3-rc.1+build.789 -m "RC with build"

# ═══════════════════════════════════════
# 서비스별 태그 (모노레포)
# ═══════════════════════════════════════
git tag -a api/v1.0.0 -m "API service release"
git tag -a web/v2.0.0 -m "Web frontend release"
git tag -a worker/v1.5.0 -m "Background worker release"

# ═══════════════════════════════════════
# 환경별 배포 태그
# ═══════════════════════════════════════
git tag -a deploy/prod/2024-12-28-1 -m "Production deployment #1"
git tag -a deploy/staging/2024-12-28-1 -m "Staging deployment"

# ═══════════════════════════════════════
# Calendar Versioning (CalVer)
# ═══════════════════════════════════════
git tag -a 2024.12.28 -m "Daily release"
git tag -a 2024.12.28.1 -m "Hotfix release"
git tag -a 24.12.1 -m "YY.MM.MICRO format"
```

---

## 1.3 태그 조회 명령어

```bash
# ═══════════════════════════════════════
# 기본 조회
# ═══════════════════════════════════════
# 모든 태그 조회
git tag

# 패턴으로 필터링
git tag -l "v1.*"         # v1.x.x 태그만
git tag -l "*-rc*"        # RC 태그만
git tag -l "api/*"        # api 서비스 태그만
git tag -l "v[0-9]*"      # 숫자로 시작하는 태그

# ═══════════════════════════════════════
# 상세 정보 조회
# ═══════════════════════════════════════
# 태그 상세 정보 (Annotated만 의미있음)
git show v1.0.0

# 태그가 가리키는 커밋만
git rev-list -n 1 v1.0.0

# 태그 메시지만
git tag -l -n1 v1.0.0     # 1줄
git tag -l -n10 v1.0.0    # 10줄

# ═══════════════════════════════════════
# 정렬 및 필터
# ═══════════════════════════════════════
# 버전순 정렬 (최신순)
git tag -l --sort=-v:refname

# 버전순 정렬 (오래된순)
git tag -l --sort=v:refname

# 생성일 기준 정렬
git tag -l --sort=-creatordate

# 커밋 날짜 기준 정렬
git tag -l --sort=-committerdate

# ═══════════════════════════════════════
# 특수 조회
# ═══════════════════════════════════════
# 최신 태그 조회
git describe --tags --abbrev=0

# 현재 커밋의 태그
git tag --points-at HEAD

# 특정 커밋의 태그
git tag --points-at <commit-hash>

# 태그와 커밋 매핑
git show-ref --tags

# 태그 개수
git tag | wc -l

# 현재 상태 설명 (태그 + 추가 커밋 수)
git describe --tags
# v1.2.3-5-gabc1234
# v1.2.3 태그 이후 5개 커밋, 현재 커밋은 abc1234
```

---

## 1.4 태그 공유 및 삭제

### 원격 저장소에 태그 푸시

```bash
# 단일 태그 푸시
git push origin v1.0.0

# 모든 태그 푸시 (Lightweight 포함)
git push origin --tags

# Annotated 태그만 푸시 (권장)
git push origin --follow-tags

# 특정 패턴 태그만 푸시
git tag -l "v1.2.*" | xargs -I {} git push origin {}
```

### 태그 삭제

```bash
# ═══════════════════════════════════════
# 로컬 태그 삭제
# ═══════════════════════════════════════
git tag -d v1.0.0

# 여러 태그 삭제
git tag -d v1.0.0 v1.0.1 v1.0.2

# 패턴으로 삭제
git tag -l "v1.0.*" | xargs git tag -d

# ═══════════════════════════════════════
# 원격 태그 삭제
# ═══════════════════════════════════════
git push origin --delete v1.0.0
# 또는
git push origin :refs/tags/v1.0.0

# 여러 원격 태그 삭제
git push origin --delete v1.0.0 v1.0.1 v1.0.2

# 로컬 + 원격 동시 삭제
git tag -d v1.0.0 && git push origin --delete v1.0.0
```

---

## 1.5 태그 수정 및 이동

```bash
# ═══════════════════════════════════════
# 태그 메시지 수정 (태그 재생성)
# ═══════════════════════════════════════
# 같은 커밋에 새 메시지로 덮어쓰기
git tag -a -f v1.0.0 -m "Updated release message"
git push origin -f v1.0.0

# ═══════════════════════════════════════
# 태그를 다른 커밋으로 이동
# ═══════════════════════════════════════
# 로컬 태그 삭제 후 재생성
git tag -d v1.0.0
git tag -a v1.0.0 <new-commit-hash> -m "Moved tag to correct commit"
git push origin -f v1.0.0

# ═══════════════════════════════════════
# 태그 이름 변경
# ═══════════════════════════════════════
# 새 이름으로 생성 후 기존 삭제
git tag -a v1.0.0 v1.0.0-old^{} -m "Renamed from v1.0.0-old"
git tag -d v1.0.0-old
git push origin v1.0.0
git push origin --delete v1.0.0-old

# ⚠️ 주의: 이미 배포된 태그 변경은 매우 위험!
# 팀원들이 기존 태그를 참조하고 있을 수 있음
```

---

## 1.6 CI/CD에서의 태그 활용

### 태그 기반 파이프라인 트리거 (GitHub Actions)

```yaml
name: Release Pipeline

on:
  push:
    tags:
      # 정식 릴리즈만
      - 'v[0-9]+.[0-9]+.[0-9]+'
      
      # Pre-release 제외
      - '!v*.*.*-*'

---
name: Staging Pipeline

on:
  push:
    tags:
      # RC만 트리거
      - 'v*.*.*-rc.*'
      
      # Beta만 트리거
      - 'v*.*.*-beta.*'

---
name: Service-specific Pipeline

on:
  push:
    tags:
      # 특정 서비스만
      - 'api/v*'
      - 'web/v*'
```

### 태그에서 버전 추출

```bash
# 현재 태그 버전 추출
VERSION=$(git describe --tags --abbrev=0)
echo "Building version: $VERSION"

# 태그에서 'v' 제거
VERSION=$(git describe --tags --abbrev=0 | sed 's/^v//')
# v1.2.3 → 1.2.3

# 태그 파싱 (Major.Minor.Patch)
TAG="v1.2.3"
MAJOR=$(echo $TAG | cut -d. -f1 | sed 's/v//')
MINOR=$(echo $TAG | cut -d. -f2)
PATCH=$(echo $TAG | cut -d. -f3)

# Docker 이미지 태깅
docker build -t myapp:$VERSION .
docker build -t myapp:latest .
docker push myapp:$VERSION
docker push myapp:latest

# 멀티 태그
docker tag myapp:$VERSION myapp:$MAJOR
docker tag myapp:$VERSION myapp:$MAJOR.$MINOR
```

### 자동 릴리즈 노트 생성

```bash
# 이전 태그 이후 변경사항
PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^)
CURRENT_TAG=$(git describe --tags --abbrev=0)

echo "## Changes in $CURRENT_TAG"
git log $PREVIOUS_TAG..$CURRENT_TAG --oneline --no-merges

# Conventional Commits 기반 분류
echo "### Features"
git log $PREVIOUS_TAG..$CURRENT_TAG --oneline --grep="^feat"

echo "### Bug Fixes"
git log $PREVIOUS_TAG..$CURRENT_TAG --oneline --grep="^fix"

echo "### Breaking Changes"
git log $PREVIOUS_TAG..$CURRENT_TAG --oneline --grep="BREAKING CHANGE"
```

---

# 2. 롤백 전략 및 명령어

## 2.1 롤백 방식 비교

| 방식 | 명령어 | 이력 보존 | Force Push | 안전성 | 권장 상황 |
|------|--------|----------|------------|--------|----------|
| **Revert** | `git revert` | ✅ 보존 | ❌ 불필요 | 🟢 높음 | **프로덕션 롤백 (권장)** |
| **Reset** | `git reset` | ❌ 삭제 | ✅ 필요 | 🟡 중간 | 로컬/개인 브랜치 |
| **Checkout** | `git checkout` | ✅ 보존 | ❌ 불필요 | 🟢 높음 | 파일 단위 복구 |
| **Restore** | `git restore` | ✅ 보존 | ❌ 불필요 | 🟢 높음 | Git 2.23+ 파일 복구 |

### 시각적 비교

```
원본:  A---B---C---D (HEAD, main)
                 ↑
              문제 커밋

[Revert 후]
       A---B---C---D---D' (HEAD, main)
                       ↑
                    Revert 커밋 (D의 변경 취소)

[Reset --hard 후]
       A---B---C (HEAD, main)
               ↑
            D는 사라짐 (reflog에는 존재)
```

---

## 2.2 Git Revert (권장 - 이력 보존)

### 기본 Revert

```bash
# 단일 커밋 되돌리기
git revert <commit-hash>
# 에디터가 열리면 커밋 메시지 확인 후 저장
git push origin main

# 커밋 메시지 직접 지정
git revert <commit-hash> -m "Revert: rollback feature X due to bug"

# 자동 커밋 없이 되돌리기 (스테이징만)
git revert --no-commit <commit-hash>
# 추가 수정 가능
git commit -m "Revert with modifications"

# 에디터 열지 않고 기본 메시지 사용
git revert --no-edit <commit-hash>
```

### 여러 커밋 Revert

```bash
# ═══════════════════════════════════════
# 연속된 커밋 범위 되돌리기
# ═══════════════════════════════════════
# HEAD~3부터 HEAD까지 (3개 커밋)
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert: rollback last 3 commits"

# 특정 범위
git revert --no-commit abc1234..def5678
git commit -m "Revert: rollback commits from abc to def"

# ═══════════════════════════════════════
# 개별 커밋들 되돌리기 (비연속)
# ═══════════════════════════════════════
git revert --no-commit <commit1> <commit2> <commit3>
git commit -m "Revert: rollback specific problematic commits"

# ═══════════════════════════════════════
# 역순으로 하나씩 되돌리기 (충돌 최소화)
# ═══════════════════════════════════════
# 최신 것부터 순서대로
git revert HEAD --no-edit
git revert HEAD~1 --no-edit
git revert HEAD~2 --no-edit
# 각각 별도 커밋으로 남음
```

### 머지 커밋 Revert (중요!)

머지 커밋은 두 개의 부모를 가지므로 `-m` 옵션으로 어느 부모를 유지할지 지정해야 합니다.

```bash
# 머지 커밋 구조 확인
git log --oneline --graph
# *   M (HEAD) Merge branch 'feature/broken' into main
# |\
# | * F2 feature commit 2
# | * F1 feature commit 1
# * | B  main commit
# |/
# *   A  common ancestor

# 부모 확인
git cat-file -p M
# parent B (첫 번째 부모 = main)
# parent F2 (두 번째 부모 = feature)

# ═══════════════════════════════════════
# -m 1: 첫 번째 부모(main) 유지, feature 변경 취소
# ═══════════════════════════════════════
git revert -m 1 <merge-commit-hash>
# feature 브랜치의 변경사항(F1, F2)이 취소됨
# 가장 일반적인 롤백 케이스

# ═══════════════════════════════════════
# -m 2: 두 번째 부모(feature) 유지, main 변경 취소
# ═══════════════════════════════════════
git revert -m 2 <merge-commit-hash>
# main 브랜치의 변경사항(B)이 취소됨
# 거의 사용하지 않음
```

### Revert 후 다시 머지하기 (주의!)

Revert된 브랜치를 다시 머지하려면 **revert를 revert**해야 합니다.

```bash
# 상황: feature/broken을 머지했다가 revert함
git revert -m 1 <merge-commit>  # R1 커밋 생성

# 나중에 feature/broken의 버그를 수정하고 다시 머지하려면?
git checkout main

# 방법 1: revert 커밋을 revert
git revert <R1-commit>  # revert의 revert
git merge feature/broken

# 방법 2: feature 브랜치를 main에 rebase
git checkout feature/broken
git rebase main
git checkout main
git merge feature/broken
```

---

## 2.3 Git Reset (주의 - Force Push 필요)

### Reset 모드 상세 비교

| 모드 | HEAD | Index (Staging) | Working Directory | 커밋 이력 |
|------|------|-----------------|-------------------|----------|
| `--soft` | ✅ 이동 | 유지 | 유지 | 제거 |
| `--mixed` (기본) | ✅ 이동 | ⬅️ 초기화 | 유지 | 제거 |
| `--hard` | ✅ 이동 | ⬅️ 초기화 | ⬅️ 초기화 | 제거 |

### 시각적 이해

```
Before: A---B---C---D (HEAD)

[--soft HEAD~2]
HEAD: A---B (C, D의 변경사항은 staged 상태)
Index: C + D 변경사항 (commit 가능)
Working: C + D 변경사항

[--mixed HEAD~2] (기본값)
HEAD: A---B
Index: 비어있음
Working: C + D 변경사항 (unstaged)

[--hard HEAD~2]
HEAD: A---B
Index: 비어있음
Working: 비어있음 (C, D 변경사항 삭제!)
```

### Reset 명령어

```bash
# ═══════════════════════════════════════
# Soft Reset - 커밋만 취소
# ═══════════════════════════════════════
git reset --soft HEAD~1
# 용도: 커밋 메시지 수정, 여러 커밋 하나로 합치기
# 변경사항은 staged 상태로 유지

git reset --soft HEAD~3
git commit -m "Combined: feature implementation"

# ═══════════════════════════════════════
# Mixed Reset - 커밋 + 스테이징 취소 (기본값)
# ═══════════════════════════════════════
git reset HEAD~1
# 또는
git reset --mixed HEAD~1
# 용도: 커밋 내용 수정 후 재커밋
# 변경사항은 unstaged 상태로 유지

# ═══════════════════════════════════════
# Hard Reset - 완전 삭제 (주의!)
# ═══════════════════════════════════════
git reset --hard HEAD~1
# 용도: 완전한 롤백
# ⚠️ 변경사항 모두 삭제됨!

# 특정 커밋으로 Reset
git reset --hard <commit-hash>

# 태그로 Reset
git reset --hard v1.0.0

# 원격 브랜치와 동기화
git reset --hard origin/main
```

### Reset 후 원격 동기화

```bash
# ⚠️ Force Push (팀원과 반드시 협의!)
git reset --hard <safe-commit>
git push --force origin main

# 더 안전한 Force with lease
git push --force-with-lease origin main
# 다른 사람이 push한 경우 실패함 (충돌 방지)

# Force push 전 확인
git log origin/main..HEAD --oneline
# (비어있어야 안전)
```

---

## 2.4 파일 단위 복구

### Git Checkout (구 방식, Git 2.23 이전)

```bash
# 특정 파일을 이전 커밋 버전으로 복구
git checkout <commit-hash> -- path/to/file.txt

# 특정 파일의 수정 취소 (HEAD로 복구)
git checkout HEAD -- path/to/file.txt

# 전체 디렉토리 복구
git checkout <commit-hash> -- src/

# 삭제된 파일 복구
git checkout HEAD~1 -- deleted-file.txt
```

### Git Restore (Git 2.23+, 권장)

`checkout`의 파일 복구 기능을 분리한 명령어입니다.

```bash
# ═══════════════════════════════════════
# Working Directory 복구
# ═══════════════════════════════════════
# 수정 취소 (staged 아닌 변경사항)
git restore path/to/file.txt

# 여러 파일
git restore file1.txt file2.txt

# 전체 복구
git restore .

# ═══════════════════════════════════════
# Staging 취소 (unstage)
# ═══════════════════════════════════════
git restore --staged path/to/file.txt

# 전체 unstage
git restore --staged .

# ═══════════════════════════════════════
# 특정 커밋에서 파일 복구
# ═══════════════════════════════════════
# Working Directory로 복구
git restore --source=<commit-hash> path/to/file.txt

# Staging Area로 복구
git restore --source=<commit-hash> --staged path/to/file.txt

# 둘 다 (staged + working)
git restore --source=<commit-hash> --staged --worktree path/to/file.txt

# 태그 버전으로 복구
git restore --source=v1.0.0 src/config.js
```

### 비교: checkout vs restore vs reset

| 작업 | checkout (구) | restore (신) | reset |
|------|--------------|--------------|-------|
| 파일 수정 취소 | `checkout -- file` | `restore file` | - |
| Unstage | `reset HEAD file` | `restore --staged file` | `reset file` |
| 특정 버전 복구 | `checkout commit -- file` | `restore --source=commit file` | - |
| 브랜치 전환 | `checkout branch` | - | - |

---

## 2.5 Reflog를 활용한 복구

`reflog`는 HEAD의 모든 이동 기록을 저장합니다. 실수로 삭제한 커밋도 복구할 수 있습니다.

```bash
# ═══════════════════════════════════════
# Reflog 조회
# ═══════════════════════════════════════
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~3
# def5678 HEAD@{1}: commit: important feature
# ghi9012 HEAD@{2}: commit: another commit
# jkl3456 HEAD@{3}: checkout: moving from feature to main

# 특정 브랜치의 reflog
git reflog show main

# 시간 기준 조회
git reflog --since="2 hours ago"
git reflog --since="2024-12-28"

# ═══════════════════════════════════════
# 실수로 reset --hard 한 경우 복구
# ═══════════════════════════════════════
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~3  ← 실수!
# def5678 HEAD@{1}: commit: important feature ← 이걸 복구하고 싶음

git reset --hard HEAD@{1}
# 또는
git reset --hard def5678

# ═══════════════════════════════════════
# 삭제된 브랜치 복구
# ═══════════════════════════════════════
git branch -D feature/important  # 실수로 삭제!

git reflog
# ... feature/important 관련 기록 찾기

git checkout -b feature/important HEAD@{5}
# 또는
git branch feature/important <commit-hash>

# ═══════════════════════════════════════
# Rebase 실수 복구
# ═══════════════════════════════════════
git rebase main  # 문제 발생!

git reflog
# abc1234 HEAD@{0}: rebase (finish)
# def5678 HEAD@{5}: rebase (start)  ← rebase 시작 전

git reset --hard HEAD@{5}

# ═══════════════════════════════════════
# Reflog 만료 설정
# ═══════════════════════════════════════
# 기본: 90일 (도달 가능), 30일 (도달 불가)
git config gc.reflogExpire 120.days
git config gc.reflogExpireUnreachable 60.days
```

---

## 2.6 긴급 롤백 시나리오 가이드

### 시나리오 1: 최신 배포 즉시 롤백

```bash
# 방법 A: Revert (권장)
git revert HEAD --no-edit
git push origin main
# → GitOps 감지 → 자동 재배포 (30초~1분)

# 방법 B: 이전 이미지로 직접 롤백 (GitOps)
cd k8s-manifests
PREVIOUS_TAG=$(git log -2 --format="%s" | tail -1 | grep -oP 'v[\d.]+')
yq -i ".image.tag = \"$PREVIOUS_TAG\"" deployment.yaml
git commit -am "EMERGENCY: rollback to $PREVIOUS_TAG"
git push origin main
```

### 시나리오 2: 특정 기능만 롤백

```bash
# 해당 기능의 머지 커밋 찾기
git log --oneline --merges | grep "feature/payment"
# abc1234 Merge branch 'feature/payment' into main

# 머지 커밋 Revert
git revert -m 1 abc1234
git push origin main
```

### 시나리오 3: 여러 릴리즈 전으로 롤백

```bash
# 안정 버전 태그 확인
git tag -l --sort=-v:refname | head -10

# 되돌릴 커밋 범위 확인
git log v1.0.0..HEAD --oneline

# 범위 Revert
git revert --no-commit v1.0.0..HEAD
git commit -m "Revert: rollback to v1.0.0"
git push origin main
```

### 시나리오 4: DB 마이그레이션 포함 롤백

```bash
# 1. 트래픽 차단 (optional)
kubectl scale deployment myapp --replicas=0

# 2. DB 롤백 마이그레이션
kubectl exec -it migration-pod -- ./migrate down -steps=1

# 3. 애플리케이션 롤백
git revert HEAD
git push origin main

# 4. 트래픽 복구
kubectl scale deployment myapp --replicas=3
```

---

## 2.7 롤백 충돌 해결

```bash
# Revert 중 충돌 발생 시
git revert <commit-hash>
# CONFLICT (content): Merge conflict in src/app.js

# 충돌 상태 확인
git status
# both modified: src/app.js

# 충돌 파일 내용
cat src/app.js
# <<<<<<< HEAD
# 현재 버전
# =======
# revert 하려는 버전
# >>>>>>> parent of abc1234

# 해결 방법 1: 수동 편집
vim src/app.js
git add src/app.js
git revert --continue

# 해결 방법 2: 특정 버전 선택
git checkout --ours src/app.js    # 현재 버전 유지
git checkout --theirs src/app.js  # revert 버전 적용
git add src/app.js
git revert --continue

# 롤백 중단
git revert --abort
```

---

# 3. 머지 전략 비교 분석

## 3.1 머지 전략 종류 개요

| 전략 | 명령어 | 커밋 이력 | 충돌 해결 | 주요 특징 |
|------|--------|----------|----------|----------|
| **Merge Commit** | `git merge` | 분기 보존 | 1회 | 기본값, 안전 |
| **Fast-Forward** | `git merge --ff` | 선형 | 없음 | 분기 없을 때만 |
| **No Fast-Forward** | `git merge --no-ff` | 머지 커밋 강제 | 1회 | Git Flow 표준 |
| **Squash Merge** | `git merge --squash` | 단일 커밋 | 1회 | PR 정리용 |
| **Rebase** | `git rebase` | 선형 재배치 | 커밋별 | 클린 히스토리 |
| **Rebase + FF** | `rebase` → `merge --ff` | 완전 선형 | 커밋별 | Trunk-based |

---

## 3.2 Merge Commit (기본 머지)

### 개념도

```
Before:
main:    A---B---C
              \
feature:       D---E

After (git merge feature):
main:    A---B---C-------M
              \         /
feature:       D---E---/

M = Merge commit (부모가 C와 E 두 개)
```

### 명령어

```bash
git checkout main
git merge feature/login

# 메시지 직접 지정
git merge feature/login -m "Merge: integrate login feature (#123)"

# 머지 커밋 강제 (ff 가능해도)
git merge --no-ff feature/login
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 브랜치 히스토리 완전 보존 | ❌ 히스토리가 복잡해짐 |
| ✅ 롤백 용이 (`revert -m 1`) | ❌ 불필요한 머지 커밋 증가 |
| ✅ 기본 동작으로 안전 | ❌ 그래프 시각화 복잡 |
| ✅ 기능 개발 맥락 유지 | |

### 권장 상황

- 장기 개발 브랜치 통합
- release → main 머지
- 여러 사람이 작업한 feature 브랜치
- **Git Flow의 기본 전략**

---

## 3.3 Fast-Forward Merge

### 개념도

```
Before (main에서 feature가 분기, main은 진행 없음):
main:    A---B
              \
feature:       C---D

After (git merge --ff feature):
main:    A---B---C---D
              ↑
        (main 포인터만 이동)

# 결과: 분기점이 보이지 않음
```

### 조건

Fast-forward는 **main이 feature의 조상**일 때만 가능합니다.

```bash
# FF 가능한 경우
main:    A---B
              \
feature:       C---D  ✅ main(B)가 feature의 조상

# FF 불가능한 경우
main:    A---B---E
              \
feature:       C---D  ❌ main(E)이 분기됨
```

### 명령어

```bash
git checkout main
git merge --ff feature/hotfix

# FF만 허용 (불가능하면 실패)
git merge --ff-only feature/hotfix
# fatal: Not possible to fast-forward, aborting.
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 깔끔한 선형 히스토리 | ❌ 브랜치 존재 흔적 없음 |
| ✅ 머지 커밋 없음 | ❌ 기능 단위 구분 어려움 |
| ✅ 간단한 동기화에 적합 | ❌ 롤백 시 개별 커밋 revert 필요 |

### 권장 상황

- 핫픽스 적용
- upstream 동기화
- 단순한 버그 수정
- 개인 작업 브랜치

---

## 3.4 No Fast-Forward Merge

### 개념도

```
Before (FF 가능한 상황에서도):
main:    A---B
              \
feature:       C---D

After (git merge --no-ff feature):
main:    A---B-----------M
              \         /
feature:       C---D---/

# FF 가능해도 강제로 머지 커밋 생성
```

### 명령어

```bash
git checkout main
git merge --no-ff feature/user-auth

# 전역 설정 (항상 --no-ff 사용)
git config --global merge.ff false

# 프로젝트별 설정
git config merge.ff false
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 기능 단위 명확히 구분 | ❌ 커밋 수 증가 |
| ✅ 기능 롤백 용이 (`revert -m 1`) | ❌ 단순 수정에는 과함 |
| ✅ PR/MR 경계 명확 | |
| ✅ `git log --first-parent` 깔끔 | |

### 권장 상황

- **Git Flow에서 표준**
- feature → develop 머지
- release → main 머지
- 코드 리뷰 완료된 PR 머지

---

## 3.5 Squash Merge

### 개념도

```
Before:
main:    A---B---C
              \
feature:       D---E---F (3개의 WIP 커밋)

After (git merge --squash feature):
main:    A---B---C---S

S = D+E+F 변경사항을 하나로 합친 새 커밋
⚠️ feature 브랜치와 연결 없음 (부모가 C 하나)
```

### 명령어

```bash
git checkout main
git merge --squash feature/messy-commits
# 변경사항이 staged 상태로 적용됨

# 반드시 별도 커밋 필요!
git commit -m "feat: add user authentication (#123)"
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 깔끔한 main 히스토리 | ❌ 세부 커밋 이력 손실 |
| ✅ WIP 커밋 정리 불필요 | ❌ feature 브랜치와 연결 끊김 |
| ✅ 의미 있는 단위로 통합 | ❌ 재머지 시 충돌 발생 |
| ✅ git blame 단순화 | ❌ 상세 디버깅 어려움 |

### 권장 상황

- **GitHub/GitLab PR 기본 옵션**
- 실험적 커밋이 많은 브랜치
- 외부 기여자 PR 정리
- "WIP", "fixup", "tmp" 커밋 정리

### 주의사항: 재머지 문제

```bash
# 첫 번째 squash 머지
git merge --squash feature/x
git commit -m "feat: add X"

# feature/x에서 추가 작업
git checkout feature/x
# 추가 커밋...

# 두 번째 squash 머지 시도
git checkout main
git merge --squash feature/x
# ⚠️ 충돌 발생! (Git이 이미 머지된 것을 모름)

# 해결: squash 후 feature 브랜치 삭제
git branch -d feature/x
```

---

## 3.6 Rebase

### 개념도

```
Before:
main:    A---B---C
              \
feature:       D---E

After (git rebase main from feature):
main:    A---B---C
                  \
feature:           D'---E'

D', E' = D, E의 변경사항을 C 위에 재적용
⚠️ 새로운 커밋 해시! (D ≠ D')
```

### 명령어

```bash
# feature 브랜치에서 main 기준으로 rebase
git checkout feature/login
git rebase main

# 충돌 해결
git add <resolved-files>
git rebase --continue

# rebase 중단 (원래대로)
git rebase --abort

# rebase 건너뛰기 (현재 커밋 스킵)
git rebase --skip
```

### Interactive Rebase

커밋을 정리, 합치기, 수정할 수 있습니다.

```bash
git rebase -i HEAD~5
# 또는
git rebase -i main

# 에디터에서:
pick abc1234 feat: add user model
squash def5678 WIP: user validation     # 이전 커밋에 합침
reword ghi9012 fix: typo                 # 메시지 수정
drop jkl3456 debug: console logs         # 커밋 삭제
fixup mno7890 fix: minor bug             # 합치되 메시지 무시
edit pqr1234 feat: complex feature       # 커밋 분할/수정

# 옵션 설명:
# pick (p)   = 커밋 유지
# reword (r) = 커밋 유지, 메시지 수정
# edit (e)   = 커밋에서 멈춤 (수정 가능)
# squash (s) = 이전 커밋에 합침 (메시지 합침)
# fixup (f)  = 이전 커밋에 합침 (메시지 버림)
# drop (d)   = 커밋 삭제
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 완벽한 선형 히스토리 | ❌ 커밋 해시 변경됨 |
| ✅ `git log` 깔끔 | ❌ 공유 브랜치에서 위험 |
| ✅ 커밋 정리 가능 | ❌ 충돌 여러 번 해결 필요 |
| ✅ bisect 용이 | ❌ 원본 타임스탬프 손실 가능 |

### ⚠️ Golden Rule

```bash
# ❌ 절대 하면 안 되는 것
git checkout main
git rebase feature  # 공유 브랜치(main) rebase 금지!

# ✅ 올바른 사용
git checkout feature
git rebase main     # 개인 브랜치만 rebase
```

공유 브랜치를 rebase하면 다른 팀원의 히스토리와 충돌합니다.

---

## 3.7 Rebase and Merge (복합 전략)

### 워크플로우

```bash
# 1. feature 브랜치에서 main 최신화
git checkout feature/login
git fetch origin
git rebase origin/main

# 결과:
# main:    A---B---C
#                   \
# feature:           D'---E' (리베이스됨)

# 2. 충돌 해결 (있다면)
git add .
git rebase --continue

# 3. main에서 fast-forward merge
git checkout main
git merge --ff-only feature/login

# 결과:
# main:    A---B---C---D'---E'

# 4. push
git push origin main
```

### 장단점

| 장점 | 단점 |
|------|------|
| ✅ 완벽한 선형 히스토리 | ❌ 2단계 과정 필요 |
| ✅ 머지 커밋 없음 | ❌ rebase 충돌 해결 필요 |
| ✅ 각 커밋 개별 보존 | ❌ 팀 교육 필요 |
| ✅ `git bisect` 최적화 | |

### 권장 상황

- **Trunk-Based Development**
- 엄격한 선형 히스토리 정책
- 소규모 팀
- 높은 커밋 품질 요구

---

## 3.8 머지 전략 시각적 비교

```
═══════════════════════════════════════════════════════════════

원본 상태:
main:    A───B───C
              \
feature:       D───E───F

═══════════════════════════════════════════════════════════════

[1. Merge Commit]
main:    A───B───C───────────M
              \             /
feature:       D───E───F───┘
                            
특징: 머지 커밋 M 생성, 두 부모(C, F) 보유

═══════════════════════════════════════════════════════════════

[2. Fast-Forward] (C가 없는 경우만 가능)
main:    A───B───D───E───F
              
특징: main 포인터만 이동, 분기 흔적 없음

═══════════════════════════════════════════════════════════════

[3. No Fast-Forward]
main:    A───B───C───────────M
              \             /
feature:       D───E───F───┘

특징: FF 가능해도 머지 커밋 강제 생성

═══════════════════════════════════════════════════════════════

[4. Squash Merge]
main:    A───B───C───S

특징: S = D+E+F 합침, feature 연결 없음

═══════════════════════════════════════════════════════════════

[5. Rebase then Fast-Forward]
main:    A───B───C───D'───E'───F'

특징: 완전 선형, 각 커밋 보존 (해시 변경)

═══════════════════════════════════════════════════════════════
```

---

## 3.9 브랜치 전략별 권장 머지 방식

| 브랜치 전략 | 권장 머지 방식 | 이유 |
|------------|---------------|------|
| **Git Flow** | `--no-ff` | 기능/릴리즈 구분 명확 |
| **GitHub Flow** | Squash 또는 Merge | PR 단위 정리 |
| **GitLab Flow** | `--no-ff` | 환경별 추적 용이 |
| **Trunk-Based** | Rebase + FF | 선형 히스토리 |
| **Release Flow** | Cherry-pick | 선택적 배포 |

### 플랫폼별 설정

```yaml
# GitHub Repository Settings
# Settings > General > Pull Requests
☑️ Allow merge commits      # 일반 머지
☑️ Allow squash merging     # Squash 머지 (기본 선택 권장)
☐ Allow rebase merging      # Rebase 머지

# Default commit message: PR title and description

# GitLab Project Settings  
# Settings > Merge requests
Merge method: Merge commit with semi-linear history
Squash commits when merging: Encourage
Fast-forward merge: Disabled
```

---

## 3.10 머지 충돌 해결 전략

### 충돌 발생 시

```bash
git merge feature/login
# Auto-merging src/auth.js
# CONFLICT (content): Merge conflict in src/auth.js
# Automatic merge failed; fix conflicts and then commit.

# 충돌 상태 확인
git status
# both modified: src/auth.js
```

### 충돌 마커 이해

```javascript
// src/auth.js
<<<<<<< HEAD
// 현재 브랜치 (main) 버전
const timeout = 3000;
=======
// 머지 대상 브랜치 (feature/login) 버전
const timeout = 5000;
>>>>>>> feature/login
```

### 해결 방법

```bash
# 방법 1: 수동 편집
vim src/auth.js
# 충돌 마커 제거하고 원하는 코드로 수정
git add src/auth.js
git commit  # 또는 git merge --continue

# 방법 2: 특정 버전 선택
git checkout --ours src/auth.js    # 현재 브랜치 버전
git checkout --theirs src/auth.js  # 머지 대상 버전
git add src/auth.js
git commit

# 방법 3: 머지 전략 지정
git merge -X ours feature/login    # 충돌 시 현재 브랜치 우선
git merge -X theirs feature/login  # 충돌 시 대상 브랜치 우선

# 방법 4: 머지 툴 사용
git mergetool
# 설정된 머지 툴 실행 (vimdiff, meld, kdiff3 등)

# 머지 중단
git merge --abort
```

### 충돌 예방

```bash
# 머지 전 미리 충돌 확인
git merge --no-commit --no-ff feature/login
git diff --cached  # 충돌 확인
git merge --abort  # 취소

# 자주 동기화
git checkout feature/login
git merge main  # 또는 git rebase main
# 작은 충돌을 자주 해결 > 큰 충돌 한 번
```

---

# 4. DevOps Workflow 구현 시 고려사항

## 4.1 Git 이벤트 감지 포인트

| 이벤트 | Webhook 타입 | 페이로드 키 | 활용 |
|--------|-------------|------------|------|
| Push | `push` | `ref`, `commits` | 빌드 트리거 |
| Tag 생성 | `create` | `ref_type: tag` | 릴리즈 배포 |
| Tag 삭제 | `delete` | `ref_type: tag` | 정리 작업 |
| Branch 생성 | `create` | `ref_type: branch` | 프리뷰 환경 |
| Branch 삭제 | `delete` | `ref_type: branch` | 환경 정리 |
| PR Open | `pull_request` | `action: opened` | 코드 리뷰 |
| PR Merge | `pull_request` | `action: closed, merged: true` | 배포 |
| PR Comment | `issue_comment` | `action: created` | ChatOps |

## 4.2 파이프라인에서 자주 쓰는 Git 명령어

```bash
# ═══════════════════════════════════════
# 정보 추출
# ═══════════════════════════════════════
# 현재 브랜치
git rev-parse --abbrev-ref HEAD

# 커밋 해시 (전체)
git rev-parse HEAD

# 커밋 해시 (짧은 버전)
git rev-parse --short HEAD

# 최신 태그
git describe --tags --abbrev=0

# 현재 상태 설명
git describe --tags --always
# v1.2.3-5-gabc1234

# 커밋 메시지
git log -1 --format="%s"

# 작성자
git log -1 --format="%an <%ae>"

# ═══════════════════════════════════════
# 변경 감지 (모노레포)
# ═══════════════════════════════════════
# 변경된 파일 목록
git diff --name-only HEAD~1 HEAD

# 특정 경로 변경 여부
git diff --name-only HEAD~1 HEAD -- services/user/

# 마지막 태그 이후 변경사항
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# ═══════════════════════════════════════
# 브랜치/태그 패턴 매칭
# ═══════════════════════════════════════
# 특정 패턴 브랜치 존재 확인
git branch -r --list 'origin/release/*'

# 태그 패턴 확인
git tag -l 'v1.2.*'

# 머지 커밋 여부
git rev-list --merges -1 HEAD
```

## 4.3 자동화 스크립트 템플릿

### 태그 기반 배포 결정

```bash
#!/bin/bash
# deploy-by-tag.sh

TAG=$(git describe --tags --exact-match 2>/dev/null)

if [[ -z "$TAG" ]]; then
    echo "No tag on current commit"
    exit 0
fi

if [[ $TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Production release: $TAG"
    ENVIRONMENT="production"
elif [[ $TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+-rc\.[0-9]+$ ]]; then
    echo "Release candidate: $TAG"
    ENVIRONMENT="staging"
elif [[ $TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+-beta\.[0-9]+$ ]]; then
    echo "Beta release: $TAG"
    ENVIRONMENT="beta"
else
    echo "Unknown tag pattern: $TAG"
    exit 0
fi

# 버전 추출
VERSION=$(echo $TAG | sed 's/^v//')

# 배포 실행
echo "Deploying $VERSION to $ENVIRONMENT"
kubectl set image deployment/myapp app=myregistry/myapp:$TAG -n $ENVIRONMENT
```

### 모노레포 변경 감지

```bash
#!/bin/bash
# detect-changes.sh

CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

declare -A SERVICES=(
    ["user-service"]="services/user"
    ["order-service"]="services/order"
    ["payment-service"]="services/payment"
)

SERVICES_TO_BUILD=""

# 공통 라이브러리 변경 확인
if echo "$CHANGED_FILES" | grep -qE "^(libs/|shared/)"; then
    echo "Common library changed - building all services"
    SERVICES_TO_BUILD="all"
else
    # 개별 서비스 변경 감지
    for service in "${!SERVICES[@]}"; do
        path="${SERVICES[$service]}"
        if echo "$CHANGED_FILES" | grep -q "^$path/"; then
            SERVICES_TO_BUILD="$SERVICES_TO_BUILD $service"
        fi
    done
fi

echo "SERVICES_TO_BUILD=${SERVICES_TO_BUILD:-none}"
```

### 롤백 자동화

```bash
#!/bin/bash
# rollback.sh

usage() {
    echo "Usage: $0 [revert|tag] [target]"
    echo "  revert [n]     - Revert last n commits (default: 1)"
    echo "  tag [version]  - Rollback to specific tag"
    exit 1
}

case "$1" in
    revert)
        N=${2:-1}
        echo "Reverting last $N commits..."
        git revert --no-commit HEAD~$N..HEAD
        git commit -m "Rollback: revert last $N commits"
        git push origin main
        ;;
    tag)
        TARGET_TAG=${2:-$(git describe --tags --abbrev=0 HEAD^)}
        echo "Rolling back to: $TARGET_TAG"
        git revert --no-commit $TARGET_TAG..HEAD
        git commit -m "Rollback: revert to $TARGET_TAG"
        git push origin main
        ;;
    *)
        usage
        ;;
esac
```

## 4.4 체크리스트

### 태그 관리

- [ ] Annotated 태그 사용 (`git tag -a`)
- [ ] Semantic Versioning 준수
- [ ] Pre-release 태그 패턴 정의
- [ ] 태그 기반 배포 파이프라인 구성
- [ ] 태그 보호 규칙 설정

### 롤백 전략

- [ ] 프로덕션은 `git revert` 사용
- [ ] 롤백 자동화 스크립트 준비
- [ ] 머지 커밋 revert 테스트 완료
- [ ] Reflog 복구 절차 문서화
- [ ] DB 마이그레이션 롤백 절차

### 머지 전략

- [ ] 팀 브랜치 전략 결정
- [ ] 머지 방식 통일 (Squash/Merge/Rebase)
- [ ] PR 설정에서 머지 방식 제한
- [ ] 충돌 해결 가이드라인
- [ ] Protected branch 규칙 설정

---

*이전 문서: [01-cicd-gitops-scenarios.md](./01-cicd-gitops-scenarios.md)*
