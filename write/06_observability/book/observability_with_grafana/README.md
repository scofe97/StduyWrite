---
title: Observability with Grafana (정독 노트 MOC)
tags: [moc, observability, grafana, loki, mimir, tempo, lgtm, book]
status: draft
source:
  - 《Observability with Grafana》(Packt, ISBN 9781803248004) — 장별 PDF 및 Part 1~4 디바이더
related:
  - ../../README.md
  - ../mastering_prometheus/README.md
  - ../dgos_opensearch/README.md
updated: 2026-08-02
---

# Observability with Grafana
---
> Packt 단행본(ISBN 9781803248004)입니다. 형제 폴더 [`mastering_prometheus/`](../mastering_prometheus/README.md) 가 **메트릭 한 축을 깊게** 판다면, 이 책은 **LGTM 스택 전체로 넓게** 갑니다. 관측 가능성 개념과 다섯 사용자 페르소나로 기초를 세운 뒤 로그·메트릭·트레이스를 각 제품(Loki·Mimir·Tempo)으로 구현하고, 대시보드·알림·IaC 로 운영에 올린 다음, RUM·프로파일링·부하 테스트까지 넓히는 **15개 장(4개 파트)** 구성입니다.

## 이 책을 여기 두는 이유

상위 [`06_observability/README.md`](../../README.md) 는 `02_LGTMStack/` 아래 Grafana Core·Alloy·Loki·Tempo·Mimir·Beyla 를 **컴포넌트별로** 이미 한 편씩 정리해 두었습니다. 그 편들은 각 제품이 *무엇인지* 를 답합니다. 이 책이 채우는 것은 그 옆의 질문, **왜 이 조합인지** 입니다. Grafana Labs 가 왜 저장소를 세 개로 나눴고 셋 다 오브젝트 스토리지를 쓰는지, 그 위에 어떤 사용자가 어떤 질문을 들고 오는지가 이 책의 축입니다.

형제 폴더와의 관계는 **깊이 대 넓이** 로 갈립니다. `mastering_prometheus` 는 단일 신호(메트릭)를 TSDB 내부 구조까지 파고들어 카디널리티·샤딩·Thanos 까지 갑니다. 이 책은 그 깊이를 포기하는 대신 신호 셋을 한 화면에 놓고 *서로 어떻게 잇는지* 를 봅니다. 같은 Mimir 를 다뤄도 전자는 remote write 튜닝 파라미터를, 후자는 "왜 Prometheus 대신 Mimir 인가" 를 답하는 식입니다. 두 폴더를 나란히 두면 한 축이 다른 축의 공백을 메웁니다.

실무 접점도 분명합니다. 이 저장소의 [`03_Project/`](../../README.md) 묶음은 LGTM+Spring Boot 실전 구축과 305P 운영기록을 담고 있는데, 그 구축이 *이미 내린* 결정들(왜 Alloy 인가, 로그 라벨을 어디까지 쪼갤 것인가)의 근거가 이 책의 앞부분에 있습니다. 노트를 쓸 때 그 지점마다 교차참조를 남깁니다.



## 파트 구조

각 파트 디바이더 PDF(`Part 1_*.pdf` ~ `Part 4_*.pdf`)에서 제목과 장 범위를 직접 확인했습니다. 네 파트 모두 원문이 확보돼 추정 구간이 없습니다.

| 파트 | 제목 | 장 | 이 파트가 맡는 질문 |
|------|------|----|--------------------|
| Part 1 | Get Started with Grafana and Observability | 1–3 | 관측 가능성이 무엇이고 누가 쓰는가, 어떻게 계측하는가 |
| Part 2 | Implement Telemetry in Grafana | 4–7 | 신호별로 어떤 제품을 어떻게 쓰는가, 클라우드는 어떻게 붙는가 |
| Part 3 | Grafana in Practice | 8–11 | 보여주고·알리고·자동화하고·설계하는 운영 활동 |
| Part 4 | Advanced Applications and Best Practices | 12–15 | 프론트엔드·성능·DevOps 로 넓히고 모범 사례로 닫기 |



