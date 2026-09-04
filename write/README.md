---
title: README
tags: [moc, index]
status: final
related:
  - 02_os/networking/roadmap.md
  - 08_cloud/kubernetes/04_networking/README.md
updated: 2026-09-05
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
| — | `tools/` <!-- 링크 끊김(2026-09): 99_ETC/tools/ 가 사라짐 --> | tmux·vim·Git·Claude Code |
| — | [`99_ETC/security/`](99_ETC/security/) | OAuth/JWT·OWASP·Spring Security |
| 09 | [`09_spring/`](09_spring/) | Spring 본질 이론. 도메인과 얽힌 Spring 문서는 각 카테고리에 흩어져 있고, 이 폴더가 집계점 |
| 10 | [`10_AI/`](10_AI/) | 생성형 AI·에이전트 활용 |
| 11 | [`11_career/`](11_career/) | 커리어·성장 기록 |
| 99 | [`99_ETC/`](99_ETC/) | 분류 보류. 일정 기간 체류한 뒤 재배치하거나 아카이브 |



## 학습 로드맵

> 한 카테고리에 담기지 않는 주제의 읽기 순서입니다. 여러 카테고리를 가로질러서 카테고리 README가 혼자 가질 수 없어 이 층에 둡니다.

| 로드맵 | 무엇을 정하나 | 가로지르는 카테고리 |
|---|---|---|
| [network-roadmap.md](network-roadmap.md) | Kubernetes 네트워크를 요소 단위로 덮는 읽기 순서 | `02_os` · `08_cloud` · `99_ETC/security` |
| [os-roadmap.md](os-roadmap.md) | DevOps 로서 쓰는 OS 지식부터 커널 내부까지 | `02_os` · `08_cloud` |
| [go-roadmap.md](go-roadmap.md) | 문법을 빨리 통과하고 관용구와 동시성에 시간을 몰아주는 순서 | `01_language` · `02_os` · `08_cloud` |

셋 다 단계마다 배우는 개념 표와 책 밖 키워드 표를 두고, 출간 연도로 낡은 책을 걸러 공식 문서로 대신합니다.



## Spring 문서를 찾을 때

Spring 자료는 주제별로 흩어져 있습니다. WebFlux나 테스트처럼 Spring 본질에 가까운 문서는 `09_spring/`에 있고, QueryDSL이나 Kafka 연동처럼 도메인과 붙은 문서는 해당 카테고리에 있습니다. 전 카테고리에 걸친 Spring 문서 집계는 [`09_spring/README.md`](09_spring/README.md)에서 확인합니다.



## 예약 폴더

카테고리 번호가 아니라 밑줄로 시작하는 폴더는 일반 최종본이 아닙니다. [`_meta/`](_meta/)는 이 저장소의 컨벤션과 워크플로우 가이드를 담고, [`_archive/`](_archive/)는 오래 갱신되지 않고 다른 문서가 참조하지도 않는 글을 수납합니다. [`_company/`](_company/)는 회사 업무에서 나온 분석과 기록이라 학습 문서와 성격이 달라 따로 두고, [`_review/`](_review/)는 날짜별 리뷰 기록이라 결과가 아니라 과정입니다.



## 작성 규칙

모든 `.md`는 프론트매터(`status`·`updated`·`tags`·`related`)를 갖추고, 파일명은 `{장}-{절}.{제목}.md` 형식을 따릅니다(예: `04-01.EDA 기초.md`). 자세한 규약은 [`_meta/conventions.md`](_meta/conventions.md)에 있습니다.
