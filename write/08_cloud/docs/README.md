---
title: 08_cloud/docs — 쿠버네티스 공식문서 정독
tags: [moc, kubernetes, official-docs]
status: final
related:
  - ../README.md
  - ../kubernetes/README.md
updated: 2026-08-27
---

# 08_cloud/docs — 쿠버네티스 공식문서 정독

---

> k8s.io 공식문서를 1차 자료로 삼아 궁금한 주제만 한 편씩 파고드는 자리입니다. 전체 개념을 순서대로 훑는 일은 [book/](../book/)의 정독 노트와 [kubernetes/](../kubernetes/README.md)의 주제별 노트가 맡습니다.

## 폴더 규칙

> 하위 폴더는 k8s.io 의 섹션 슬러그와 1:1 로 맞춥니다. 공식문서를 다시 폈을 때 그 페이지가 어느 폴더로 갔는지 고민하지 않게 하려는 규약입니다.

| 폴더 | 대응 k8s.io 섹션 |
|------|------------------|
| [architecture/](architecture/README.md) | `/docs/concepts/architecture/` |
| [cluster-administration/](cluster-administration/README.md) | `/docs/concepts/cluster-administration/` |
| [scheduling-eviction/](scheduling-eviction/README.md) | `/docs/concepts/scheduling-eviction/` |

새 주제를 쓸 때는 그 문서의 1차 근거가 가장 많이 나오는 섹션 폴더에 넣습니다. 한 문서가 여러 섹션을 가로지르는 일은 흔하므로, 나머지 섹션은 프론트매터 `source` 와 본문 각주로 남깁니다. 해당 섹션 폴더가 아직 없으면 그때 만들고 이 표에 한 줄을 더합니다.

파일명은 `05-file-placement.md` §5.1 의 `{장}-{절}.{제목}.md` 를 따릅니다. 번호는 작성 순서가 아니라 주제 묶음 기준이라, 같은 묶음이 늘면 `01-02` 로, 묶음이 바뀌면 `02-01` 로 넘어갑니다.



## 문서 목록

> 폴더별 현재 문서입니다. 각 폴더 README 에 그 섹션의 읽기 순서가 있습니다.

| 폴더 | 번호 | 제목 |
|------|------|------|
| architecture | 01-01 | [노드와 클러스터의 소속](architecture/01-01.%EB%85%B8%EB%93%9C%EC%99%80%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EC%9D%98%20%EC%86%8C%EC%86%8D%20%E2%80%94%20%EA%B2%B9%EC%B3%90%20%EB%B3%B4%EC%9D%B4%EB%8A%94%20%ED%81%B4%EB%9F%AC%EC%8A%A4%ED%84%B0%EB%8A%94%20%EC%96%B4%EB%8A%90%20%EC%B8%B5%EC%97%90%EC%84%9C%20%EA%B2%B9%EC%B9%98%EB%8A%94%EA%B0%80.md) |
| cluster-administration | 01-01 | [자원 모니터링 파이프라인](cluster-administration/01-01.%EC%9E%90%EC%9B%90%20%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%20%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8%20%E2%80%94%20kubelet%EC%9D%B4%20%EC%9E%AC%EB%8A%94%20%EA%B2%83%EA%B3%BC%20kubectl%20top%EC%9D%B4%20%EC%9D%BD%EB%8A%94%20%EA%B2%83.md) |
| scheduling-eviction | 01-01 | [노드 압박 축출과 디스크 관리](scheduling-eviction/01-01.%EB%85%B8%EB%93%9C%20%EC%95%95%EB%B0%95%20%EC%B6%95%EC%B6%9C%EA%B3%BC%20%EB%94%94%EC%8A%A4%ED%81%AC%20%EA%B4%80%EB%A6%AC%20%E2%80%94%20DiskPressure%EB%8A%94%20%EB%AC%B4%EC%97%87%EC%9D%84%20%EB%B3%B4%EA%B3%A0%20%EC%BC%9C%EC%A7%80%EB%8A%94%EA%B0%80.md) |



## 관련 문서

> 이 폴더가 딛고 서거나 이어지는 이웃입니다.

- [08_cloud MOC](../README.md) — 대분류 지도
- [kubernetes/](../kubernetes/README.md) — 주제별 학습 노트. 공식문서 정독과 겹치는 주제는 서로 링크로 잇습니다
- [book/](../book/) — 책 정독 노트. 전체 개념의 뼈대는 이쪽에서 잡습니다
