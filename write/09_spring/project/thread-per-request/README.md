---
title: thread-per-request — 요청당 스레드와 Go 비교 인덱스
tags: [lab, spring, virtual-thread, concurrency, go]
status: draft
source:
  - ~/study/runners-lab/jvm/thread-per-request
updated: "2026-11-04"
---

# thread-per-request — 요청당 스레드와 Go 비교 인덱스

Spring MVC 는 요청 하나에 스레드 하나를 붙이는데, 작은 요청이 대량으로 올 때와 요청 하나가 느리거나 클 때 이 모델이 어디서 막히는지를 Go 와 같은 부하로 재어 본 랩이다. 플랫폼 스레드(풀 200·20)와 가상 스레드, Go goroutine 을 비교한다.

결과 표와 읽는 법은 랩의 `README.md`(`~/study/runners-lab/jvm/thread-per-request/README.md`)에 있다.
