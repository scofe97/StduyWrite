---
title: 07_devops/docs/gitops — GitOps 배포 전략·검증·롤백
tags: [moc, devops, gitops, argo-rollouts, argocd, deployment]
status: final
related:
  - ../../README.md
  - ../iac/README.md
  - ../../book/argocd-up-and-running/README.md
updated: 2026-11-26
---

# 07_devops/docs/gitops — GitOps 배포 전략·검증·롤백

---

> 새 버전을 올리고 트래픽을 나누다 이상이 생기면 되돌려야 합니다. 이 폴더는 배포 → 트래픽 전환 → 검증 → 롤백과 Git 재일치를 한 흐름으로 다룹니다.

## 읽는 순서

> 전략 고르기부터 도구 분리, 지표 검증, 롤백 절차 순서로 이어집니다. 1편에서 여섯 전략의 차이를 잡은 뒤 2~4편을 차례로 읽으면 배포 수명주기가 한 줄로 엮입니다.

| 편 | 이 편이 답하는 질문 | 핵심 키워드 |
|----|---------------------|-------------|
| [01-01. 배포 전략 비교](01-01.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EB%B9%84%EA%B5%90%20%E2%80%94%20Rolling%C2%B7Recreate%C2%B7Blue-Green%C2%B7Canary%C2%B7A-B%C2%B7Shadow.md) | 여섯 배포 전략은 어느 계층에서 트래픽을 나누며 언제 무엇을 고르는가 | RollingUpdate, Blue-Green, Canary, A-B, Shadow |
| [01-02. Argo CD 와 Argo Rollouts](01-02.Argo%20CD%20%EC%99%80%20Argo%20Rollouts%20%E2%80%94%20%EB%8F%99%EA%B8%B0%ED%99%94%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%EC%97%AD%ED%95%A0%20%EB%82%98%EB%88%94.md) | Git 동기화와 점진적 트래픽 제어의 경계를 어떻게 나누고 가중치를 다루는가 | Rollout CR, setWeight, trafficRouting, Progressive Sync |
| [01-03. 배포 검증과 자동 롤백](01-03.%EB%B0%B0%ED%8F%AC%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%9E%90%EB%8F%99%20%EB%A1%A4%EB%B0%B1%20%E2%80%94%20Health%20Check%20%EC%99%80%20Analysis.md) | Pod 기동이 성공한 뒤 터지는 장애를 어떤 지표와 조건으로 잡아 자동 중단하는가 | readinessProbe, AnalysisTemplate, failureLimit, SLO |
| [01-04. 배포 롤백 정책과 메커니즘](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md) | 장애 시 Rollback 과 Roll Forward 중 무엇을 고르고 Git 상태를 어떻게 다시 맞추는가 | Roll Forward, argocd app rollback, git revert, Expand and Contract |



## 주제 지도

> 필요한 주제만 바로 찾아야 할 때는 아래 다섯 축에서 해당 편과 절로 바로 건너뜁니다. 한 개념의 상세는 한 편에만 두었습니다.

