# CI/CD 파이프라인 개요

> 작성일: 2025-01-14
> 목적: CI/CD 파이프라인의 구조, 단계, 베스트 프랙티스 정리

---

## 1. CI/CD 파이프라인이란?

**CI/CD 파이프라인은 코드 변경 사항이 소스에서 프로덕션까지 자동으로 이동하는 일련의 단계입니다.**

### 핵심 구성 요소

| 구성 요소 | 설명 |
|----------|------|
| **CI (Continuous Integration)** | 코드 변경을 자주 통합하고 자동 빌드/테스트 |
| **CD (Continuous Delivery)** | 언제든 프로덕션 배포 가능한 상태 유지 |
| **CD (Continuous Deployment)** | 모든 변경을 자동으로 프로덕션에 배포 |

---

## 2. 파이프라인 단계 (Stages)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CI/CD 파이프라인 흐름                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐│
│  │ Trigger  │ → │  Build   │ → │   Test   │ → │  Deploy  │ → │Monitor ││
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └────────┘│
│       │              │              │              │              │     │
│       ▼              ▼              ▼              ▼              ▼     │
│   코드 변경      컴파일/빌드    자동화 테스트   스테이징/프로덕션  성능 추적  │
│   감지           의존성 설치    품질 검증       환경 배포        안정성 확인│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Trigger (트리거)

파이프라인을 시작하는 이벤트:
- **Push 이벤트**: 특정 브랜치에 코드 푸시
- **Pull Request**: PR 생성/업데이트
- **Tag 푸시**: 릴리스 태그 생성 (예: `v1.0.0`)
- **스케줄**: 정해진 시간에 자동 실행 (Cron)
- **수동 트리거**: 사용자가 직접 실행

### 2.2 Build (빌드)

```yaml
# GitHub Actions 예시
build:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
    - run: npm run build
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: build-output
        path: dist/
```

**베스트 프랙티스**:
- 컨테이너 이미지는 **한 번만 빌드**하고 환경별로 재사용
- 빌드 환경을 깨끗하게 유지 (캐시 활용)
- 의존성 락 파일 사용 (`package-lock.json`, `yarn.lock`)

### 2.3 Test (테스트)

테스트 단계 구성:

```
Fast Tests (먼저 실행)          Slow Tests (나중에 실행)
─────────────────────────────────────────────────────────
│ Lint/Format Check    │       │ Integration Tests  │
│ Unit Tests           │   →   │ E2E Tests          │
│ Security Scan (SAST) │       │ Performance Tests  │
─────────────────────────────────────────────────────────
```

**권장 파이프라인 구성**:
- 빠른 테스트 먼저 실행 → 실패 시 즉시 중단
- 느린 테스트는 빠른 테스트 통과 후 실행
- **이상적인 CI 파이프라인 시간: 10분 이내**

### 2.4 Security Scanning (보안 스캔)

| 스캔 유형 | 설명 | 도구 예시 |
|----------|------|----------|
| **SAST** | 정적 코드 분석 | SonarQube, Semgrep, CodeQL |
| **SCA** | 의존성 취약점 스캔 | Snyk, Dependabot, Trivy |
| **DAST** | 동적 애플리케이션 테스트 | OWASP ZAP, Burp Suite |
| **Container Scan** | 컨테이너 이미지 취약점 | Trivy, Clair, Anchore |
| **Secret Detection** | 하드코딩된 시크릿 탐지 | GitLeaks, TruffleHog |

**Shift Left Security**: 보안 스캔을 파이프라인 초기에 배치

### 2.5 Deploy (배포)

배포 전략:

| 전략 | 설명 | 장점 | 단점 |
|-----|------|-----|------|
| **Rolling** | 점진적 인스턴스 교체 | 무중단, 리소스 효율 | 롤백 느림 |
| **Blue-Green** | 새 환경에 전체 배포 후 전환 | 빠른 롤백 | 2배 리소스 필요 |
| **Canary** | 일부 트래픽만 새 버전으로 | 위험 최소화 | 복잡한 라우팅 |
| **A/B Testing** | 사용자 그룹별 다른 버전 | 비즈니스 검증 | 분석 필요 |

### 2.6 Monitor (모니터링)

