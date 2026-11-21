---
title: 08_cloud/kubernetes — Kubernetes 데브툴스 운영
tags: [moc, kubernetes, devtools, jenkins, sonarqube, harbor]
status: final
related:
  - ../README.md
  - ../docs/kubernetes/README.md
  - 11_devtools/README.md
  - ../../07_devops/book/argocd-up-and-running/README.md
updated: 2026-11-21
---

# 08_cloud/kubernetes — Kubernetes 데브툴스 운영

---

> Kubernetes 위에서 동작하는 CI/CD·레지스트리 데브툴스 운영 노트를 다룹니다.

쿠버네티스 핵심 개념과 순정 아키텍처·운영 문서는 [`../docs/kubernetes/`](../docs/kubernetes/README.md) 및 [`../book/`](../book/)으로 이관되었습니다. 현재 이 폴더에는 쿠버네티스 클러스터 위에 배포해 사용하는 개발 생산성 도구 모음인 [`11_devtools/`](11_devtools/README.md)만 남겨 운영합니다.

## 폴더 구조

| 폴더 | 다루는 것 | 문서 |
|------|-----------|------|
| [`11_devtools/`](11_devtools/README.md) | K8s 기반 CI/CD·레지스트리 도구 운영 | 3편 |

## 문서 목록 (11_devtools)

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 11-01 | [Jenkins on K8s](11_devtools/11-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins가 무엇이 달라지는지(동적 Agent 등) 봅니다. |
| 11-02 | [SonarQube on K8s](11_devtools/11-02.SonarQube%20on%20K8s.md) | SonarQube의 영속성 전략을 봅니다. |
| 11-04 | [Harbor](11_devtools/11-04.Harbor.md) | 이미지와 OCI Helm chart를 어디서 통합 관리하는지 봅니다. |

옛 11-03 은 [Argo CD Up and Running — 정독 인덱스](../../07_devops/book/argocd-up-and-running/README.md)로 흡수되어 번호가 비어 있습니다.

## 관련 문서

- [08_cloud MOC](../README.md) — 클라우드·인프라 대분류 지도
- [docs/kubernetes MOC](../docs/kubernetes/README.md) — 쿠버네티스 공식 문서 정독 및 클러스터 운영 노트
- [Argo CD Up and Running 정독](../../07_devops/book/argocd-up-and-running/README.md) — ArgoCD 상세 운영 시리즈
