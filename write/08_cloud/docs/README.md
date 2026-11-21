---
title: 08_cloud/docs MOC — 공식 문서·제품 사이트 정독
tags: [moc, cloud, official-docs, kubernetes, cncf-certification]
status: final
related:
  - ../README.md
  - kubernetes/README.md
  - cncf-certification/README.md
  - istio/README.md
  - cmd/README.md
updated: 2026-11-21
---

# 08_cloud/docs — 공식 문서·제품 사이트 정독

---

> 공식 문서나 제품 사이트를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/](../book/)의 정독 노트와 [kubernetes/](../kubernetes/README.md)의 주제별 노트가 맡습니다.

## 폴더 규칙

> 바로 아래에는 제품(사이트)마다 폴더를 하나씩 둡니다. 공식 문서를 다시 폈을 때 그 제품의 노트가 어디 있는지 고민하지 않게 하려는 규약입니다.

| 폴더 | 1차 자료 |
|------|----------|
| [kubernetes/](kubernetes/README.md) | kubernetes.io 공식 문서 |
| [cncf-certification/](cncf-certification/README.md) | CNCF·Linux Foundation 자격증 커리큘럼·시험 안내 |
| [istio/](istio/README.md) | istio.io 공식 문서 |

Helm·Kustomize 와 Argo Rollouts 는 쿠버네티스 위에서 쓰지만 플랫폼보다 전달 절차에 속해서 [07_devops](../../07_devops/README.md) 로 옮겼습니다. 각각 [`iac/`](../../07_devops/docs/iac/README.md) 개념 폴더와 [Blue/Green 무중단 전환과 아키텍처 결정 기록](../../07_devops/book/aic_ai-infra-claude/05-02.Blue-Green%20%EB%AC%B4%EC%A4%91%EB%8B%A8%20%EC%A0%84%ED%99%98%EA%B3%BC%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EA%B2%B0%EC%A0%95%20%EA%B8%B0%EB%A1%9D.md)·[점진적 배포 Canary와 claude-context](../../07_devops/book/aic_ai-infra-claude/06-02.%EC%A0%90%EC%A7%84%EC%A0%81%20%EB%B0%B0%ED%8F%AC%20Canary%EC%99%80%20claude-context.md) 정독 노트에 있습니다.

[`cmd/`](cmd/README.md) 는 제품 폴더가 아니라 컨테이너·쿠버네티스 명령어 시트 자리입니다. 지금은 docker 이미지 반입 시트 한 편이 있고, 나머지는 분류와 후보 명령만 정해 두었습니다.

제품 안의 하위 폴더 규칙은 그 폴더의 README 가 정합니다. `kubernetes/` 는 파일명에 번호를 붙이지 않고 문서를 묶음 폴더 넷(`architecture/`·`scheduling/`·`operations/`·`api/`)에 나눠 둡니다. 새 제품을 다루게 되면 그 제품 폴더를 만들고 이 표에 한 줄을 더합니다.



## 문서 목록

> 제품별 현재 문서입니다. 각 제품 README 에 그 제품의 읽기 순서가 있습니다.

| 제품 | 폴더 | 묶음·번호 | 제목 |
|------|------|------|------|
| kubernetes | architecture | 아키텍처 | [노드·클러스터 소속](kubernetes/architecture/%EB%85%B8%EB%93%9C%C2%B7%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%86%8C%EC%86%8D.md) |
| kubernetes | architecture | 아키텍처 | [컨테이너 런타임 인터페이스·crictl](kubernetes/architecture/%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88%20%EB%9F%B0%ED%83%80%EC%9E%84%20%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4%C2%B7crictl.md) |
| kubernetes | architecture | 아키텍처 | [이미지 pull·폐쇄망 반입](kubernetes/architecture/%EC%9D%B4%EB%AF%B8%EC%A7%80%20pull%C2%B7%ED%8F%90%EC%87%84%EB%A7%9D%20%EB%B0%98%EC%9E%85.md) |
| kubernetes | scheduling | 스케줄링·축출 | [노드 압박 축출·디스크 관리](kubernetes/scheduling/%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%C2%B7%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC.md) |
| kubernetes | operations | 클러스터 운영 | [자원 모니터링 파이프라인](kubernetes/operations/%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8.md) |
| kubernetes | operations | 클러스터 운영 | [etcd 헬스·유지보수](kubernetes/operations/etcd%20%ED%97%AC%EC%8A%A4%C2%B7%EC%9C%A0%EC%A7%80%EB%B3%B4%EC%88%98.md) |
| kubernetes | operations | 클러스터 운영 | [클러스터 업그레이드·ETCD 백업·복구](kubernetes/operations/%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%97%85%EA%B7%B8%EB%A0%88%EC%9D%B4%EB%93%9C%C2%B7ETCD%20%EB%B0%B1%EC%97%85%C2%B7%EB%B3%B5%EA%B5%AC.md) |
| kubernetes | operations | 클러스터 운영 | [모니터링 개요·트러블슈팅 루틴](kubernetes/operations/%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%EA%B0%9C%EC%9A%94%C2%B7%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85%20%EB%A3%A8%ED%8B%B4.md) |
| kubernetes | operations | 클러스터 운영 | [노드 추가·제거](kubernetes/operations/%EB%85%B8%EB%93%9C%20%EC%B6%94%EA%B0%80%C2%B7%EC%A0%9C%EA%B1%B0.md) |
| kubernetes | operations | 클러스터 운영(사례) | [OOMKilled 사례](kubernetes/operations/OOMKilled%20%EC%82%AC%EB%A1%80%20%E2%80%94%20Endowus%20Rebalance%20%EC%84%9C%EB%B9%84%EC%8A%A4.md) |
| kubernetes | api | API | [API 서버 헬스 엔드포인트](kubernetes/api/API%20%EC%84%9C%EB%B2%84%20%ED%97%AC%EC%8A%A4%20%EC%97%94%EB%93%9C%ED%8F%AC%EC%9D%B8%ED%8A%B8.md) |
| kubernetes | api | API | [TLS·API 접근 보안](kubernetes/api/TLS%C2%B7API%20%EC%A0%91%EA%B7%BC%20%EB%B3%B4%EC%95%88.md) |
| kubernetes | api | API | [JSONPath·kubectl 고급 조회](kubernetes/api/JSONPath%C2%B7kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) |
| kubernetes | api | API | [kubeconfig·여러 클러스터 접근](kubernetes/api/kubeconfig%C2%B7%EC%97%AC%EB%9F%AC%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%20%EC%A0%91%EA%B7%BC.md) |
| cncf-certification | (바로 아래) | 01-01 | [CKA 대비와 문제 풀이 전략](cncf-certification/01-01.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) |
| istio | (바로 아래) | — | [Ambient 모드·ztunnel·waypoint](istio/Ambient%20%EB%AA%A8%EB%93%9C%C2%B7ztunnel%C2%B7waypoint.md) |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [08_cloud MOC](../README.md) — 대분류 지도
- [kubernetes/](../kubernetes/README.md) — 주제별 학습 노트. 공식 문서 정독과 겹치는 주제는 서로 링크로 잇습니다
- [book/](../book/) — 책 정독 노트. 전체 개념의 뼈대는 이쪽에서 잡습니다
