# Ch05. 배포 전략 심화

**핵심 질문**: "Feature Toggle/A/B/Dark Launch는 언제 사용하는가?"

---

## 🎯 학습 목표

1. Feature Toggle의 4가지 유형(Release/Experiment/Ops/Permission)을 구분하고 적절한 상황에 선택할 수 있다
2. Unleash를 사용해 Feature Toggle을 프로덕션 수준으로 구현한다
3. A/B Testing과 배포 파이프라인의 관계를 이해하고 통계적 유의성의 의미를 설명한다
4. Dark Launch(Shadow Traffic)를 통해 신규 버전의 안정성을 검증하는 방법을 이해한다
5. CDEvents 스펙으로 CI/CD 이벤트를 표준화하고 파이프라인 간 통합을 설계한다
6. SLSA와 OPA를 결합해 공급망 보안과 정책 기반 배포 게이트를 구축한다

---

## 1. 기본 배포 전략 리캡

Rolling, Blue-Green, Canary는 Jenkins 학습 Ch07에서 자세히 다뤘으므로 여기서는 핵심만 정리한다. 이 세 전략은 **인프라 수준**에서 트래픽을 제어하는 방법이다.

- **Rolling**: 인스턴스를 순차적으로 교체한다. 다운타임이 없지만, 두 버전이 동시에 실행되는 시간이 있어 API 하위 호환성이 필수다.
- **Blue-Green**: 동일한 환경을 두 벌 유지하고 DNS/LB에서 전환한다. 즉시 롤백이 가능하지만 비용이 두 배다.
- **Canary**: 전체 트래픽의 일부(예: 5%)를 신규 버전으로 먼저 보낸다. 위험을 점진적으로 노출하지만, 두 버전의 데이터 스키마가 달라지면 혼란이 발생한다.

이 장에서 다루는 Feature Toggle, A/B Testing, Dark Launch는 **애플리케이션 코드 수준**에서 동작한다는 점이 다르다. 인프라를 전환하지 않고도 특정 사용자에게만 새 기능을 노출하거나, 새 로직을 실행하되 결과를 숨길 수 있다.

### 배포 전략 비교

| 전략 | 다운타임 | 위험도 | 복잡도 | 비용 | 롤백 속도 |
|------|---------|--------|--------|------|----------|
| Recreate | 있음 | 높음 | 낮음 | 낮음 | 느림 |
| Rolling | 없음 | 중간 | 중간 | 낮음 | 느림 |
| Blue-Green | 없음 | 중간 | 높음 | 높음 | 즉시 |
| Canary | 없음 | 낮음 | 높음 | 중간 | 빠름 |
| Feature Toggle | 없음 | 낮음 | 중간 | 낮음 | 즉시(코드) |
| Dark Launch | 없음 | 없음 | 높음 | 높음 | 해당없음 |

---

## 2. Feature Toggle 심화

Feature Toggle(Feature Flag라고도 한다)은 코드 배포와 기능 릴리스를 분리하는 기법이다. 코드를 프로덕션에 배포하되, 토글이 꺼진 상태에서는 새 코드가 실행되지 않는다. 이 분리 덕분에 긴 수명의 피처 브랜치 없이 main 브랜치에 지속적으로 통합할 수 있다.

### 2.1 4가지 유형과 의사결정 트리

Pete Hodgson의 분류에 따르면 Feature Toggle은 수명과 역동성(dynamism)에 따라 4가지로 나뉜다.

```mermaid
flowchart TD
    Q1{토글의 목적은?}
    Q1 -->|"미완성 기능 숨기기"| RT[Release Toggle\n수명: 며칠~몇 주\n결정권: 개발팀]
    Q1 -->|"A/B 실험"| ET[Experiment Toggle\n수명: 며칠~몇 주\n결정권: 제품팀]
    Q1 -->|"성능 튜닝/회로차단기"| OT[Ops Toggle\n수명: 몇 주~몇 달\n결정권: 운영팀]
    Q1 -->|"유료 기능/권한제어"| PT[Permission Toggle\n수명: 영구\n결정권: 비즈니스]

    RT -->|"기능 완성 후 제거"| DEL[토글 삭제]
    ET -->|"실험 종료 후 승자 선택"| DEL
    OT -->|"안정화 후 제거 검토"| KEEP[유지 또는 삭제]
    PT --> KEEP
```

