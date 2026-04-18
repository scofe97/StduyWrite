# Ch11. 비즈니스 로직 활용과 Webhook/API - 면접 질문

---

## Q1. Jenkins를 비즈니스 워크플로우 엔진으로 사용할 때의 장단점을 설명하고, 적합하지 않은 상황을 구체적으로 제시하시오.

**핵심 포인트:**

- **장점 - 기존 인프라 활용**: 대부분의 조직에 Jenkins가 이미 존재하므로, 별도의 워크플로우 엔진을 구축하지 않고 Job 하나를 추가하는 것만으로 비즈니스 작업을 자동화할 수 있다. 인프라 구축 비용, 팀 학습 비용, 운영 부담이 없다는 점이 현실적 이점이다.
- **장점 - 내장 기능**: 스케줄링(cron 트리거), 실행 로그 저장, 실패 알림(이메일/Slack), 수동 재실행 UI, 파라미터 입력 폼, Role-Based Access Control이 모두 기본 제공된다. 이 기능들을 자체 개발하려면 수 주 이상의 공수가 필요하다.
- **장점 - 플러그인 생태계**: 1,800개 이상의 플러그인이 거의 모든 외부 시스템과의 연동을 제공하므로, 통합 비용이 낮다.
- **단점 - 단일 장애점**: Controller가 다운되면 모든 비즈니스 작업이 중단된다. Jenkins HA 구성은 가능하지만 복잡하고, 대부분의 조직은 단일 Controller로 운영한다.
- **단점 - 상태 관리 부재**: Jenkins는 각 빌드를 독립적인 stateless 실행으로 취급한다. "이전 단계의 결과에 따라 분기"하거나 "실패 시 이전 단계를 보상"하는 로직을 Groovy로 직접 구현해야 하며, 유지보수가 어렵다.
- **단점 - 리소스 경쟁**: CI/CD 빌드와 비즈니스 작업이 같은 Executor 풀을 공유하므로, 비즈니스 배치가 대량 실행되면 개발자의 빌드가 큐에서 대기하게 된다.
- **부적합한 상황**: 복잡한 DAG 기반 데이터 파이프라인(수십 개의 태스크 의존성 → Airflow), 보상 트랜잭션이 필요한 비즈니스 워크플로우(주문 취소 시 결제 환불 + 재고 복구 → Temporal), 밀리초 단위 응답이 필요한 실시간 처리(Jenkins Job 시작 오버헤드가 수 초), 수백 개 이상의 동시 작업 실행(Executor 고갈).

**심화 질문:**
- Jenkins를 비즈니스 로직에 사용하다가 한계에 부딪혀 전용 도구로 마이그레이션한 경험이 있는가? 어떤 시점에서 마이그레이션을 결정하는 것이 적절한가?
- Jenkins Controller의 HA(High Availability)를 구성하는 방법에는 어떤 것이 있는가? 그 한계는 무엇인가?
- 비즈니스 작업 전용 Agent Pool을 분리하는 것과 별도 Jenkins 인스턴스를 운영하는 것 중 어느 접근이 더 적절한가?

---

## Q2. Jenkins REST API의 인증 방식과 CSRF Protection이 동작하는 원리를 설명하시오.

**핵심 포인트:**