## 장별 목표

| 장 | 제목 | 주요 토픽 |
|----|------|----------|
| 1 | Introducing Observability and the Grafana Stack | 관측 가능성 개념(제어 이론) · 파나마 운하 사례 · 텔레메트리 3종+α · 사용자 페르소나 5인 · Grafana 스택 · 대안 도구 · 배포 방식 |
| 2 | Instrumenting Applications and Infrastructure | 애플리케이션·인프라 계측 기초 |
| 3 | Setting Up a Learning Environment with Demo Applications | 데모 앱으로 학습 환경 구축 |
| 4 | Looking at Logs with Grafana Loki | Loki 로 로그 다루기 · 인덱스 필드 선택 |
| 5 | Monitoring with Metrics Using Grafana Mimir and Prometheus | Mimir·Prometheus 로 메트릭 모니터링 |
| 6 | Tracing Technicalities with Grafana Tempo | Tempo 로 분산 트레이싱 |
| 7 | Interrogating Infrastructure with Kubernetes, AWS, GCP, and Azure | 쿠버네티스·3대 클라우드 인프라 관측 |
| 8 | Displaying Data with Dashboards | 청중 요구를 고려한 대시보드 설계 |
| 9 | Managing Incidents Using Alerts | 알림 룰 · OnCall · Incident |
| 10 | Automation with Infrastructure as Code | Ansible·Terraform·Helm 자동화 |
| 11 | Architecting an Observability Platform | 관측 플랫폼 아키텍처 · 수집 인프라 설계 |
| 12 | Real User Monitoring with Grafana | Faro 로 RUM · web vitals |
| 13 | Application Performance with Grafana Pyroscope and k6 | 연속 프로파일링 · 부하 테스트 |
| 14 | Supporting DevOps Processes with Observability | DevOps 프로세스와 관측의 결합 |
| 15 | Troubleshooting, Implementing Best Practices, and More with Grafana | 트러블슈팅 · 모범 사례 · 향후 흐름 |

> 2~15장의 토픽은 파트 디바이더의 장 소개와 각 장 제목에서 뽑은 것입니다. 각 장 PDF 앞머리의 "main topics" 목록으로 확정하는 일은 그 장을 읽을 때 합니다.



## 작성된 정독 노트

> PDF 를 장별로 읽는 대로 `NN-NN.제목.md` 형식으로 채웁니다.

