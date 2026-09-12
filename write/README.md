---
title: README
tags: [moc, index]
status: final
related:
  - roadmap/README.md
  - 08_cloud/kubernetes/04_networking/README.md
updated: 2026-09-12
---

# write — 학습 문서 지도(MOC)

---

> 공부한 내용의 최종본만 모이는 공간입니다. 실험과 초안은 다른 곳에서 하고, 다시 읽을 가치가 생긴 결과만 여기로 올립니다.

이 문서는 지도입니다. 각 카테고리에 무엇이 있는지 한눈에 보여 주고, 세부 목록은 카테고리별 README로 넘깁니다. 그래서 여기서는 개별 문서를 나열하지 않습니다. 찾는 주제의 카테고리로 들어가면 그 안의 README가 다시 안내합니다.

## 카테고리

> 주제가 1차 분류 축입니다. 언어·프레임워크 구분은 그 아래 폴더로 내려갑니다. 예를 들어 JVM은 `01_language/book/Inside the Java Virtual Machine JVM Advanced Features and Best Practices/`에 있습니다.

| # | 카테고리 | 범위 |
|---|----------|------|
| 01 | [`01_language/`](01_language/) | Java·Python 등 언어별 문법·관용구·표준 API. JVM 심화 포함 |
| 02 | [`02_os/`](02_os/) | 커널·네임스페이스·cgroup·네트워킹 등 OS 공통 기반. K8s에서 반복되는 메커니즘을 한곳에 |
| 03 | [`03_architecture/`](03_architecture/) | DDD·Hexagonal·Clean, 설계 원칙과 패턴 |
| 04 | [`04_messaging/`](04_messaging/) | Kafka·Redpanda·Avro·Schema Registry, 이벤트 기반 아키텍처 구현 |
| 05 | [`05_data/`](05_data/) | 분산 이론(CAP·합의·트랜잭션)부터 DB·CDC·QueryDSL까지 |
| 06 | [`06_observability/`](06_observability/) | 로깅·트레이싱·메트릭·OpenTelemetry |
| 07 | [`07_devops/`](07_devops/) | CI/CD·Jenkins·Nexus·SonarQube |
| 08 | [`08_cloud/`](08_cloud/) | Kubernetes·Service Mesh·ArgoCD·OpenStack |
| — | [`99_ETC/security/`](99_ETC/security/) | OAuth/JWT·OWASP·Spring Security |
| 09 | [`09_spring/`](09_spring/) | Spring 본질 이론. 도메인과 얽힌 Spring 문서는 각 카테고리에 흩어져 있고, 이 폴더가 집계점 |
| 10 | [`10_AI/`](10_AI/) | 생성형 AI·에이전트 활용 |
| 11 | [`11_career/`](11_career/) | 커리어·성장 기록 |
| — | [`troubleshooting/`](troubleshooting/) | 장애 사례와 진단 훈련. 주제를 가로지르는 형식이라 번호 없음 |
| 99 | [`99_ETC/`](99_ETC/) | 분류 보류. 일정 기간 체류한 뒤 재배치하거나 아카이브 |



## 학습 로드맵

> 무엇을 어떤 순서로 읽을지는 [`roadmap/`](roadmap/) 이 정합니다. 카테고리 README 는 자료가 *어디에* 있는지를 맡고, 로드맵은 *무엇부터* 열지를 맡습니다.

로드맵을 카테고리 안에 두지 않는 이유는 하나입니다 — **학습 주제가 카테고리 경계를 지키지 않습니다.** 네트워크는 `02_os`·`08_cloud`·`99_ETC` 에 걸쳐 있고, Kubernetes 로드맵은 커널·분산 합의·관측을 각각 다른 카테고리에서 끌어옵니다. 로드맵을 폴더에 두면 문서마다 "이건 저쪽" 위임 각주를 달아야 하고 그 각주가 서로를 가리킵니다. 한곳에 모으면 그 조율을 문서 사이에서 한 번만 합니다.

| 로드맵 | 무엇을 정하나 | 상태 |
|---|---|---|
| [go-roadmap.md](roadmap/go-roadmap.md) | 문법을 빨리 통과하고 관용구와 동시성에 시간을 몰아주는 순서 | `final` |
| [network-roadmap.md](roadmap/network-roadmap.md) | socket과 Linux 패킷 경로에서 Kubernetes 네트워크까지 | `final` |
| [os-roadmap.md](roadmap/os-roadmap.md) | DevOps 로서 쓰는 OS 지식부터 커널 내부까지 | `final` |
| [k8s-roadmap.md](roadmap/k8s-roadmap.md) | 오브젝트를 굴려 보고 안 될 때 한 층씩 안으로 | `final` |
| [data-roadmap.md](roadmap/data-roadmap.md) | 데이터 시스템의 축에서 저장 엔진·복제·합의·스트림까지 | `final` |
| [observability-roadmap.md](roadmap/observability-roadmap.md) | 계측과 세 신호에서 SLO·확장·플랫폼까지 | `final` |
| [jvm-roadmap.md](roadmap/jvm-roadmap.md) | 런타임 데이터 영역에서 GC·동시성·장애 진단까지 | `final` |
| [ai-roadmap.md](roadmap/ai-roadmap.md) | 모델을 도구로 부리는 법에서 GitAIOps 운영까지 | `final` |
| [spring-roadmap.md](roadmap/spring-roadmap.md) | 컨테이너와 프록시에서 부트·보안·운영·배포까지 | `final` |

로드맵은 단계마다 배우는 개념 표와 우선순위, 그 개념을 다루는 책의 읽을 장을 함께 둡니다.

OS 기반은 `os-roadmap.md`, Kubernetes 오브젝트와 운영은 `k8s-roadmap.md`, 패킷 경로는 `network-roadmap.md`를 정본으로 봅니다.



## Spring 문서를 찾을 때

Spring 자료는 주제별로 흩어져 있습니다. WebFlux나 테스트처럼 Spring 본질에 가까운 문서는 `09_spring/`에 있고, QueryDSL이나 Kafka 연동처럼 도메인과 붙은 문서는 해당 카테고리에 있습니다. 전 카테고리에 걸친 Spring 문서 집계는 [`09_spring/README.md`](09_spring/README.md)에서 확인합니다.



## 예약 폴더

카테고리 번호가 아니라 밑줄로 시작하는 폴더는 일반 최종본이 아닙니다. [`_meta/`](_meta/)는 이 저장소의 컨벤션과 워크플로우 가이드를 담고, [`_archive/`](_archive/)는 오래 갱신되지 않고 다른 문서가 참조하지도 않는 글을 수납합니다. [`_company/`](_company/)는 회사 업무에서 나온 분석과 기록이라 학습 문서와 성격이 달라 따로 두고, [`_review/`](_review/)는 날짜별 리뷰 기록이라 결과가 아니라 과정입니다.



## 작성 규칙

모든 `.md`는 프론트매터(`status`·`updated`·`tags`·`related`)를 갖추고, 파일명은 `{장}-{절}.{제목}.md` 형식을 따릅니다(예: `04-01.EDA 기초.md`). 자세한 규약은 [`_meta/conventions.md`](_meta/conventions.md)에 있습니다.
