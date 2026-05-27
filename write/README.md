---
title: README
tags: []
status: draft
related: []
updated: 2026-04-19
---

# runners-high / write — 학습 MOC

> 최종본만 모이는 공간이다. 실험은 `poc/`에서, 결과만 여기로 올린다. 하네스는 `~/.claude/skills/writing/references/second-brain-harness.md` 참조.

## 카테고리

| # | 경로 | 범위 |
|---|------|------|
| 01 | [01_language/](01_language/) | Java·Go·TS 등 언어별 문법·관용구·생태계. JVM은 Java 하위 `09_jvm/` |
| 02 | [02_os/](02_os/) | OS 공통 기반. Linux 네트워킹(`networking/`)과 커널·namespace·cgroup·/proc(`kernel/`)을 분리해 K8s에서 반복 등장하는 메커니즘을 한 곳에서 관리 |
| 03 | [03_architecture/](03_architecture/) | DDD, Hexagonal, Clean, 설계 원칙·패턴 |
| 04 | [05_data/](05_data/) | CAP, Consistency, Saga, Outbox 등 분산 이론·패턴 |
| 05 | [04_messaging/](04_messaging/) | Kafka, Redpanda, Avro, Schema Registry, EDA 구현 |
| 06 | [05_data/](05_data/) | DB, CDC, Transaction, Indexing (미래) |
| 07 | [06_observability/](06_observability/) | Logging, Tracing, Metrics, OpenTelemetry |
| 08 | [07_devops/](07_devops/) | CI/CD, Jenkins, Nexus, Sonarqube |
| 09 | [08_cloud/](08_cloud/) | Kubernetes(20장)·Service Mesh(26장)·Spring Cloud. 2026-04-19 poc 이관 완료 |
| 10 | [09_tools/](09_tools/) | tmux, vim, Claude Code, Git |
| 11 | [10_security/](10_security/) | OAuth/JWT, OWASP, 위협 모델링, Spring Security |
| 12 | [11_spring/](11_spring/) | Spring 본질 이론 (WebFlux/WebClient, Testing). 도메인 결합 Spring 문서는 각 카테고리에 분산 — 본 폴더 README가 집계점 |
| 99 | [99_ETC/](99_ETC/) | 분류 보류 — 3개월 내 재배치 또는 `_archive`로 |

## Spring 전용 통합 인덱스

Spring 문서는 주제별로 분산 배치되지만 [`11_spring/README.md`](11_spring/README.md)가 전 카테고리 집계점 역할을 한다.

## 예약 폴더 (일반 최종본 아님)

- [`_meta/`](_meta/) — 이 저장소 자체 메타 (컨벤션, 워크플로우 가이드)
- `_company/` — 사내 전용 분석. `.gitignore` 등록
- [`_archive/`](_archive/) — 6개월 무갱신·무참조 문서 수납

## 최근 추가된 final 문서