- **API Token 인증**: 사용자별로 발급하는 토큰으로, Jenkins UI의 `사용자 설정 → API Token`에서 생성한다. 비밀번호 대신 토큰을 사용하는 이유는 세 가지다: (1) 토큰은 개별적으로 폐기할 수 있어 유출 시 영향 범위를 제한할 수 있고, (2) Jenkins 로그인 비밀번호 변경과 독립적이므로 자동화 스크립트가 깨지지 않으며, (3) 토큰별 사용 기록을 추적할 수 있다.
- **Basic Auth 전달**: HTTP Authorization 헤더에 `username:apiToken`을 Base64 인코딩하여 전달한다. curl에서는 `-u admin:API_TOKEN` 플래그로 간편하게 사용한다. HTTPS가 아닌 환경에서는 토큰이 평문으로 노출되므로 반드시 TLS를 적용해야 한다.
- **CSRF Protection 원리**: Jenkins는 POST/PUT/DELETE 같은 상태 변경 요청에 대해 CSRF 방지를 적용한다. 공격 시나리오는 다음과 같다: 악의적인 웹 페이지가 `<form action="http://jenkins/job/deploy/build" method="POST">`를 포함하면, Jenkins에 로그인된 사용자의 브라우저가 자동으로 세션 쿠키를 첨부하여 빌드를 트리거할 수 있다. 이를 방지하기 위해 Jenkins는 crumb 토큰을 요구한다.
- **crumb 발급 과정**: `/crumbIssuer/api/json`에 GET 요청을 보내면 `{"crumb": "abc123", "crumbRequestField": "Jenkins-Crumb"}` 형태의 응답을 받는다. 이후 POST 요청 시 `Jenkins-Crumb: abc123` 헤더를 포함해야 한다. crumb는 사용자 세션에 바인딩되어 있어 다른 사용자의 crumb로는 요청할 수 없다.
- **tree 파라미터**: API 응답이 매우 클 수 있으므로, `?tree=builds[number,result]{0,5}`처럼 필요한 필드만 지정하여 응답 크기를 줄일 수 있다. 이는 네트워크 효율뿐 아니라 Jenkins Controller의 직렬화 부하도 줄여준다.

**심화 질문:**
- Jenkins API Token과 OAuth 2.0 토큰의 차이점은 무엇인가? Jenkins에서 OAuth를 사용하려면 어떤 플러그인이 필요한가?
- crumb가 세션에 바인딩되어 있다면, 자동화 스크립트에서 crumb 만료 문제를 어떻게 처리하는가?
- Jenkins API에 Rate Limiting이 기본 제공되는가? 대량의 API 호출로 인한 Controller 과부하를 방지하려면 어떻게 해야 하는가?

---

## Q3. Generic Webhook Trigger와 SCM Webhook의 차이를 설명하고, 각각 어떤 상황에서 사용하는지 설명하시오.

**핵심 포인트:**

- **SCM Webhook의 동작**: GitHub/GitLab이 코드 변경 이벤트(push, pull_request, tag 등)를 Jenkins의 전용 endpoint(`/github-webhook/`)로 전송하면, GitHub Plugin이 자동으로 이벤트를 파싱하여 해당 Job을 트리거한다. 플러그인이 SCM 이벤트 구조를 이미 알고 있으므로 별도의 매핑 설정이 불필요하다.
- **Generic Webhook Trigger의 동작**: 외부 시스템이 `/generic-webhook-trigger/invoke?token=xxx`로 HTTP POST를 보내면, 플러그인이 payload를 JSONPath/XPath로 파싱하여 `genericVariables`에 정의된 매핑에 따라 환경 변수를 추출하고 파이프라인을 트리거한다. 어떤 시스템이든 JSON payload를 보낼 수 있으면 연동 가능하다.
- **SCM Webhook을 선택하는 상황**: 코드 변경에 의한 빌드 트리거가 목적일 때 사용한다. GitHub Branch Source Plugin과 Multibranch Pipeline을 조합하면 새 브랜치 자동 감지, PR 빌드, 브랜치별 필터링이 자동으로 동작한다. 이미 최적화된 처리를 제공하므로 굳이 Generic으로 재구현할 이유가 없다.
- **Generic Webhook Trigger를 선택하는 상황**: (1) Slack 커맨드로 배포 트리거, (2) Prometheus AlertManager 알림에 의한 자동 복구 파이프라인, (3) JIRA 이슈 상태 변경 시 테스트 환경 프로비저닝, (4) 커스텀 내부 시스템에서 Jenkins 작업 트리거. 핵심은 "비-SCM 이벤트"를 처리해야 할 때이다.
- **필터링의 차이**: SCM Webhook은 브랜치 필터를 Branch Source 설정에서 지정하고, Generic Webhook Trigger는 `regexpFilterText`와 `regexpFilterExpression`으로 payload 내용을 정규식으로 필터링한다. Generic 방식이 더 유연하지만 설정이 복잡하다.
- **보안 차이**: SCM Webhook은 GitHub Secret Token으로 payload 서명을 검증하고, Generic Webhook Trigger는 URL의 token 파라미터로 인증한다. GitHub Secret Token 방식이 더 안전한 이유는 토큰이 URL에 노출되지 않기 때문이다.

