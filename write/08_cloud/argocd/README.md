---
title: 08_cloud/argocd — ArgoCD와 GitOps 실전
tags: [moc, argocd, gitops, applicationset, app-of-apps]
status: final
source:
  - ../../../docs/03_CloudNative/03_ArgoCD/01_Introduction_to_Argo_CD.md
  - https://argo-cd.readthedocs.io/en/stable/
related:
  - ../README.md
  - ../kubernetes/README.md
  - ../../07_devops/README.md
updated: 2026-04-25
---

# 08_cloud/argocd
---
> ArgoCD를 단순 배포 도구가 아니라 GitOps 운영 체계로 이해하기 위한 문서 묶음이다. 설치와 Application 기초부터 App of Apps, ApplicationSet, Image Updater, 운영 확장성까지 한 흐름으로 정리한다.

이 카테고리는 Kubernetes 기본 네트워킹과 워크로드 위에 놓이는 GitOps/CD 계층을 다룬다. Pod, Service, Ingress, Helm 같은 기본 개념은 `kubernetes` 카테고리에서 먼저 읽고, 여기서는 Git을 기준 상태로 삼아 클러스터를 어떻게 운영하는지에 집중한다.



## 학습 흐름
> 설치와 기초를 먼저 익히고, 배포 단위와 동기화 전략, 권한과 보안, 확장과 운영 심화로 넘어간다.

### Part 1 — 입문과 설치 (Ch01)
ArgoCD가 왜 필요한지, 어떤 컴포넌트로 이루어지는지, 어떻게 접근하고 선언적으로 설정하는지 먼저 잡는다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 01-01 | [ArgoCD와 GitOps 기초](./01-01.ArgoCD와%20GitOps%20기초.md) | GitOps는 왜 Pull 모델을 택하는가? |
| 01-02 | [ArgoCD 설치와 아키텍처](./01-02.ArgoCD%20설치와%20아키텍처.md) | 어떤 설치 모드와 컴포넌트 구성이 필요한가? |
| 01-03 | [ArgoCD 접근과 선언적 설정](./01-03.ArgoCD%20접근과%20선언적%20설정.md) | UI, CLI, ConfigMap/Secret, 선언적 관리 방식은 어떻게 연결되는가? |

### Part 2 — 배포 단위와 동기화 (Ch02)
Application, Sync, App of Apps, ApplicationSet처럼 ArgoCD를 실제 배포 체계로 쓰는 핵심 개념을 묶는다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 02-01 | [Application과 배포 대상 관리](./02-01.Application과%20배포%20대상%20관리.md) | 무엇을 어디에 배포할지 ArgoCD는 어떻게 선언하는가? |
| 02-02 | [Sync 전략과 배포 순서 제어](./02-02.Sync%20전략과%20배포%20순서%20제어.md) | 자동 동기화, Hook, Wave, Sync Window는 어떻게 조합하는가? |
| 02-03 | [App of Apps와 ApplicationSet](./02-03.App%20of%20Apps와%20ApplicationSet.md) | 여러 앱을 어떻게 계층화하고 대규모로 생성하는가? |

### Part 3 — 권한, 멀티클러스터, 보안 (Ch03)
실제 조직에서 운영하려면 권한 경계와 여러 클러스터, 저장소 보안을 함께 봐야 한다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 03-01 | [인증·인가와 AppProject](./03-01.인증·인가와%20AppProject.md) | SSO, RBAC, Project 경계는 어떻게 설계하는가? |
| 03-02 | [멀티클러스터와 멀티테넌시](./03-02.멀티클러스터와%20멀티테넌시.md) | 여러 클러스터와 팀을 어떻게 한 컨트롤 플레인에서 다루는가? |
| 03-03 | [보안 운영](./03-03.보안%20운영.md) | TLS, 저장소 인증, 서명 검증, impersonation은 어떻게 운영하는가? |

### Part 4 — 확장과 자동화 (Ch04)
ArgoCD를 실무에 붙이면 플러그인, 자동 태그 갱신, 점진 배포, 마이크로서비스 CI/CD 통합이 같이 따라온다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 04-01 | [ArgoCD 확장과 플러그인](./04-01.ArgoCD%20확장과%20플러그인.md) | CMP와 UI 확장은 언제 필요한가? |
| 04-02 | [CI 연동과 Image Updater](./04-02.CI%20연동과%20Image%20Updater.md) | CI, 레지스트리, Git write-back을 어떻게 안전하게 묶는가? |
| 04-03 | [Argo Rollouts와 배포 전략](./04-03.Argo%20Rollouts와%20배포%20전략.md) | Blue-Green/Canary/Progressive Delivery를 어떻게 spec으로 표현하는가? |
| 04-04 | [마이크로서비스 CI/CD 파이프라인 통합](./04-04.마이크로서비스%20CI_CD%20파이프라인%20통합.md) | Jenkins+Harbor+ImageUpdater+Rollouts+Notifications를 어떻게 한 흐름으로 묶는가? |

### Part 5 — 운영 심화 (Ch05)
모니터링, HA, 샤딩, Progressive Sync, GitOps 성숙도 같은 운영 주제를 묶는다.

| Ch | 제목 | 핵심 질문 |
|----|------|----------|
| 05-01 | [모니터링·알림·HA 운영](./05-01.모니터링·알림·HA%20운영.md) | UI 밖에서 ArgoCD를 어떻게 운영 관측하는가? |
| 05-02 | [대규모 운영과 Progressive Sync](./05-02.대규모%20운영과%20Progressive%20Sync.md) | 수백 개 앱을 어떻게 순차적으로 안전하게 배포하는가? |
| 05-03 | [GitOps 성숙도와 미래 고려사항](./05-03.GitOps%20성숙도와%20미래%20고려사항.md) | 조직이 커질수록 저장소 구조와 GitOps 워크플로우는 어떻게 바뀌는가? |



## 심화 탐구 (deepdive/)
> 각 장에는 같은 번호 체계를 따르는 `실습.md` 또는 `점검.md`가 짝을 이룬다.

설치·접근·멀티클러스터·플러그인처럼 절차가 중요한 장은 `실습.md`를 붙인다. 반대로 AppProject, App of Apps, 보안, Image Updater, 운영 심화처럼 판단 포인트가 많은 장은 `점검.md`를 붙인다. `02-03`과 `04-02`는 실무 난도가 높으므로 실습과 점검을 함께 둔다. `04-03`은 Blue-Green/Canary 매니페스트를 단계별로 적용해 보는 실습을, `04-04`는 12개 마이크로서비스 통합 파이프라인 설계 점검을 둔다.



## 실습 환경
> 개인 GCP K8s 클러스터를 기준으로 하되, 본문은 가능한 한 범용 명령으로 유지한다.

현재 기준 실습은 개인 GCP K8s 클러스터(dev-server 1~3, asia-northeast3-a, kubeadm v1.31.14)에서 수행한다. 본문은 `kubectl`, `argocd`, Helm 중심의 범용 흐름으로 쓰고, 환경 특화 값은 deepdive 상단의 `## 실습 환경`에만 둔다.



## 관련 문서
> Kubernetes 기초, DevOps 카테고리, 기존 브리지 문서와의 관계를 함께 본다.

- [kubernetes MOC](../kubernetes/README.md) — Helm, Ingress, RBAC, Operator 같은 선행 개념
- [ArgoCD와 GitOps](../kubernetes/04-03.ArgoCD와%20GitOps.md) — Kubernetes 카테고리 안의 입문/브리지 문서
- [devops MOC](../../07_devops/README.md) — Jenkins, SonarQube, CI 파이프라인 자체 설계
