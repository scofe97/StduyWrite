---
title: 11_devtools — DevTools와 GitOps
tags: [moc, kubernetes, jenkins, sonarqube, argocd, harbor, gitops]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 11_devtools — DevTools와 GitOps

> Jenkins·SonarQube·ArgoCD·Harbor를 K8s 위에 올려 개발 생산성과 배포 자동화를 얻습니다. ArgoCD 상세 운영은 별도 [argocd](../../argocd/README.md) 카테고리로 넘깁니다.



## 문서 목록
> 공식 concepts에는 없는 비공식 주제입니다 — K8s 위에 올려 쓰는 CI/CD·GitOps·레지스트리 도구를 모았습니다. 파일 번호(`11-MM`)가 읽기 순서입니다. 각 본문에는 같은 번호의 `점검.md`가 짝을 이룹니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 11-01 | [Jenkins on K8s](11-01.Jenkins%20on%20K8s.md) | K8s 네이티브 Jenkins가 무엇이 달라지는지(동적 Agent 등) 봅니다. |
| 11-02 | [SonarQube on K8s](11-02.SonarQube%20on%20K8s.md) | SonarQube의 영속성 전략을 봅니다. |
| 11-03 | [ArgoCD와 GitOps](11-03.ArgoCD%EC%99%80%20GitOps.md) | Git을 단일 진실 공급원으로 삼는 배포 모델을 입문 수준으로 봅니다. |
| 11-04 | [Harbor](11-04.Harbor.md) | 이미지와 OCI Helm chart를 어디서 통합 관리하는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