**심화 질문:**
- Generic Webhook Trigger에서 동일한 token을 사용하는 여러 Job이 있으면 어떤 일이 발생하는가? 이를 방지하려면 어떻게 설계해야 하는가?
- webhook이 중복 전달되는 경우(네트워크 재시도 등)에 같은 빌드가 두 번 실행되지 않도록 하려면 어떤 전략을 사용하는가?
- SCM Webhook과 SCM Polling의 차이점은 무엇이며, 각각의 장단점은 무엇인가?

---

## Q4. Jenkins API를 통해 파라미터 빌드를 트리거하는 전체 과정을 curl 명령어와 함께 설명하시오.

**핵심 포인트:**

- **전체 과정 4단계**: (1) CSRF crumb 발급, (2) 파라미터와 함께 빌드 트리거, (3) 큐 아이템에서 빌드 번호 확인, (4) 빌드 결과 조회. 이 4단계를 순서대로 수행해야 하는 이유는 Jenkins의 CSRF 보호 메커니즘과 비동기 빌드 실행 구조 때문이다.
- **Step 1 - crumb 발급**:
  ```bash
  CRUMB=$(curl -s -u admin:API_TOKEN \
    'http://localhost:8080/crumbIssuer/api/json' | jq -r '.crumb')
  ```
  POST 요청 전에 반드시 crumb를 먼저 발급받아야 한다. crumb 없이 POST를 보내면 `403 Forbidden`이 반환된다.
- **Step 2 - 빌드 트리거**:
  ```bash
  QUEUE_URL=$(curl -s -i -X POST -u admin:API_TOKEN \
    -H "Jenkins-Crumb: $CRUMB" \
    'http://localhost:8080/job/my-pipeline/buildWithParameters' \
    --data-urlencode 'DEPLOY_ENV=staging' \
    --data-urlencode 'IMAGE_TAG=v1.2.3' \
    | grep -i '^Location:' | awk '{print $2}' | tr -d '\r')
  ```
  `201 Created` 응답의 `Location` 헤더에 큐 아이템 URL이 포함된다. 빌드는 즉시 실행되지 않고 큐에 등록되므로, 이 URL로 상태를 추적해야 한다.
- **Step 3 - 빌드 번호 확인**: 큐 아이템 API를 polling하여 빌드가 Executor에 할당되면 `executable.number`에서 빌드 번호를 얻는다.
  ```bash
  BUILD_NUM=$(curl -s -u admin:API_TOKEN \
    "${QUEUE_URL}api/json" | jq -r '.executable.number // empty')
  ```
  큐에서 대기 중이면 `executable`이 null이므로 polling이 필요하다.
- **Step 4 - 빌드 결과 조회**:
  ```bash
  curl -s -u admin:API_TOKEN \
    "http://localhost:8080/job/my-pipeline/${BUILD_NUM}/api/json" \
    | jq '{result: .result, duration: .duration}'
  ```
  `result`가 null이면 아직 실행 중이고, `SUCCESS`, `FAILURE`, `ABORTED` 등의 값이 채워지면 완료된 것이다.
