# Ch05. 멀티 도구 CI/CD 구축 — 심화 탐구

LEARN.md의 개념을 검증하고 실무 판단력을 기르기 위한 질문들이다.
각 질문에 직접 답하고 나서 아래 힌트와 비교해 본다.

---

## Q1. GitHub Actions의 Runner 아키텍처: Hosted vs Self-hosted

**탐구 질문**: `ubuntu-latest` runner와 self-hosted runner의 실행 환경은 어떻게 다른가? 언제 self-hosted를 선택하는 것이 합리적인가?

**탐구 방향**:
- GitHub-hosted runner가 Job마다 새 VM을 제공하는 것과 self-hosted가 기존 머신에서 실행되는 차이를 비교한다.
- `ubuntu-latest`가 구체적으로 어떤 버전을 가리키는지, 그리고 버전 고정이 필요한 이유를 생각해 본다.
- 프라이빗 네트워크 내 자원(온프레미스 DB, 내부 아티팩트 저장소)에 접근해야 하는 파이프라인에서 hosted runner가 가진 한계를 정리한다.

**핵심 판단 기준**:

| 상황 | 선택 |
|------|------|
| 퍼블릭 저장소, 표준 빌드 | GitHub-hosted |
| 프라이빗 네트워크 접근 필요 | Self-hosted |
| GPU 빌드, 특수 하드웨어 | Self-hosted |
| 빌드 시간이 길고 비용 민감 | Self-hosted (월 2,000분 무료 한도 초과 시) |
| 빠른 캐시 재사용이 중요 | Self-hosted (디스크 영구 유지) |

**확인할 것**: `runs-on: self-hosted` 레이블 설정 방법과 runner 등록 절차를 GitHub 공식 문서에서 확인하고, runner 그룹으로 환경별 접근을 제어하는 방법을 찾아본다.

---

## Q2. OIDC 인증이 Static Secret보다 나은 이유

**탐구 질문**: `AWS_ACCESS_KEY_ID`와 `AWS_SECRET_ACCESS_KEY`를 GitHub Secrets에 저장하는 방식과 OIDC AssumeRole 방식의 보안 차이는 무엇인가?

**탐구 방향**:
- 정적 자격증명이 유출되는 시나리오를 구체적으로 나열한다 (로그 출력, 포크된 저장소의 PR, 퇴직한 직원의 접근 등).
- OIDC JWT가 발급되고 AWS가 이를 검증하는 흐름을 단계별로 그려본다: `GitHub OIDC Provider → JWT 발급 → AWS IAM OIDC Provider → AssumeRoleWithWebIdentity → 임시 STS 토큰`.
- `role-to-assume`의 Trust Policy에서 `token.actions.githubusercontent.com:sub` 조건으로 특정 저장소/브랜치만 허용하는 설정을 찾아본다.

**핵심 차이**:

| 항목 | Static Secret | OIDC |
|------|--------------|------|
| 유효 기간 | 만료 없음 (수동 로테이션) | 최대 1시간, 파이프라인 완료 시 무효화 |
| 저장 위치 | GitHub Secrets DB | 저장 없음 (런타임 발급) |
| 유출 시 피해 | 즉시 전체 권한 노출 | 유출된 토큰은 짧은 시간 후 만료 |
| 감사 로그 | IAM 사용자 단위 | Job 단위 (저장소/브랜치 조건 포함) |

**확인할 것**: AWS IAM Trust Policy에서 `StringLike` 조건으로 `repo:my-org/my-repo:ref:refs/heads/main`만 허용하는 설정 예시를 작성해 본다.

---

## Q3. Push-based vs Pull-based CD의 트레이드오프

**탐구 질문**: 소규모 팀이 시작할 때 GitHub Actions로 직접 `kubectl apply`하는 방식과 ArgoCD를 도입하는 방식 중 어떤 것이 나은가? 그 판단 기준은 무엇인가?

**탐구 방향**:
- Push-based에서 CI 서버가 클러스터에 접근하려면 kubeconfig나 ServiceAccount 토큰을 외부에 저장해야 한다. 이 자격증명이 탈취되면 어떤 일이 일어나는지 생각해 본다.
- Pull-based에서 ArgoCD는 클러스터 내부에서 Git을 폴링한다. 클러스터가 인터넷 없는 에어갭 환경이더라도 동작한다는 점이 왜 중요한지 파악한다.
- "드리프트"가 무엇인지 정의하고, 수동으로 `kubectl edit`한 내용이 Pull-based에서 어떻게 처리되는지 확인한다.

**실무 결정 트리**:
- 클러스터 1개, 팀 3명, 빠른 출시 필요 → Push-based로 시작
- 클러스터 3개 이상 또는 강한 컴플라이언스 요구 → ArgoCD 도입
- 온프레미스 에어갭 환경 → ArgoCD 필수

---

## Q4. ArgoCD의 Sync 전략: Auto vs Manual, Prune

**탐구 질문**: `automated.selfHeal: true`와 `automated.prune: true`를 프로덕션에 적용할 때 어떤 위험이 있는가? 어떻게 안전하게 설정하는가?

