# Jenkins 오픈소스 분석 → 면접 어필 소재 (2026-05-30)

> resume-research 워크플로우 산출. 회사 제품(외부 Jenkins 호출/추적 실행 엔진 + 멀티 Jenkins 운영) 기준으로, Jenkins 내부 동작을 깊이 이해했음을 보여주는 면접 소재 모음입니다.
> **출처 표기**: [검증됨] = 공식문서 확인(jenkins.io·plugins.jenkins.io·docs.cloudbees.com·javadoc) / [지원자근거] = 실제 작업(메모리·work 명시) / [추가제안] = 실근거 없음, "할 수 있다/검토 중" 톤만.
> ⚠️ "본인 확인 필요" 항목은 실작업 여부를 사용자가 확정해야 합니다 — 안 했으면 "이렇게 설계하는 게 맞다고 판단" 톤으로 낮춥니다.

---

## A. 실제 작업 근거가 강한 항목 ("해봤다"로 어필 가능)

### A-1. Queue/Executor 모델 + queueId 추적 ★최강 소재

**Jenkins 내부 [검증됨]**: 빌드를 트리거하면 잡은 먼저 빌드 큐에 들어가 Queue ID를 받습니다(`jenkins.model.queue`, pluggable `QueueIdStrategy`). 빌드 번호는 큐 적재 시점이 아니라 executor가 할당되어 빌드가 실제 시작될 때 부여됩니다. 큐 sorter/dispatcher가 순서를 바꿀 수 있고, 취소된 아이템이 빌드 번호를 소비하면 갭이 생기기 때문입니다. REST `POST /job/X/build`는 HTTP 201 + `Location: /queue/item/{id}/` 헤더를 비동기로 반환하고, `/queue/item/{id}/api/json`을 폴링해 `executable.number`가 나타날 때까지 기다립니다. 큐 아이템 URL은 빌드 시작 후 약 5분 유지됩니다.

**지원자 연결 [지원자근거]**: 메모리에 `project_executor_queueid_migration`(buildNumber→queueId 매칭 전환), `project_executor_dispatch_gate_redesign`(큐 적재량 quota + FOR UPDATE 직렬화), POL-002 identity 그룹화가 명시돼 있습니다. Jenkins 큐 모델을 정확히 이해하고 대응한 실작업입니다.

**면접 답변 구성**:
> "외부 Jenkins를 호출하는 실행 엔진을 만들면서 처음엔 buildNumber로 우리 실행 레코드와 Jenkins 빌드를 매칭했습니다. 그런데 Jenkins는 빌드 번호를 큐 진입이 아니라 executor 할당 시점에 부여합니다. 트리거 직후엔 번호가 없고 Location 헤더의 queue item만 있죠. 동시 트리거 상황에서 '아직 번호 없는 빌드'와 '취소되어 번호를 안 받은 빌드'를 buildNumber로 추적하니 매칭이 깨졌습니다. 그래서 트리거 응답의 queue item ID를 1차 키로 잡고, queue item API를 폴링해 executable.number가 나타나면 빌드 번호로 보강하는 2단계 추적으로 전환했습니다. 동시에 dispatch 게이트를 큐 적재량 quota + DB 비관적 락(FOR UPDATE)으로 직렬화해서 중복 트리거가 들어가도 한 건만 진행되게 했습니다."

가장 강력한 소재입니다 — Jenkins 내부 모델 이해 + 분산 동시성 직렬화(지원자 강점) + 실제 버그 동기가 모두 들어갑니다.

### A-2. REST 호출 추상화 + Crumb/CSRF 인증

**Jenkins 내부 [검증됨]**: username/password 인증은 crumb이 세션에 묶이므로 `/crumbIssuer/api/json`에서 받아 JSESSIONID 쿠키와 함께 보내야 합니다(`crumbRequestField`는 보통 `Jenkins-Crumb`). 반면 API 토큰 인증은 Jenkins 2.96+부터 CSRF 보호에서 면제되어 crumb이 불필요하고 stateless합니다. 이 차이가 스크립트 클라이언트 설계의 핵심입니다.

**지원자 연결 [지원자근거]**: 멀티 Jenkins 인스턴스를 호출하는 실행 엔진 담당 + 헥사고날 아키텍처 강점. "Jenkins 호출"을 outbound port로 추상화한 경험과 직결됩니다.

**면접 답변 구성**:
> "멀티 Jenkins를 호출하는 클라이언트를 헥사고날의 outbound adapter로 뺐습니다. crumb은 세션에 종속돼서 여러 인스턴스를 stateless하게 병렬 호출하는 환경엔 맞지 않았습니다. API 토큰은 2.96부터 CSRF가 면제되기 때문에 인증을 토큰 기반으로 통일하면 crumb/쿠키 왕복을 없애고 adapter를 단순화할 수 있습니다."

⚠️ **본인 확인 필요**: API 토큰 전환이 실제 작업인지 확인. 안 했다면 "이렇게 설계하는 게 맞다고 판단했다" 톤으로 낮춥니다.

