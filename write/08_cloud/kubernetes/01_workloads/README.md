---
title: 01_workloads — 워크로드
tags: [moc, kubernetes, pod, deployment, job, cronjob, daemonset]
status: final
related:
  - ../README.md
updated: 2026-07-10
---

# 01_workloads — 워크로드

> 애플리케이션을 감싸 실행하는 리소스를 봅니다. 상시 실행되는 워크로드(Pod·Deployment)부터 끝나는 배치 작업(Job·CronJob)까지 한 묶음입니다.



## 문서 목록
> 공식 concepts의 Workloads에 대응합니다. 파일 번호(`01-MM`)가 읽기 순서입니다. 각 본문에는 같은 번호의 `점검.md`가 짝을 이룹니다(일부 입문 편 제외).

| 번호 | 제목 | 한 줄 소개 |
|------|------|-----------|
| 01-01 | [핵심 워크로드](01-01.%ED%95%B5%EC%8B%AC%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Pod·Deployment·Service가 각각 무엇을 책임지는지, 셋의 역할 분담으로 애플리케이션이 어떻게 굴러가는지 봅니다. |
| 01-02 | [배치 워크로드](01-02.%EB%B0%B0%EC%B9%98%20%EC%9B%8C%ED%81%AC%EB%A1%9C%EB%93%9C.md) | Job·CronJob·DaemonSet·InitContainer·Sidecar가 각각 어떤 의도를 표현하는지 봅니다. |



## 관련 문서
> 이 폴더가 딛고 서거나 이어지는 이웃 대주제입니다.

- [kubernetes MOC](../README.md) — 전체 대주제 지도와 딥다이브 로드맵 연결