**탐구 방향**:
- `selfHeal: true`가 없을 때 누군가 `kubectl scale deployment my-app --replicas=0`를 실행하면 어떻게 되는지 생각한다. 반대로 `selfHeal: true`가 있을 때 HPA가 replica를 조정하면 어떤 일이 일어나는지 확인한다.
- `prune: true`가 없으면 Git에서 삭제한 리소스가 클러스터에 남는다. 이것이 문제가 되는 상황을 구체적으로 서술한다.
- LEARN.md의 Application YAML에서 `ignoreDifferences`로 HPA가 관리하는 `replicas` 필드를 드리프트 감지에서 제외한 이유를 설명한다.

**프로덕션 권장 설정**:
```yaml
syncPolicy:
  automated:
    prune: true       # 삭제된 리소스 정리 (필수)
    selfHeal: true    # 수동 변경 복구 (단, ignoreDifferences 설정 필요)
  syncOptions:
    - ApplyOutOfSyncOnly=true  # 변경된 것만 적용 (대규모 클러스터에서 중요)
```

**확인할 것**: ArgoCD의 `sync wave`와 `sync hook`(PreSync, Sync, PostSync)으로 DB 마이그레이션을 애플리케이션 배포 전에 실행하는 패턴을 찾아본다.

---

## Q5. GitHub Actions 캐싱 전략과 비용 최적화

**탐구 질문**: `actions/cache`와 `setup-node`의 `cache: npm` 옵션은 내부적으로 어떻게 다른가? 캐시 키 설계가 빌드 속도에 어떤 영향을 주는가?

**탐구 방향**:
- `setup-node`의 `cache: npm`은 내부적으로 `actions/cache`를 사용하며 `package-lock.json` 해시를 캐시 키로 사용한다. 이 해시가 변경되는 시점과 캐시가 무효화되는 시점을 연결해 생각한다.
- Docker 레이어 캐싱에서 `cache-from: type=gha`와 `cache-from: type=registry`의 차이를 비교한다. GitHub Actions 캐시는 10GB 한도가 있고 7일 후 만료된다.
- 캐시 히트율을 높이는 키 설계 원칙: 자주 바뀌는 값을 키에 포함할수록 캐시 히트율이 낮아진다.

**캐시 키 설계 예시**:
```yaml
# 좋은 예: OS + lock 파일 해시 조합
key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
restore-keys: |
  ${{ runner.os }}-node-  # 정확히 일치하지 않으면 prefix로 부분 복구

# 나쁜 예: SHA를 키에 포함하면 매번 새 캐시 생성 (항상 미스)
key: ${{ runner.os }}-node-${{ github.sha }}
```

**확인할 것**: GitHub Actions 캐시의 저장소당 10GB 한도를 초과하면 오래된 캐시가 자동 삭제된다. Monorepo에서 여러 패키지가 캐시를 공유할 때 키 충돌을 방지하는 방법을 찾아본다.

---

## Q6. 멀티 환경 배포에서 환경별 설정 관리

**탐구 질문**: dev/staging/production 환경마다 다른 데이터베이스 URL, 레플리카 수, 리소스 제한을 어떻게 관리하는가? Kustomize와 Helm 중 어떤 방식이 더 적합한가?

**탐구 방향**:
- Kustomize의 base + overlay 구조를 그려본다. base에는 공통 설정을, overlay에는 환경별 패치를 둔다. 파일 구조를 직접 설계해 본다.
- Helm의 values.yaml과 values-production.yaml 방식과 Kustomize overlay 방식의 차이를 비교한다. 어떤 팀에 어떤 방식이 더 자연스러운지 생각한다.
- 시크릿(DB 패스워드, API 키)은 Git에 저장하면 안 된다. Sealed Secrets, External Secrets Operator, AWS Secrets Manager 연동 중 하나를 선택해 설계한다.

**Kustomize 구조 예시**:
```
apps/my-app/
├── base/
│   ├── deployment.yaml    # 공통 설정 (이미지, 포트, 환경변수 키)
│   ├── service.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml  # replicas: 1, resources: small
    │   └── patch-replicas.yaml
    ├── staging/
    │   ├── kustomization.yaml  # replicas: 2, resources: medium
    │   └── patch-replicas.yaml
    └── production/
        ├── kustomization.yaml  # replicas: 5, resources: large, HPA 추가
        ├── patch-replicas.yaml
        └── hpa.yaml
```

**확인할 것**: ArgoCD ApplicationSet의 `Git Directory generator`를 사용하면 `overlays/` 디렉토리를 자동 스캔해 환경마다 Application을 생성한다. List generator와의 차이를 찾아 언제 어느 것이 더 편리한지 판단해 본다.

---

## 탐구 완료 체크리스트

- [ ] Q1: self-hosted runner 등록 절차와 runner 그룹 설정 방법 확인
- [ ] Q2: AWS IAM Trust Policy에서 저장소/브랜치 조건 설정 예시 작성
- [ ] Q3: 현재 팀 상황(클러스터 수, 팀 규모)에 맞는 CD 방식 결정
- [ ] Q4: ArgoCD sync hook으로 DB 마이그레이션 순서 제어 패턴 찾기
- [ ] Q5: 실제 프로젝트의 캐시 키 설계 검토 및 히트율 개선 여지 확인
- [ ] Q6: 멀티 환경 시크릿 관리 방식 선택 및 설계 문서 작성