- **Release Toggle**: "이 기능은 아직 완성 안 됐어"라고 코드에 알려준다. 기능이 완성되면 즉시 제거해야 한다. 오래 유지할수록 기술 부채가 된다.
- **Experiment Toggle**: 두 가지 구현을 비교한다. 사용자를 두 그룹으로 나눠 다른 코드 경로를 실행한다. A/B Testing의 구현 수단이다.
- **Ops Toggle**: 운영 중 문제가 생겼을 때 특정 기능을 끄는 용도다. 회로 차단기(Circuit Breaker) 역할을 한다. 예를 들어, 무거운 추천 알고리즘에 문제가 생기면 토글로 즉시 단순 버전으로 전환한다.
- **Permission Toggle**: 특정 사용자(베타 테스터, 유료 고객)에게만 기능을 노출한다. 영구적으로 유지되므로 성능에 유의해야 한다.

### 2.2 Unleash 완전 설정

Unleash는 오픈소스 Feature Toggle 플랫폼이다. 서버가 토글 상태를 관리하고, 클라이언트 SDK가 주기적으로 폴링해서 로컬 캐시에 저장한다. 네트워크 장애가 나도 마지막 알려진 상태로 동작한다.

```yaml
# docker-compose.yml — Unleash 로컬 환경
# 왜 PostgreSQL인가: Unleash는 토글 상태, 감사 로그, 환경별 설정을 관계형 DB에 저장한다
version: "3.8"
services:
  unleash-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: unleash
      POSTGRES_PASSWORD: unleash_secret
      POSTGRES_DB: unleash
    volumes:
      - unleash-db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U unleash"]
      interval: 5s
      timeout: 5s
      retries: 5

  unleash:
    image: unleashorg/unleash-server:5
    ports:
      - "4242:4242"
    environment:
      DATABASE_URL: postgres://unleash:unleash_secret@unleash-db/unleash
      DATABASE_SSL: "false"
      # 초기 API 토큰 — 프로덕션에서는 환경변수 주입 방식으로 교체할 것
      INIT_CLIENT_API_TOKENS: "default:development.unleash-insecure-api-token"
      INIT_ADMIN_API_TOKENS: "*:*.unleash-insecure-admin-api-token"
    depends_on:
      unleash-db:
        condition: service_healthy

volumes:
  unleash-db-data:
```

```javascript
// feature-toggle.js — Unleash Node.js SDK 초기화 및 사용
// 왜 SDK인가: HTTP 직접 호출 대신 SDK를 쓰면 로컬 캐시, 자동 재시도, 메트릭 전송을 무료로 얻는다
const { initialize } = require("unleash-client");

const unleash = initialize({
  url: process.env.UNLEASH_URL || "http://localhost:4242/api",
  // API 토큰은 환경변수로만 주입 — 코드에 하드코딩 절대 금지
  customHeaders: {
    Authorization: process.env.UNLEASH_API_TOKEN,
  },
  appName: "payment-service",
  environment: process.env.NODE_ENV || "development",
  // 폴링 주기 (ms) — 1분마다 최신 토글 상태를 가져온다
  refreshInterval: 60_000,
  // 메트릭 전송 주기 — 어떤 토글이 얼마나 평가됐는지 서버에 보고한다
  metricsInterval: 30_000,
});

// SDK가 준비되기 전에 토글 평가를 막는다
unleash.on("ready", () => {
  console.log("Unleash client ready");
});

unleash.on("error", (err) => {
  // 연결 실패 시에도 로컬 캐시 덕분에 마지막 알려진 상태로 동작한다
  console.error("Unleash connection error:", err);
});

// Express 미들웨어에서의 사용 예시
function paymentRoute(req, res) {
  const userId = req.user.id;
  const userContext = {
    userId,
    // 점진적 롤아웃에 사용되는 세션 ID — 같은 사용자는 항상 같은 결과를 받는다
    sessionId: req.sessionID,
    properties: {
      plan: req.user.plan,         // Permission Toggle용 속성
      region: req.user.region,     // 지역별 롤아웃용 속성
    },
  };

  // Release Toggle: 새 결제 엔진이 아직 완성 안 된 상태
  if (unleash.isEnabled("new-payment-engine", userContext)) {
    return newPaymentEngine(req, res);
  }

  // Ops Toggle: 외부 사기 탐지 서비스가 응답 느릴 때 끌 수 있다
  if (unleash.isEnabled("fraud-detection-v2", userContext)) {
    return withFraudDetection(req, res);
  }

  return legacyPaymentEngine(req, res);
}

module.exports = { unleash, paymentRoute };
```

