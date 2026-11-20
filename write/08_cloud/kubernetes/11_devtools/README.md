---
title: 11_devtools — DevTools
tags: [moc, kubernetes, jenkins, sonarqube, harbor]
status: final
related:
  - ../README.md
updated: 2026-11-21
---

# 11_devtools — DevTools

> Jenkins·SonarQube·Harbor를 K8s 위에 올려 개발 생산성을 얻습니다. ArgoCD 와 GitOps 는 07_devops 의 [ArgoCD와 GitOps](../../../07_devops/docs/deployment/ArgoCD%C2%B7GitOps.md)와 [Argo CD Up and Running 정독](../../../07_devops/book/argocd-up-and-running/README.md)이 맡습니다.



## 문서 목록
> 공식 concepts에는 없는 비공식 주제입니다 — K8s 위에 올려 쓰는 CI/CD·레지스트리 도구를 모았습니다. 파일 번호(`11-MM`)가 읽기 순서입니다. 각 본문 끝에는 `## N. 점검 질문` 절이 있어, 개념 설명과 심화 Q&A를 한 문서에서 이어 읽습니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 11-01 | [Jenkins on K8s](11-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins가 무엇이 달라지는지(동적 Agent 등) 봅니다. |
| 11-02 | [SonarQube on K8s](11-02.SonarQube%20on%20K8s.md) | SonarQube의 영속성 전략을 봅니다. |
| 11-04 | [Harbor](11-04.Harbor.md) | 이미지와 OCI Helm chart를 어디서 통합 관리하는지 봅니다. |

11-03 [ArgoCD와 GitOps](../../../07_devops/docs/deployment/ArgoCD%C2%B7GitOps.md)는 2026-11-21 에 `07_devops/docs/deployment/` 로 옮겨서 번호가 비어 있습니다.



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