| 노트 | 범위 |
|------|------|
| [01-01 관측 가능성과 Grafana 스택 — 파나마 운하·페르소나·LGTM](./01-01.관측%20가능성과%20Grafana%20스택%20—%20파나마%20운하·페르소나·LGTM.md) | 1장 전체 — complicated 와 complex 의 구분 · 파나마 운하 갑문으로 본 모니터링과 관측의 경계 · 신호 3종의 운하 대응과 이벤트·프로파일 · 사용자 페르소나 5인과 각자의 질문 · LGTM 네 제품의 자리와 공통 설계(오브젝트 스토리지) · Faro·k6·Pyroscope · 대안 도구 지형 · SaaS 대 셀프호스팅 |
| [02-01 계측 — 로그 형식·메트릭 타입·트레이싱 프로토콜·인프라 표준](./02-01.계측%20—%20로그%20형식·메트릭%20타입·트레이싱%20프로토콜·인프라%20표준.md) | 2장 전체 — 구조화·반구조화·비구조화와 캡슐화(한 사건이 네 이벤트로 쪼개짐) · 로그 형식 7종 · 메트릭 타입 넷의 능력 7축 비교 · **같은 이름이 프로토콜마다 다르게 동작**(StatsD 는 flush 마다, Prometheus 는 프로세스 재시작 시 카운터 리셋) · 서머리의 합산 불가 · 카디널리티 비용(서버 수백 대 사용자 수백만) · 트레이스·스팬 필드와 부모 샘플링 전파 · 자동 대 수동 계측 · Syslog·SNMP·Modbus |
| [03-01 학습 환경 — Grafana Cloud·OTel 데모·자격증명과 트러블슈팅](./03-01.학습%20환경%20—%20Grafana%20Cloud·OTel%20데모·자격증명과%20트러블슈팅.md) | 3장 전체 — ⛔ **버전 전면 노후**(책 2023 기준: Grafana 10.2→13.1.1 · Collector 0.73.1→0.157.0 · Demo 0.26.0→3.0.0, 2026-08-01 실측). 클릭 절차 대신 **오래 사는 것**만 남김 — 데이터 경로(데모→Collector→신호별 엔드포인트) · 자격증명 구조(토큰은 공유, 사용자명·주소는 갈림) · **Tempo 만 `https://` 떼고 `:443`** · 무료 티어 한도(메트릭만 개수 10,000, 나머지는 용량) · 트러블슈팅 3단계 · 내 앱 붙이는 4317/4318 |
| [04-01 Loki 와 LogQL — 파이프라인·메트릭 쿼리·아키텍처](./04-01.Loki%20와%20LogQL%20—%20파이프라인·메트릭%20쿼리·아키텍처.md) | 4장 전체 — 설계 목표 4가지(**메타데이터만 색인**이 나머지를 결정) · 로그 항목 3구성과 스트림 정의 · LogQL 파이프라인 5단계(셀렉터→라인필터→파서→라벨필터→포맷) · 빈 값 셀렉터 실패(`.*` 불가 `.+` 가능) · 파서 5종 구분 · 값 타입 4종과 `__error__` · `ip()`·`decolorize`·`drop` · **로그에서 메트릭 만들기**(로그 범위 vs unwrap 범위 집계) · 아키텍처 컴포넌트(distributor·ingester·querier·compactor·ruler) · 좋은/나쁜 라벨 |
| [05-01 메트릭 — 수집 프로토콜·저장 아키텍처·exemplar](./05-01.메트릭%20—%20수집%20프로토콜·저장%20아키텍처·exemplar.md) | 5장 전체 — **PromQL·TSDB·Mimir 는 형제 폴더가 정본이라 위임하고 차이분만**. 메트릭·시계열·샘플 3층 · 범위 벡터는 Instant 로 실행(Range 는 오류) · `$__rate_interval` 은 Grafana 기능 · **수집 프로토콜을 push·pull 축으로 비교**(StatsD UDP 8125·인증 없음, OTLP 4317/4318·인증 있음, Prometheus pull 이 앱 설정을 줄임, SNMP 는 감시 pull + trap push) · **저장 계보**(Whisper 파일당 시계열 → Prometheus 불변 블록 2시간·chunk 512MB → Mimir 오브젝트 스토리지) · exemplar 를 Grafana 에서 켜고 Tempo 로 건너가기 |
| [06-01 Tempo 와 TraceQL — 구조 연산자·전파 헤더·아키텍처](./06-01.Tempo%20와%20TraceQL%20—%20구조%20연산자·전파%20헤더·아키텍처.md) | 6장 전체 — TraceQL 은 **선택만 되고 분석은 없음**(집필 시점 v2.3.x) · intrinsic 필드 8종과 span/resource 속성 접두사 · **구조 연산자**(`>` 직계자식 · `>>` 자손 · `~` 형제) — TraceQL 만의 관계 검색 · **전파 헤더 4형식 규격**(Jaeger `uber-trace-id` 콜론 묶음 · B3 필드별 헤더 + `b3` 단일 · W3C `traceparent` 16/8바이트 · baggage 64멤버·8,192바이트·민감정보 금지) · Jaeger 는 채택 비권장 · Tempo 는 **trace ID 로 라우팅**(Loki 는 라벨) · Metrics generator 는 선택적 |
| [07-01 인프라 관측 — 쿠버네티스 수집기와 클라우드 3사 연결](./07-01.인프라%20관측%20—%20쿠버네티스%20수집기와%20클라우드%203사%20연결.md) | 7장 전체(**Part 2 마지막**) — 앞은 K8s 수집기 7종으로 실질, 뒤는 클라우드 UI 안내라 판단 축만 남김. **배포 형태가 컴포넌트를 정함** — Kubeletstats·Filelog·HostMetrics 는 DaemonSet, **Cluster·Object Receiver 는 단일 인스턴스**(여러 개면 데이터 중복) · Prometheus Receiver 는 **stateful** 이라 복제본마다 다른 설정 필요 · Attributes Processor 가 붙이는 K8s 속성 6종이 상관관계의 전제 · hostMetrics 프리셋 **기본 10초 → 60초 권고** · Object Receiver 의 pull vs watch · **클라우드는 원격 조회(데이터 소스) vs 가져오기(통합)** — AWS 만 양쪽, GCP·Azure 는 데이터 소스만. MQL·KQL·ARG · CloudWatch 는 태그 있는 리소스만 발견 · 모범 사례 4축(성능·비용·제약·보안) |
| [08-01 대시보드 — 목적 정의·시각화 선택·인지 부하 줄이기](./08-01.대시보드%20—%20목적%20정의·시각화%20선택·인지%20부하%20줄이기.md) | 8장 전체(**Part 3 시작**) — 데이터를 *모으는* 이야기가 끝나고 *보여주는* 이야기로. 기술 난도는 낮고 **판단**이 어려운 장. **세 질문**(청중·요구·어디서 보는가)에 답하지 않으면 대시보드가 이야기를 못 함 · Explore 쿼리 → Add to dashboard 경로와 저자들이 스스로 지적한 **첫 화면 문제 셋** · **카운트를 비율로**(`$__rate_interval`) + 범례를 `{{method}}` 로 · **패널 설정 7종**(title·description / legend / standard options / 패널별 / thresholds / overrides / value mappings) · 1장 페르소나 5인의 요구가 **설계 결정으로 내려옴**(Ophelia=색·임계값, Pelé=내보내기, Masha=PDF 배치) · **행 접기의 성능 이점**(펼치기 전까지 쿼리 미실행) · 하드코딩 금지·상대 시간 기본값 · 폴더는 **권한 경계**, 태그는 발견성 · 사례 연구 — **행 하나 = 팀 하나, 첫 패널은 연락처 텍스트 패널**로 인지 부하 감축. Golden Signals 는 정의만(정본은 `01_Foundations/01-03`) |
| [09-01 사고 관리 — 금은동 지휘·SLI 알림·IRM 도구 셋](./09-01.사고%20관리%20—%20금은동%20지휘·SLI%20알림·IRM%20도구%20셋.md) | 9장 전체 — **절반이 조직 이야기**. 나쁜 사고 관리가 번아웃을 넘어 심장마비·뇌졸중 위험까지 높인다는 문장으로 시작. **금·은·동 지휘 구조**(영국 응급 서비스) — 금은 전략·미디어·법적 이슈, 은은 전술·문서화·도구선택이자 **금과 동 사이 통로**, 동은 운영 통제. 금 팀은 **전술 결정에 끌려들어 가면 안 됨** · 프레임워크 4종(ITIL·SRE·NIST·SANS) 공통 역할 3종 · **화이트박스**(RED·USE·golden signals·core web vitals) 대 **블랙박스**(합성·RUM) — 블랙박스는 **통제 밖까지 봐서 오탐 위험** · AIOps 는 도메인 지식을 대체하지 못함 · **영웅 문화** 탈피 · **비난 없는 사후 검토는 책임을 없애는 게 아니라 두려움을 없애는 것** · **SLI 는 서비스당 3~5개**(혼란·가짜알림·감시비용) · 알림 규칙 3상태(normal·pending·firing)와 **평가 주기 함정**(1분 1,440회 대 10초 8,640회, 자원 6배) · **주기 > 기간이면 평가 공백** · 소스 라벨로 팀 라우팅 · **IRM 셋** Alerting(무료)·OnCall(당직·Jinja2·에스컬레이션 11단계)·Incident(타임라인·Insights 90일). Golden Signals·에러버짓은 `01_Foundations` 에 위임. ⚠️ **FID → INP 대체(2024-03-12)는 책 밖 보강** |
| [10-01 코드형 인프라 — 네 층 분할·Helm 우선순위·Terraform 관리](./10-01.코드형%20인프라%20—%20네%20층%20분할·Helm%20우선순위·Terraform%20관리.md) | 10장 전체 — **네 계층**(생산·수집·저장·시각화)으로 쪼개 주인을 정함. **생산 계층은 제외**(생산자마다 전략이 다름) · ④ 시각화는 **공유 책임** — ②·③ 팀이 나머지 조직에 권한을 준다 · **배포 모드가 프리셋을 정함**(daemonset = logsCollection·kubeletMetrics·hostMetrics / deployment·statefulset = kubernetesEvents·clusterMetrics, kubernetesAttributes 만 모든 모드 안전) · **로깅 캐스케이드**와 `includeCollectorLogs: false` · 파이프라인 4요소와 **커넥터**(spanmetrics 가 RED 를, servicegraph 가 서비스 그래프를 만든다) · ⚠️ **Helm `--values` 우선순위** — 마지막 파일이 이기고 **배열은 병합 안 됨** · Helm 직접 설치는 **중앙이 각 클러스터를 알아야** 해서 병목, **오퍼레이터+GitOps 가 방향을 뒤집음**(단 메이저·마이너는 여전히 helm upgrade) · **API 가 둘** — Cloud API(SaaS 전용, API keys 폐기 예정) 대 Grafana API(Cloud+로컬, 서비스 계정) · **ID 는 설치 안에서만, UID 는 설치를 넘어 고유** · 대시보드는 JSON 이라 fileset·with_fileglob 로 순회 · ⚠️ **알림 코드화는 Terraform 만**(Ansible 미지원). 오퍼레이터·CRD 는 `mastering_prometheus/02-01` 에 위임 |
| [11-01 플랫폼 설계 — 데이터 아키텍처·수집 참조 구조·RBAC](./11-01.플랫폼%20설계%20—%20데이터%20아키텍처·수집%20참조%20구조·RBAC.md) | 11장 전체(**Part 3 마지막**) — **가장 저평가된 단계는 문제 정의**라는 선언으로 시작. 저자의 일화: `tenantID` 와 `customerID` 가 다른 개념으로 결론 나자 **두 시스템 몇 달 작업** — 데이터 모델 책임자가 있었다면 피할 일 · **MoSCoW** 로 요구사항 문서 · **카디널리티가 자리를 정함**(Loki 는 색인 여부로 둘 다, 메트릭은 낮은~중간만, 트레이스는 높은 것) · ⚠️ **조직 고유 필드는 라이브러리가 테스트해 주지 않음** · **수집 참조 아키텍처 4종**(에이전트 없음 → 로컬 → 게이트웨이 → K8s 3부분) — **클러스터 에이전트는 단독이어야 중복이 없음** · 원격만 두면 **HPA 선택지가 사라짐** · 버퍼링은 batch(메모리)·file storage(디스크) · **배포 모드 3종**(monolithic 은 프로덕션 비권장 / Mimir·Tempo=microservices / **Loki 만 simple scalable**) · 메트릭을 Prometheus·OTLP **양쪽**으로 보내는 이유는 **자동 확장** · ⚠️ **가장 좋은 증명 장소는 프로덕션** — 나머지는 모의 환경 · KinD·Vagrant·k6 로 시험 · **RBAC 는 Cloud 와 인스턴스 두 곳** · 기본→고정→커스텀 역할, 커스텀은 **API 로만 생성** · **Cloud 에선 조직 대신 스택** · BI 연계는 기록 규칙으로 미리 계산 |
| [12-01 RUM — Faro SDK·Web Vitals·프론트에서 백엔드로](./12-01.RUM%20—%20Faro%20SDK·Web%20Vitals·프론트에서%20백엔드로.md) | 12장 전체(**Part 4 시작**) — **관측 대상이 처음으로 우리 인프라 밖으로** 나갑니다. 방문자 브라우저에서 도는 코드가 보내오는 데이터라 "우리가 지불하지 않는 비용을 남에게 지운다"는 사실이 거의 모든 판단을 지배 · **Faro Web SDK 기본 수집 6종**(Web Vitals·미처리 예외·브라우저 환경·URL 변경·세션 식별·활동 트레이스) · ⚠️ **메트릭만 저장되지 않음** — 로그는 Loki, 트레이스는 Tempo 로 가지만 **메트릭은 LogQL 메트릭 쿼리로 로그에서 생성**(4장이 제품 기능으로 쓰임) · 앱 라벨 = **Loki 로그에 붙는 라벨** · **주요 섹션 셋**(Overview·Errors·Sessions) + 설정 탭은 별개 · **Web Vitals 여섯**을 로딩 축(TTFB·FCP·LCP)과 상호작용 축(FID·INP·CLS)으로 갈라 봄, CLS 만 무단위 · ⚠️ **책이 예고한 FID→INP 교체가 실제로 일어남**(2024-03-12, 근거는 9장) — 책 표에 FID 는 Core, INP 는 "그 외"로 있어 **자리가 뒤바뀐 표** · **세션 ID 가 접착제** — Sessions → 세션 상세 → Explore → 백엔드 Loki, 단 **나머지 시스템이 계측돼 있어야** 링크가 생김 · 기본 세션은 **종료 이벤트를 안 보냄**(지속 시간 못 구함) · 확장들의 대가는 셋으로 공통(설정·개발 노력·**방문자 브라우저 부담**) · 커스텀 이벤트는 `kind=event` 라벨 로그 |