### 2.3 안티패턴: 장수 피처 브랜치

```bash
# BAD: 3주짜리 feature 브랜치 — 병합 지옥의 시작
git checkout -b feature/new-checkout-flow
# ... 3주 동안 작업 ...
git merge main  # 수백 개의 충돌

# GOOD: Feature Toggle로 main에 직접 통합
git checkout main
# 토글 뒤에 숨겨진 코드는 실행되지 않으므로 안전하게 푸시 가능
git push origin main
# 준비되면 Unleash 대시보드에서 토글 ON
```

---

## 3. A/B Testing과 배포 파이프라인

A/B Testing은 두 가지 구현 중 어떤 것이 비즈니스 목표에 더 효과적인지 데이터로 검증하는 방법이다. 중요한 것은, A/B Testing은 **배포 기법이 아니라 의사결정 기법**이라는 점이다. 배포는 Canary나 Feature Toggle이 담당하고, A/B Testing은 그 위에서 "어느 쪽이 더 나은가"라는 질문에 답한다.

### 3.1 nginx로 트래픽 분할

```nginx
# nginx.conf — 80/20 A/B 트래픽 분할
# 왜 nginx split_clients인가: 클라이언트 IP나 쿠키를 해시해서 일관된 그룹 배정을 보장한다
# (같은 사용자가 매 요청마다 다른 버전을 보는 일을 방지)
upstream backend_a {
    server app-v1:8080;
}

upstream backend_b {
    server app-v2:8080;
}

# $remote_addr을 해시 — 같은 IP는 항상 같은 그룹에 배정된다
split_clients "${remote_addr}" $variant {
    80%     a;   # 80%는 기존 버전
    *       b;   # 나머지 20%는 새 버전
}

server {
    listen 80;

    location / {
        # 실험 그룹을 쿠키로 기록 — 분석 시스템이 어느 그룹인지 알 수 있다
        add_header Set-Cookie "ab_variant=$variant; Path=/; Max-Age=86400";

        if ($variant = "a") {
            proxy_pass http://backend_a;
        }
        if ($variant = "b") {
            proxy_pass http://backend_b;
        }
    }
}
```

### 3.2 통계적 유의성이 중요한 이유

A/B 테스트를 빨리 끝내고 싶은 충동을 "Peeking Problem"이라고 부른다. 중간에 데이터를 보고 우연히 좋아 보이는 시점에 실험을 종료하면, 실제로는 차이가 없는데도 차이가 있다고 결론 내릴 확률이 높아진다.