배포 후 확인 사항:
- **Smoke Tests**: 기본 기능 동작 확인
- **Health Checks**: 서비스 상태 확인
- **APM**: 애플리케이션 성능 모니터링
- **Log Aggregation**: 로그 수집 및 분석
- **Alerting**: 이상 징후 알림

---

## 3. 주요 CI/CD 도구 비교

### 3.1 시장 점유율 (2025)

| 도구 | 채택률 | 특징 |
|-----|-------|------|
| **Jenkins** | 54% | 레거시 시스템, 높은 커스터마이징 |
| **GitHub Actions** | 51% | GitHub 네이티브, 개인/OSS 강세 |
| **GitLab CI** | 상당수 | All-in-one DevOps 플랫폼 |
| **CircleCI** | - | 클라우드 네이티브, 빠른 빌드 |
| **Azure DevOps** | - | Microsoft 생태계 통합 |

### 3.2 도구 선택 가이드

```
프로젝트 특성에 따른 선택:

GitHub 저장소 사용?
├── Yes → GitHub Actions (추천)
└── No
    ├── GitLab 저장소 사용? → GitLab CI (추천)
    └── 온프레미스 필요?
        ├── Yes → Jenkins
        └── No → CircleCI / AWS CodePipeline
```

### 3.3 AWS CI/CD 서비스

| 서비스 | 역할 |
|-------|------|
| **CodePipeline** | 파이프라인 오케스트레이션 |
| **CodeBuild** | 빌드 및 테스트 실행 |
| **CodeDeploy** | EC2, ECS, Lambda 배포 |
| **CodeArtifact** | 아티팩트 저장소 |

---

## 4. 파이프라인 설계 베스트 프랙티스

### 4.1 파이프라인 최적화

```yaml
# 병렬 실행 예시 (GitHub Actions)
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: npm run lint

  unit-test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - run: npm audit

  # 위 3개가 모두 성공해야 빌드 진행
  build:
    needs: [lint, unit-test, security-scan]
    runs-on: ubuntu-latest
    steps:
      - run: npm run build
```

### 4.2 캐싱 전략

```yaml
# 효과적인 캐시 키 설정
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 4.3 환경 분리

| 환경 | 목적 | 배포 트리거 |
|-----|------|-----------|
| **Development** | 개발자 테스트 | PR 또는 feature 브랜치 |
| **Staging** | QA 및 통합 테스트 | develop 브랜치 머지 |
| **Production** | 실제 서비스 | main 브랜치 또는 태그 |

### 4.4 시크릿 관리

**절대 금지사항**:
- 코드에 시크릿 하드코딩
- 설정 파일에 평문 저장
- 로그에 시크릿 출력

**권장 방법**:
- CI/CD 플랫폼의 시크릿 기능 사용
- 외부 시크릿 매니저 연동 (Vault, AWS Secrets Manager)
- 환경 변수를 통한 주입

---

## 5. 파이프라인 보안

### 5.1 CI/CD 보안 체크리스트

- [ ] 각 서비스별 최소 권한 IAM 역할 사용
- [ ] 시크릿을 Secrets Manager에 저장
- [ ] 소스 저장소 인증 및 암호화
- [ ] 코드 리뷰 필수화 (최소 1명 시니어)
- [ ] 프로덕션 배포 전 수동 승인
- [ ] 감사 로깅 활성화
- [ ] 정기적인 의존성 취약점 스캔

### 5.2 인시던트 대응

```
배포 실패 또는 장애 발생 시:

1. 즉시 롤백 (자동화된 롤백 권장)
2. 장애 격리 (영향받은 컴포넌트 분리)
3. 원인 분석 (로그, 메트릭 확인)
4. 수정 및 재배포
5. 포스트모템 작성
```

---

## 6. 참고 자료

- [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html)
- [AWS CI/CD Best Practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/strategy-cicd-litmus/cicd-best-practices.html)
- [CI/CD Pipeline Security Best Practices (Wiz)](https://www.wiz.io/academy/ci-cd-security-best-practices)
- [CI/CD Process: Flow, Stages, and Critical Best Practices (Codefresh)](https://codefresh.io/learn/ci-cd-pipelines/ci-cd-process-flow-stages-and-critical-best-practices/)
- [CI/CD Pipeline: A Gentle Introduction (Semaphore)](https://semaphore.io/blog/cicd-pipeline)