- **파라미터 없는 빌드와의 차이**: 파라미터가 없는 Job은 `/build` 엔드포인트를 사용하고, 파라미터가 있는 Job은 `/buildWithParameters`를 사용한다. 파라미터가 있는 Job에 `/build`를 호출하면 기본값으로 실행되거나 에러가 발생한다.
- **tree 파라미터 활용**: 빌드 정보 조회 시 `?tree=result,duration,timestamp`로 필요한 필드만 요청하면 응답 크기를 크게 줄일 수 있다.

**심화 질문:**
- 빌드 트리거 후 완료까지 기다리는 스크립트를 작성한다면 어떤 polling 전략을 사용하겠는가? exponential backoff를 적용해야 하는 이유는 무엇인가?
- Jenkins Pipeline의 `parameters {}` 블록에서 정의한 파라미터 타입(string, choice, boolean)에 따라 API 호출 방식이 달라지는가?
- 여러 Job을 순차적으로 트리거하고 모두 성공해야 다음 단계로 진행하는 오케스트레이션을 API만으로 구현할 때의 한계는 무엇인가?

---

## Q5. Jenkins를 다른 시스템(Slack, JIRA, 모니터링)과 연동할 때의 패턴과 주의사항을 설명하시오.

**핵심 포인트:**

- **Push 패턴 (Jenkins -> 외부)**: Jenkins 파이프라인의 `post` 블록에서 빌드 결과에 따라 외부 시스템에 알림을 보내는 패턴이다. 성공/실패를 다른 Slack 채널로 보내는 이유는 정보성 알림과 긴급 알림의 수신 대상이 다르기 때문이다. 실패 알림에는 빌드 로그 URL(`${env.BUILD_URL}console`)을 반드시 포함하여 즉시 원인을 파악할 수 있게 해야 한다.
- **Pull 패턴 (외부 -> Jenkins)**: REST API나 Webhook으로 외부 시스템이 Jenkins를 트리거하는 패턴이다. ChatOps(Slack에서 `/deploy` 명령), 모니터링 자동 복구(Prometheus alert → 롤백 파이프라인), 이벤트 기반 프로비저닝(JIRA 이슈 생성 → 테스트 환경 생성)이 대표적이다.
- **모니터링 연동의 가치**: 배포 이벤트를 Datadog/Grafana에 annotation으로 전송하면, 성능 메트릭 그래프에서 "이 시점에 배포가 발생했다"를 시각적으로 확인할 수 있다. 배포 후 지연 시간이 급증했을 때 원인 파악 시간을 크게 단축시킨다.
- **크레덴셜 관리**: 외부 시스템의 API 키/토큰은 반드시 Jenkins Credentials Store에 저장하고 `credentials()` 바인딩으로 접근해야 한다. Jenkinsfile에 평문으로 작성하면 Git 저장소에 시크릿이 노출된다.
- **타임아웃 필수**: 외부 시스템 호출에 타임아웃을 설정하지 않으면, 모니터링 API가 응답하지 않을 때 배포 파이프라인 전체가 멈출 수 있다. 알림은 "best effort"로 처리해야 한다.
- **실패 격리**: 알림 전송 실패가 파이프라인 전체를 실패시키면 안 된다. `try-catch`로 감싸거나 `post` 블록 내에서 처리하여, Slack API 장애 때문에 배포가 실패하는 상황을 방지해야 한다.
- **멱등성**: webhook 중복 전달에 대비하여, 동일한 이벤트로 같은 작업이 두 번 실행되지 않도록 체크 로직을 고려해야 한다.

**심화 질문:**
- Slack 알림의 내용을 풍부하게 만들기 위해 Block Kit 형식을 사용하려면 Jenkins에서 어떻게 구현하는가?
- JIRA 이슈와 Jenkins 빌드를 양방향으로 연결하려면(빌드에서 이슈 링크, 이슈에서 빌드 상태 표시) 어떤 플러그인과 설정이 필요한가?
- 배포 이벤트를 여러 모니터링 시스템에 동시에 전송할 때, 하나의 시스템이 실패해도 나머지는 정상 전송되도록 하려면 파이프라인을 어떻게 설계하는가?