통계적 유의성(p < 0.05)은 "관측된 차이가 우연일 확률이 5% 미만"을 의미한다. 이를 계산하려면 실험 시작 전에 표본 크기를 미리 정해야 한다. 온라인 표본 크기 계산기(예: Evan Miller's)를 쓰면 전환율 기준선, 기대 효과 크기, 유의수준(α)을 입력해 필요한 방문자 수를 얻을 수 있다.

파이프라인 관점에서 중요한 건, A/B 테스트 종료 조건을 자동화하는 것이다. 실험 플랫폼(Optimizely, GrowthBook)이 통계적 유의성 달성 시 웹훅으로 파이프라인을 트리거하면, 승자 버전을 자동으로 전체 롤아웃할 수 있다.

---

## 4. Dark Launch (Shadow Traffic)

Dark Launch는 신규 버전을 실제 프로덕션 트래픽으로 테스트하되, 사용자에게는 결과를 보여주지 않는 방법이다. 새 서비스가 실제 부하를 감당할 수 있는지, 응답 결과가 기존과 일치하는지 확인할 때 쓴다.

```
프로덕션 요청
     │
     ├──────────────────► 기존 서비스 → 사용자에게 응답 (항상 실행)
     │
     └──[Shadow Proxy]──► 신규 서비스 → 결과 비교 (응답은 버림)
                                ↓
                         비교 결과를 로그/메트릭에 기록
```

Dark Launch의 핵심 구현은 **비동기 트래픽 복제**다. 기존 서비스의 응답 시간에 영향을 주지 않으려면 신규 서비스 호출은 별도 스레드나 fire-and-forget 방식으로 처리해야 한다.

```javascript
// shadow-proxy.js — 트래픽 복제 미들웨어
// 왜 fire-and-forget인가: shadow 요청이 느려도 사용자 응답에 영향을 주면 안 된다
async function shadowMiddleware(req, res, next) {
  // 1. 기존 서비스는 정상 흐름으로 처리
  next();

  // 2. 요청 본문을 복제 (next() 이후에는 stream이 소비됐을 수 있으므로 미리 캐시)
  const shadowPayload = {
    method: req.method,
    path: req.path,
    headers: { ...req.headers, "x-shadow-request": "true" },
    body: req.cachedBody,  // 미들웨어에서 미리 캐시한 본문
  };

  // 3. 비동기로 shadow 서비스 호출 — await하지 않는다
  compareShadow(shadowPayload).catch((err) => {
    // shadow 실패는 로그만 남기고 무시 — 사용자 경험에 영향 없음
    metrics.increment("shadow.error", { reason: err.message });
  });
}

async function compareShadow(payload) {
  const [legacyResult, shadowResult] = await Promise.allSettled([
    callLegacyService(payload),
    callShadowService(payload),
  ]);

  const isDifferent =
    legacyResult.status !== shadowResult.status ||
    JSON.stringify(legacyResult.value) !== JSON.stringify(shadowResult.value);

  // 차이가 있으면 메트릭 기록 — 대시보드에서 모니터링
  if (isDifferent) {
    metrics.increment("shadow.divergence");
    logger.warn("Shadow divergence detected", {
      path: payload.path,
      legacy: legacyResult.value,
      shadow: shadowResult.value,
    });
  } else {
    metrics.increment("shadow.match");
  }
}
```

Dark Launch의 리스크는 두 가지다. 첫째, 신규 서비스가 부수 효과(DB 쓰기, 이메일 발송)를 일으키면 안 된다. Shadow 요청은 읽기 전용이거나, 별도 테스트 DB를 사용해야 한다. 둘째, 트래픽이 두 배로 늘어나므로 인프라 비용이 증가한다.

---

## 5. CDEvents — 파이프라인 이벤트 표준화

CDEvents는 CDF(Continuous Delivery Foundation)가 만든 CI/CD 이벤트 스펙이다. 다양한 CI/CD 도구들이 같은 형식으로 이벤트를 발행하면, 툴체인이 달라도 파이프라인 상태를 통합해서 볼 수 있다.

```json
// CDEvents 파이프라인 실행 완료 이벤트 예시
// 왜 표준화인가: Jenkins 이벤트, GitHub Actions 이벤트, ArgoCD 이벤트가 제각각이면
// 통합 대시보드나 자동화 트리거를 만들 때 각 도구마다 파서를 따로 만들어야 한다
{
  "specversion": "1.0",
  "id": "a10b1600-c4a1-4f5f-b03c-9b3b2c1d4e5f",
  "source": "https://ci.example.com/pipeline/payment-service",
  "type": "dev.cdevents.pipelinerun.finished.0.1.1",
  "datacontenttype": "application/json",
  "time": "2026-03-05T09:00:00Z",
  "data": {
    "pipelinerun": {
      "id": "pipeline-run-42",
      "name": "payment-service-main",
      "url": "https://ci.example.com/runs/42",
      "outcome": "success",
      "errors": ""
    },
    "pipeline": {
      "id": "payment-service",
      "name": "Payment Service CI",
      "url": "https://ci.example.com/pipeline/payment-service"
    }
  }
}
```

CDEvents가 실용적인 이유는 DORA 메트릭 자동 수집이다. Deployment Frequency, Lead Time for Changes 같은 메트릭을 각 도구에서 수작업으로 가져올 필요 없이, 표준 이벤트를 구독해서 집계할 수 있다.

---

## 6. Supply Chain Security: SLSA

SLSA(Supply-chain Levels for Software Artifacts, 발음은 "살사")는 소프트웨어 빌드 프로세스의 신뢰성을 4단계로 정의하는 프레임워크다. "이 바이너리가 정말 이 소스코드에서 빌드됐는가"를 증명하는 것이 핵심이다.

- **SLSA Level 1**: 빌드 과정이 스크립트화(자동화)되어 있고 provenance(출처 정보)를 생성한다.
- **SLSA Level 2**: 빌드 서비스가 소스와 provenance에 서명한다. 빌드 환경이 외부에서 관리된다.
- **SLSA Level 3**: 빌드 환경이 격리되고, provenance가 빌드 서비스 자체에서 생성된다(빌더를 신뢰할 필요가 없다).
- **SLSA Level 4**: 두 독립적인 빌드가 동일한 결과를 낸다(재현 가능한 빌드).

```yaml
# GitHub Actions에서 SLSA Level 3 provenance 생성
# slsa-github-generator는 별도의 신뢰된 워크플로에서 서명을 생성한다
name: SLSA Release

on:
  push:
    tags: ["v*"]

jobs:
  build:
    outputs:
      # 빌드 아티팩트의 해시값을 다음 잡에 전달한다
      hashes: ${{ steps.hash.outputs.hashes }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build binary
        run: |
          make build
          # 결정론적 빌드를 위해 SOURCE_DATE_EPOCH 설정
          SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct) make build
      - name: Generate hashes
        id: hash
        run: |
          # SHA-256 해시를 Base64로 인코딩 — provenance에 포함된다
          echo "hashes=$(sha256sum ./dist/* | base64 -w0)" >> $GITHUB_OUTPUT

  # 신뢰된 빌더가 서명된 provenance를 생성한다
  provenance:
    needs: [build]
    permissions:
      actions: read
      id-token: write       # OIDC 토큰 — 서명에 사용
      contents: write       # Release에 provenance 첨부
    uses: slsa-framework/slsa-github-generator/.github/workflows/generator_generic_slsa3.yml@v1.9.0
    with:
      base64-subjects: "${{ needs.build.outputs.hashes }}"
      upload-assets: true   # GitHub Release에 .intoto.jsonl 파일로 첨부
```

```bash
# provenance 검증 — 배포 전 CI에서 실행
# slsa-verifier는 서명을 검증하고 빌더와 소스 저장소가 예상과 일치하는지 확인한다
slsa-verifier verify-artifact \
  ./dist/payment-service-linux-amd64 \
  --provenance-path payment-service-linux-amd64.intoto.jsonl \
  --source-uri github.com/example/payment-service \
  --source-tag v1.2.3
```

---

## 7. Policy as Code: OPA 배포 게이트

OPA(Open Policy Agent)는 정책을 코드로 표현하고, API 호출로 정책을 평가하는 범용 정책 엔진이다. 배포 파이프라인에서 "이 이미지를 프로덕션에 배포해도 되는가"라는 질문을 Rego 정책으로 표현할 수 있다.

```rego
# deployment-policy.rego
# 왜 Policy as Code인가: "이미지에 Critical 취약점이 없어야 한다"는 규칙을
# 구어체 문서 대신 실행 가능한 코드로 관리한다. 정책 변경 이력이 Git에 남는다.
package deployment

import future.keywords.if
import future.keywords.in

# 기본값은 거부 — 명시적으로 허용된 경우에만 배포한다 (Fail Closed)
default allow = false

# 모든 조건이 충족될 때만 허용한다
allow if {
    test_passed
    image_signed
    no_critical_vulnerabilities
    approved_base_image
    not deployment_frozen
}

# 조건 1: 테스트 통과 여부
test_passed if {
    input.pipeline.test_status == "passed"
    input.pipeline.test_coverage >= 80    # 커버리지 80% 미만이면 거부
}

# 조건 2: 이미지 서명 검증 (Cosign)
image_signed if {
    input.image.signed == true
    input.image.signer in {"ci-bot@example.com", "release-bot@example.com"}
}

# 조건 3: Critical 취약점 없음 (Trivy 스캔 결과)
no_critical_vulnerabilities if {
    # input.vulnerabilities가 없거나 빈 배열이면 통과
    count([v | v := input.vulnerabilities[_]; v.severity == "CRITICAL"]) == 0
}

# 조건 4: 승인된 베이스 이미지 사용
approved_base_image if {
    approved_images := {
        "gcr.io/distroless/static:nonroot",
        "gcr.io/distroless/java17:nonroot",
        "alpine:3.19",
    }
    input.image.base_image in approved_images
}

# 조건 5: 배포 동결 기간 확인 (예: 연말 동결)
deployment_frozen if {
    data.deployment_freeze.active == true
    # 단, hotfix 태그가 붙은 경우는 동결에서 제외한다
    not startswith(input.image.tag, "hotfix-")
}

# 거부 이유를 명확히 반환 — CI에서 이 메시지를 파이프라인 로그에 출력한다
deny[reason] {
    not test_passed
    reason := sprintf(
        "Tests failed or coverage below 80%% (current: %d%%)",
        [input.pipeline.test_coverage]
    )
}

deny[reason] {
    not image_signed
    reason := "Image is not signed by an approved signer"
}

deny[reason] {
    not no_critical_vulnerabilities
    critical_count := count([v | v := input.vulnerabilities[_]; v.severity == "CRITICAL"])
    reason := sprintf("Found %d critical vulnerabilities", [critical_count])
}

deny[reason] {
    not approved_base_image
    reason := sprintf("Base image '%s' is not in the approved list", [input.image.base_image])
}
```

```bash
# Jenkins/GitHub Actions에서 OPA 정책 평가
# 왜 API 호출인가: OPA는 별도 서비스로 실행되므로 정책 변경 시 파이프라인을 재배포할 필요가 없다

# 평가에 사용할 입력 데이터 구성
INPUT=$(cat <<'EOF'
{
  "pipeline": {
    "test_status": "passed",
    "test_coverage": 85
  },
  "image": {
    "name": "payment-service",
    "tag": "v1.2.3",
    "signed": true,
    "signer": "ci-bot@example.com",
    "base_image": "gcr.io/distroless/java17:nonroot"
  },
  "vulnerabilities": []
}
EOF
)

# OPA 서버에 정책 평가 요청
RESULT=$(curl -s -X POST http://opa:8181/v1/data/deployment/allow \
  -H "Content-Type: application/json" \
  -d "{\"input\": $INPUT}")

# 결과 파싱 — allow가 true가 아니면 파이프라인 중단
ALLOWED=$(echo "$RESULT" | jq -r '.result')
if [ "$ALLOWED" != "true" ]; then
  echo "Deployment blocked by policy:"
  # 거부 이유 출력
  curl -s -X POST http://opa:8181/v1/data/deployment/deny \
    -H "Content-Type: application/json" \
    -d "{\"input\": $INPUT}" | jq -r '.result[]'
  exit 1
fi

echo "Policy check passed. Proceeding with deployment."
```

---

## 8. Feature Toggle 기술 부채 관리

Feature Toggle은 강력하지만, 관리하지 않으면 코드베이스를 오염시킨다. 토글이 많아질수록 코드 경로의 조합이 폭발적으로 늘어나 테스트가 불가능해진다.

실용적인 규칙은 **토글에 만료일을 설정하는 것**이다. Unleash는 토글 생성 시 만료 날짜를 지정할 수 있고, 만료된 토글에는 경고 표시가 나타난다. 코드 수준에서는 만료된 토글을 감지해 빌드를 실패시키는 린트 규칙을 추가할 수 있다.

```javascript
// feature-flags.js — 만료 날짜가 포함된 토글 레지스트리
// 왜 만료일인가: "나중에 지울게"는 지켜진 적이 없다. 만료일이 없으면 영원히 남는다.
const FEATURE_FLAGS = {
  "new-payment-engine": {
    description: "신규 결제 엔진 (PCI DSS 재인증 완료 후 ON)",
    owner: "payments-team",
    // 이 날짜가 지나면 CI에서 경고 또는 실패 처리
    expiresAt: "2026-06-01",
    type: "release",
  },
  "fraud-detection-v2": {
    description: "ML 기반 사기 탐지 v2 (성능 문제 시 OFF)",
    owner: "risk-team",
    expiresAt: null,  // Ops Toggle은 만료일 없음
    type: "ops",
  },
};

// CI에서 만료된 토글을 감지해 빌드를 실패시키는 스크립트
function checkExpiredFlags() {
  const today = new Date();
  const expired = Object.entries(FEATURE_FLAGS)
    .filter(([_, config]) => {
      if (!config.expiresAt) return false;
      return new Date(config.expiresAt) < today;
    })
    .map(([name]) => name);

  if (expired.length > 0) {
    console.error("Expired feature flags found. Remove them before merging:");
    expired.forEach((flag) => console.error(`  - ${flag}`));
    process.exit(1);  // CI 빌드 실패
  }
}

module.exports = { FEATURE_FLAGS, checkExpiredFlags };
```

---

## 9. 정리

이 장에서 다룬 배포 전략들은 공통된 철학을 가진다. 코드 배포와 기능 릴리스를 분리하고, 위험 노출을 최소화하며, 데이터 기반으로 의사결정을 내리는 것이다.

Feature Toggle은 장수 브랜치 없이 trunk-based development를 가능하게 한다. A/B Testing은 추측이 아닌 실험으로 제품 결정을 내린다. Dark Launch는 사용자 영향 없이 실제 부하로 신규 버전을 검증한다. SLSA와 OPA는 배포 파이프라인에 보안과 정책을 코드로 내재화한다.

이들을 조합하면 "기능은 언제든 배포하되, 언제 어떻게 릴리스할지는 비즈니스가 결정한다"는 원칙을 실현할 수 있다.

---

## 참조

- Jenkins 배포 전략 심화: `../../../01-jenkins/learning/07-deployment-patterns/LEARN.md`
- CI/CD 기초 패턴: `../01-cicd-design-pattern-foundations/LEARN.md`
- 구조적 CI/CD 패턴: `../04-structural-cicd-patterns/LEARN.md`
- Unleash 공식 문서: https://docs.getunleash.io
- SLSA 스펙: https://slsa.dev/spec
- OPA/Rego 언어 가이드: https://www.openpolicyagent.org/docs/latest/policy-language/
- CDEvents 스펙: https://cdevents.dev/docs/