- 배포 전략: 여섯 전략의 동작은 [01-01 §2](01-01.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EB%B9%84%EA%B5%90%20%E2%80%94%20Rolling%C2%B7Recreate%C2%B7Blue-Green%C2%B7Canary%C2%B7A-B%C2%B7Shadow.md#2-%EC%97%AC%EC%84%AF-%EB%B0%B0%ED%8F%AC-%EC%A0%84%EB%9E%B5%EC%9D%98-%EB%8F%99%EC%9E%91%EA%B3%BC-%ED%8A%B8%EB%9E%98%ED%94%BD-%EB%B6%84%EB%B0%B0)에, 비교표와 선택은 [§3](01-01.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EB%B9%84%EA%B5%90%20%E2%80%94%20Rolling%C2%B7Recreate%C2%B7Blue-Green%C2%B7Canary%C2%B7A-B%C2%B7Shadow.md#3-%EC%97%AC%EC%84%AF-%EC%A0%84%EB%9E%B5-%EB%B9%84%EA%B5%90%EC%99%80-%EC%83%81%ED%99%A9%EB%B3%84-%EC%84%A0%ED%83%9D)에 있습니다.
- 트래픽 라우팅: 계층 분할은 [01-01 §1](01-01.%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%EB%B9%84%EA%B5%90%20%E2%80%94%20Rolling%C2%B7Recreate%C2%B7Blue-Green%C2%B7Canary%C2%B7A-B%C2%B7Shadow.md#1-%ED%8A%B8%EB%9E%98%ED%94%BD-%EB%B6%84%ED%95%A0-%EA%B3%84%EC%B8%B5%EA%B3%BC-%EC%97%AC%EC%84%AF-%EC%A0%84%EB%9E%B5%EC%9D%98-%ED%9D%90%EB%A6%84)에, `trafficRouting` 과 Pod 근사는 [01-02 §2](01-02.Argo%20CD%20%EC%99%80%20Argo%20Rollouts%20%E2%80%94%20%EB%8F%99%EA%B8%B0%ED%99%94%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%EC%97%AD%ED%95%A0%20%EB%82%98%EB%88%94.md#trafficrouting-%EC%9C%A0%EB%AC%B4%EC%99%80-%EA%B0%80%EC%A4%91%EC%B9%98)에 있습니다.
- 도구 역할: Argo CD·Rollouts 경계는 [01-02 §1](01-02.Argo%20CD%20%EC%99%80%20Argo%20Rollouts%20%E2%80%94%20%EB%8F%99%EA%B8%B0%ED%99%94%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%EC%97%AD%ED%95%A0%20%EB%82%98%EB%88%94.md#1-git-%EB%8F%99%EA%B8%B0%ED%99%94%EC%99%80-%EC%A0%90%EC%A7%84%EC%A0%81-%EB%B0%B0%ED%8F%AC%EC%9D%98-%EB%B6%84%EB%A6%AC)·[§3](01-02.Argo%20CD%20%EC%99%80%20Argo%20Rollouts%20%E2%80%94%20%EB%8F%99%EA%B8%B0%ED%99%94%EC%99%80%20%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%EC%97%AD%ED%95%A0%20%EB%82%98%EB%88%94.md#3-argo-cd-%EC%9D%98-rollout-%EC%83%81%ED%83%9C-%ED%8C%90%EC%A0%95)에, Helm 제약은 [01-04 §2](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md#helm-%EB%A6%B4%EB%A6%AC%EC%8A%A4-%EB%A1%A4%EB%B0%B1%EA%B3%BC-argo-cd-%EC%A0%9C%EC%95%BD)에 있습니다.
- 검증: Health Check·Analysis 는 [01-03 §1](01-03.%EB%B0%B0%ED%8F%AC%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%9E%90%EB%8F%99%20%EB%A1%A4%EB%B0%B1%20%E2%80%94%20Health%20Check%20%EC%99%80%20Analysis.md#1-pod-%EA%B8%B0%EB%8F%99-%EC%84%B1%EA%B3%B5%EA%B3%BC-%EB%B0%B0%ED%8F%AC-%EC%8B%A4%ED%8C%A8%EC%9D%98-%EA%B0%84%EA%B7%B9)·[§3](01-03.%EB%B0%B0%ED%8F%AC%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%9E%90%EB%8F%99%20%EB%A1%A4%EB%B0%B1%20%E2%80%94%20Health%20Check%20%EC%99%80%20Analysis.md#3-analysistemplate-%EA%B5%AC%EC%A1%B0%EC%99%80-%ED%8C%90%EC%A0%95)에, 저트래픽·SLO 는 [§4](01-03.%EB%B0%B0%ED%8F%AC%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%9E%90%EB%8F%99%20%EB%A1%A4%EB%B0%B1%20%E2%80%94%20Health%20Check%20%EC%99%80%20Analysis.md#4-prometheus-%EC%BF%BC%EB%A6%AC-%EC%A0%84%EC%A0%9C%EC%99%80-%EC%A0%80%ED%8A%B8%EB%9E%98%ED%94%BD-%ED%95%A8%EC%A0%95)·[§5](01-03.%EB%B0%B0%ED%8F%AC%20%EA%B2%80%EC%A6%9D%EA%B3%BC%20%EC%9E%90%EB%8F%99%20%EB%A1%A4%EB%B0%B1%20%E2%80%94%20Health%20Check%20%EC%99%80%20Analysis.md#5-slisloerror-budget-%EC%97%B0%EA%B2%B0)에 있습니다.
- 복구: Rollback·Roll Forward·Git revert 는 [01-04 §1](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md#1-%EB%B3%B5%EA%B5%AC-%EB%B0%A9%EC%8B%9D-%EA%B5%AC%EB%B6%84%EA%B3%BC-%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0-%EC%B6%A9%EB%8F%8C)·[§2](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md#2-%EB%A1%A4%EB%B0%B1-%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98-%EB%8B%A4%EC%84%AF-%EA%B0%80%EC%A7%80)·[§3](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md#3-%EB%B3%B5%EA%B5%AC-%EC%88%98%EB%8B%A8-%EC%84%A0%ED%83%9D%EA%B3%BC-git-%EC%9E%AC%EC%9D%BC%EC%B9%98-%EC%A0%88%EC%B0%A8)에, DB 호환은 [§4](01-04.%EB%B0%B0%ED%8F%AC%20%EB%A1%A4%EB%B0%B1%20%EC%A0%95%EC%B1%85%EA%B3%BC%20%EB%A9%94%EC%BB%A4%EB%8B%88%EC%A6%98.md#4-db-%EB%B9%84%EA%B0%80%EC%97%AD%EC%84%B1%EA%B3%BC-%EC%9A%B4%EC%98%81-%EC%A0%95%EC%B1%85-%ED%95%9C%EA%B3%84)에 있습니다.



## 함께 볼 책 노트

> 기존 정독 노트와 다른 폴더 문서가 이미 풀어 둔 배경은 여기 다시 적지 않았습니다. 필요한 선행 개념은 아래 노트에서 함께 봅니다.

- [03-01. 푸시 배포의 한계와 ArgoCD GitOps](../../book/aic_ai-infra-claude/03-01.%ED%91%B8%EC%8B%9C%20%EB%B0%B0%ED%8F%AC%EC%9D%98%20%ED%95%9C%EA%B3%84%EC%99%80%20ArgoCD%20GitOps%20%E2%80%94%20%EC%84%A4%EC%B9%98%C2%B7%EC%97%B0%EA%B2%B0%C2%B7%EB%A1%A4%EB%A7%81%C2%B7%EB%A1%A4%EB%B0%B1.md) — Pull 기반 GitOps 전환 배경과 기본 설치
- [05-02. Blue-Green 무중단 전환과 아키텍처 결정 기록](../../book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md) — Blue-Green 전환 구조와 설계 결정 기록
- [06-02. 점진적 배포 Canary와 claude-context](../../book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) — Canary 단계 설계와 문맥 관리
- [15-02. Deployment 업데이트](../../../08_cloud/book/kubernetes-in-action/15-02.Deployment%20%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8%20%E2%80%94%20Recreate%C2%B7RollingUpdate%C2%B7maxSurge.md) — Recreate·RollingUpdate 와 maxSurge 동작
- [15-03. rollout 제어와 배포 전략](../../../08_cloud/book/kubernetes-in-action/15-03.rollout%20%EC%A0%9C%EC%96%B4%EC%99%80%20%EB%B0%B0%ED%8F%AC%20%EC%A0%84%EB%9E%B5%20%E2%80%94%20pause%C2%B7faulty%C2%B7rollback%C2%B7%EC%A0%84%EB%9E%B5%205%EC%A2%85.md) — ReplicaSet 제어와 `kubectl rollout`
- [05-01. 위험에 노출되는 트래픽을 줄여 가는 순서](../../../08_cloud/book/istio-in-action/05-01.%EC%9C%84%ED%97%98%EC%97%90%20%EB%85%B8%EC%B6%9C%EB%90%98%EB%8A%94%20%ED%8A%B8%EB%9E%98%ED%94%BD%EC%9D%84%20%EC%A4%84%EC%97%AC%20%EA%B0%80%EB%8A%94%20%EC%88%9C%EC%84%9C.md) — 서비스 메시 기반 트래픽 미러링과 Flagger
- [05-01. Application 동기화](../../book/argocd-up-and-running/05-01.Application%20%EB%8F%99%EA%B8%B0%ED%99%94%20%E2%80%94%20%EC%9E%90%EB%8F%99%20%EB%8F%99%EA%B8%B0%ED%99%94%C2%B7Sync%20Option%C2%B7Hook%C2%B7Sync%20Wave%20%EC%99%80%20%EC%B0%A8%EC%9D%B4%20%EB%AC%B4%EC%8B%9C.md) — Argo CD 자동 동기화·Sync Option·Sync Wave
- [10-01. Application 여럿을 순서대로](../../book/argocd-up-and-running/10-01.Application%20%EC%97%AC%EB%9F%BF%EC%9D%84%20%EC%88%9C%EC%84%9C%EB%8C%80%EB%A1%9C%20%E2%80%94%20%ED%97%AC%EC%8A%A4%20%EC%B2%B4%ED%81%AC%C2%B7App-of-Apps%20sync%20wave%C2%B7Progressive%20Sync.md) — ApplicationSet Progressive Sync
- [Helm 릴리스 운영](../iac/Helm%20%EB%A6%B4%EB%A6%AC%EC%8A%A4%20%EC%9A%B4%EC%98%81.md) — Helm 리비전 관리와 `helm rollback`
- [01-04. SLO와 알림 — Error Budget, Burn Rate](../../../06_observability/01_Foundations/01-04.SLO%EC%99%80%20%EC%95%8C%EB%A6%BC%20%E2%80%94%20Error%20Budget%2C%20Burn%20Rate.md) — SLI·SLO 와 Error Budget 산정 기준



## 아직 다루지 않은 주제

> 현재 네 편은 Argo CD·Argo Rollouts 중심의 1차 흐름만 다루고 있어 아래 도구와 원서 장은 후속 주제로 남았습니다.

- 도구·운영: Flagger, Feature Flag 도구(Unleash·LaunchDarkly), Release Freeze 운영
- Continuous Delivery: 10장(Deploying and Releasing Applications)·12장(Managing Data)
- Building Secure and Reliable Systems: 9장(Design for Recovery)
- Kubernetes Best Practices: 6·7·18장
- Building Microservices: 8장(Deployment)
