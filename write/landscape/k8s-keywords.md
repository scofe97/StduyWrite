---
title: Kubernetes 개발 키워드
tags: [landscape, kubernetes, k8s, cloud-native, operations, security, eks, iac]
status: final
source:
  - ../08_cloud/kubernetes/README.md
  - ../08_cloud/book/kubernetes-in-action/README.md
related:
  - README.md
  - os-keywords.md
  - network-keywords.md
  - observability-keywords.md
  - devops-keywords.md
  - ../08_cloud/kubernetes/README.md
updated: 2026-10-28
---

# Kubernetes 개발 키워드
---

> Kubernetes 개발 키워드 표. 문서를 쓸 때 참고합니다.



## 1단계 · 오브젝트

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| API resource · 매니페스트 · `metadata` · `spec` · `status` | 필수 | [API와 매니페스트](../08_cloud/book/kubernetes-in-action/04-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20API%EC%99%80%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EB%A7%A4%EB%8B%88%ED%8E%98%EC%8A%A4%ED%8A%B8%20%EA%B5%AC%EC%A1%B0.md) · [Node·Event 필드 실습](../08_cloud/book/kubernetes-in-action/04-02.Node%EC%99%80%20Event%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%ED%95%84%EB%93%9C%20%EC%8B%A4%EC%8A%B5.md) | Kubernetes in Action 4장 |
| Pod · 컨테이너 그룹화 · 사이드카 | 필수 | [Pod 이해](../08_cloud/book/kubernetes-in-action/05-01.Pod%20%EC%9D%B4%ED%95%B4%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B7%B8%EB%A3%B9%ED%99%94%EC%99%80%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4.md) · [멀티 컨테이너·사이드카](../08_cloud/book/kubernetes-in-action/05-03.%EB%A9%80%ED%8B%B0%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7init%C2%B7%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EC%99%80%20%EC%82%AD%EC%A0%9C.md) | Kubernetes in Action 5장 |
| phase · conditions · 컨테이너 상태 · restart 정책 | 필수 | [Pod 상태](../08_cloud/book/kubernetes-in-action/06-01.Pod%20%EC%83%81%ED%83%9C%20%E2%80%94%20phase%C2%B7conditions%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%83%81%ED%83%9C.md) | Kubernetes in Action 6장 |
| liveness · readiness · startup probe | 필수 | [liveness·startup probe](../08_cloud/book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) · [Health Probe](../08_cloud/book/kubernetes-patterns/04-01.Health%20Probe%20%E2%80%94%20%EC%95%B1%EC%9D%B4%20%EC%9E%90%EA%B8%B0%20%EA%B1%B4%EA%B0%95%EC%9D%84%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Kubernetes Patterns 4장 |
| lifecycle hook · 종료 흐름 | 필수 | [lifecycle hook](../08_cloud/book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) · [Managed Lifecycle](../08_cloud/book/kubernetes-patterns/05-01.Managed%20Lifecycle%20%E2%80%94%20%ED%94%8C%EB%9E%AB%ED%8F%BC%EC%9D%98%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%9D%B4%EB%B2%A4%ED%8A%B8%EC%97%90%20%EB%B0%98%EC%9D%91%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 5장 |
| namespace · label · label selector | 필수 | [namespace](../08_cloud/book/kubernetes-in-action/07-01.namespace%EB%A1%9C%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A5%BC%20%EA%B0%80%EC%83%81%20%EB%B6%84%ED%95%A0%ED%95%98%EA%B8%B0.md) · [label·selector](../08_cloud/book/kubernetes-in-action/07-02.label%EA%B3%BC%20label%20selector%EB%A1%9C%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%A1%B0%EC%A7%81%ED%95%98%EA%B8%B0.md) | Kubernetes in Action 7장 |
| field selector · annotation | 추천 | [field selector·annotation](../08_cloud/book/kubernetes-in-action/07-03.field%20selector%EC%99%80%20annotation.md) | Kubernetes in Action 7장 |
| `command` · `args` · 환경변수 | 필수 | [command·args](../08_cloud/book/kubernetes-in-action/08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md) · [EnvVar Configuration](../08_cloud/book/kubernetes-patterns/19-01.EnvVar%20Configuration%20%E2%80%94%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98%EB%A1%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%99%B8%EB%B6%80%ED%99%94%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 19장 |
| ConfigMap · Secret · Downward API | 필수 | [ConfigMap](../08_cloud/book/kubernetes-in-action/08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md) · [Secret과 Downward API](../08_cloud/book/kubernetes-in-action/08-03.Secret%EA%B3%BC%20Downward%20API.md) · [Configuration Resource](../08_cloud/book/kubernetes-patterns/20-01.Configuration%20Resource%20%E2%80%94%20ConfigMap%EA%B3%BC%20Secret%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC.md) · [Immutable Configuration](../08_cloud/book/kubernetes-patterns/21-01.Immutable%20Configuration%20%E2%80%94%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EB%B6%88%EB%B3%80%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A1%9C.md) · [Configuration Template](../08_cloud/book/kubernetes-patterns/22-01.Configuration%20Template%20%E2%80%94%20%ED%81%B0%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%8B%9C%EC%9E%91%20%EC%8B%9C%20%ED%85%9C%ED%94%8C%EB%A6%BF%EC%9C%BC%EB%A1%9C%20%EC%83%9D%EC%84%B1.md) | Kubernetes Patterns 20~22장 |
| kubectl 기본 조회 | 필수 | | Kubernetes: Up and Running 4장 |
| 컨테이너 격리 — namespace · cgroup | 추천 | [namespace·cgroup 격리](../08_cloud/book/kubernetes-in-action/02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) · [OS 로드맵](os-keywords.md) · [컨테이너와 가상머신](../08_cloud/book/kubernetes-in-action/02-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0.md) | Kubernetes in Action 2장 |
| 12-Factor App · 설정 관리 | 선택 | [설정 관리](../09_spring/books/cloud-native-spring-in-action/04.%EC%99%B8%EB%B6%80%ED%99%94%20%EC%84%A4%EC%A0%95%20%EA%B4%80%EB%A6%AC.md) | |
| 불변 인프라 | 선택 | [불변 인프라](../99_ETC/2026-04-19_Reconciliation%20Loop%EC%9D%98%20%EA%B3%84%EB%B3%B4%20%E2%80%94%20%EC%A0%9C%EC%96%B4%EC%9D%B4%EB%A1%A0%EC%97%90%EC%84%9C%20GitOps%EA%B9%8C%EC%A7%80.md) | |
| 타입 1 하이퍼바이저 · 타입 2 하이퍼바이저 | 선택 | [타입 1 하이퍼바이저](../08_cloud/book/container-security/05-01.%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%20%E2%80%94%20%EC%99%9C%20VM%20%EA%B2%A9%EB%A6%AC%EA%B0%80%20%EB%8D%94%20%EA%B0%95%ED%95%98%EB%8B%A4%EA%B3%A0%20%ED%95%98%EB%8A%94%EA%B0%80.md) · [타입 2 하이퍼바이저](../08_cloud/book/container-security/05-01.%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0%20%E2%80%94%20%EC%99%9C%20VM%20%EA%B2%A9%EB%A6%AC%EA%B0%80%20%EB%8D%94%20%EA%B0%95%ED%95%98%EB%8B%A4%EA%B3%A0%20%ED%95%98%EB%8A%94%EA%B0%80.md) | |
| 헬스 체크 · 헬스 체크 엔드포인트 · 헬스 프로브 · 레디니스 프로브 · 라이브니스 프로브 · 스타트업 프로브 | 선택 | [헬스 체크 엔드포인트](../08_cloud/docs/kubernetes/04-01.API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%20%E2%80%94%20livez%EC%99%80%20readyz%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%82%98%EB%88%A0%20%EB%AC%BB%EB%8A%94%EA%B0%80.md) · [헬스 프로브](../08_cloud/book/networking-and-kubernetes/04-01.Kubernetes%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9%20%EB%AA%A8%EB%8D%B8%20%E2%80%94%20Pod%20IP%C2%B7%EB%A0%88%EC%9D%B4%EC%95%84%EC%9B%83%C2%B7Probe.md) · [레디니스 프로브](../08_cloud/book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) · [라이브니스 프로브](../08_cloud/book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) · [스타트업 프로브](../08_cloud/book/kubernetes-in-action/06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) | |
| 우아한 종료 · 그레이스풀 셧다운 훅 · 시그널 핸들링 · 연결 드레인 · 프로세스 슈퍼비전 · 재시작 정책 | 선택 | [우아한 종료](../01_language/book/Inside%20the%20Java%20Virtual%20Machine%20JVM%20Advanced%20Features%20and%20Best%20Practices/ch05_efficient-concurrency/04-01.Executor%20%ED%94%84%EB%A0%88%EC%9E%84%EC%9B%8C%ED%81%AC.md) · [그레이스풀 셧다운 훅](../08_cloud/book/kubernetes-in-action/06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) · [연결 드레인](../02_os/project/npg-lab/01-03.%EB%A6%AC%EB%B2%84%EC%8A%A4%20%ED%94%84%EB%A1%9D%EC%8B%9C%20%EB%8B%A4%EC%9A%B4%EC%8A%A4%ED%8A%B8%EB%A6%BC%20%EC%B8%B5%20%E2%80%94%20%ED%8B%88%20%EC%8B%9C%EA%B3%84%C2%B7%EC%B5%9C%EC%86%8C%20%EC%86%8D%EB%8F%84%C2%B7%EB%93%9C%EB%A0%88%EC%9D%B8.md) · [프로세스 슈퍼비전](../07_devops/02_Jenkins/02_security/03-01.%ED%94%84%EB%A1%9C%EC%84%B8%EC%8A%A4%C2%B7%ED%8C%8C%EC%9D%BC%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EA%B2%A9%EB%A6%AC%20%E2%80%94%20%EC%9B%8C%ED%82%B9%20%EB%94%94%EB%A0%89%ED%86%A0%EB%A6%AC%20%EB%B0%96%EC%9C%BC%EB%A1%9C%20%EB%AA%BB%20%EB%82%98%EA%B0%80%EA%B2%8C.md) · [재시작 정책](../08_cloud/book/kubernetes-up-and-running/12-01.Jobs%20%E2%80%94%20%EB%81%9D%EB%82%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20work%20queue%20%EB%9E%A9.md) | |



## 2단계 · 워크로드

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| ReplicaSet · reconciliation · 소유 관계 | 필수 | [ReplicaSet 기초](../08_cloud/book/kubernetes-in-action/14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) · [ReplicaSet 컨트롤러](../08_cloud/book/kubernetes-in-action/14-02.ReplicaSet%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20%E2%80%94%20reconciliation%C2%B7%EC%9E%A5%EC%95%A0%EB%B3%B5%EA%B5%AC%C2%B7%EC%82%AD%EC%A0%9C.md) | Kubernetes in Action 14장 |
| Deployment · pod-template-hash | 필수 | [Deployment 기초](../08_cloud/book/kubernetes-in-action/15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | Kubernetes in Action 15장 |
| RollingUpdate · Recreate · `maxSurge` · `maxUnavailable` | 필수 | [Deployment 업데이트](../08_cloud/book/kubernetes-in-action/15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md) · [Declarative Deployment](../08_cloud/book/kubernetes-patterns/03-01.Declarative%20Deployment%20%E2%80%94%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%C2%B7%EB%A1%A4%EB%B0%B1%EC%9D%84%20%EC%84%A0%EC%96%B8%EC%9C%BC%EB%A1%9C.md) | Kubernetes Patterns 3장 |
| rollout 제어 · pause · rollback · 배포 전략 다섯 | 필수 | [rollout 제어](../08_cloud/book/kubernetes-in-action/15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) | Kubernetes in Action 15장 |
| StatefulSet · ordinal · headless Service · retention | 필수 | [StatefulSet 기초](../08_cloud/book/kubernetes-in-action/16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md) · [StatefulSet 동작](../08_cloud/book/kubernetes-in-action/16-02.StatefulSet%20%EB%8F%99%EC%9E%91%20%E2%80%94%20%EB%AF%B8%EC%8B%B1%20%ED%8C%8C%EB%93%9C%C2%B7%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%C2%B7retention.md) · [Stateful Service](../08_cloud/book/kubernetes-patterns/12-01.Stateful%20Service%20%E2%80%94%20StatefulSet%EC%9C%BC%EB%A1%9C%20%EC%83%81%ED%83%9C%EB%A5%BC%20first-class%EB%A1%9C.md) | Kubernetes Patterns 12장 |
| DaemonSet · hostNetwork · hostPort | 필수 | [DaemonSet 기초](../08_cloud/book/kubernetes-in-action/17-01.DaemonSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%ED%95%98%EB%82%98%C2%B7node%20selector%C2%B7%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8.md) · [노드 에이전트 기능](../08_cloud/book/kubernetes-in-action/17-02.%EB%85%B8%EB%93%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8A%B9%EC%88%98%20%EA%B8%B0%EB%8A%A5%20%E2%80%94%20privileged%C2%B7hostPath%C2%B7hostNetwork%C2%B7PriorityClass.md) · [Daemon Service](../08_cloud/book/kubernetes-patterns/09-01.Daemon%20Service%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%EB%8F%84%EB%8A%94%20%EC%9D%B8%ED%94%84%EB%9D%BC%20Pod.md) | Kubernetes Patterns 9장 |
| Job · CronJob · 병렬 · 완료 모드 · work queue | 추천 | [Job 기초](../08_cloud/book/kubernetes-in-action/18-01.Job%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%8B%A4%ED%96%89%C2%B7%EC%83%81%ED%83%9C%C2%B7suspend%C2%B7%EC%9E%90%EB%8F%99%EC%82%AD%EC%A0%9C.md) ~ [work queue·CronJob](../08_cloud/book/kubernetes-in-action/18-03.work%20queue%C2%B7pod%20%ED%86%B5%EC%8B%A0%C2%B7sidecar%C2%B7CronJob.md) · [Batch Job](../08_cloud/book/kubernetes-patterns/07-01.Batch%20Job%20%E2%80%94%20%EC%9C%A0%ED%95%9C%ED%95%9C%20%EC%9E%91%EC%97%85%EC%9D%84%20%EC%99%84%EB%A3%8C%EA%B9%8C%EC%A7%80%20%EC%95%88%EC%A0%95%EC%A0%81%EC%9C%BC%EB%A1%9C.md) · [Periodic Job](../08_cloud/book/kubernetes-patterns/08-01.Periodic%20Job%20%E2%80%94%20CronJob%EC%9C%BC%EB%A1%9C%20%EC%8B%9C%EA%B0%84%20%EC%B6%95%EC%9D%84%20%EB%8D%94%ED%95%98%EB%8B%A4.md) | Kubernetes Patterns 7·8장 |
| init container · sidecar | 추천 | [Init Container](../08_cloud/book/kubernetes-patterns/15-01.Init%20Container%20%E2%80%94%20%EC%B4%88%EA%B8%B0%ED%99%94%EB%A5%BC%20%EC%95%B1%EA%B3%BC%20%EB%B6%84%EB%A6%AC%ED%95%B4%20%EB%B3%84%EB%8F%84%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%EB%A1%9C.md) · [Sidecar](../08_cloud/book/kubernetes-patterns/16-01.Sidecar%20%E2%80%94%20%EA%B8%B0%EC%A1%B4%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EB%A5%BC%20%EB%B0%94%EA%BE%B8%EC%A7%80%20%EC%95%8A%EA%B3%A0%20%ED%99%95%EC%9E%A5.md) | Kubernetes Patterns 15·16장 |
| adapter · ambassador | 선택 | [Adapter](../08_cloud/book/kubernetes-patterns/17-01.Adapter%20%E2%80%94%20%EC%9D%B4%EC%A7%88%EC%A0%81%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%9D%84%20%ED%86%B5%EC%9D%BC%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%EB%A1%9C.md) · [Ambassador](../08_cloud/book/kubernetes-patterns/18-01.Ambassador%20%E2%80%94%20%EB%B0%94%EA%B9%A5%EC%84%B8%EC%83%81%EC%9C%BC%EB%A1%9C%EC%9D%98%20smart%20proxy.md) | Kubernetes Patterns 17·18장 |
| Singleton Service · Stateless Service | 선택 | [Singleton Service](../08_cloud/book/kubernetes-patterns/10-01.Singleton%20Service%20%E2%80%94%20%ED%95%9C%20%EB%B2%88%EC%97%90%20%ED%95%98%EB%82%98%EB%A7%8C%20%ED%99%9C%EC%84%B1%EC%9D%B4%EB%90%98%20%EA%B3%A0%EA%B0%80%EC%9A%A9.md) · [Stateless Service](../08_cloud/book/kubernetes-patterns/11-01.Stateless%20Service%20%E2%80%94%20%EB%8F%99%EC%9D%BC%C2%B7%EA%B5%90%EC%B2%B4%20%EA%B0%80%EB%8A%A5%ED%95%9C%20replica%EB%A1%9C%20%EC%88%98%ED%8F%89%20%ED%99%95%EC%9E%A5.md) | Kubernetes Patterns 10·11장 |
| 스테이트풀셋 · 데몬셋 · 크론잡 · 리소스 리퀘스트 · 리소스 리밋 · 노드 어피니티 | 선택 | [스테이트풀셋](../08_cloud/book/networking-and-kubernetes/05-01.StatefulSet%C2%B7Endpoints%C2%B7EndpointSlices%20%E2%80%94%20%EC%84%9C%EB%B9%84%EC%8A%A4%EC%9D%98%20%EC%9E%AC%EB%A3%8C.md) · [크론잡](../07_devops/book/aic_ai-infra-claude/08-02.CronJob%20%EB%B0%B0%EC%B9%98%20%EC%9E%90%EB%8F%99%ED%99%94%EC%99%80%20command-guardrails.md) · [리소스 리퀘스트](../08_cloud/book/kubernetes-patterns/02-01.Predictable%20Demands%20%E2%80%94%20%EC%9E%90%EC%9B%90%20%EC%9A%94%EA%B5%AC%EB%A5%BC%20%EC%84%A0%EC%96%B8%ED%95%B4%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) · [리소스 리밋](../08_cloud/book/kubernetes-patterns/02-01.Predictable%20Demands%20%E2%80%94%20%EC%9E%90%EC%9B%90%20%EC%9A%94%EA%B5%AC%EB%A5%BC%20%EC%84%A0%EC%96%B8%ED%95%B4%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | |
| 서버리스 · 콜드 스타트 · 웜 스타트 · 프리워밍 · 프로비저닝 동시성 · 예약 동시성 | 선택 | [서버리스](../03_architecture/book/bytebytego-system-design/06-01.IaaS%C2%B7PaaS%C2%B7SaaS%20%EC%99%80%20%EA%B0%80%EC%83%81%20%EB%A8%B8%EC%8B%A0%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7%EC%84%9C%EB%B2%84%EB%A6%AC%EC%8A%A4%EB%8A%94%20%EC%9A%B4%EC%98%81%20%EC%B1%85%EC%9E%84%EC%9D%84%20%EC%96%B4%EB%94%94%EA%B9%8C%EC%A7%80%20%EB%84%98%EA%B8%B0%EB%8A%94%EC%A7%80%EB%A1%9C%20%EA%B0%88%EB%A6%B0%EB%8B%A4.md) | |



## 3단계 · 연결

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| Service · ClusterIP · 세션 어피니티 | 필수 | [Service 기초](../08_cloud/book/kubernetes-in-action/11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md) · [Service 5유형](../08_cloud/book/networking-and-kubernetes/05-02.Service%205%EC%9C%A0%ED%98%95%20%E2%80%94%20ClusterIP%EC%97%90%EC%84%9C%20LoadBalancer%EA%B9%8C%EC%A7%80.md) | Kubernetes in Action 11장 |
| NodePort · LoadBalancer · 트래픽 정책 | 필수 | [외부 노출](../08_cloud/book/kubernetes-in-action/11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) | Kubernetes in Action 11장 |
| Endpoint · EndpointSlice · readiness 연동 · 토폴로지 | 필수 | [엔드포인트·DNS·readiness](../08_cloud/book/kubernetes-in-action/11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) | Networking and Kubernetes 5장 |
| 클러스터 DNS · Service FQDN | 필수 | [Kubernetes 레코드](../08_cloud/book/learning-coredns/06-01.%EB%AC%B4%EC%97%87%EC%9D%84%20%EC%84%A0%EC%96%B8%ED%96%88%EB%8A%90%EB%83%90%EA%B0%80%20%EB%A0%88%EC%BD%94%EB%93%9C%20%EB%AA%A8%EC%96%91%EC%9D%84%20%EC%A0%95%ED%95%9C%EB%8B%A4.md) · [Service Discovery](../08_cloud/book/kubernetes-patterns/13-01.Service%20Discovery%20%E2%80%94%20%EA%B3%A0%EC%A0%95%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%EB%A1%9C%20%EB%8F%99%EC%A0%81%20Pod%EB%A5%BC%20%EC%B0%BE%EA%B8%B0.md) | Kubernetes Patterns 13장 |
| Ingress · IngressClass · TLS | 필수 | [Ingress](../08_cloud/book/kubernetes-in-action/12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) · [Ingress TLS](../08_cloud/book/kubernetes-in-action/12-02.Ingress%20TLS%C2%B7%EC%84%A4%EC%A0%95%C2%B7IngressClass.md) | Kubernetes in Action 12장 |
| Gateway API · HTTPRoute · 필터 | 필수 | [Gateway API](../08_cloud/book/kubernetes-in-action/13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) · [HTTPRoute](../08_cloud/book/kubernetes-in-action/13-02.HTTPRoute%20%E2%80%94%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%ED%95%84%ED%84%B0.md) | Kubernetes in Action 13장 |
| 크로스 네임스페이스 · mesh 연동 | 추천 | [크로스 네임스페이스·mesh](../08_cloud/book/kubernetes-in-action/13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md) | Kubernetes in Action 13장 |
| Service Discovery — DNS 로 못 하는 일 | 추천 | [DNS 밖의 Service Discovery](../08_cloud/book/kubernetes-up-and-running/07-01.Service%20Discovery%20%E2%80%94%20DNS%EA%B0%80%20%EB%AA%BB%20%ED%95%98%EB%8A%94%20%EC%9D%BC%EA%B3%BC%20%EB%B0%94%EA%B9%A5%EC%9D%84%20%EC%9E%87%EB%8A%94%20%EB%B2%95.md) | Kubernetes: Up and Running 7장 |
| Gateway API Inference Extension · `InferencePool` | 선택 |  | [Gateway API Inference Extension](https://gateway-api-inference-extension.sigs.k8s.io/) |



## 4단계 · 자원과 저장

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| requests · limits · QoS | 필수 | [Predictable Demands](../08_cloud/book/kubernetes-patterns/02-01.Predictable%20Demands%20%E2%80%94%20%EC%9E%90%EC%9B%90%20%EC%9A%94%EA%B5%AC%EB%A5%BC%20%EC%84%A0%EC%96%B8%ED%95%B4%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EC%97%90%20%EC%95%8C%EB%A6%AC%EA%B8%B0.md) | Kubernetes Patterns 2장 |
| LimitRange · ResourceQuota — 네임스페이스 단위 상한 | 추천 | | [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) · [Limit Ranges](https://kubernetes.io/docs/concepts/policy/limit-range/) |
| taint · toleration · affinity · 스케줄러 동작 | 필수 | [Automated Placement](../08_cloud/book/kubernetes-patterns/06-01.Automated%20Placement%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EA%B0%80%20Pod%EB%A5%BC%20%EB%85%B8%EB%93%9C%EC%97%90%20%EB%B0%B0%EC%B9%98%ED%95%98%EB%8A%94%20%EB%B2%95.md) | Kubernetes Patterns 6장 |
| 토폴로지 분산 · PodDisruptionBudget | 추천 | [Automated Placement](../08_cloud/book/kubernetes-patterns/06-01.Automated%20Placement%20%E2%80%94%20%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC%EA%B0%80%20Pod%EB%A5%BC%20%EB%85%B8%EB%93%9C%EC%97%90%20%EB%B0%B0%EC%B9%98%ED%95%98%EB%8A%94%20%EB%B2%95.md) · [Singleton Service](../08_cloud/book/kubernetes-patterns/10-01.Singleton%20Service%20%E2%80%94%20%ED%95%9C%20%EB%B2%88%EC%97%90%20%ED%95%98%EB%82%98%EB%A7%8C%20%ED%99%9C%EC%84%B1%EC%9D%B4%EB%90%98%20%EA%B3%A0%EA%B0%80%EC%9A%A9.md#drain-%EC%A0%88%EC%B0%A8%EC%99%80-pdb-%EC%9A%B4%EC%98%81%EC%9D%98-%ED%95%A8%EC%A0%95) | |
| PriorityClass · preemption · eviction | 추천 | [PriorityClass](../08_cloud/book/kubernetes-in-action/17-02.%EB%85%B8%EB%93%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8A%B9%EC%88%98%20%EA%B8%B0%EB%8A%A5%20%E2%80%94%20privileged%C2%B7hostPath%C2%B7hostNetwork%C2%B7PriorityClass.md) · [노드 압박 축출과 디스크 관리](../08_cloud/docs/kubernetes/02-01.%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%EA%B3%BC%20%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20DiskPressure%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%B4%EA%B3%A0%20%EC%BC%9C%EC%A7%80%EB%8A%94%EA%B0%80.md) | |
| Volume · emptyDir · hostPath · projected | 필수 | [볼륨과 emptyDir](../08_cloud/book/kubernetes-in-action/09-01.%EB%B3%BC%EB%A5%A8%20%EC%9D%B4%ED%95%B4%EC%99%80%20emptyDir%EB%A1%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B3%B4%EC%A1%B4%ED%95%98%EA%B8%B0.md) ~ [projected 볼륨](../08_cloud/book/kubernetes-in-action/09-03.ConfigMap%C2%B7Secret%C2%B7Downward%20API%C2%B7projected%20%EB%B3%BC%EB%A5%A8.md) | Kubernetes in Action 9장 |
| PV · PVC · StorageClass · 동적 프로비저닝 | 필수 | [PV·PVC·StorageClass](../08_cloud/book/kubernetes-in-action/10-01.PV%C2%B7PVC%C2%B7StorageClass%EC%99%80%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md) · [정적 프로비저닝](../08_cloud/book/kubernetes-in-action/10-02.%EC%A0%95%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D%EA%B3%BC%20node-local%20%EB%B3%BC%EB%A5%A8.md) | Kubernetes in Action 10장 |
| CSI · access mode · reclaim policy · 스냅샷 · ephemeral | 추천 | [PV 관리](../08_cloud/book/kubernetes-in-action/10-03.PV%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20%EB%A6%AC%EC%82%AC%EC%9D%B4%EC%A6%88%C2%B7%EC%8A%A4%EB%83%85%EC%83%B7%C2%B7ephemeral.md) | Production Kubernetes 4장 |
| 외부 저장소 통합 · 복제하지 않는 선택지 | 선택 | [저장소 통합 랩](../08_cloud/book/kubernetes-up-and-running/16-01.Integrating%20Storage%20%E2%80%94%20%EB%B3%B5%EC%A0%9C%ED%95%98%EC%A7%80%20%EC%95%8A%EB%8A%94%20%EC%84%A0%ED%83%9D%EC%A7%80%EC%99%80%20MySQL%20%EC%8B%B1%EA%B8%80%ED%84%B4%20%EB%9E%A9.md) | Kubernetes: Up and Running 16장 |
| HPA · VPA · Cluster Autoscaler · KEDA | 추천 | [Elastic Scale](../08_cloud/book/kubernetes-patterns/29-01.Elastic%20Scale%20%E2%80%94%20%EB%B6%80%ED%95%98%EC%97%90%20%EB%A7%9E%EC%B6%B0%20%EC%84%B8%20%EC%B0%A8%EC%9B%90%EC%9C%BC%EB%A1%9C%20%EC%9E%90%EB%8F%99%20%ED%99%95%EC%9E%A5.md) | Production Kubernetes 13장 |
| 노드 오토스케일링 두 방식 — Cluster Autoscaler 와 Karpenter | 선택 | | [Karpenter](https://karpenter.sh/docs/) |
| CA 가 AZ 를 고르지 못하는 이유 — AZ 별 노드 그룹 · `--balance-similar-node-groups` | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [CA FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md) |
| Karpenter NodePool · EC2NodeClass · weight · consolidation 정책 | 선택 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [Karpenter NodePools](https://karpenter.sh/docs/concepts/nodepools/) |
| overprovisioning — 낮은 PriorityClass 의 자리 표시 Pod | 선택 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [CA FAQ](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md#how-can-i-configure-overprovisioning-with-cluster-autoscaler) |
| Self Awareness — 자기 메타데이터 | 선택 | [Self Awareness](../08_cloud/book/kubernetes-patterns/14-01.Self%20Awareness%20%E2%80%94%20downward%20API%EB%A1%9C%20%EC%9E%90%EA%B8%B0%20%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%96%BB%EA%B8%B0.md) | Kubernetes Patterns 14장 |
| 장애 도메인 · 가용 영역 · 리전 · 멀티 AZ · 크로스 리전 · 멀티 리전 · 지역 복제 | 선택 | [가용 영역](../08_cloud/book/production-kubernetes/02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md) · [멀티 AZ](../08_cloud/book/production-kubernetes/02-01.Deployment%20Models%20%E2%80%94%20%EB%B0%B0%ED%8F%AC%20%EB%AA%A8%EB%8D%B8%EA%B3%BC%20%EA%B3%A0%EA%B0%80%EC%9A%A9%EC%84%B1%20%EC%9D%B8%ED%94%84%EB%9D%BC%20%EA%B5%AC%EC%B6%95.md) | |



## 5단계 · 내부 구조

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| API Server · etcd · Scheduler · Controller Manager | 필수 | [쿠버네티스 아키텍처](../08_cloud/book/kubernetes-in-action/01-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EA%B8%B0%EC%9B%90%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | Kubernetes in Action 1장 |
| kubelet · CRI · CNI · CSI · containerd | 필수 | [Kubernetes MOC](../08_cloud/kubernetes/README.md) | Production Kubernetes 3~5장 |
| 조정 루프 · watch · informer · client-go | 필수 | | Programming Kubernetes 2·3장 |
| List·Watch 와 resourceVersion · 410 Gone | 필수 | | Programming Kubernetes 3장 |
| level-driven 과 edge-driven 의 차이 | 필수 | | Programming Kubernetes 1장 |
| GVK · Scheme · TypeMeta | 추천 | | Programming Kubernetes 2·3장 |
| Reflector · DeltaFIFO · Indexer · Lister | 추천 | | Programming Kubernetes 3장 |
| SharedInformer 와 resync | 추천 | | Programming Kubernetes 3장 |
| 이벤트 병합과 upsert — 감사 로그가 아니다 | 추천 | | Programming Kubernetes 1장 |
| 여러 주체가 한 필드를 다툴 때 — Server-Side Apply · field manager · 충돌 | 추천 | | [Server-Side Apply](https://kubernetes.io/docs/reference/using-api/server-side-apply/) |
| authentication · authorization · admission | 필수 | [TLS와 API 접근 보안](../08_cloud/kubernetes/06_architecture/06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | Production Kubernetes 8장 |
| OIDC 사용자 인증 — API server 가 IdP 토큰을 검증 · Dex 로 여러 IdP 묶기 | 추천 | [Access Control](../08_cloud/book/kubernetes-patterns/26-01.Access%20Control%20%E2%80%94%20RBAC%EC%9C%BC%EB%A1%9C%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EC%A7%80.md) | Production Kubernetes 10장 · [Authenticating](https://kubernetes.io/docs/reference/access-authn-authz/authentication/) |
| TLS · PKI · 인증서 수명 | 필수 | [TLS와 API 접근 보안](../08_cloud/kubernetes/06_architecture/06-02.TLS%EC%99%80%20API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) | |
| etcd quorum · Raft · 백업 · 복구 | 필수 | [업그레이드·etcd 백업](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | |
| 클러스터 업그레이드 | 추천 | [업그레이드·etcd 백업](../08_cloud/kubernetes/06_architecture/06-01.%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%EC%99%80%20ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) | |
| 클러스터 세우기 — kubeadm · static pod · kubeconfig · 부트스트랩 토큰 | 추천 | | Production Kubernetes 2장 · [kubeadm](https://kubernetes.io/docs/reference/setup-tools/kubeadm/) |
| 로컬 클러스터 — kind · minikube · k3s | 선택 | | [kind](https://kind.sigs.k8s.io/) · [k3s](https://docs.k3s.io/) |
| kubectl 뒤의 HTTP — 클라이언트가 감추는 요청 | 선택 | [클라이언트와 HTTP](../08_cloud/book/kubernetes-up-and-running/18-01.Accessing%20Kubernetes%20%E2%80%94%20%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8%EA%B0%80%20%EA%B0%90%EC%B6%94%EB%8A%94%20HTTP%EC%99%80%20%EC%9B%90%EC%84%9C%20%EC%BD%94%EB%93%9C%20%EC%8B%A4%EC%A6%9D%20%EB%9E%A9.md) | Kubernetes: Up and Running 18장 |



## 6단계 · 보안과 확장

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| RBAC · Role · ClusterRole · RoleBinding · ServiceAccount | 필수 | [RBAC 설계와 운영](../08_cloud/book/kubernetes-up-and-running/14-01.RBAC%20%E2%80%94%20%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EC%84%A4%EA%B3%84%ED%95%98%EA%B3%A0%20%EC%9A%B4%EC%98%81%ED%95%98%EB%8A%94%20%EB%B2%95.md) · [Access Control](../08_cloud/book/kubernetes-patterns/26-01.Access%20Control%20%E2%80%94%20RBAC%EC%9C%BC%EB%A1%9C%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EC%A7%80.md) | Kubernetes: Up and Running 14장 |
| SelfSubjectAccessReview · `kubectl auth can-i` | 추천 |  | Kubernetes: Up and Running 14장 |
| 권한 기반 기능 노출 — 볼 수 없는 기능은 끈다 | 추천 |  | [Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/) |
| API 접근 하드닝 — anonymous 인증 · SA 토큰 자동 마운트 끄기 | 추천 | | CKS Study Guide 3장 |
| SecurityContext · capability · seccomp · 최소 권한 | 필수 | [Process Containment](../08_cloud/book/kubernetes-patterns/23-01.Process%20Containment%20%E2%80%94%20%EC%B5%9C%EC%86%8C%20%EA%B6%8C%ED%95%9C%EC%9C%BC%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EB%A5%BC%20%EA%B0%80%EB%91%90%EA%B8%B0.md) · [시스템 콜·capability](../08_cloud/book/container-security/02-01.Linux%20%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%C2%B7%EA%B6%8C%ED%95%9C%C2%B7capability%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%EC%9D%98%20%EB%B0%94%EB%8B%A5.md) | Kubernetes Patterns 23장 |
| AppArmor 프로파일 · `appArmorProfile` 필드 | 추천 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) · [보안 컨텍스트 랩](../08_cloud/book/kubernetes-up-and-running/19-01.Securing%20Applications%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%EC%8B%A4%EC%8A%B5%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%99%80%20proc%20%EB%A1%9C%20%EB%8B%A4%EC%8B%9C%20%EC%84%B8%EC%9A%B4%20%EB%9E%A9.md) | CKS Study Guide 4장 |
| Pod Security Admission · PSS 세 등급 — Privileged · Baseline · Restricted | 필수 | [보안 컨텍스트 랩](../08_cloud/book/kubernetes-up-and-running/19-01.Securing%20Applications%20%E2%80%94%20%EC%A3%BD%EC%9D%80%20%EC%8B%A4%EC%8A%B5%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EC%99%80%20proc%20%EB%A1%9C%20%EB%8B%A4%EC%8B%9C%20%EC%84%B8%EC%9A%B4%20%EB%9E%A9.md) | CKS Study Guide 5장 |
| NetworkPolicy · 네트워크 분할 | 추천 | [NetworkPolicy와 DNS](../08_cloud/book/networking-and-kubernetes/04-03.NetworkPolicy%EC%99%80%20DNS%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%9D%98%20%EB%B0%A9%ED%99%94%EB%B2%BD%EA%B3%BC%20%EC%9D%B4%EB%A6%84.md) · [Network Segmentation](../08_cloud/book/kubernetes-patterns/24-01.Network%20Segmentation%20%E2%80%94%20%ED%86%B5%EC%8B%A0%EC%9D%84%20%ED%95%84%EC%9A%94%ED%95%9C%20%EA%B2%BD%EB%A1%9C%EB%A7%8C%20%EB%82%A8%EA%B8%B0%EA%B8%B0.md) · [컨테이너 네트워크 보안](../08_cloud/book/container-security/10-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EB%B3%84%EB%A1%9C%20%EB%82%98%EB%88%A0%20%EB%A7%89%EA%B8%B0.md) | Kubernetes Patterns 24장 |
| Secret 관리 · 외부 저장소 · 안전한 설정 | 추천 | [Secure Configuration](../08_cloud/book/kubernetes-patterns/25-01.Secure%20Configuration%20%E2%80%94%20%EB%AF%BC%EA%B0%90%ED%95%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%A4%EB%A3%A8%EA%B8%B0.md) · [시크릿 전달](../08_cloud/book/container-security/12-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%97%90%20%EC%8B%9C%ED%81%AC%EB%A6%BF%20%EC%A0%84%EB%8B%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%8B%A4%EC%84%AF%20%EA%B2%BD%EB%A1%9C%EC%99%80%20root%EB%9D%BC%EB%8A%94%20%EC%B2%9C%EC%9E%A5.md) | Production Kubernetes 7장 |
| 저장 암호화 — EncryptionConfiguration · KMS provider | 추천 | [Secure Configuration](../08_cloud/book/kubernetes-patterns/25-01.Secure%20Configuration%20%E2%80%94%20%EB%AF%BC%EA%B0%90%ED%95%9C%20%EC%84%A4%EC%A0%95%EC%9D%84%20%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C%20%EB%8B%A4%EB%A3%A8%EA%B8%B0.md) | Production Kubernetes 7장 |
| 격리 강화 · 경계 파괴 · 런타임 보호 | 추천 | [컨테이너 격리 강화](../08_cloud/book/container-security/08-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B0%95%ED%99%94%20%E2%80%94%20%EC%83%8C%EB%93%9C%EB%B0%95%EC%8B%B1%EC%9D%98%20%EC%84%B8%20%EA%B0%88%EB%9E%98.md) · [컨테이너 격리 깨뜨리기](../08_cloud/book/container-security/09-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC%20%EA%B9%A8%EB%9C%A8%EB%A6%AC%EA%B8%B0%20%E2%80%94%20%EC%84%A4%EC%A0%95%20%ED%95%98%EB%82%98%EB%A1%9C%20%EB%AC%B4%EB%84%88%EC%A7%80%EB%8A%94%20%EA%B2%BD%EA%B3%84.md) | Container Security 8·9·13장 |
| EKS 워크로드 신원 — IRSA | 추천 | | Production Kubernetes 10장 |
| EKS Pod Identity | 추천 | | [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html) |
| EKS 봉투 암호화 · 제어부 로깅 | 선택 | | [envelope encryption](https://docs.aws.amazon.com/eks/latest/userguide/envelope-encryption.html) · [control plane logs](https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html) |
| 위협 모델 · 공격 체인 · 횡적 이동 | 추천 | [컨테이너 보안 위협](../08_cloud/book/container-security/01-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%B3%B4%EC%95%88%20%EC%9C%84%ED%98%91%20%E2%80%94%20%EC%9C%84%ED%98%91%20%EB%AA%A8%EB%8D%B8%EB%B6%80%ED%84%B0%20%EB%B3%B4%EC%95%88%20%EC%9B%90%EC%B9%99%EA%B9%8C%EC%A7%80.md) · [Network Segmentation](../08_cloud/book/kubernetes-patterns/24-01.Network%20Segmentation%20%E2%80%94%20%ED%86%B5%EC%8B%A0%EC%9D%84%20%ED%95%84%EC%9A%94%ED%95%9C%20%EA%B2%BD%EB%A1%9C%EB%A7%8C%20%EB%82%A8%EA%B8%B0%EA%B8%B0.md) | Container Security 1장 |
| CIS Benchmark · kube-bench · KISA 점검 가이드 | 추천 | [OWASP Top 10](../08_cloud/book/container-security/14-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20OWASP%20Top%2010%20%E2%80%94%20%EC%9B%B9%20%EB%A6%AC%EC%8A%A4%ED%81%AC%EB%A5%BC%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%8C%80%EC%9D%91%EC%9C%BC%EB%A1%9C%20%EC%9E%87%EB%8B%A4.md) | CKS Study Guide 2장 |
| 감사 로그 — audit policy · 로그 백엔드 | 추천 | | CKS Study Guide 7장 |
| 런타임 탐지 — Falco · Tetragon · 탐지와 강제의 차이 | 추천 | [런타임 보호](../08_cloud/book/container-security/13-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EB%B3%B4%ED%98%B8%20%E2%80%94%20%EC%A0%95%EC%83%81%EC%9D%84%20%EC%A0%95%EC%9D%98%ED%95%B4%20%EC%9D%B4%EC%83%81%EC%9D%84%20%EC%9E%A1%EB%8B%A4.md) · [eBPF 보안 도구](../02_os/book/learning-ebpf/09-01.%EC%8B%9C%EC%8A%A4%ED%85%9C%20%EC%BD%9C%20%EC%9E%85%EA%B5%AC%20%EA%B2%80%EC%82%AC%EB%8A%94%20TOCTOU%20%EC%97%90%20%EB%9A%AB%EB%A0%A4%20%EB%B3%B4%EC%95%88%20%EB%8F%84%EA%B5%AC%EB%8A%94%20LSM%20%ED%9B%85%EA%B3%BC%20%EC%BB%A4%EB%84%90%20%ED%95%A8%EC%88%98%EC%97%90%EC%84%9C%20%ED%8C%90%EC%A0%95%ED%95%98%EA%B3%A0%20SIGKILL%20%EB%A1%9C%20%EB%A7%89%EB%8A%94%EB%8B%A4.md) | CKS Study Guide 7장 · Learning eBPF 9장 |
| Discovery API · Unstructured — 동적 리소스 | 추천 | | Programming Kubernetes 3장 |
| CRD · custom resource | 추천 | [StatefulSet과 Operator](../08_cloud/book/kubernetes-in-action/16-03.StatefulSet%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%99%80%20Operator%20%E2%80%94%20partition%C2%B7OnDelete%C2%B7CRD.md) · [어드미션 검증 랩](../08_cloud/book/kubernetes-up-and-running/17-01.Extending%20Kubernetes%20%E2%80%94%20%EC%96%B4%EB%93%9C%EB%AF%B8%EC%85%98%C2%B7%EC%BB%A4%EC%8A%A4%ED%85%80%20%EB%A6%AC%EC%86%8C%EC%8A%A4%EC%99%80%20%EC%9D%B8%EC%A6%9D%EC%84%9C%20%EC%97%86%EB%8A%94%20%EA%B2%80%EC%A6%9D%20%EB%9E%A9.md) | Programming Kubernetes 4장 |
| Controller · Operator · finalizer · OwnerReference | 추천 | [Controller](../08_cloud/book/kubernetes-patterns/27-01.Controller%20%E2%80%94%20Observe-Analyze-Act%EB%A1%9C%20%EC%83%81%ED%83%9C%EB%A5%BC%20%EC%A1%B0%EC%A0%95%ED%95%98%EA%B8%B0.md) · [Operator](../08_cloud/book/kubernetes-patterns/28-01.Operator%20%E2%80%94%20CRD%EB%A1%9C%20%EB%8F%84%EB%A9%94%EC%9D%B8%20%EC%A7%80%EC%8B%9D%EC%9D%84%20%EC%9E%90%EB%8F%99%ED%99%94%ED%95%98%EA%B8%B0.md) | Programming Kubernetes 6장 |
| controller-runtime 으로 감싸기 | 추천 | | Programming Kubernetes 6장 |
| status subresource · 코드 생성 | 선택 | | Programming Kubernetes 5·9장 |
| 스케줄러 확장 — scheduling framework · 스케줄러 프로파일 · custom scheduler · scheduler extender | 선택 | | [Scheduling Framework](https://kubernetes.io/docs/concepts/scheduling-eviction/scheduling-framework/) |
| 배치 다시 고르기 — descheduler | 선택 | | [descheduler](https://github.com/kubernetes-sigs/descheduler) |
| 어드미션 웹훅 · OPA · Gatekeeper · Kyverno | 추천 | [Gatekeeper 정책](../08_cloud/book/kubernetes-up-and-running/20-01.Policy%20and%20Governance%20%E2%80%94%20Gatekeeper%20%EB%A1%9C%20%EB%A7%8C%EB%93%A4%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EB%A7%89%EA%B3%A0%20%EB%A7%8C%EB%93%A0%20%EB%92%A4%EC%97%90%20%EC%84%B8%EB%8A%94%20%EB%B2%95.md) | Policy as Code 7·8장 |
| ValidatingAdmissionPolicy — 웹훅 없는 CEL 정책 | 선택 | | [Validating Admission Policy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/) |
| 공급망 보안 · SBOM · 이미지 서명 · 취약점 스캔 | 추천 | [이미지 공급망 보안](../08_cloud/book/container-security/06-02.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B3%B5%EA%B8%89%EB%A7%9D%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EB%B9%8C%EB%93%9C%EB%B6%80%ED%84%B0%20%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80.md) · [이미지 취약점](../08_cloud/book/container-security/07-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%86%8D%20%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%20%EC%B7%A8%EC%95%BD%EC%A0%90%20%E2%80%94%20CVE%EB%B6%80%ED%84%B0%20%EC%8A%A4%EC%BA%94%20%EC%9A%B4%EC%98%81%EA%B9%8C%EC%A7%80.md) | CKS Study Guide 6장 · Policy as Code 14장 |
| 클러스터 안에서 이미지 빌드 | 선택 | [Image Builder](../08_cloud/book/kubernetes-patterns/30-01.Image%20Builder%20%E2%80%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%95%88%EC%97%90%EC%84%9C%20%EC%9D%B4%EB%AF%B8%EC%A7%80%EB%A5%BC%20%EB%B9%8C%EB%93%9C%ED%95%98%EA%B8%B0.md) | Kubernetes Patterns 30장 |
| 시크릿 볼트 · 동적 시크릿 · 시크릿 로테이션 | 선택 | | |
| 이그레스 · 네트워크 정책 · 서비스 계정 · 롤 바인딩 · 네임스페이스 격리 | 선택 | [네트워크 정책](../08_cloud/book/container-security/10-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EB%B3%B4%EC%95%88%20%E2%80%94%20%EA%B3%84%EC%B8%B5%EB%B3%84%EB%A1%9C%20%EB%82%98%EB%88%A0%20%EB%A7%89%EA%B8%B0.md) · [롤 바인딩](../08_cloud/book/kubernetes-patterns/26-01.Access%20Control%20%E2%80%94%20RBAC%EC%9C%BC%EB%A1%9C%20%EB%88%84%EA%B0%80%20%EB%AC%B4%EC%97%87%EC%9D%84%20%ED%95%A0%20%EC%88%98%20%EC%9E%88%EB%8A%94%EC%A7%80.md) · [네임스페이스 격리](../07_devops/book/aic_ai-infra-claude/07-02.App%20of%20Apps%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) | |
| 인그레스 | 선택 | | |



## 7단계 · 운영

| 개념 | 우선순위 | 노트 | 책 |
|---|:---:|---|---|
| 이벤트 · 로그 · 지표를 한 시간축에 | 필수 | [모니터링과 트러블슈팅](../08_cloud/kubernetes/09_operations/09-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | Kubernetes Best Practices 3장 |
| kubectl 고급 조회 · JSONPath | 필수 | [JSONPath 조회](../08_cloud/kubernetes/09_operations/09-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | |
| kubelet 지표 엔드포인트 — `/stats/summary` 직접 호출 · `nodes/stats` 와 `nodes/proxy` RBAC | 추천 | [kubelet 이 재는 것](../08_cloud/docs/kubernetes/03-01.%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%E2%80%94%20kubelet%EC%9D%B4%20%EC%9E%AC%EB%8A%94%20%EA%B2%83%EA%B3%BC%20kubectl%20top%EC%9D%B4%20%EC%9D%BD%EB%8A%94%20%EA%B2%83.md) | Kubernetes Best Practices 3장 · [Node metrics](https://kubernetes.io/docs/reference/instrumentation/node-metrics/) · [Kubelet 인증·인가](https://kubernetes.io/docs/reference/access-authn-authz/kubelet-authn-authz/) |
| ephemeral container · `kubectl debug` | 추천 | | [Debug Running Pods](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/) |
| OOMKilled · exit code 137 · CPU throttling | 필수 | [OOMKilled 사례 분석](../08_cloud/kubernetes/09_operations/09-02.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) · [OS 로드맵](os-keywords.md) | |
| SIGTERM · PID 1 · PreStop · `terminationGracePeriodSeconds` | 필수 | [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | |
| node pressure · eviction · NodeNotReady | 추천 | [Kubernetes 장애 기록](../troubleshooting/kubernetes/README.md) | |
| 노드 추가·제거 — cordon · drain · PDB 와의 맞물림 | 필수 | | [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) |
| 노드 회수를 막는 PDB · `maxSurge` 로 배포 중 노드 급증 제어 | 추천 | [당근 발표 정리](_digest/2026-10-10_당근_빌더_밋업_2026_인프라_발표_5편.md) | [Karpenter Disruption](https://karpenter.sh/docs/concepts/disruption/) |
| OS 자동 업데이트 — 파이프라인 밖에서 노드를 바꾸는 장치 | 선택 | [진단 개념](../troubleshooting/_concepts/os-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8-%EB%B0%96%EC%97%90%EC%84%9C-%EB%85%B8%EB%93%9C%EB%A5%BC-%EB%B0%94%EA%BE%B8%EB%8A%94-%EC%9E%A5%EC%B9%98.md) |  |
| 멀티테넌시 | 추천 | | Production Kubernetes 12장 |
| 가상 컨트롤 플레인 — tenant 와 host 를 잇는 sync 방향 | 선택 | | Production Kubernetes 12장 |
| 이름 변환과 충돌 회피 · status back-sync | 선택 |  | [vcluster](https://www.vcluster.com/docs) |
| 멀티클러스터 세 모델 | 추천 | [멀티클러스터 세 모델](../08_cloud/book/kubernetes-up-and-running/21-01.Multicluster%20%E2%80%94%20%EB%8A%98%EB%A6%AC%EA%B8%B0%20%EC%A0%84%EC%97%90%20%EA%B0%96%EC%B6%9C%20%EA%B2%83%EA%B3%BC%20%EB%8A%98%EB%A6%B0%20%EB%92%A4%20%EA%B0%88%EB%A6%AC%EB%8A%94%20%EC%84%B8%20%EB%AA%A8%EB%8D%B8.md) | Kubernetes: Up and Running 21장 |
| 관리형 대 자체 운영 — EKS · GKE · AKS 를 고르는 기준 | 추천 | | Production Kubernetes 2장 |
| OpenShift — Route · SCC · 설치 방식 | 선택 | | Operating OpenShift 2·3장 |
| 서비스 메시를 쓸 것인가 | 선택 | [서비스 메시 판단](../08_cloud/book/kubernetes-up-and-running/15-01.Service%20Meshes%20%E2%80%94%20%EC%93%B8%20%EA%B2%83%EC%9D%B8%EA%B0%80%EB%A5%BC%20%EB%A8%BC%EC%A0%80%20%EB%94%B0%EC%A7%84%EB%8B%A4.md) · [네트워크 로드맵](network-keywords.md) | Kubernetes: Up and Running 15장 |
| CKA 대비와 문제 풀이 | 추천 | [CKA 대비](../08_cloud/kubernetes/09_operations/09-04.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) | |
| CKAD 대비 — 시험 범위는 1~4단계 워크로드 · 연결 · 저장 | 선택 |  | [CKAD 커리큘럼](https://github.com/cncf/curriculum) |
| 액티브-액티브 · 액티브-패시브 · 페일오버 · 페일오버 자동화 · 페일백 · 리플리카 승격 | 선택 | [액티브-액티브](../07_devops/03_Nexus/05-04.%ED%94%84%EB%A1%9C%EB%8D%95%EC%85%98%20%EC%9A%B4%EC%98%81%20%ED%8C%A8%ED%84%B4.md) | |
| 재해 복구 · 전체 백업 · 증분 백업 · 스냅샷 복원 · 포인트 인 타임 복구 | 선택 | [재해 복구](../06_observability/book/dgos_opensearch/03-01.%EB%B0%B0%ED%8F%AC%20%EC%98%B5%EC%85%98%20%E2%80%94%20Amazon%20OpenSearch%20Service%EC%99%80%20Serverless.md) · [증분 백업](../07_devops/03_Nexus/05-02.%EB%B0%B1%EC%97%85%20%EB%B3%B5%EA%B5%AC%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C.md) | |
| 테넌트 격리 · 데이터 레지던시 | 선택 | [테넌트 격리](../07_devops/book/aic_ai-infra-claude/07-02.App%20of%20Apps%EC%99%80%20%EB%A9%80%ED%8B%B0%ED%85%8C%EB%84%8C%EC%8B%9C.md) | |
| 사용량 추적 · 빌링 미터링 · 사용량 기반 과금 | 선택 | | |
| FinOps · 리소스 태깅 · 코스트 할당 · 차지백 · 쇼백 | 선택 | | |
| 이그레스 비용 | 선택 | | |
| 멀티 테넌시 | 선택 | [멀티 테넌시](../08_cloud/book/argocd-up-and-running/08-01.%EB%A9%80%ED%8B%B0%20%ED%85%8C%EB%84%8C%EC%8B%9C%20%E2%80%94%20%EC%84%A4%EC%B9%98%20%EB%AA%A8%EB%93%9C%EC%99%80%20AppProject%C2%B7%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20%EC%97%AD%ED%95%A0.md) | |



## 넣지 않은 것

> 다른 문서가 정본이거나 이 로드맵의 축과 다른 것들입니다.

| 대상 | 이유 |
|---|---|
| 패킷 경로 · CNI 데이터패스 · eBPF · Cilium · CNI 구현체 비교 | [네트워크 로드맵](network-keywords.md)이 맡습니다 |
| cgroup · namespace 의 커널 구현 | [OS 로드맵](os-keywords.md) 3단계가 맡습니다 |
| Prometheus · Grafana · OpenTelemetry | [관측 가능성 로드맵](observability-keywords.md)이 맡습니다 |
| 이미지 빌드 · CI 파이프라인 · Helm · GitOps · 점진 배포 · IaC | [DevOps 로드맵](devops-keywords.md)이 맡습니다 |
| Istio 의 트래픽 관리와 mTLS | [네트워크 로드맵](network-keywords.md) 7단계가 맡습니다. 여기는 "쓸 것인가"까지입니다 |
| VPC · Security Group · 클라우드 네트워크 경계 | [네트워크 로드맵](network-keywords.md) 5단계가 맡습니다 |
| Kubernetes in Action 3장 | 클러스터를 띄우는 절차입니다. 순서가 아니라 준비 단계입니다 |
| Kubernetes 대안 — Nomad · ECS · Cloud Run | 오케스트레이터를 고르는 축입니다. 이 로드맵은 Kubernetes 를 쓰기로 한 뒤의 순서입니다 |
