---
title: Kubernetes in Action, 2nd Edition — 정독 인덱스
tags: [moc, study-index, book, kubernetes, k8s, kubernetes-in-action]
status: draft
source:
  - 《Kubernetes in Action, Second Edition》(Marko Lukša, Manning, 2025)
  - https://www.manning.com/books/kubernetes-in-action-second-edition  # 원서 (2026-07-01 조회)
  - https://github.com/luksa/kubernetes-in-action-2nd-edition  # 저자 예제 코드 저장소 (2026-07-01 조회)
related:
  - ../networking-and-kubernetes/README.md
  - ../kubernetes-patterns/README.md
  - ../kubernetes-up-and-running/README.md
  - ../production-kubernetes/README.md
  - ../../docs/kubernetes/README.md
  - ../../../_archive/08_cloud/kubernetes/README.md
  - ../../README.md
learning:
  topic: kubernetes-in-action
  scope: durable
  level: 내림 유지 — 2026-09-10 재학습 드릴 평균 2.0. 회차 2의 quality 1에서는 올랐지만 한 번으로 안 닫혔다. 「무슨 일이 일어난 화면인가」는 나오고 「무엇과 무엇이 어떻게 다른가」는 안 나온다
  last_verified: 2026-09-10
  blocked_count: 2
  next_lesson: "8장 재학습 표적 재확인 대기(2026-09-10 드릴 평균 2.0): 1) exec 유무, 2) PID 1 종료 시 네임스페이스 정리, 3) command만 적으면 CMD 덮어쓰기, 4) --from-literal·--from-file·--from-env-file 구분. 통과 후 08-01·08-02 회차 3 진행, 미통과 시 ~/study/runners-lab/k8s/k8s-in-action/08-configuring-apps/command-env/ 실습. 챕터별 복습 상태 정본은 _review/_queue.md 참조."
updated: 2026-11-29
---

# Kubernetes in Action, 2nd Edition — 정독 인덱스

---

> 『Kubernetes in Action, Second Edition』(Marko Lukša, Manning, 2025)을 장·절 단위로 정독한 책-종속 학습노트입니다. 예제 앱 Kiada를 클러스터에 올리며 기초·파드·스토리지·네트워킹·컨트롤러 순으로 오브젝트를 쌓아 올립니다.

## 작성 현황

> 1~18장 정독 노트 49편과 오답 노트 1편(총 50편)의 목록입니다.

