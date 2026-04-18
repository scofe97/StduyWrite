# Bitbucket → GitLab 브랜치 이관 가이드

TPS 프로젝트가 Bitbucket 모노레포에서 GitLab 개별 레포로 이관되었다. Bitbucket에서 작업한 특정 브랜치(예: `release/v3.0.4.1`)의 변경 사항을 GitLab 개별 레포로 옮기는 절차를 정리한다.

## 현재 구조

| 항목 | Bitbucket | GitLab |
|------|-----------|--------|
| 경로 | `~/okestro/tps-bitbucket/` | `~/okestro/tps-gitlab2/` |
| 구조 | **모노레포** (전체 서비스 1개 `.git`) | **멀티레포** (서비스별 개별 `.git`) |
| Remote | `bitbucket.org/okestrolab/tps.git` | `gitlab.prd.console.trombone.okestro.cloud/TRB305/{service}.git` |

## 서비스 매핑 (Bitbucket 디렉토리 → GitLab 개별 레포)

| Bitbucket 디렉토리 | GitLab 레포 | 비고 |
|-------------------|-------------|------|
| `auth-api/` | `tps-gitlab2/auth-api/` | |
| `common-api/` | `tps-gitlab2/common-api/` | |
| `core-lib/` | `tps-gitlab2/core-lib/` | |
| `notificator/` | `tps-gitlab2/notificator/` | |
| `pipeline-api/` | `tps-gitlab2/pipeline-api/` | |
| `pms-api/` | `tps-gitlab2/pms-api/` | |
| `ppln-logging-api/` | `tps-gitlab2/ppln-logging-api/` | |
| `react-app/` | `tps-gitlab2/react-app/` | |
| `scheduler/` | `tps-gitlab2/scheduler/` | |
| `workflow-api/` | `tps-gitlab2/workflow-api/` | |
| `api-gateway/` | — | GitLab에 없음 |
| `cloud-config/` | — | GitLab에 없음 |
| `core-persistence/` | — | GitLab에 없음 |
| `service-discovery-server/` | — | GitLab에 없음 |

---

## 이관 절차

### Step 1. 이관 대상 변경 사항 파악

Bitbucket 모노레포에서 해당 브랜치의 서비스별 변경 파일을 확인한다.

```bash
cd ~/okestro/tps-bitbucket
git checkout release/v3.0.4.1

# develop 대비 변경된 파일 목록 (서비스별 그룹핑)
git diff origin/develop --name-only | sort
```

서비스별로 변경 파일을 분류한다:
```bash
# 예시: workflow-api 변경 파일만 확인
git diff origin/develop --name-only -- workflow-api/

# 예시: react-app 변경 파일만 확인
git diff origin/develop --name-only -- react-app/
```

### Step 2. 서비스별 패치 추출

각 서비스 디렉토리의 변경 사항을 패치 파일로 추출한다.

```bash
# 서비스별 패치 생성 (경로 prefix 제거)
BRANCH="release/v3.0.4.1"
BASE="origin/develop"

for SERVICE in workflow-api pipeline-api react-app common-api; do
  # 변경이 있는 서비스만 패치 생성
  if git diff $BASE -- $SERVICE/ | grep -q '^diff'; then
    git diff $BASE -- $SERVICE/ > /tmp/tps-patch-${SERVICE}.patch
    echo "✅ ${SERVICE}: 패치 생성"
  else
    echo "⏭️ ${SERVICE}: 변경 없음"
  fi
done
```

> **주의**: `BASE`는 Bitbucket 브랜치가 분기된 시점에 맞춰야 한다. `origin/develop`이 아닐 수 있으므로 `git merge-base`로 정확한 분기점을 확인할 것.

```bash
# 정확한 분기점 확인
git merge-base origin/develop release/v3.0.4.1
```

### Step 3. GitLab 개별 레포에 브랜치 생성 및 패치 적용

```bash
cd ~/okestro/tps-gitlab2

for SERVICE in workflow-api pipeline-api react-app common-api; do
  PATCH="/tmp/tps-patch-${SERVICE}.patch"
  if [ -f "$PATCH" ]; then
    cd ~/okestro/tps-gitlab2/${SERVICE}

    # 1) 최신 dev 브랜치에서 릴리스 브랜치 생성
    git checkout dev
    git pull
    git checkout -b release/v3.0.4.1

    # 2) 패치 적용 (경로에서 서비스 디렉토리 prefix 제거)
    # git diff 출력의 경로가 "workflow-api/src/..." 형태이므로 -p1 + strip
    git apply --stat "$PATCH" -p2  # dry-run: 적용될 파일 확인
    git apply "$PATCH" -p2         # 실제 적용

    # 3) 커밋 & 푸시
    git add -A
    git commit -m "release/v3.0.4.1 변경사항 이관 (from Bitbucket)"
    git push -u origin release/v3.0.4.1

    echo "✅ ${SERVICE}: 이관 완료"
    cd ~/okestro/tps-gitlab2
  fi
done
```

### Step 4. 커밋 단위 보존이 필요한 경우 (선택)

패치 방식은 변경 사항을 1개 커밋으로 뭉친다. 원본 커밋 히스토리를 보존하려면 `format-patch`를 사용한다.

```bash
cd ~/okestro/tps-bitbucket
BASE=$(git merge-base origin/develop release/v3.0.4.1)

# 브랜치의 모든 커밋을 패치 시리즈로 추출
git format-patch $BASE..release/v3.0.4.1 -- workflow-api/ -o /tmp/patches-workflow-api/
```

GitLab 레포에 적용:
```bash
cd ~/okestro/tps-gitlab2/workflow-api
git checkout -b release/v3.0.4.1

# 패치 시리즈 적용 (커밋 메시지, 작성자 보존)
git am --directory=. -p2 /tmp/patches-workflow-api/*.patch
```

> `git am`은 충돌 시 중단된다. 충돌 발생 시 수동 해결 후 `git am --continue`.

---

## 주의사항

1. **경로 strip level (`-p` 옵션)**
   - Bitbucket 모노레포의 경로: `workflow-api/src/main/...`
   - GitLab 개별 레포의 경로: `src/main/...`
   - `git apply -p2` 또는 `git am -p2`로 첫 번째 디렉토리(서비스명)를 제거해야 한다

2. **Base 브랜치 불일치**
   - Bitbucket `develop`과 GitLab `dev`의 코드가 다를 수 있다
   - 패치 적용 전 `git apply --check`로 충돌 여부를 먼저 확인할 것

3. **루트 레벨 파일**
   - `build.gradle`, `settings.gradle` 등 모노레포 루트 파일은 이관 대상이 아님
   - `git diff` 시 `-- workflow-api/` 처럼 서비스 디렉토리를 명시해야 루트 파일이 빠짐

4. **GitLab에 없는 서비스**
   - `api-gateway`, `cloud-config`, `core-persistence`, `service-discovery-server`는 GitLab에 없으므로 이관 불가 (별도 레포 생성 필요 여부 확인)

5. **application-local.yml 등 로컬 설정**
   - 환경별 설정 파일은 이관 대상에서 제외하거나, 이관 후 GitLab 환경에 맞게 수정할 것

---

## 검증 체크리스트

- [ ] 각 GitLab 레포에서 `release/v3.0.4.1` 브랜치 존재 확인
- [ ] `git diff dev..release/v3.0.4.1`로 변경 사항이 Bitbucket과 일치하는지 대조
- [ ] 빌드 확인 (특히 `core-lib` 의존성 버전 일치 여부)
