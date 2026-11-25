---
title: 책에 없는 Go·K8s 개념 모음
tags: [go, kubernetes, helm, istio, index]
status: draft
updated: 2026-11-25
---

# 책에 없는 Go·K8s 개념 모음

> 정독한 책(Network Programming with Go 등)이 다루지 않았지만 실무 코드에서 자주 만나는 개념을 정리해 둔 임시 참고 폴더입니다. 13편은 각 카테고리 정본 문서로 옮겼고, 현재는 Go 테스트 대역 1편만 남았습니다.



## 이 폴더를 읽는 법

원래 14편이 있던 임시 문서(`status: draft`) 가운데 13편은 각 카테고리의 정본 문서로 옮겨 지금은 1편만 남았습니다. 번호는 붙이지 않았으며 서로 가까운 개념은 한 편으로 묶었습니다.

인용문은 2026-11-06 에 원문과 대조했습니다. 공식 문서와 소스를 `curl`·`go doc` 로 받아 159건을 맞춰 봤고, 어긋난 서술 1건(miniredis 의 `CLUSTER` 지원 범위)은 고쳤습니다.

출처 주소는 가능한 곳마다 버전이나 커밋을 고정했습니다. 고정 주소가 없는 페이지(Go 명세, Dockerfile reference, WHATWG, nginx 등)에는 `(2026-11-06 확인)` 을 붙였습니다. Go 예제는 go1.25.1 에서 `go vet`·빌드를 통과했지만, Kubernetes·Istio 내용은 클러스터에서 직접 돌려 보지 않았습니다.



## 남은 문서

| 문서 | 다루는 것 |
|------|----------|
| [Go 테스트 대역 — 시간 주입·fake clientset·miniredis·kfake](./Go%20테스트%20대역%20—%20시간%20주입·fake%20clientset·miniredis·kfake.md) | 시계·K8s API·Redis·Kafka 를 테스트에서 대신하는 도구 |



## 옮겨 간 곳

- 최신값만 전달하는 채널 — 버퍼 1·drop-oldest → [01-01.최신값만 전달하는 채널·drop-oldest](../../01_language/docs/go/concurrency/01-01.최신값만%20전달하는%20채널·drop-oldest.md)
- 요청 본문 제한 — http.MaxBytesReader·MaxBytesHandler → [03-03.MaxBytesReader·MaxBytesHandler](../../01_language/docs/go/net-http/03-03.MaxBytesReader·MaxBytesHandler.md)
- 종료 신호 전파 — signal.NotifyContext·Server.BaseContext·Shutdown → [03-02.Server 타임아웃·Shutdown](../../01_language/docs/go/net-http/03-02.Server%20타임아웃·Shutdown.md)
- SSE 서버 — http.Flusher·text-event-stream·ping → [03-04.SSE·Flusher·ResponseController](../../01_language/docs/go/net-http/03-04.SSE·Flusher·ResponseController.md)
- HMAC 서명 쿠키 세션 — crypto-hmac → [03-05.Cookie·SameSite·HMAC 서명](../../01_language/docs/go/net-http/03-05.Cookie·SameSite·HMAC%20서명.md)
- franz-go — kgo·kadm·컨슈머 lag → [kgo·kadm](../../04_messaging/docs/franz-go/kgo·kadm.md)
- 멀티 플랫폼 Go 이미지 빌드 — BUILDPLATFORM·TARGETARCH → [buildx](../../07_devops/docs/cmd/image/buildx.md)
- Helm 템플릿 값 검증·차트 파일 읽기 — required·fail·Files.Get → [Helm 템플릿 값 검증](../../07_devops/docs/iac/Helm%20템플릿%20값%20검증.md)
- Helm 렌더 결과 테스트 — helm template·helm lint·helm-unittest → [Helm 렌더 테스트](../../07_devops/docs/iac/Helm%20렌더%20테스트.md)
- Helm 배포 동작 — checksum-config·resource-policy keep·reset-then-reuse-values → [Helm 릴리스 운영](../../07_devops/docs/iac/Helm%20릴리스%20운영.md) · [Helm values와 렌더 검증](../../07_devops/docs/iac/Helm%20values와%20렌더%20검증.md) · [Helm 차트 작성](../../07_devops/docs/iac/Helm%20차트%20작성.md)
- Istio 사이드카 시동 순서 — holdApplicationUntilProxyStarts → [사이드카 시동·종료 순서](../../08_cloud/docs/istio/사이드카%20시동·종료%20순서.md)
- Istio VirtualService — delegate·매치 순서·rewrite·redirect → [VirtualService 라우팅](../../08_cloud/docs/istio/VirtualService%20라우팅.md)
- kubelet 통계 API — stats-summary·nodes-stats RBAC → [자원 모니터링 파이프라인](../../08_cloud/docs/kubernetes/operations/자원%20모니터링%20파이프라인.md)
