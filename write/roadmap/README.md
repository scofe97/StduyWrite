---
title: 학습 로드맵
tags: [moc, roadmap, index]
status: final
related:
  - ../README.md
updated: 2026-09-23
---

# 학습 로드맵
---

> 무엇을 어떤 순서로 읽을지 정리한 로드맵의 인덱스입니다.

## 로드맵

> 배울 키워드를 기록하고 정리하는 참고용 지도입니다. 규약은 writing-method 스킬의 로드맵 문서 규약이 정본입니다.

| 로드맵 | 범위 |
|---|---|
| [OS](os-roadmap.md) | Linux 사용에서 프로세스·격리·성능·커널 내부까지 |
| [네트워크](network-roadmap.md) | socket과 Linux 패킷 경로에서 클라우드 underlay와 오버레이 터널까지 |
| [Kubernetes](k8s-roadmap.md) | 오브젝트 선언에서 클러스터 내부 구조·확장·운영까지 |
| [Go](go-roadmap.md) | 문법과 타입 설계에서 동시성·서비스·터미널 세션까지 |
| [데이터](data-roadmap.md) | 데이터 시스템의 축에서 저장 엔진·복제·합의·스트림까지 |
| [관측 가능성](observability-roadmap.md) | 계측과 세 신호에서 SLO·확장·플랫폼까지 |
| [JVM](jvm-roadmap.md) | 런타임 데이터 영역에서 클래스 로딩·GC·동시성·장애 진단까지 |
| [Spring](spring-roadmap.md) | 컨테이너와 프록시에서 부트·보안·운영·배포까지 |
| [AI](ai-roadmap.md) | 모델을 도구로 부리는 법에서 GitAIOps 배포 운영까지 |



## 목적별 진입 경로

> 한 분야를 처음부터 다 읽지 않고, 목적에 닿는 단계만 이어 읽는 길입니다. 각 로드맵의 `경계` 절이 같은 증상을 여러 층에서 보는 자리를 이미 짚어 두었고, 그것을 단계 순으로 엮었습니다.

| 목적 | 이어 읽는 단계 |
|---|---|
| 컨테이너가 OOMKilled 로 죽는 이유 | [OS](os-roadmap.md) 2단계 종료 신호 · 3단계 `memory.max` 와 OOM Killer, [Kubernetes](k8s-roadmap.md) 7단계 자원 장애, [JVM](jvm-roadmap.md) 1단계 컨테이너 네이티브 메모리 |
| Service 로 부르면 실패하는 호출 | [Kubernetes](k8s-roadmap.md) 3단계 Service · EndpointSlice, [네트워크](network-roadmap.md) 4단계 kube-proxy · 2단계 conntrack · MTU |
| 응답이 느려졌을 때 층 가르기 | [관측 가능성](observability-roadmap.md) 5단계 SLO, [OS](os-roadmap.md) 4단계 USE · run queue, [Kubernetes](k8s-roadmap.md) 7단계 CPU throttling, [네트워크](network-roadmap.md) 3단계 재전송 판독, [JVM](jvm-roadmap.md) 7단계 GC 로그 |



## 도식

> SVG는 같은 이름의 생성기에서 만듭니다.

| 로드맵 | SVG | 생성기 |
|---|---|---|
| OS | [학습 순서](_assets/os-roadmap.svg) · [책 읽기 흐름](_assets/os-books.svg) | [학습 순서](_assets/_gen/gen-os-roadmap.py) · [책 흐름](_assets/_gen/gen-os-books.py) |
| 네트워크 | [학습 순서](_assets/network-roadmap.svg) · [책 읽기 흐름](_assets/network-books.svg) | [학습 순서](_assets/_gen/gen-network-roadmap.py) · [책 흐름](_assets/_gen/gen-network-books.py) |
| Kubernetes | [학습 순서](_assets/k8s-roadmap.svg) · [책 읽기 흐름](_assets/k8s-books.svg) | [학습 순서](_assets/_gen/gen-k8s-roadmap.py) · [책 흐름](_assets/_gen/gen-k8s-books.py) |
| Go | [학습 순서](_assets/go-roadmap.svg) · [책 읽기 흐름](_assets/go-books.svg) | [학습 순서](_assets/_gen/gen-go-roadmap.py) · [책 흐름](_assets/_gen/gen-go-books.py) |
| 데이터 | [학습 순서](_assets/data-roadmap.svg) · [책 읽기 흐름](_assets/data-books.svg) | [학습 순서](_assets/_gen/gen-data-roadmap.py) · [책 흐름](_assets/_gen/gen-data-books.py) |
| JVM | [학습 순서](_assets/jvm-roadmap.svg) · [책 읽기 흐름](_assets/jvm-books.svg) | [학습 순서](_assets/_gen/gen-jvm-roadmap.py) · [책 흐름](_assets/_gen/gen-jvm-books.py) |
| 관측 가능성 | [학습 순서](_assets/observability-roadmap.svg) · [책 읽기 흐름](_assets/observability-books.svg) | [학습 순서](_assets/_gen/gen-observability-roadmap.py) · [책 흐름](_assets/_gen/gen-observability-books.py) |
| AI | [학습 순서](_assets/ai-roadmap.svg) · [책 읽기 흐름](_assets/ai-books.svg) | [학습 순서](_assets/_gen/gen-ai-roadmap.py) · [책 흐름](_assets/_gen/gen-ai-books.py) |
| Spring | [학습 순서](_assets/spring-roadmap.svg) · [책 읽기 흐름](_assets/spring-books.svg) | [학습 순서](_assets/_gen/gen-spring-roadmap.py) · [책 흐름](_assets/_gen/gen-spring-books.py) |