- 2026-05-16 — [`02_os/kernel/01-06`](02_os/kernel/01-06.cgroup%20사례%20—%20Endowus%20OOMKilled.md) cgroup 사례 — Endowus OOMKilled. Pod 6GB·힙 4.37GB 안전 가정이 깨진 이유를 cgroup RSS 합산(힙 + 오프힙 + 사각지대) 관점으로 풀이. NMT + 힙 덤프 + Grafana 교차 분석으로 jimage 153MB / Akka mailbox 28MB×N / Netty 8코어×16버퍼 = 256MB 범인 식별. 페이지 단위 1단계 reclaim → 2단계 OOMKilled(exit 137 = 128+9) 흐름 + 언어별(Go·Python·Node) 사각지대 일반화 + Pod limit 산정 체크리스트 5항목
- 2026-05-16 — [`02_os/kernel/01-07`](02_os/kernel/01-07.OverlayFS와%20user%20namespace%20—%20Netflix%20UID%20격리.md) OverlayFS와 user namespace — Netflix UID 격리. 컨테이너 탈출 방어용 user namespace + ID map 도입이 OverlayFS lowerdir idmapped mount 호출 폭주(컨테이너 1개당 ~200회 → 100개 동시 = 20,000회)로 이어진 경위. 마운트 글로벌 락 + 스핀 대기 + NUMA + 하이퍼스레딩 + LLC 단일 캐시 토폴로지가 결합해 노드 30초 스톨 → NotReady 5단계로 번진 분석. Linux 6.3 recursive bind mount로 호출 33배 감소. AWS R5 Metal vs M7a/M7i CCX 분산 캐시 비교
- 2026-05-10 — [`01_language/python/testing/`](01_language/python/testing/README.md) Python 통합 테스트 학습 묶음 7편 신규(`qa/python` 기반): 01-01 pytest 기초·마커·parametrize, 01-02 conftest 2단 계층과 fixture(scope·yield), 01-03 requests Session(connection pool·basic auth·5xx vs 4xx 단언 정책), 01-04 pymysql raw SQL·placeholder·`wait_status` 폴링·`FOR UPDATE` 락 경합, 01-05 ThreadPoolExecutor와 pytest-xdist의 두 단 동시성(GIL+I/O bound·QUEUE_ID race 검증), 01-06 chaos fixture(`subprocess.run`·`/etc/hosts` swap·docker compose stop+healthy 폴링·`SKIP_NET_CHAOS` 안전망), 01-07 cryptography hazmat으로 Java `CryptoService`(AES/CBC/PKCS5)와 비트 단위 호환·시드 템플릿 + render 스크립트 자동화. 묶음과 함께 [`01_language/python/`](01_language/python/README.md) 카테고리 신설
- 2026-05-09 — [`11_spring/04_testing/`](11_spring/04_testing/README.md) Spring 테스트 학습 묶음 9편 신규(Spring Boot 3.x 기준): 1장 기초(테스트 피라미드·JUnit5+AssertJ·Mockito+MockMvc·@SpringBootTest와 ApplicationContextRunner), 2장 통합·E2E·가드레일(Testcontainers MariaDB·EmbeddedKafka+DLQ+@RetryableTopic 가드·ArchUnit 5룰 베이스라인·WireMock 외부 시스템 E2E·종합 메시징 플로우 E2E). TPS 3개 모듈(operator/message-lib/executor) 232개 테스트 자산을 사례로 인용 — `AbstractMariaDbIntegrationTest`(`@ServiceConnection`+`@Tag` 베이스), `OutboxPollerIT`(EmbeddedKafka+Testcontainers MariaDB 결합), `KafkaErrorIntegrationIT`(`FailingDeserializer` Test Double + DLQ), `RetryableTopicConfigurationGuardTest`(클래스패스 스캔 가드), `ApprovalArchitectureTest`/`jenkins/ArchitectureTest`(헥사고날 5룰), `SubmittedRecoveryE2ETest`(WireMock + 스케줄러 수동 호출), `ExampleMessageFlowE2ETest`(MockMvc + Outbox + Kafka 풀 E2E + race 흡수 폴링)
- 2026-05-09 — [`11_spring/03_webflux/`](11_spring/03_webflux/README.md) Spring WebClient 학습 묶음 11개 문서 신규(Spring Framework 6.2 / Spring Boot 3.3+ 기준): 입문(RestTemplate·RestClient 비교) → 빌드와 인프라 설정 → 요청 빌딩 → 응답 처리(retrieve/exchangeToMono) → 에러 처리와 재시도 → ExchangeFilterFunction → multipart 업·다운로드 → 동기·비동기 결정(block 안티패턴) → 테스트(MockWebServer·WebTestClient) → TPS `ApprovalUrlAdapter` 사례 분석. 마지막 챕터는 `operator/ticket/approval/` 어댑터(Hexagonal port-out, codecs 50MB, 동적 메서드/헤더, multipart 평탄화, `.block()`, `rsltCd` 검증, `ApprovalUrlInvocationException` wrap)를 풀어 분석
- 2026-05-07 — [`05_data/querydsl/`](05_data/querydsl/README.md) QueryDSL 6.12 (OpenFeign fork) + Spring Boot 3.2.3 학습 묶음: 표준 9편(입문/셋업, 기본 문법·조인, 동적 쿼리, 프로젝션·DTO, 페이징·fetch join 함정, 테스트·멀티모듈, 6.12→7.x 마이그레이션) + 실무 변형 1편(PathBuilder·Embedded ID·상관 서브쿼리·JPQL limit 한계·동적 검색 추상 베이스·nullExpression) + 락·동시성 1편(02-05) + window 함수 대체 1편(02-06). 커스텀 리포지토리 패턴은 [`05_data/jpa/03-05`](05_data/jpa/03-05.커스텀%20리포지토리%20패턴.md) 로 이동(Spring Data JPA 주제)
- 2026-04-26 — [`02_os/`](02_os/README.md) 신설: `networking/`(Linux 네트워크 자료구조)과 `kernel/`(시스템 콜·namespace·cgroup·/proc) 두 하위 폴더로 분리. 기존 `02_runtime/linux/`에서 마이그레이션
- 2026-04-26 — [`02_os/networking/01-01`](02_os/networking/01-01.네트워킹%20기초.md) Linux 네트워킹 기초(netns·veth·bridge·netfilter·conntrack·TC·eBPF)
- 2026-04-26 — [`02_os/kernel/01-01`](02_os/kernel/01-01.커널과%20컨테이너.md) Linux 커널 영역 정리 — 유저/커널 스페이스, 시스템 콜, 코어 7대 영역, namespace/cgroup, /proc, K8s 노드 필수 커널 파라미터, runc create 시퀀스
- 2026-04-26 — [`02_os/kernel/01-02`](02_os/kernel/01-02.cgroup%20v2%20깊이.md) cgroup v2 깊이 — 단일 트리, 컨트롤러 인터페이스, PSI, kubepods.slice·QoS 매핑, throttling/OOM 분석
- 2026-04-26 — [`02_os/kernel/01-03`](02_os/kernel/01-03.마운트%20네임스페이스와%20propagation.md) 마운트 네임스페이스와 propagation — 4종 타입, K8s mountPropagation, CSI 드라이버가 Bidirectional을 요구하는 이유
- 2026-04-26 — K8s 04-* 파일 번호를 학습 순서로 재정렬 — 04-02 Pod·Linux, 04-03 오버레이/BGP, 04-04 Service, 04-05 DNS, 04-06 Ingress
- 2026-04-25 — [`08_cloud/kubernetes/04-02`](08_cloud/kubernetes/04-02.Pod%20네트워크와%20Linux%20기반.md) Pod 네트워크 Linux 기반 + [`04-03`](08_cloud/kubernetes/04-03.오버레이와%20노드%20간%20트래픽.md) 오버레이/BGP 추가, 인터랙티브 시각화 2종 포함
- 2026-04-25 — [`08_cloud/service-mesh/14-05`](08_cloud/service-mesh/14-05.Cilium과%20Istio%20Ambient%20통합%20전략.md) Cilium+Ambient 통합 전략 추가
- 2026-04-19 — [`08_cloud/kubernetes/`](08_cloud/kubernetes/README.md) 20장 + 실습 20편 이관 (로컬 클러스터·Helm·Operator·DB/DevTools·GitOps·보안·오토스케일링·자원 관리)
- 2026-04-19 — [`08_cloud/service-mesh/`](08_cloud/service-mesh/README.md) 26장 + 실습 26편 이관 (기초·Linkerd·Istio·멀티클러스터·eBPF·도입 전략)

## 규칙 요약

- 모든 `.md`에 프론트매터 필수(`status`, `updated`, `tags`, `related`)
- 파일명: `{장}-{절}.{제목}.md` (`08-01.EDA 기초.md` 형태)
- 상세: [`_meta/conventions.md`](_meta/conventions.md)