---

## Q6. "Jenkins는 CI/CD 도구이지 범용 워크플로우 엔진이 아니다"라는 주장에 대해 찬반 논거를 제시하시오.

**핵심 포인트:**

- **찬성 논거 1 - 아키텍처적 한계**: Jenkins는 "트리거 → 실행 → 완료"라는 단방향 실행 모델에 최적화되어 있다. 복잡한 비즈니스 워크플로우에서 요구하는 장기 실행(long-running) 프로세스, 상태 머신 전이, 보상 트랜잭션(Saga)은 Jenkins의 설계 범위를 벗어난다. Temporal이나 AWS Step Functions는 이런 패턴을 네이티브로 지원하지만, Jenkins에서는 모두 Groovy 코드로 직접 구현해야 한다.
- **찬성 논거 2 - 운영 리스크**: CI/CD와 비즈니스 로직이 같은 Jenkins 인스턴스에 공존하면, Controller 장애 시 두 영역이 동시에 중단된다. 관심사 분리(Separation of Concerns) 원칙에 따라 CI/CD와 비즈니스 작업은 별도 시스템에서 운영하는 것이 안정적이다.
- **찬성 논거 3 - 보안 확대**: CI/CD 크레덴셜(Git 토큰, Docker Registry)에 비즈니스 시크릿(DB 비밀번호, 결제 API 키)까지 같은 Credentials Store에 저장하면 공격 표면이 넓어진다. Jenkins 취약점 하나가 전체 비즈니스 시크릿을 노출시킬 수 있다.
- **반대 논거 1 - 현실적 합리성**: 소규모 팀(5-10명)에서 Airflow 클러스터를 구축하고 운영하는 것은 과잉 엔지니어링이다. 이미 존재하는 Jenkins에 간단한 배치 Job을 추가하는 것이 비용 대비 효과적이며, "적절한 도구"보다 "충분히 좋은 도구"가 현실에서는 더 나은 선택일 수 있다.
- **반대 논거 2 - 내장 기능의 가치**: 스케줄링, 로깅, 알림, 인증/인가, UI를 모두 새로 구축하는 비용은 상당하다. Jenkins는 이 모든 것을 즉시 사용 가능한 형태로 제공한다. 별도 도구를 도입하면 "또 하나의 시스템을 운영"하는 부담이 추가된다.
- **반대 논거 3 - 점진적 전환 가능**: Jenkins에서 시작하여 복잡도가 증가하면 전용 도구로 마이그레이션하는 점진적 접근이 가능하다. 처음부터 Temporal을 도입했다가 "결국 간단한 cron 작업만 필요했다"는 결론에 이를 수도 있다.
- **균형 잡힌 결론**: Jenkins는 "간단한 비즈니스 자동화의 진입점"으로서 충분히 유효하다. 그러나 작업의 복잡도가 증가하는 시점을 인식하고, 그때 전용 도구로 전환하는 판단력이 중요하다. "Jenkins로 시작하되 Jenkins에 갇히지 말라"가 실용적 지침이다.

**심화 질문:**
- "Jenkins에서 시작하여 Airflow로 마이그레이션"하는 시점을 어떻게 판단하겠는가? 구체적인 기준(작업 수, 의존성 복잡도, 실패 빈도 등)을 제시하시오.
- Jenkins Pipeline을 Temporal Workflow로 전환할 때, 어떤 부분이 자연스럽게 매핑되고 어떤 부분에서 패러다임 차이가 발생하는가?
- 조직에서 "이미 Jenkins가 있으니 여기에 다 올리자"는 관성을 어떻게 관리하겠는가? 기술 부채 관점에서의 접근법은?