| 편 | 제목과 한 줄 요약 | 상태 |
|----|------------------|------|
| [오답 노트](./_mistakes.md) | 복습·세션에서 막힌 문항과 원인 기록 | 진행 중 |
| [01-01](./01-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%EB%9E%80%20%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80%20%E2%80%94%20%EA%B8%B0%EC%9B%90%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.md) | 쿠버네티스란 무엇인가 — 기원과 아키텍처 (Ch1 §1.1~1.2) | 완료 (draft) |
| [01-02](./01-02.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%EB%8F%84%EC%9E%85%20%ED%8C%90%EB%8B%A8.md) | 쿠버네티스 도입 판단 (Ch1 §1.3) | 완료 (draft) |
| [02-01](./02-01.%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%EC%99%80%20%EA%B0%80%EC%83%81%EB%A8%B8%EC%8B%A0.md) | 컨테이너와 가상머신 (Ch2 §2.1) | 완료 (draft) |
| [02-02](./02-02.Kiada%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B9%8C%EB%93%9C%EC%99%80%20%EB%B0%B0%ED%8F%AC.md) | Kiada 애플리케이션 빌드와 배포 (Ch2 §2.2) | 완료 (draft) |
| [02-03](./02-03.%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%EC%99%80%20cgroup%EC%9C%BC%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B2%A9%EB%A6%AC.md) | 네임스페이스와 cgroup으로 보는 컨테이너 격리 (Ch2 §2.3) | 완료 (draft) |
| [03-01](./03-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%8B%A4%ED%96%89%ED%95%98%EA%B8%B0.md) | 쿠버네티스 클러스터 실행하기 (Ch3 §3.1~3.2) | 완료 (draft) |
| [03-02](./03-02.%EC%B2%AB%20%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98%20%EB%B0%B0%ED%8F%AC%EC%99%80%20%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | 첫 애플리케이션 배포와 스케일링 (Ch3 §3.3) | 완료 (draft) |
| [04-01](./04-01.%EC%BF%A0%EB%B2%84%EB%84%A4%ED%8B%B0%EC%8A%A4%20API%EC%99%80%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EB%A7%A4%EB%8B%88%ED%8E%98%EC%8A%A4%ED%8A%B8%20%EA%B5%AC%EC%A1%B0.md) | 쿠버네티스 API와 오브젝트 매니페스트 구조 (Ch4 §4.1) | 완료 (draft) |
| [04-02](./04-02.Node%EC%99%80%20Event%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%EB%A1%9C%20%EB%B3%B4%EB%8A%94%20%ED%95%84%EB%93%9C%20%EC%8B%A4%EC%8A%B5.md) | Node와 Event 오브젝트로 보는 필드 실습 (Ch4 §4.2~4.3) | 완료 (draft) |
| [05-01](./05-01.Pod%20%EC%9D%B4%ED%95%B4%20%E2%80%94%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B7%B8%EB%A3%B9%ED%99%94%EC%99%80%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4.md) | Pod 이해 — 컨테이너 그룹화와 사이드카 (Ch5 §5.1) | 완료 (draft) |
| [05-02](./05-02.Pod%20%EC%83%9D%EC%84%B1%EA%B3%BC%20%EC%83%81%ED%98%B8%EC%9E%91%EC%9A%A9.md) | Pod 생성과 상호작용 (Ch5 §5.2~5.3) | 완료 (draft) |
| [05-03](./05-03.%EB%A9%80%ED%8B%B0%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%C2%B7init%C2%B7%EB%84%A4%EC%9D%B4%ED%8B%B0%EB%B8%8C%20%EC%82%AC%EC%9D%B4%EB%93%9C%EC%B9%B4%EC%99%80%20%EC%82%AD%EC%A0%9C.md) | 멀티 컨테이너·init·네이티브 사이드카와 삭제 (Ch5 §5.4~5.6) | 완료 (draft) |
| [06-01](./06-01.Pod%20%EC%83%81%ED%83%9C%20%E2%80%94%20phase%C2%B7conditions%C2%B7%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EC%83%81%ED%83%9C.md) | Pod 상태 — phase·conditions·컨테이너 상태 (Ch6 §6.1) | 완료 (draft) |
| [06-02](./06-02.liveness%C2%B7startup%20probe%EB%A1%9C%20%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EA%B1%B4%EA%B0%95%20%EC%9C%A0%EC%A7%80.md) | liveness·startup probe로 컨테이너 건강 유지 (Ch6 §6.2) | 완료 (draft) |
| [06-03](./06-03.lifecycle%20hook%EA%B3%BC%20Pod%20%EC%83%9D%EC%95%A0%EC%A3%BC%EA%B8%B0%20%EC%A0%84%EC%B2%B4.md) | lifecycle hook과 Pod 생애주기 전체 (Ch6 §6.3~6.4) | 완료 (draft) |
| [07-01](./07-01.namespace%EB%A1%9C%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%A5%BC%20%EA%B0%80%EC%83%81%20%EB%B6%84%ED%95%A0%ED%95%98%EA%B8%B0.md) | namespace로 클러스터를 가상 분할하기 (Ch7 §7.1) | 완료 |
| [07-02](./07-02.label%EA%B3%BC%20label%20selector%EB%A1%9C%20%EC%98%A4%EB%B8%8C%EC%A0%9D%ED%8A%B8%20%EC%A1%B0%EC%A7%81%ED%95%98%EA%B8%B0.md) | label과 label selector로 오브젝트 조직하기 (Ch7 §7.2~7.3) | 완료 |
| [07-03](./07-03.field%20selector%EC%99%80%20annotation.md) | field selector와 annotation (Ch7 §7.4~7.5) | 완료 (draft) |
| [08-01](./08-01.command%C2%B7args%EC%99%80%20%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98.md) | command·args와 환경변수 (Ch8 §8.1) | 완료 (draft) |
| [08-02](./08-02.ConfigMap%EC%9C%BC%EB%A1%9C%20%EC%84%A4%EC%A0%95%20%EB%B6%84%EB%A6%AC%ED%95%98%EA%B8%B0.md) | ConfigMap으로 설정 분리하기 (Ch8 §8.2) | 완료 (draft) |
| [08-03](./08-03.Secret%EA%B3%BC%20Downward%20API.md) | Secret과 Downward API (Ch8 §8.3~8.4) | 완료 (draft) |
| [09-01](./09-01.%EB%B3%BC%EB%A5%A8%20%EC%9D%B4%ED%95%B4%EC%99%80%20emptyDir%EB%A1%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B3%B4%EC%A1%B4%ED%95%98%EA%B8%B0.md) | 볼륨 이해와 emptyDir로 데이터 보존하기 (Ch9 §9.1~9.2) | 완료 (draft) |
| [09-02](./09-02.image%C2%B7hostPath%20%EB%B3%BC%EB%A5%A8.md) | image·hostPath 볼륨 (Ch9 §9.3~9.4) | 완료 (draft) |
| [09-03](./09-03.ConfigMap%C2%B7Secret%C2%B7Downward%20API%C2%B7projected%20%EB%B3%BC%EB%A5%A8.md) | ConfigMap·Secret·Downward API·projected 볼륨 (Ch9 §9.5~9.6) | 완료 (draft) |
| [10-01](./10-01.PV%C2%B7PVC%C2%B7StorageClass%EC%99%80%20%EB%8F%99%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D.md) | PV·PVC·StorageClass와 동적 프로비저닝 (Ch10 §10.1~10.2) | 완료 (draft) |
| [10-02](./10-02.%EC%A0%95%EC%A0%81%20%ED%94%84%EB%A1%9C%EB%B9%84%EC%A0%80%EB%8B%9D%EA%B3%BC%20node-local%20%EB%B3%BC%EB%A5%A8.md) | 정적 프로비저닝과 node-local 볼륨 (Ch10 §10.3) | 완료 (draft) |
| [10-03](./10-03.PV%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20%EB%A6%AC%EC%82%AC%EC%9D%B4%EC%A6%88%C2%B7%EC%8A%A4%EB%83%85%EC%83%B7%C2%B7ephemeral.md) | PV 관리 — 리사이즈·스냅샷·ephemeral (Ch10 §10.4~10.5) | 완료 (draft) |
| [11-01](./11-01.Service%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%C2%B7ClusterIP%C2%B7%EC%84%B8%EC%85%98%20%EC%96%B4%ED%94%BC%EB%8B%88%ED%8B%B0.md) | Service 기초 — 파드 통신·ClusterIP·세션 어피니티 (Ch11 §11.1) | 완료 (draft) |
| [11-02](./11-02.%EC%99%B8%EB%B6%80%20%EB%85%B8%EC%B6%9C%20%E2%80%94%20NodePort%C2%B7LoadBalancer%C2%B7%ED%8A%B8%EB%9E%98%ED%94%BD%20%EC%A0%95%EC%B1%85.md) | 외부 노출 — NodePort·LoadBalancer·트래픽 정책 (Ch11 §11.2) | 완료 (draft) |
| [11-03](./11-03.%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8%C2%B7DNS%C2%B7%ED%86%A0%ED%8F%B4%EB%A1%9C%EC%A7%80%C2%B7readiness.md) | 엔드포인트·DNS·토폴로지·readiness (Ch11 §11.3~11.6) | 완료 (draft) |
| [12-01](./12-01.Ingress%EB%A1%9C%20%EC%97%AC%EB%9F%AC%20%EC%84%9C%EB%B9%84%EC%8A%A4%EB%A5%BC%20%ED%95%9C%20IP%EC%97%90%20%EB%85%B8%EC%B6%9C%ED%95%98%EA%B8%B0.md) | Ingress로 여러 서비스를 한 IP에 노출하기 (Ch12 §12.1~12.2) | 완료 (draft) |
| [12-02](./12-02.Ingress%20TLS%C2%B7%EC%84%A4%EC%A0%95%C2%B7IngressClass.md) | Ingress TLS·설정·IngressClass (Ch12 §12.3~12.6) | 완료 (draft) |
| [13-01](./13-01.Gateway%20API%20%EA%B0%9C%EB%85%90%EA%B3%BC%20Gateway%20%EB%B0%B0%ED%8F%AC.md) | Gateway API 개념과 Gateway 배포 (Ch13 §13.1~13.2) | 완료 (draft) |
| [13-02](./13-02.HTTPRoute%20%E2%80%94%20%EB%9D%BC%EC%9A%B0%ED%8C%85%EA%B3%BC%20%ED%95%84%ED%84%B0.md) | HTTPRoute — 라우팅과 필터 (Ch13 §13.3) | 완료 (draft) |
| [13-03](./13-03.TLS%C2%B7%EA%B8%B0%ED%83%80%20%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C%C2%B7%ED%81%AC%EB%A1%9C%EC%8A%A4%20%EB%84%A4%EC%9E%84%EC%8A%A4%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7mesh.md) | TLS·기타 프로토콜·크로스 네임스페이스·mesh (Ch13 §13.4~13.7) | 완료 (draft) |
| [14-01](./14-01.ReplicaSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7%EC%86%8C%EC%9C%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | ReplicaSet 기초 — 생성·소유·스케일링 (Ch14 §14.1~14.2) | 완료 (draft) |
| [14-02](./14-02.ReplicaSet%20%EC%BB%A8%ED%8A%B8%EB%A1%A4%EB%9F%AC%20%E2%80%94%20reconciliation%C2%B7%EC%9E%A5%EC%95%A0%EB%B3%B5%EA%B5%AC%C2%B7%EC%82%AD%EC%A0%9C.md) | ReplicaSet 컨트롤러 — reconciliation·장애복구·삭제 (Ch14 §14.3~14.4) | 완료 (draft) |
| [15-01](./15-01.Deployment%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%83%9D%EC%84%B1%C2%B7pod-template-hash%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.md) | Deployment 기초 — 생성·pod-template-hash·스케일링 (Ch15 §15.1) | 완료 (draft) |
| [15-02](./15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md) | Deployment 업데이트 — Recreate·RollingUpdate·maxSurge (Ch15 §15.2.1~15.2.3) | 완료 (draft) |
| [15-03](./15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) | rollout 제어와 배포 전략 — pause·faulty·rollback·전략 5종 (Ch15 §15.2.4~15.3) | 완료 (draft) |
| [16-01](./16-01.StatefulSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20Pets%20vs%20Cattle%C2%B7ordinal%C2%B7headless%20Service.md) | StatefulSet 기초 — Pets vs Cattle·ordinal·headless Service (Ch16 §16.1) | 완료 (draft) |
| [16-02](./16-02.StatefulSet%20%EB%8F%99%EC%9E%91%20%E2%80%94%20%EB%AF%B8%EC%8B%B1%20%ED%8C%8C%EB%93%9C%C2%B7%EB%85%B8%EB%93%9C%20%EC%9E%A5%EC%95%A0%C2%B7%EC%8A%A4%EC%BC%80%EC%9D%BC%C2%B7retention.md) | StatefulSet 동작 — 미싱 파드·노드 장애·스케일·retention (Ch16 §16.2) | 완료 (draft) |
| [16-03](./16-03.StatefulSet%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%EC%99%80%20Operator%20%E2%80%94%20partition%C2%B7OnDelete%C2%B7CRD.md) | StatefulSet 업데이트와 Operator — partition·OnDelete·CRD (Ch16 §16.3~16.4) | 완료 (draft) |
| [17-01](./17-01.DaemonSet%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EB%85%B8%EB%93%9C%EB%A7%88%EB%8B%A4%20%ED%95%98%EB%82%98%C2%B7node%20selector%C2%B7%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8.md) | DaemonSet 기초 — 노드마다 하나·node selector·업데이트 (Ch17 §17.1) | 완료 (draft) |
| [17-02](./17-02.%EB%85%B8%EB%93%9C%20%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%20%ED%8A%B9%EC%88%98%20%EA%B8%B0%EB%8A%A5%20%E2%80%94%20privileged%C2%B7hostPath%C2%B7hostNetwork%C2%B7PriorityClass.md) | 노드 에이전트 특수 기능 — privileged·hostPath·hostNetwork·PriorityClass (Ch17 §17.2) | 완료 (draft) |
| [17-03](./17-03.%EB%A1%9C%EC%BB%AC%20daemon%20%ED%8C%8C%EB%93%9C%20%ED%86%B5%EC%8B%A0%20%E2%80%94%20hostPort%C2%B7hostNetwork%C2%B7internalTrafficPolicy.md) | 로컬 daemon 파드 통신 — hostPort·hostNetwork·internalTrafficPolicy (Ch17 §17.3) | 완료 (draft) |
| [18-01](./18-01.Job%20%EA%B8%B0%EC%B4%88%20%E2%80%94%20%EC%8B%A4%ED%96%89%C2%B7%EC%83%81%ED%83%9C%C2%B7suspend%C2%B7%EC%9E%90%EB%8F%99%EC%82%AD%EC%A0%9C.md) | Job 기초 — 실행·상태·suspend·자동삭제 (Ch18 §18.1.1) | 완료 (draft) |
| [18-02](./18-02.Job%20%EB%B3%91%EB%A0%AC%C2%B7%EC%8B%A4%ED%8C%A8%C2%B7%EC%99%84%EB%A3%8C%20%EB%AA%A8%EB%93%9C.md) | Job 병렬·실패·완료 모드 (Ch18 §18.1.2~18.1.4) | 완료 (draft) |
| [18-03](./18-03.work%20queue%C2%B7pod%20%ED%86%B5%EC%8B%A0%C2%B7sidecar%C2%B7CronJob.md) | work queue·pod 통신·sidecar·CronJob (Ch18 §18.1.5~18.2) | 완료 (draft) |



## 학습 상태

> 세션을 열 때 현재 진행 위치만 빠르게 확인하는 요약입니다. 챕터별 복습 상태 정본은 복습 대기 큐에 있습니다.

| 항목 | 현재 값 |
|------|--------|
| 진행률 | 18/18장 완주 — 장별 노트 49편(final 2 · draft 47) + 오답 노트 1편 |
| 현재 상태 | 난이도 `내림 유지` (2026-09-10 기준). 1~7·9~13장 Phase 4 완료(대기), 8장 재학습(표적 재확인 대기), 14~18장 Phase 1 완료(Phase 4 미실시) |
| 실습 코드 | `~/study/runners-lab/k8s/k8s-in-action/` (`02-isolation/` ~ `18-job/`) |
| 복습·오답 | [복습 대기 큐](../../../_review/_queue.md) (`kia` ch01~ch18) · [오답 노트](./_mistakes.md) |



## 관련 문서

> 같은 book/ 영역의 형제 정독본, 공식문서 정독, 저자 예제 저장소입니다.

- [Networking and Kubernetes 정독 인덱스](../networking-and-kubernetes/README.md) — 패킷·CNI·Service 네트워킹 계층 심화
- [Kubernetes Patterns 정독 인덱스](../kubernetes-patterns/README.md) — 오브젝트 조합 패턴 카탈로그
- [Kubernetes: Up and Running 정독 인덱스](../kubernetes-up-and-running/README.md) — 운영자 최소 조작 경로 실전서
- [Production Kubernetes 정독 인덱스](../production-kubernetes/README.md) — 플랫폼 엔지니어링 관점의 아키텍처 결정
- [08_cloud/docs/kubernetes — 쿠버네티스 공식문서 정독](../../docs/kubernetes/README.md) — 쿠버네티스 공통 개념 정본
- [08_cloud MOC](../../README.md) — 상위 카테고리 경계
- [_archive/08_cloud/kubernetes](../../../_archive/08_cloud/kubernetes/README.md) — 데브툴스 운영 아카이브(11_devtools 3편)
- [Kubernetes in Action 2판 예제 코드 (luksa/kubernetes-in-action-2nd-edition)](https://github.com/luksa/kubernetes-in-action-2nd-edition) — 저자 공개 장별 매니페스트·앱 소스
