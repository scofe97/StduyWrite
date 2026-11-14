---
title: README
tags: [moc, index]
status: final
related:
  - _digest/README.md
updated: 2026-10-06
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

`01`부터 `10`까지의 주제 폴더 안은 출처에 따라 세 갈래로 나눕니다. 책 한 권의 정독 노트는 `book/`에, 직접 만든 실습 프로젝트의 학습 문서는 `project/`에, 공식문서·가이드·블로그·강의·세미나 정리와 여러 출처를 합친 개념 노트는 `docs/`에 둡니다. 예를 들어 TCP/IP Illustrated 노트는 `02_os/book/`에 있습니다.

이 규칙보다 먼저 만든 번호 폴더(`03_architecture/01_foundation/` 등)와 주제 루트의 낱장 문서는 아직 옮기지 않았습니다. 자세한 기준은 writing-method 스킬의 파일 배치 규약 §4.2.1 에 있습니다.



## 개발 키워드와 AI 요약

> 분야별 개발 키워드 표는 각 카테고리 폴더 바로 아래에, 외부 AI 요약은 [`_digest/`](_digest/README.md) 에 둡니다. 카테고리 README 는 자료가 *어디에* 있는지를 맡고, 키워드 표는 문서를 쓸 때 *어떤 개념이 있는지* 를 짚습니다.

키워드 표는 `노트` 칸 링크가 가장 많이 가리키는 카테고리에 둡니다. 다른 카테고리의 개념은 링크로 가리킵니다.

| 키워드 표 | 다루는 범위 | 상태 |
|---|---|---|
| [go-keywords.md](01_language/go-keywords.md) | 문법·타입 설계·동시성·서비스·터미널 세션 | `final` |
| [network-keywords.md](02_os/network-keywords.md) | socket과 Linux 패킷 경로에서 클라우드 underlay와 오버레이 터널까지 | `final` |
| [os-keywords.md](02_os/os-keywords.md) | DevOps 로서 쓰는 OS 지식부터 커널 내부까지 | `final` |
| [k8s-keywords.md](08_cloud/k8s-keywords.md) | 오브젝트에서 내부 구조·보안·운영까지 | `final` |
| [devops-keywords.md](07_devops/devops-keywords.md) | 전달 모델과 CI 파이프라인에서 GitOps·점진 배포·파이프라인 보안까지 | `draft` |
| [data-keywords.md](05_data/data-keywords.md) | 데이터 시스템의 축에서 저장 엔진·복제·합의·스트림까지 | `final` |
| [observability-keywords.md](06_observability/observability-keywords.md) | 계측과 세 신호에서 SLO·확장·플랫폼까지 | `final` |
| [jvm-keywords.md](01_language/jvm-keywords.md) | 런타임 데이터 영역에서 GC·동시성·장애 진단까지 | `final` |
| [ai-keywords.md](10_AI/ai-keywords.md) | 모델을 도구로 부리는 법에서 GitAIOps 운영까지 | `final` |
| [spring-keywords.md](09_spring/spring-keywords.md) | 컨테이너와 프록시에서 부트·보안·운영·배포까지 | `final` |

키워드 표는 개념마다 우선순위와 그 개념을 다루는 노트·책을 함께 둡니다. 외부 AI 요약은 `_digest/` 에 `YYYY-MM-DD_주제.md` 로 둡니다. 출처·날짜·분야·미검증을 머리 한 줄에 적고, Pages 에는 올라가지 않습니다.

OS 기반은 `os-keywords.md`, Kubernetes 오브젝트와 운영은 `k8s-keywords.md`, 패킷 경로는 `network-keywords.md`를 정본으로 봅니다.



## Spring 문서를 찾을 때

Spring 자료는 주제별로 흩어져 있습니다. WebFlux나 테스트처럼 Spring 본질에 가까운 문서는 `09_spring/`에 있고, QueryDSL이나 Kafka 연동처럼 도메인과 붙은 문서는 해당 카테고리에 있습니다. 전 카테고리에 걸친 Spring 문서 집계는 [`09_spring/README.md`](09_spring/README.md)에서 확인합니다.



## 예약 폴더

카테고리 번호가 아니라 밑줄로 시작하는 폴더는 일반 최종본이 아닙니다. [`_company/`](_company/)는 회사 업무에서 나온 분석과 기록이라 학습 문서와 성격이 달라 따로 두고, [`_review/`](_review/)는 날짜별 리뷰 기록이라 결과가 아니라 과정입니다.



## 작성 규칙

모든 `.md`는 프론트매터(`status`·`updated`·`tags`·`related`)를 갖추고, 파일명은 `{장}-{절}.{제목}.md` 형식을 따릅니다(예: `04-01.EDA 기초.md`).
