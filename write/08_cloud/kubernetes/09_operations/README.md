---
title: 09_operations — Day-2 운영
tags: [moc, kubernetes, observability, troubleshooting, jsonpath, cka]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 09_operations — Day-2 운영

> 클러스터를 안정적으로 굴리기 위한 관측·진단·조회 주제를 모았습니다. 장애를 감이 아니라 증거로 좁히는 것이 목표입니다.



## 문서 목록
> 공식 concepts의 Cluster Administration에 대응합니다. 파일 번호(`09-MM`)가 읽기 순서입니다. 각 본문에는 같은 번호의 `점검.md`가 짝을 이룹니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 09-01 | [모니터링과 트러블슈팅](09-01.%EB%AA%A8%EB%8B%88%ED%84%B0%EB%A7%81%EA%B3%BC%20%ED%8A%B8%EB%9F%AC%EB%B8%94%EC%8A%88%ED%8C%85.md) | 클러스터 장애를 어떻게 체계적으로 진단하는지 봅니다. |
| 09-02 | [OOMKilled 사례 분석](09-02.OOMKilled%20%EC%82%AC%EB%A1%80%20%EB%B6%84%EC%84%9D.md) | 6GB Pod가 반복 OOMKilled되는 실제 사례에서 JVM heap과 cgroup이 보는 메모리가 왜 어긋나는지 추적합니다. |
| 09-03 | [JSONPath와 kubectl 고급 조회](09-03.JSONPath%EC%99%80%20kubectl%20%EA%B3%A0%EA%B8%89%20%EC%A1%B0%ED%9A%8C.md) | 반복 조회·스크립팅에 필요한 출력 제어를 익힙니다. |
| 09-04 | [CKA 대비와 문제 풀이 전략](09-04.CKA%20%EB%8C%80%EB%B9%84%EC%99%80%20%EB%AC%B8%EC%A0%9C%20%ED%92%80%EC%9D%B4%20%EC%A0%84%EB%9E%B5.md) | 시험 범위를 실무 문서와 어떻게 잇는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
