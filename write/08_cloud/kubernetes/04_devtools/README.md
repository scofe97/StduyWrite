---
title: Kubernetes DevTools 학습 MOC — CI/CD와 GitOps
tags: [moc, kubernetes, jenkins, sonarqube, argocd, harbor, gitops]
status: draft
related:
  - ../README.md
  - ../03_platform/README.md
  - ../05_operations/README.md
  - ../../argocd/README.md
updated: 2026-05-30
---

# Kubernetes DevTools 학습 MOC — CI/CD와 GitOps

---

> 클러스터 위에서 코드를 빌드·검증하고(Jenkins·SonarQube), 이미지를 보관하고(Harbor), Git 을 단일 진실 공급원 삼아 배포하는(ArgoCD) 도구들을 한 폴더에 모았습니다. 이 묶음을 끝내면 "커밋 한 번이 클러스터의 실제 배포로 이어지는 파이프라인을 어떤 도구가 어디서 책임지는가" 에 답할 수 있습니다.

## 왜 한 폴더로 묶었는가

네 도구는 따로 보면 별개지만, 이어 붙이면 하나의 배포 파이프라인이 됩니다. Jenkins 가 빌드를 돌리고, SonarQube 가 코드 품질 게이트를 걸고, Harbor 가 결과 이미지를 보관하고, ArgoCD 가 그 이미지를 Git 선언에 맞춰 클러스터에 반영합니다. "개발 생산성과 배포 자동화" 라는 한 목적으로 묶이므로 같은 폴더에 두었습니다.

ArgoCD 는 이 폴더에서 입문 수준으로만 다룹니다. App of Apps·ApplicationSet·Image Updater 같은 상세 운영은 별도 [`argocd`](../../argocd/README.md) 카테고리로 분리했습니다.

## 학습 순서

| 장 | 문서 | 다루는 핵심 |
|----|------|-----------|
| 04-01 | [Jenkins on K8s](04-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins — 동적 에이전트·Pod 템플릿 |
| 04-02 | [SonarQube on K8s](04-02.SonarQube%20on%20K8s.md) | SonarQube 영속성 전략·품질 게이트 |
| 04-03 | [ArgoCD와 GitOps](04-03.ArgoCD%EC%99%80%20GitOps.md) | Git 을 단일 진실 공급원으로 삼는 선언적 배포 |
| 04-04 | [Harbor](04-04.Harbor.md) | 컨테이너 이미지·OCI Helm chart 통합 레지스트리 |

각 본문에는 같은 이름의 ` 점검.md` 가 짝으로 들어 있습니다.

## 사전 지식

> 이 묶음은 다음을 안다고 가정합니다.

1. [`03_platform`](../03_platform/README.md) 의 Helm 으로 애플리케이션을 배포해 봤습니다.
2. CI/CD 라는 용어를 한 줄로 설명할 수 있습니다 — "코드 변경을 자동으로 빌드·검증·배포한다".
3. Git 브랜치·커밋·푸시 흐름에 익숙합니다.

## 면접 대비 체크리스트

> 네 장을 다 읽은 뒤 다음 질문에 답할 수 있어야 합니다.

1. K8s 위 Jenkins 의 동적 에이전트는 기존 정적 에이전트와 무엇이 다릅니까?
2. SonarQube 의 품질 게이트는 파이프라인의 어느 지점에서 빌드를 막습니까?
3. GitOps 에서 "Git 이 단일 진실 공급원" 이라는 말은 구체적으로 무엇을 의미합니까?
4. ArgoCD 의 sync 와 self-heal 은 각각 무엇을 보장합니까?
5. Harbor 가 단순 레지스트리를 넘어 제공하는 것(스캔·서명·OCI Helm)은?

각 질문에 막히면 해당 장 본문으로 돌아가서 다시 읽습니다.
