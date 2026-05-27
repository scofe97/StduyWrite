# message-lib Outbox 메트릭이 Prometheus 에 수집되지 않는 원인

- **발생일**: 2026-05-22
- **영향 범위**: TPS v305p. 정도 차이가 있음 — operator-api 는 application.yml + ServiceMonitor 양쪽 차단(가장 심함), 나머지 9개 모듈(auth-api, pipeline-api, executor, notificator, scheduler, ppln-logging-api, pms-api, workflow-api, common-api) 은 ServiceMonitor 만 차단(애플리케이션 안에서는 `/actuator/prometheus` 가 응답하지만 Prometheus 가 긁지 않음). 모든 환경(local·dev·tst·prd) 공통.
- **심각도**: 운영 가시성 부재. Outbox 폴러는 정상 동작하지만 외부에서 발행/실패/DEAD/PENDING 큐 깊이를 알 길이 없다. 장애는 아니나 IGMU-1040 의 모니터링 정책 자체가 무력화된다.
- **상태**: dev 적용·검증 완료. operator-api 는 운영 중(메트릭 4종 실시간 수집), executor 는 코드 push 완료·이미지 재배포 대기. 나머지 8개 모듈은 별도 PR 영역.
- **관련 티켓**: [IGMU-1040](https://okestro.atlassian.net/browse/IGMU-1040)
- **fix 회차**: 1 (operator-api dev 검증 통과, executor 재배포 대기)
- **커밋**:
  - `operator-api/2774ef4c` — application.yml management 블록 추가
  - `executor/3f1225c` — engine/build.gradle micrometer-registry-prometheus 추가
  - `tps-manifest/9d09947` — values/apps/{operator-api,executor}.yaml metrics 활성화
  - `tps-manifest/8fe2da6` — servicemonitor.yaml 에 release=prometheus 라벨 부여

---

## 1. 증상

`message-lib/src/main/java/org/okestro/tps/messaging/infrastructure/outbox/OutboxMetrics.java` 는 Micrometer 가 classpath 에 있으면 4개 메트릭을 등록한다.

```
outbox.events.published   (Counter)
outbox.events.failed      (Counter)
outbox.events.dead        (Counter)
outbox.queue.pending      (Gauge)
```

그러나 dev 환경 Prometheus 어디에도 위 메트릭이 보이지 않는다.

```bash
curl -sG --data-urlencode 'match[]={__name__=~"outbox_.*"}' \
  https://prometheus.dev.trombone-v2.okestro.cloud/api/v1/series
# → []
```

`/actuator/prometheus` 엔드포인트 자체도 404.

```bash
kubectl -n trb-app exec deploy/operator-api -- \
  curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8091/actuator/prometheus
# → 404
```

---

## 2. 근본 원인

**operator 단일 모듈에만 management 블록이 누락**됐다. 의존성·라이브러리 표준은 이미 잡혀 있었고, 한 곳만 빠진 것이다. 처음 가설(조직 차원 결함)은 추가 조사로 정정한다.

### (1) 실제 차단점 — operator application.yml 에 `management` 블록 자체가 없다

```bash
$ grep -nE '^management:' operator/app/src/main/resources/application.yml
# (출력 없음)
```

같은 위치를 다른 9개 모듈에서 확인하면 모두 동일한 표준 블록을 가지고 있다.

```yaml
# pipeline-api, auth-api, common-api, scheduler, notificator, ppln-logging-api,
# pms-api, workflow-api, executor 모두 동일
management:
  endpoints:
    web:
      exposure:
        include: ["health", "refresh", "prometheus", "env"]
  endpoint:
    health:
      show-details: "always"
      probes:
        enabled: true
```

Spring Boot 기본 노출 목록(`health,info`)에 `prometheus` 가 없으면 `/actuator/prometheus` 가 404 다. operator 만 이 블록을 가지고 있지 않아 다른 모듈은 다 노출되는데 operator 만 빠졌다.

### (2) actuator·prometheus registry 는 이미 클래스패스에 있다

`core-lib` (외부 의존 아티팩트, `org.okestro:core-lib`) 의 build.gradle 이 actuator 와 prometheus registry 를 모두 제공한다.

```gradle
// core-lib/build.gradle
implementation 'org.springframework.boot:spring-boot-starter-actuator'   // L175
runtimeOnly 'io.micrometer:micrometer-registry-prometheus'               // L178
```

operator/app 은 `implementation "org.okestro:core-lib:${coreModuleVersion}"` 로 core-lib 을 의존하므로 두 라이브러리가 transitively 들어온다. `./gradlew :app:dependencies` 출력으로 확인되었다.

```
+--- org.okestro:core-lib:...
|    +--- org.springframework.boot:spring-boot-starter-actuator -> 3.2.3
|    |    \--- io.micrometer:micrometer-core:1.12.3
|    \--- io.micrometer:micrometer-registry-prometheus -> 1.12.3
```

즉 라이브러리 의존성 추가는 **불필요**했다. message-lib 의 `OutboxAutoConfiguration` (L64-75) 도 `MeterRegistry` 빈을 정상적으로 주입받고 `OutboxMetrics(registry, repo)` 분기로 진입한다. 메트릭 자체는 등록되었지만 `/actuator/prometheus` 가 404 라 외부로 못 나간 것이다.

### (3) ServiceMonitor — 진짜 부차 차단점

`tps-manifest/tps-helm/charts/operator-api/templates/servicemonitor.yaml` 은 `metrics.enabled` 조건부 렌더링이다.

```yaml
{{- if .Values.metrics.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
...
  endpoints:
  - port: http
    path: {{ .Values.metrics.path }}
    interval: 10s
{{- end }}
```

`charts/operator-api/values.yaml:34-36` 기본값:

```yaml
metrics:
  enabled: false       # ← ServiceMonitor 자체 미렌더링
  path: /metrics       # ← actuator 경로 (/actuator/prometheus) 와 불일치
```

`values/apps/operator-api.yaml` (환경별 override) 에도 metrics 블록이 없어 기본값 그대로 사용 중이다. operator 는 context-path 가 `/operator/api` 라 prometheus 실제 경로는 `/operator/api/actuator/prometheus` 다.

### 비교 대조 — 왜 operator 만 막혔나

| 단계 | core-lib 의존(actuator+registry) | yml management 블록 | ServiceMonitor enabled |
|---|---|---|---|
| operator/app | ✓ | ✗ **(차단)** | ✗ **(차단)** |
| pipeline-api | ✓ | ✓ | ✗ **(차단)** |
| auth-api | ✓ | ✓ | ✗ **(차단)** |
| 그 외 7개 | ✓ | ✓ | ✗ **(차단)** |

operator 는 application.yml + ServiceMonitor **둘 다** 막혀 메트릭이 안 나가고, 나머지 9개는 ServiceMonitor 만 막혀 있다. 즉 다른 9개는 application 안에서 `/actuator/prometheus` 가 응답하지만 Prometheus 가 긁지 않는 상태이고, operator 는 양쪽 다 막혀 가장 늦게 발견된 것이다.

### 추가 진단 — ServiceMonitor 만 켜도 안 됐던 이유 (실 적용 중 드러남)

`values/apps/operator-api.yaml` 에 `metrics.enabled: true` 를 켠 뒤 실제 클러스터에서 확인해보니 Prometheus 가 여전히 ServiceMonitor 를 못 봤다.

```bash
$ kubectl -n trb-app get servicemonitor --show-labels
NAME                   AGE     LABELS
trb-app-executor       7m16s   argocd.argoproj.io/instance=trb-app-executor
trb-app-operator-api   6m36s   argocd.argoproj.io/instance=trb-app-operator-api
```

```bash
$ kubectl get prometheus -n trb-mgm -o yaml | grep -A2 serviceMonitorSelector
    serviceMonitorSelector:
      matchLabels:
        release: prometheus
```

kube-prometheus-stack 의 Prometheus CR 이 **`release=prometheus` 라벨이 붙은 ServiceMonitor 만 스캔**하도록 설정돼 있는데, 차트의 `templates/servicemonitor.yaml` 에는 `metadata.labels` 자체가 없어 ArgoCD instance 라벨 외에 아무것도 안 붙는다. 이게 5번째 차단점이다.

### 추가 진단 — executor 는 actuator 가 있어도 prometheus endpoint 가 등록되지 않음

operator-api 와 executor 의 의존 구조가 다르다.

| 모듈 | 외부 `org.okestro:core-lib` 의존 | 결과 |
|---|---|---|
| operator-api | ✓ (`implementation "org.okestro:core-lib:${coreModuleVersion}"`) | actuator + micrometer-registry-prometheus 둘 다 transitively 들어옴 |
| executor | ✗ (로컬 subproject `:core-library` 만 사용) | actuator 는 다른 경로로 transitively, **registry 는 없음** |

executor pod 안에서 직접 확인해보니 `/actuator` listing 에 `prometheus` 가 없었다.

```bash
$ kubectl -n trb-app exec deploy/trb-app-executor -- \
  curl -s http://localhost:8092/executor/api/actuator | jq '._links | keys'
["env", "env-toMatch", "health", "health-path", "refresh"]
# ← prometheus 없음
```

application.yml 에 `prometheus` 노출은 적혀있지만, Spring Boot Actuator 는 `MeterRegistry` 빈이 없으면 `prometheus` endpoint 자체를 등록하지 않는다. 따라서 executor 는 build.gradle 에 registry 를 명시해야 한다.

### 5번째 가설 — EventPublisher 호출 부재

`operator/cicd` 안에 `EventPublisher.publish()` 의 실제 호출처를 grep 으로 찾으니 0건이다. ApplicationEvent 용 `eventPublisher.publishEvent()` 1건이 잡혔지만 이건 Spring 자체 이벤트라 message-lib 의 Outbox 와 무관하다. application.yml + ServiceMonitor 를 다 뚫어도 카운터가 안 움직일 가능성이 있다. **dev 적용 후 파이프라인 실행 1회를 트리거하여 별도 확인이 필요하다.**

---

## 3. 수정안 (실제 적용된 변경)

차단점 5단을 푸는 데 **3 repo · 4 커밋** 이 들어갔다.

### 3.1 operator-api repo — application.yml management 블록 추가 (`2774ef4c`)

다른 9개 모듈과 동일한 표준 블록을 그대로 따라간다. 새 컨벤션을 만들지 않는다. build.gradle 변경은 불필요했다 — `core-lib` 이 actuator + registry 를 transitively 제공한다.

```yaml
# operator/app/src/main/resources/application.yml
# Actuator 설정
management:
  endpoints:
    web:
      exposure:
        include: ["health", "refresh", "prometheus", "env"]
  endpoint:
    health:
      show-details: "always"
      probes:
        enabled: true
```

### 3.2 executor repo — build.gradle registry 의존 추가 (`3f1225c`)

executor 는 외부 core-lib 의존이 없으므로 registry 를 직접 명시해야 한다.

```gradle
// executor/engine/build.gradle
implementation 'io.micrometer:micrometer-registry-prometheus'
```

application.yml 의 management 블록은 이미 표준 그대로 있어 변경 불필요했다.

### 3.3 tps-manifest repo — values/apps 두 파일 metrics 활성화 (`9d09947`)

차트 default(`enabled: false`, `path: /metrics`) 를 환경 override 에서 켜고 actuator 경로로 교정한다. context-path 를 포함해야 한다.

```yaml
# tps-manifest/values/apps/operator-api.yaml
metrics:
  enabled: true
  path: /operator/api/actuator/prometheus
```

```yaml
# tps-manifest/values/apps/executor.yaml
metrics:
  enabled: true
  path: /executor/api/actuator/prometheus
```

### 3.4 tps-manifest repo — ServiceMonitor 에 release=prometheus 라벨 부여 (`8fe2da6`)

5번째 차단점. Prometheus CR 의 `serviceMonitorSelector.matchLabels.release=prometheus` 매칭용 라벨을 차트 ServiceMonitor 템플릿에 명시.

```yaml
# tps-manifest/tps-helm/charts/{operator-api,executor}/templates/servicemonitor.yaml
metadata:
  name: {{ include "<chart>.fullname" . }}
  labels:
    release: prometheus
```

### 3.5 다른 8개 모듈 (이번 작업 범위 밖)

application.yml management 블록은 이미 다 있다. `values/apps/<name>.yaml` 에 metrics 블록과 차트 servicemonitor.yaml 에 라벨만 추가하면 즉시 스크래핑된다. context-path 가 다른 모듈은 path 만 조정한다 (예: pipeline-api 는 `/pipeline/api/actuator/prometheus`).

---

## 4. 검증 방법

### 4.1 로컬 단위 — 차단점 (a)-(c) 통과 검증

```bash
# operator 모듈 로컬 기동 후
curl -s http://localhost:8091/actuator/prometheus | grep -E '^outbox_'
# 기대 출력:
# outbox_events_published_total 0.0
# outbox_events_failed_total 0.0
# outbox_events_dead_total 0.0
# outbox_queue_pending 0.0
```

4줄이 나오면 message-lib AutoConfiguration 이 메트릭 등록 분기로 진입한 것이다.

### 4.2 클러스터 — 차단점 (d) 통과 검증

```bash
# Deploy 서버 (10.255.37.247) SSH 후
kubectl -n trb-app exec deploy/operator-api -- \
  curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8091/actuator/prometheus
# → 200

kubectl -n trb-mgm get servicemonitor operator-api -o yaml | grep path
# → path: /actuator/prometheus
```

Prometheus UI:

```
https://prometheus.dev.trombone-v2.okestro.cloud/targets
→ operator-api 행 State=UP, Last Scrape <30s
```

PromQL 직접 검증:

```bash
curl -sG --data-urlencode 'query=outbox_events_published_total' \
  https://prometheus.dev.trombone-v2.okestro.cloud/api/v1/query | jq .
```

### 4.3 카운터 증가 검증 — 가설 5 (EventPublisher 호출 부재) 검증

operator 측에서 파이프라인 생성 API 호출 1회 → Redpanda 콘솔에서 `tps.v305p.operator.cmd.*` 토픽에 메시지 도착 확인 → 30~60초 후 Prometheus 에서 `rate(outbox_events_published_total[1m])` 그래프 우상향 여부 확인. 0 이 유지되면 EventPublisher 가 운영 코드에서 호출되지 않는 게 5번째 차단점으로 확정된다.

### 4.4 Grafana 패널 데이터 확인

`https://grafana.dev.trombone-v2.okestro.cloud → Dashboards → Outbox` 에서 4개 패널이 모두 데이터를 표시하면 종료. 4.3 단계 이전엔 패널이 "No data" 일 수 있는데, 이는 메트릭이 0인 게 정상 상태라서 그렇고, 등록 자체는 성공한 것이다.

---

## 5. 실제 적용·검증 결과

### 5.1 작업 흐름 — 차단점 발견 순서

진단을 코드 정적 분석만으로 끝낸 줄 알았는데, 실제 적용 단계에서 두 차단점이 추가로 드러났다. 가설을 조기에 닫지 않고 클러스터 상태를 직접 확인한 게 결정적이었다.

1. **1차 가설 (코드 분석)**: 4단 직렬 차단(actuator/registry/exposure/ServiceMonitor) 으로 추정 → 후속 검증에서 actuator/registry 는 `core-lib` 이 이미 제공하고 있어 차단점에서 제외.
2. **operator-api 변경 push 후 외부 검증 시도**: Istio Gateway 가 `/api/v1/*` 를 swagger schema 응답으로 가리고 있어 외부에서 Prometheus API 호출 불가. **Grafana datasource proxy(`/api/datasources/proxy/2`) 로 우회**해서 admin 인증 통과 후 직접 PromQL 조회.
3. **5번째 차단점 발견**: PromQL 로 보니 Prometheus 가 `trb-app` 네임스페이스를 아예 스크래핑하지 않음. SSH 후 `kubectl get prometheus -o yaml` 로 `serviceMonitorSelector: matchLabels.release=prometheus` 확인 → 차트 servicemonitor 템플릿에 라벨 추가.
4. **executor 도 메트릭 0**: pod 안에서 `/actuator` listing 보니 prometheus endpoint 자체가 없음. executor 는 core-lib 의존이 없어 registry 부재 → build.gradle 명시.

### 5.2 검증 명령 실 결과

operator-api 메트릭 4종 적재 확인.

```bash
$ curl ... 'api/v1/series?match[]={__name__=~"outbox_.*"}'
{
  "status": "success",
  "data": [
    { "__name__": "outbox_events_dead_total",      "job": "trb-app-operator-api", ... },
    { "__name__": "outbox_events_failed_total",    "job": "trb-app-operator-api", ... },
    { "__name__": "outbox_events_published_total", "job": "trb-app-operator-api", ... },
    { "__name__": "outbox_queue_pending",          "job": "trb-app-operator-api", ... }
  ]
}
```

Target health.

```
job=trb-app-operator-api  health=up  url=http://10.233.71.58:8091/operator/api/actuator/prometheus
job=trb-app-executor      health=down url=http://10.233.64.87:8092/executor/api/actuator/prometheus  error=404
```

executor 의 404 는 build.gradle 변경이 아직 새 이미지에 빌드되지 않아 발생한 것 — 재배포 대기 중.

### 5.3 Grafana 대시보드 import

`runners-high/issue/2026-05-22/outbox-dashboard.json` 을 Grafana API 로 import 했다.

```bash
$ curl -X POST -u admin:cloud1234 .../api/dashboards/db -d @payload.json
{ "status": "success", "uid": "tps-outbox", "url": "/d/tps-outbox/tps-c2b7-outbox", "id": 30 }
```

대시보드: https://grafana.dev.trombone-v2.okestro.cloud/d/tps-outbox

패널 4개 모두 PromQL 응답 OK. operator-api 인스턴스만 표시됨(현재 트래픽 0 이라 값은 0). executor 인스턴스는 재배포 후 자동 추가.

### 5.4 남은 검증

- `POST /operator/api/pipeline/v1/execute` 호출 1회 → `outbox_events_published_total` 카운터 증가 → 대시보드 `Publish Rate` 패널 우상향 확인. 이걸로 5번째 가설(EventPublisher 실호출 부재) 도 닫힌다.
- executor 새 이미지 배포 후 `Target health=up` 확인.

## 6. 메타 — 이 보고서 양식을 학습하지 못한 이유

사용자가 "보고서는 runners-high/issue 에 써라" 라고 짚어주기 전까지, 이 위치와 양식을 자동으로 인지하지 못했다. 원인은 셋이다.

### (a) runners-high/CLAUDE.md 에 `issue/` 디렉토리 행이 없다

`runners-high/CLAUDE.md` L11-20 의 "디렉토리 역할" 표는 6개(`write/`, `poc/`, `journal/`, `digest/`, `project/`, `docs/`)만 설명한다. `issue/` 폴더는 실제로 존재(`2026-05-21/operator-outbox-log-flood.md` 1건 보유)하지만 표에서 누락됐다. 결과적으로 "장애·결함 보고서를 어디에 쓰는가?" 라는 질문에 모델이 답할 근거 자체가 없었다.

### (b) writing 스킬 적용 범위가 `write/` 한정이다

`~/claude/.claude/skills/content/writing/SKILL.md` L28 은 "적용 범위: `write/` 디렉토리 하위" 라고 명시한다. `issue/` 는 자동 라우팅 대상이 아니다. 사람이 읽기 좋은 문서 규칙(어미 다양화, AI 강조어 금지, "왜" 포함)이 issue 보고서에도 동일하게 적용되어야 하지만, 스킬 정의가 그것을 보장하지 않는다.

### (c) 글로벌 CLAUDE.md 의 프로젝트 매핑이 디렉토리 단위까지 내려가지 않는다

`~/claude/CLAUDE.md` 의 "관리 중인 프로젝트" 표는 runners-high 의 루트 경로만 가리킨다. 하위 디렉토리별 산출물 유형(write=학습문서, issue=장애보고서, journal=일지)에 대한 매핑이 없어, 모델이 사용자 의도를 추론할 때 매번 디렉토리 트리를 재탐색해야 한다.

### 권고 조치

`runners-high/CLAUDE.md` 의 디렉토리 역할 표에 다음 한 행을 추가한다.

```
| `issue/` | 장애·결함 보고서 | 날짜 폴더(`YYYY-MM-DD/`) + 한 줄 제목 `.md`. 양식은 기존 1건 따름 |
```

같이 writing 스킬 SKILL.md L28 의 적용 범위를 `write/ + issue/` 로 확장하면, 다음번엔 사용자가 위치를 짚어주지 않아도 동일 양식·문체 규칙이 자동 적용된다. 본 권고는 이번 작업의 사이드 산출물로 같이 처리 가능하다.