### A-3. Webhook/이벤트 수신 → 폴링 제거

**Jenkins 내부 [검증됨]**: 빌드 완료를 외부로 알리는 표준 경로 — Outbound WebHook plugin(`start/success/failure/unstable` 4종 이벤트를 JSON POST), Notification plugin, HTTP Request plugin(post-build 회신). 코어 레벨엔 `RunListener`/`ItemListener` 확장점이 빌드 생애주기 훅을 제공합니다.

**지원자 연결 [지원자근거]**: 메모리에 webhook listener 작업 + Kafka/Redpanda 이벤트드리븐 강점이 있습니다.

**면접 답변 구성**:
> "처음엔 빌드 상태를 주기 폴링해서 추적했는데 Jenkins 인스턴스가 늘면서 폴링 부하와 반영 지연이 같이 커졌습니다. 그래서 Jenkins 측 post-build로 success/failure 이벤트를 우리 엔진의 webhook listener로 POST하게 하고, 받은 이벤트를 Kafka로 발행해 내부 컨슈머가 결재·티켓 상태를 갱신하도록 이벤트드리븐으로 바꿨습니다. 다만 webhook은 유실 가능성이 있어서 폴링을 완전히 버리지 않고 'webhook 우선 + 저빈도 reconcile 폴링' 하이브리드로 누락분을 보정했습니다."

⚠️ **본인 확인 필요**: 폴링→webhook 전환, reconcile 하이브리드가 실제인지 확인. 미구현이면 "이렇게 개선할 수 있다"로.

### A-4. Folder plugin(cloudbees-folder) 기반 멀티테넌시

**Jenkins 내부 [검증됨]**: cloudbees-folder는 중첩 폴더로 잡을 조직화하고 namespace-aware입니다(Folder A의 "Job A" ≠ Folder B의 "Job A", 이름 중복 허용). 자격증명을 폴더 레벨에 스코핑해 하위 잡만 접근하게 합니다. RBAC plugin과 결합 시 폴더 레벨 역할 + 정규식(`^App-1(/.*)?$`) 권한이 가능합니다.

**지원자 연결 [지원자근거]**: 메모리에 cloudbees-folder 작업 명시 + 멀티 Jenkins 운영 담당.

**면접 답변 구성**:
> "여러 팀을 한 Jenkins에 태우면서 잡 이름 충돌과 자격증명 격리가 문제였습니다. cloudbees-folder가 namespace-aware라 폴더별로 같은 잡 이름을 써도 충돌이 없고, 자격증명을 폴더 레벨에 스코핑하면 하위 잡만 접근하게 됩니다. 그래서 테넌트=폴더로 매핑하고, 실행 엔진이 잡 경로를 폴더 prefix로 라우팅하도록 했습니다."

---

## B. 동적 에이전트 — 근거가 부분적 (조심해서 어필)

### B-1. Kubernetes plugin 동적 에이전트

**Jenkins 내부 [검증됨]**: K8s plugin은 에이전트마다 Pod를 띄우고 빌드 후 삭제(ephemeral)합니다. inbound(JNLP) 에이전트로 뜨고 컨트롤러가 `JENKINS_URL/JENKINS_SECRET/JENKINS_AGENT_NAME`을 jnlp 컨테이너에 주입합니다. `node('label')` → Cloud 식별 → K8s API로 Pod 생성 → 실행 → 삭제 + orphaned pod GC.

**지원자 연결 [지원자근거]**: CKA + GCP 3노드 K8s 자가호스팅 + Kubespray/kubeadm. K8s 지식은 확실합니다. ⚠️ 단 "Jenkins K8s plugin으로 동적 에이전트를 직접 운영했다"는 메모리에 명시 없음 — 본인 확인 필수.

**면접 답변 구성(안전 버전)**:
> "실행 엔진이 외부 Jenkins를 호출할 때, 에이전트가 정적 노드인지 K8s plugin 기반 동적 Pod인지에 따라 빌드 시작 지연 특성이 다릅니다. 동적 에이전트는 Pod 프로비저닝 시간이 추가되고 JNLP 연결이 붙어야 executor가 잡히죠. 그래서 트리거 후 '큐 대기'와 '에이전트 프로비저닝 대기'를 구분해 타임아웃을 다르게 잡고, orphaned pod로 빌드가 영영 안 붙는 경우를 별도 실패로 감지하도록 설계했습니다."

K8s 지식(확실) + Jenkins 큐 모델(검증됨)의 교집합이라 안전합니다. "Pod 에이전트를 내가 운영했다"까지 단정하지 마십시오.

---

## C. 추가로 해볼 만한 것 ("할 수 있다/검토 중" 톤)