## 출처·톤 메모

- 원본: Packt — *Observability with Grafana* (ISBN 9781803248004). O'Reilly 학습 플랫폼 경로는 각 장 PDF 하단 URL 에서 확인했습니다(`learning.oreilly.com/library/view/observability-with-grafana/9781803248004`).
- **저자명은 확인하지 못했습니다.** 확보한 15개 장 PDF 와 파트 디바이더 어디에도 저자 표기가 없고, PDF 메타데이터의 author 필드는 브라우저 user-agent 문자열이라 근거가 되지 않습니다. 본문이 자신을 "the authors" 로 복수 지칭하므로 공저라는 사실만 확정입니다. 표지·판권 페이지를 확보하면 채웁니다.
- 정독 노트는 **합니다체**로 쓰고, 형제 단행본 폴더(`mastering_prometheus/`, `dgos_opensearch/`)와 동일한 구조(핵심 요약 → 학습 목표 → 본문 정리 → 책 밖으로 잇기 → 결정 치트시트 → Spring 관점 → 면접 질문 → 정답 → 체크리스트 → 참고 자료 → 관련 문서)를 따릅니다. 각 편에 SVG 또는 Mermaid 를 1장 이상 두고, 책 밖 조사분은 본문 정리와 절을 분리해 출처 링크를 남깁니다.
- 이 책은 1장부터 SaaS(Grafana Cloud 무료 티어)를 기본 전제로 삼는다고 밝힙니다. 이 저장소의 305P 운영기록은 셀프호스팅이므로, 배포 방식이 갈리는 대목마다 어느 전제의 이야기인지 표시합니다.
