# CI/CD 및 GitOps Git 시나리오

> **목적**: DevOps Workflow 제품 개발을 위한 빌드/배포/롤백 Git 시나리오 정리
> **작성일**: 2024-12-28

---

## 목차

1. [브랜치 전략 기반 빌드 트리거](#1-브랜치-전략-기반-빌드-트리거)
2. [태그 기반 배포 시나리오](#2-태그-기반-배포-시나리오)
3. [롤백 시나리오](#3-롤백-시나리오)
4. [GitOps 매니페스트 업데이트 시나리오](#4-gitops-매니페스트-업데이트-시나리오)
5. [멀티 환경 배포 시나리오](#5-멀티-환경-배포-시나리오)
6. [핫픽스 시나리오](#6-핫픽스-시나리오)
7. [Feature Flag / Canary 배포 시나리오](#7-feature-flag--canary-배포-시나리오)
8. [모노레포 시나리오](#8-모노레포-시나리오)
9. [배포 승인/게이트 시나리오](#9-배포-승인게이트-시나리오)
10. [인프라 as Code (IaC) 시나리오](#10-인프라-as-code-iac-시나리오)
11. [시크릿/설정 관리 시나리오](#11-시크릿설정-관리-시나리오)
12. [긴급 상황 시나리오](#12-긴급-상황-시나리오)
13. [시나리오 요약 표](#13-시나리오-요약-표)

---

# 1. 브랜치 전략 기반 빌드 트리거

## 1.1 Git Flow 기반

```bash
# Feature 브랜치 생성 → CI 트리거
git checkout -b feature/user-auth develop
git push origin feature/user-auth
# → PR 생성 시 린트/테스트/빌드 자동 실행

# Develop 머지 → Staging 자동 배포
git checkout develop
git merge feature/user-auth
git push origin develop
# → develop 브랜치 push 감지 → staging 환경 배포

# Release 브랜치 생성 → QA 환경 배포
git checkout -b release/v1.2.0 develop
git push origin release/v1.2.0
# → release/* 브랜치 감지 → QA 환경 배포

# Main 머지 → Production 배포
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags
# → main push + 태그 → Production 배포
```

## 1.2 Trunk-Based Development

```bash
# 짧은 수명의 feature 브랜치 (1-2일)
git checkout -b feat/login main
# 작업 완료
git checkout main
git merge feat/login
git push origin main
# → main push마다 빌드 + Canary 배포

# Feature Flag 활용
git commit -m "feat: add payment [flag:payment-v2]"
git push origin main
# → 기능은 배포되지만 flag로 비활성화
```

## 1.3 GitHub Flow

```bash
git checkout -b feature/payment main
git push origin feature/payment
# → PR 생성 → CI 자동 실행 (린트, 테스트, 빌드)
# → 코드 리뷰
# → PR 승인 후 main 머지 → 프로덕션 배포
```

## 1.4 GitLab Flow

```bash
# Feature → main
git checkout -b feature/api main
git push origin feature/api
# → MR 생성 → CI 실행

# main → pre-production (스테이징)
git checkout pre-production
git merge main
git push origin pre-production
# → pre-production push → Staging 배포

# pre-production → production
git checkout production
git merge pre-production
git push origin production
# → production push → Production 배포
```

## 1.5 Release Flow (Microsoft)

```bash
# main에서 직접 개발
git checkout main
git commit -m "feat: new feature"
git push origin main
# → CI 빌드만

# 릴리즈 브랜치 생성 (배포 시점)
git checkout -b release/2024-Q4 main
git push origin release/2024-Q4
# → release/* push → Production 배포

# 핫픽스는 release 브랜치에 cherry-pick
git checkout release/2024-Q4
git cherry-pick <hotfix-commit>
git push origin release/2024-Q4
```

---

# 2. 태그 기반 배포 시나리오

## 2.1 Semantic Versioning 릴리즈

```bash
# 정식 릴리즈 → Production
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0
# → v*.*.* 태그 감지 → Production 배포

# Pre-release → Staging
git tag -a v1.2.0-rc.1 -m "Release candidate 1"
git push origin v1.2.0-rc.1
# → *-rc.* 태그 감지 → Staging 배포

# Beta → Beta 환경
git tag -a v1.2.0-beta.1 -m "Beta release"
git push origin v1.2.0-beta.1
# → *-beta.* 태그 감지 → Beta 환경 배포

# Alpha → Dev 환경
git tag -a v1.2.0-alpha.1 -m "Alpha release"
git push origin v1.2.0-alpha.1
# → *-alpha.* 태그 감지 → Dev 환경 배포
```

## 2.2 CalVer (Calendar Versioning)

```bash
# 날짜 기반 버전
git tag -a 2024.12.28 -m "Daily release"
git push origin 2024.12.28

# 날짜 + 빌드 번호
git tag -a 2024.12.28-1 -m "First release of the day"
git tag -a 2024.12.28-2 -m "Second release of the day"
```

## 2.3 환경별 배포 태그

```bash
# 환경 명시적 태그
git tag -a deploy/staging/20241228-1 -m "Staging deployment"
git push origin deploy/staging/20241228-1
# → deploy/staging/* 감지 → Staging 배포

git tag -a deploy/prod/20241228-1 -m "Production deployment"
git push origin deploy/prod/20241228-1
# → deploy/prod/* 감지 → Production 배포
```

## 2.4 서비스별 태그 (모노레포)

```bash
# 서비스별 독립 버전
git tag -a user-service/v1.2.0 -m "User service release"
git tag -a order-service/v2.0.0 -m "Order service release"
git tag -a payment-service/v1.5.0 -m "Payment service release"
git push origin --tags
# → 각 서비스별 파이프라인 트리거
```

---

# 3. 롤백 시나리오

## 3.1 Git Revert 롤백 (권장)

```bash
# 최신 커밋 롤백
git revert HEAD
git push origin main
# → 새 revert 커밋 생성 → 자동 재배포

# 특정 커밋 롤백
git revert <problematic-commit-hash>
git push origin main

# 여러 커밋 롤백
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert: rollback last 3 commits due to bug"
git push origin main

# 머지 커밋 롤백
git revert -m 1 <merge-commit-hash>
git push origin main
```

## 3.2 Git Reset 롤백 (주의 필요)

```bash
# 특정 커밋으로 하드 리셋
git reset --hard <stable-commit-hash>
git push --force origin main
# → 이력 변경 → GitOps 감지 → 이전 상태로 배포

# 이전 태그로 리셋
git reset --hard v1.1.0
git push --force origin main

# Force with lease (더 안전)
git push --force-with-lease origin main
```

## 3.3 태그 기반 롤백

```bash
# 방법 1: 이전 태그를 새 태그로 재지정
git tag -a v1.2.1 v1.1.0^{} -m "Rollback to v1.1.0"
git push origin v1.2.1
# → 새 태그 감지 → v1.1.0 내용으로 배포

# 방법 2: 롤백 태그 생성
git tag -a rollback/v1.2.0-to-v1.1.0 v1.1.0 -m "Emergency rollback"
git push origin rollback/v1.2.0-to-v1.1.0
```

## 3.4 GitOps 매니페스트 롤백

```bash
# ArgoCD/Flux 매니페스트 저장소에서
git revert <deployment-manifest-commit>
git push origin main
# → GitOps 컨트롤러가 이전 이미지 태그로 재배포

# 또는 직접 이미지 태그 변경
yq -i '.spec.template.spec.containers[0].image = "myapp:v1.1.0"' deployment.yaml
git commit -am "rollback: revert to v1.1.0"
git push origin main
```

## 3.5 Cherry-pick 롤백

```bash
# 특정 수정사항만 선택적으로 롤백
git checkout main
git cherry-pick --no-commit -n <revert-commit-from-develop>
git commit -m "Selective rollback: remove problematic feature"
git push origin main
```

---

# 4. GitOps 매니페스트 업데이트 시나리오

## 4.1 이미지 태그 자동 업데이트

```bash
# CI에서 빌드 완료 후 매니페스트 저장소 업데이트
git clone git@github.com:org/k8s-manifests.git
cd k8s-manifests

# Kustomize 방식
cd overlays/production
kustomize edit set image myapp=myregistry/myapp:v1.2.0
git add .
git commit -m "chore: update myapp image to v1.2.0"
git push origin main
# → ArgoCD/Flux가 변경 감지 → 자동 동기화
```

## 4.2 Helm Values 업데이트

```bash
# values.yaml 이미지 태그 수정
yq -i '.image.tag = "v1.2.0"' charts/myapp/values-prod.yaml
git add .
git commit -m "chore: bump myapp to v1.2.0"
git push origin main

# 또는 sed 사용
sed -i 's/tag: .*/tag: v1.2.0/' charts/myapp/values-prod.yaml
```

## 4.3 PR 기반 GitOps (안전한 방식)

```bash
# 자동 PR 생성
git checkout -b update/myapp-v1.2.0
# 매니페스트 수정
git commit -m "chore: update myapp to v1.2.0"
git push origin update/myapp-v1.2.0
# → PR 생성 → 자동 diff 확인 → 리뷰 → 승인 후 머지 → 배포
```

## 4.4 환경별 순차 업데이트

```bash
# 1단계: Dev 환경
yq -i '.image.tag = "v1.2.0"' overlays/dev/kustomization.yaml
git commit -am "deploy(dev): update to v1.2.0"
git push origin main

# 검증 후 2단계: Staging 환경
yq -i '.image.tag = "v1.2.0"' overlays/staging/kustomization.yaml
git commit -am "deploy(staging): update to v1.2.0"
git push origin main

# 검증 후 3단계: Production 환경
yq -i '.image.tag = "v1.2.0"' overlays/production/kustomization.yaml
git commit -am "deploy(prod): update to v1.2.0"
git push origin main
```

---

# 5. 멀티 환경 배포 시나리오

## 5.1 브랜치 기반 환경 매핑

```bash
# develop 브랜치 → Dev 환경
git checkout develop
git merge feature/new-api
git push origin develop
# → develop push 감지 → dev 클러스터 배포

# staging 브랜치 → Staging 환경
git checkout staging
git merge develop
git push origin staging
# → staging push 감지 → staging 클러스터 배포

# main 브랜치 → Production 환경
git checkout main
git merge staging
git push origin main
# → main push 감지 → production 클러스터 배포
```

## 5.2 디렉토리 기반 환경 분리 (Kustomize)

```
k8s-manifests/
├── base/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   └── kustomization.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── production/
        └── kustomization.yaml
```

```bash
# 특정 환경만 업데이트
cd overlays/dev
kustomize edit set image myapp=myregistry/myapp:v1.2.0-dev
git add overlays/dev/
git commit -m "deploy(dev): update to v1.2.0-dev"
git push origin main
# → ArgoCD가 dev 앱만 동기화 (path 기반 필터)
```

## 5.3 프로모션 시나리오

```bash
# Dev → Staging 프로모션
git checkout main
cp overlays/dev/kustomization.yaml overlays/staging/
# 또는 이미지 태그만 복사
DEV_TAG=$(yq '.images[0].newTag' overlays/dev/kustomization.yaml)
yq -i ".images[0].newTag = \"$DEV_TAG\"" overlays/staging/kustomization.yaml
git commit -m "promote: dev to staging ($DEV_TAG)"
git push origin main

# Staging → Production 프로모션
STAGING_TAG=$(yq '.images[0].newTag' overlays/staging/kustomization.yaml)
yq -i ".images[0].newTag = \"$STAGING_TAG\"" overlays/production/kustomization.yaml
git commit -m "promote: staging to production ($STAGING_TAG)"
git push origin main
```

## 5.4 Region별 배포

```bash
# 멀티 리전 구조
overlays/
├── prod-us-east/
├── prod-us-west/
├── prod-eu-west/
└── prod-ap-northeast/

# US-East 먼저 배포
yq -i '.image.tag = "v1.2.0"' overlays/prod-us-east/kustomization.yaml
git commit -am "deploy(us-east): canary v1.2.0"
git push origin main

# 검증 후 나머지 리전
for region in prod-us-west prod-eu-west prod-ap-northeast; do
  yq -i '.image.tag = "v1.2.0"' overlays/$region/kustomization.yaml
done
git commit -am "deploy(global): rollout v1.2.0"
git push origin main
```

---

# 6. 핫픽스 시나리오

## 6.1 Git Flow 핫픽스

```bash
# Production 긴급 버그 수정
git checkout -b hotfix/critical-bug main
# 버그 수정 작업
git commit -m "fix: critical security vulnerability CVE-2024-XXXX"

# main에 머지 → Production 즉시 배포
git checkout main
git merge --no-ff hotfix/critical-bug
git tag -a v1.1.1 -m "Hotfix release v1.1.1"
git push origin main --tags
# → Production 즉시 배포

# develop에도 머지 → 동기화
git checkout develop
git merge --no-ff hotfix/critical-bug
git push origin develop

# 핫픽스 브랜치 삭제
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

## 6.2 Cherry-pick 핫픽스

```bash
# develop의 특정 수정사항만 main에 적용
git checkout main
git cherry-pick <fix-commit-hash>
git push origin main
# → Production 배포

# 여러 커밋 cherry-pick
git cherry-pick <commit1> <commit2> <commit3>

# 충돌 시
git cherry-pick <commit-hash>
# CONFLICT 발생
git status
# 충돌 해결
git add .
git cherry-pick --continue
```

## 6.3 핫픽스 후 Release 브랜치 동기화

```bash
# 현재 릴리즈 브랜치가 있는 경우
git checkout release/v1.2.0
git cherry-pick <hotfix-commit>
git push origin release/v1.2.0

# 또는 main에서 머지
git checkout release/v1.2.0
git merge main
git push origin release/v1.2.0
```

---

# 7. Feature Flag / Canary 배포 시나리오

## 7.1 Feature 브랜치 미리보기 환경

```bash
git checkout -b feature/new-ui
git push origin feature/new-ui
# → CI가 자동으로 미리보기 환경 생성
# → URL: feature-new-ui.preview.myapp.com
# → PR에 미리보기 URL 코멘트 자동 추가

# PR 닫히면
git checkout main
git branch -d feature/new-ui
git push origin --delete feature/new-ui
# → 미리보기 환경 자동 삭제
```

## 7.2 Canary 배포 트리거

```bash
# 방법 1: 커밋 메시지 기반
git commit -m "feat: new checkout flow [canary:10%]"
git push origin main
# → CI가 메시지 파싱 → 10% 트래픽만 새 버전

# 방법 2: 별도 브랜치
git checkout -b canary/new-feature main
git push origin canary/new-feature
# → canary/* 브랜치 감지 → Canary 배포 (5% 시작)

# 방법 3: 태그 기반
git tag -a v1.2.0-canary -m "Canary release"
git push origin v1.2.0-canary
```

## 7.3 점진적 롤아웃

```bash
# GitOps 매니페스트에서 가중치 조절
# 10% → 25% → 50% → 100%

# 10% 배포
yq -i '.spec.strategy.canary.steps[0].setWeight = 10' rollout.yaml
git commit -am "canary: 10% traffic"
git push origin main

# 모니터링 후 25%로 증가
yq -i '.spec.strategy.canary.steps[0].setWeight = 25' rollout.yaml
git commit -am "canary: increase to 25%"
git push origin main

# 문제 발생 시 롤백
yq -i '.spec.strategy.canary.steps[0].setWeight = 0' rollout.yaml
git commit -am "canary: abort - rollback to stable"
git push origin main
```

## 7.4 A/B 테스트 배포

```bash
# 버전 A, B 동시 배포
git tag -a v1.2.0-variant-a -m "Variant A"
git tag -a v1.2.0-variant-b -m "Variant B"
git push origin --tags

# 매니페스트에서 트래픽 분배
# variant-a: 50%, variant-b: 50%
```

---

# 8. 모노레포 시나리오

## 8.1 경로 기반 빌드 트리거

```bash
# 변경된 파일 확인
git diff --name-only HEAD~1 HEAD

# 결과에 따라 선택적 빌드
# services/user-service/** 변경 → user-service만 빌드
# services/order-service/** 변경 → order-service만 빌드
# shared/** 변경 → 전체 서비스 빌드
# libs/common/** 변경 → 의존하는 모든 서비스 빌드
```

## 8.2 서비스별 태그

```bash
git tag -a user-service/v1.2.0 -m "User service release"
git tag -a order-service/v2.0.0 -m "Order service release"
git tag -a payment-service/v1.5.0 -m "Payment service release"
git push origin --tags
# → 각 서비스별 독립 배포 파이프라인 트리거
```

## 8.3 영향받는 서비스 자동 감지

```bash
#!/bin/bash
# detect-affected-services.sh

CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD)

SERVICES_TO_BUILD=""

# 공통 라이브러리 변경 시 전체 빌드
if echo "$CHANGED_FILES" | grep -q "^libs/"; then
  SERVICES_TO_BUILD="all"
else
  # 개별 서비스 변경 감지
  for service in user-service order-service payment-service; do
    if echo "$CHANGED_FILES" | grep -q "^services/$service/"; then
      SERVICES_TO_BUILD="$SERVICES_TO_BUILD $service"
    fi
  done
fi

echo "Services to build: $SERVICES_TO_BUILD"
```

## 8.4 의존성 기반 빌드

```bash
# 의존성 그래프 기반 빌드
# user-service → common-lib
# order-service → common-lib, user-client
# payment-service → common-lib, order-client

# common-lib 변경 시 → 모든 서비스 빌드
# user-client 변경 시 → order-service만 빌드
```

---

# 9. 배포 승인/게이트 시나리오

## 9.1 머지 후 수동 승인

```bash
git checkout main
git merge feature/risky-change
git push origin main
# → CI 빌드 완료
# → 배포 파이프라인 "Pending Approval" 상태
# → 승인자가 UI에서 승인
# → 배포 진행
```

## 9.2 환경별 게이트

```bash
git push origin main
# → Dev: 자동 배포 (게이트 없음)
# → Staging: 자동 배포 + 스모크 테스트
# → Production: 수동 승인 대기 → 승인 → 배포
```

## 9.3 시간 기반 게이트

```bash
# 배포 가능 시간 제한
# 평일 09:00-17:00 KST만 Production 배포 허용

git push origin main
# 금요일 18:00 push → Production 배포 대기열에 추가
# 월요일 09:00 자동 배포 시작
```

## 9.4 품질 게이트

```bash
git push origin main
# → 빌드
# → 유닛 테스트 (커버리지 80% 이상 필수)
# → 통합 테스트
# → 보안 스캔 (Critical 취약점 0개 필수)
# → 성능 테스트 (P95 < 200ms 필수)
# → 모든 게이트 통과 시 배포 승인 요청
```

## 9.5 롤백 승인 면제

```bash
# 롤백은 승인 없이 즉시 실행 (긴급 상황)
git revert HEAD
git commit -m "EMERGENCY ROLLBACK: revert v1.2.0"
git push origin main
# → "EMERGENCY" 키워드 감지 → 승인 스킵 → 즉시 배포
```

---

# 10. 인프라 as Code (IaC) 시나리오

## 10.1 Terraform GitOps

```bash
# 인프라 변경 PR
git checkout -b infra/add-redis-cluster
# terraform 파일 수정
git add terraform/
git commit -m "infra: add Redis cluster for session storage"
git push origin infra/add-redis-cluster

# → PR 생성
# → terraform plan 자동 실행
# → plan 결과 PR에 코멘트로 추가
# → 리뷰어 확인 및 승인
# → PR 머지
# → terraform apply 자동 실행
```

## 10.2 Terraform Workspace별 배포

```bash
# 환경별 workspace
terraform/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/

# dev 환경 변경
git checkout -b infra/dev-scaling
cd terraform/environments/dev
# 수정
git commit -am "infra(dev): increase instance count"
git push origin infra/dev-scaling
# → dev workspace에만 apply
```

## 10.3 Ansible Playbook 배포

```bash
git tag -a ansible/v1.0.0 -m "Ansible playbook release"
git push origin ansible/v1.0.0
# → Ansible AWX/Tower가 태그 감지
# → 플레이북 자동 실행
```

## 10.4 Pulumi GitOps

```bash
git checkout -b infra/add-cdn
# Pulumi 코드 수정 (TypeScript/Python/Go)
git commit -am "infra: add CloudFront CDN"
git push origin infra/add-cdn

# → PR 생성
# → pulumi preview 실행
# → PR 머지
# → pulumi up 자동 실행
```

---

# 11. 시크릿/설정 관리 시나리오

## 11.1 Sealed Secrets 업데이트

```bash
# 평문 시크릿 생성 (로컬에서만)
kubectl create secret generic db-creds \
  --from-literal=username=admin \
  --from-literal=password=secret123 \
  --dry-run=client -o yaml > secret.yaml

# Sealed Secret으로 암호화
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Git에 암호화된 시크릿만 커밋
git add sealed-secret.yaml
git commit -m "chore: update database credentials"
git push origin main
# → GitOps가 sealed secret 배포
# → 클러스터의 Sealed Secrets Controller가 복호화
```

## 11.2 External Secrets 업데이트

```bash
# ExternalSecret 리소스 업데이트 (AWS Secrets Manager 참조)
cat > external-secret.yaml << EOF
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: prod/db/password
EOF

git add external-secret.yaml
git commit -m "chore: add external secret reference"
git push origin main
```

## 11.3 ConfigMap 업데이트

```bash
# 설정 변경
git checkout -b config/update-feature-flags
# configmap.yaml 수정
cat > configmap.yaml << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  NEW_CHECKOUT_ENABLED: "true"
  DARK_MODE_ENABLED: "false"
EOF

git add configmap.yaml
git commit -m "config: enable new checkout feature"
git push origin config/update-feature-flags
# → PR 리뷰 → 머지 → 설정 자동 반영
```

## 11.4 환경별 설정 관리

```bash
# Kustomize로 환경별 ConfigMap 오버라이드
overlays/
├── dev/
│   └── configmap-patch.yaml
├── staging/
│   └── configmap-patch.yaml
└── production/
    └── configmap-patch.yaml

# 각 환경별 설정 업데이트
echo 'LOG_LEVEL: debug' >> overlays/dev/configmap-patch.yaml
git commit -am "config(dev): enable debug logging"
git push origin main
```

---

# 12. 긴급 상황 시나리오

## 12.1 배포 프리즈 (Freeze)

```bash
# 모든 배포 즉시 중단
git tag -a deploy-freeze -m "Emergency: deployment freeze due to incident"
git push origin deploy-freeze
# → CI/CD가 태그 감지 → 모든 배포 파이프라인 중단

# 프리즈 해제
git tag -d deploy-freeze
git push origin :refs/tags/deploy-freeze
# 또는
git tag -a deploy-unfreeze -m "Incident resolved, resuming deployments"
git push origin deploy-unfreeze
```

## 12.2 즉시 롤백

```bash
# 방법 1: Git Revert
git revert HEAD --no-edit
git push origin main
# → 30초 내 이전 버전 복구

# 방법 2: 이전 태그로 재배포
PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^)
git tag -a emergency-rollback -m "Rollback to $PREVIOUS_TAG" $PREVIOUS_TAG
git push origin emergency-rollback

# 방법 3: GitOps 매니페스트 직접 수정
cd k8s-manifests
git revert HEAD
git push origin main
```

## 12.3 특정 서비스만 긴급 롤백

```bash
# 모노레포에서 특정 서비스만
git checkout main
git revert <user-service-deploy-commit> --no-edit
git push origin main

# GitOps 매니페스트에서
yq -i '.image.tag = "v1.1.0"' overlays/production/user-service/kustomization.yaml
git commit -am "EMERGENCY: rollback user-service to v1.1.0"
git push origin main
```

## 12.4 데이터베이스 마이그레이션 포함 롤백

```bash
# 1. 애플리케이션 트래픽 차단
kubectl scale deployment myapp --replicas=0

# 2. DB 롤백 마이그레이션 실행
kubectl exec -it db-migration-pod -- ./migrate down -steps=1

# 3. 이전 버전 애플리케이션 배포
git revert HEAD
git push origin main

# 4. 트래픽 복구
kubectl scale deployment myapp --replicas=3
```

## 12.5 Blue-Green 긴급 스위치

```bash
# 현재: Green (v1.2.0) 활성
# Blue (v1.1.0) 대기 중

# 즉시 Blue로 스위치
kubectl patch service myapp -p '{"spec":{"selector":{"version":"blue"}}}'

# 또는 GitOps로
yq -i '.spec.selector.version = "blue"' service.yaml
git commit -am "EMERGENCY: switch to blue (v1.1.0)"
git push origin main
```

---

# 13. 시나리오 요약 표

## 브랜치/태그별 배포 트리거

| 이벤트 | 패턴 | 타겟 환경 | 배포 방식 |
|--------|------|----------|----------|
| Push | `feature/*` | - | 빌드/테스트만 |
| Push | `develop` | Dev | 자동 배포 |
| Push | `staging` | Staging | 자동 배포 |
| Push | `main` | Production | 수동 승인 후 배포 |
| Tag | `v*.*.*` | Production | 자동 배포 |
| Tag | `v*.*.*-rc.*` | Staging | 자동 배포 |
| Tag | `v*.*.*-beta.*` | Beta | 자동 배포 |
| Tag | `deploy-freeze` | All | 배포 중단 |

## 롤백 방식 비교

| 상황 | 권장 방식 | 명령어 |
|------|----------|--------|
| 최신 배포 롤백 | Revert | `git revert HEAD` |
| 특정 기능 롤백 | Revert merge | `git revert -m 1 <merge>` |
| 여러 커밋 롤백 | Range revert | `git revert HEAD~n..HEAD` |
| 긴급 롤백 | Tag 재배포 | 이전 태그로 재배포 |
| GitOps 롤백 | Manifest revert | 매니페스트 변경 |

## Git 이벤트 → CI/CD 액션 매핑

| Git 이벤트 | 감지 방법 | CI/CD 액션 |
|-----------|----------|-----------|
| Branch push | Webhook `push` | 빌드, 테스트 |
| Tag create | Webhook `create` | 릴리즈 배포 |
| PR open | Webhook `pull_request` | 코드 리뷰 트리거 |
| PR merge | Webhook `push` (merge commit) | 환경 배포 |
| Branch delete | Webhook `delete` | 프리뷰 환경 정리 |

---

*다음 문서: [02-git-concepts-tag-rollback-merge.md](./02-git-concepts-tag-rollback-merge.md)*