### C-1. Configuration as Code(JCasC) — 멀티 인스턴스 드리프트 제거 [추가제안]
컨트롤러 설정을 YAML로 선언해 재현 가능하게 만듭니다. 멀티 Jenkins는 인스턴스별 수동 설정 드리프트가 큰 문제인데, JCasC + GitOps(ArgoCD, 지원자 강점)로 설정을 Git SSOT화하면 신규 인스턴스 부트스트랩과 일관성 검증이 자동화됩니다.
> "지금은 멀티 Jenkins 설정이 인스턴스마다 조금씩 달라 드리프트가 쌓입니다. JCasC로 컨트롤러 설정을 YAML화하고, ArgoCD를 다뤄봤으니 그 YAML을 Git SSOT로 두고 동기화하면 드리프트를 구조적으로 없앨 수 있다고 봅니다. 아직 도입은 안 했지만 다음 우선순위로 생각하고 있습니다."
⚠️ JCasC 세부 스키마는 미검증 — 깊은 질문 시 "플러그인별 문서 확인 필요"로 솔직히.

### C-2. Pipeline as Code / Shared Library 표준화 [추가제안]
Jenkinsfile + Shared Library(`vars/`, `@Library`)로 파이프라인 로직을 버전관리·재사용합니다. 공통 단계(빌드/스캔/배포/엔진 콜백)를 Shared Library로 추출해 거버넌스를 겁니다.
> "테넌트별 Jenkinsfile이 제각각이면 우리 엔진이 기대하는 webhook 콜백 규약을 빠뜨리는 잡이 생깁니다. 공통 단계를 Shared Library로 빼서 '완료 시 엔진에 이벤트 발행' 규약을 강제하면 추적 누락을 파이프라인 레벨에서 막을 수 있습니다."

### C-3. Pipeline durability / resume [추가제안]
Jenkins Pipeline은 CPS 기반으로 flow node를 영속화해 컨트롤러 재시작 후 빌드 resume이 가능합니다. 실행 엔진의 SAGA 관점에서 "Jenkins 재시작 시 진행 중 빌드 상태를 어떻게 재동기화하느냐"의 설계 포인트입니다.
> "Jenkins 컨트롤러가 재시작되면 durability 설정에 따라 빌드가 resume될 수도, 유실될 수도 있습니다. 우리 엔진 입장에선 그 사이 webhook을 못 받으면 상태가 어긋나죠. reconcile 폴링으로 재시작 후 진행 중 빌드를 다시 스캔해 상태를 맞추는 보정 루프를 두는 게 맞다고 봅니다."
⚠️ CPS/durability 세부는 미검증.

### C-4. Credentials/RBAC 최소권한 [추가제안]
엔진이 멀티 Jenkins를 호출하려면 인스턴스마다 서비스 계정 토큰이 필요합니다. Credentials store에 스코핑하고 RBAC matrix로 엔진 계정에 Job/Build 트리거 + Read만 부여(관리자 권한 금지)하는 최소권한 설계. 시크릿 하드코딩 금지 원칙과도 정합합니다.

---

## 면접 우선순위 요약 (강→약)

| 순위 | 소재 | 근거 강도 | 한 줄 |
|---|---|---|---|
| 1 | queueId vs buildNumber 추적 + dispatch 직렬화 | [지원자근거]+[검증됨] | 가장 강함. Jenkins 큐/executor 내부 + 분산 동시성 결합 |
| 2 | Crumb/CSRF vs API 토큰 + 호출 adapter 추상화 | [지원자근거]+[검증됨] | 헥사고날 outbound port와 직결. 토큰 전환 실제 여부 확인 |
| 3 | webhook 수신 + Kafka 발행 + reconcile 하이브리드 | [지원자근거]+[검증됨] | 폴링→이벤트드리븐. 유실 보정 언급이 차별점 |
| 4 | cloudbees-folder 멀티테넌시 + credential 스코핑 | [지원자근거]+[검증됨] | namespace-aware/폴더 credential 스코핑 |
| 5 | K8s 동적 에이전트 queue→executor 지연 처리 | [검증됨]+CKA | "Pod 직접 운영" 단정 금지, 지연/orphan 감지 선까지 |
| 6 | JCasC + GitOps 드리프트 제거 | [추가제안] | "할 수 있다" 톤, ArgoCD 강점 레버리지 |
| 7 | Shared Library / durability reconcile / RBAC 최소권한 | [추가제안] | 깊은 질문 대비 보강 카드 |

## 할루시네이션 방지 가드
- **단정 가능**: queue/executor 모델, queueId 부여 시점, 201+Location 헤더, crumb 세션 종속, API 토큰 2.96+ CSRF 면제, cloudbees-folder namespace-aware/credential 스코핑, K8s plugin ephemeral Pod/JNLP 주입 — 모두 공식문서 검증됨.
- **본인 확인 필요(실작업)**: API 토큰 전환, 폴링→webhook 전환, reconcile 하이브리드, K8s 동적 에이전트 직접 운영.
- **미검증(스키마·세부)**: JCasC 키 export 범위, CPS durability 레벨, RBAC matrix 세부 → 깊은 질문 시 "플러그인 문서 재확인 필요"로 솔직히.

**검증 출처**: jenkins.io/doc/book/security/csrf-protection, javadoc.jenkins.io/jenkins/model/queue, docs.cloudbees.com(folders·get-build-number-with-rest-api), plugins.jenkins.io(kubernetes·cloudbees-folder·outbound-webhook).
