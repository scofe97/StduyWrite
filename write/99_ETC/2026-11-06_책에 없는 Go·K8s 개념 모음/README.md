---
title: 책에 없는 Go·K8s 개념 모음
tags: [go, kubernetes, helm, istio, index]
status: draft
updated: 2026-11-06
---

# 책에 없는 Go·K8s 개념 모음

> 정독한 책(Network Programming with Go 등)이 다루지 않았지만 실무 코드에서 자주 만나는 개념을 한 편씩 정리해 둔 임시 참고 문서입니다. 정본 문서는 나중에 각 카테고리에 따로 만들고, 이 폴더는 그때 재료로 씁니다.



## 이 폴더를 읽는 법

이 폴더의 문서 14편은 모두 `status: draft` 인 임시 문서입니다. 번호를 붙이지 않았고, 서로 가까운 개념은 한 편으로 묶었습니다. 정본을 만들 때는 해당 편을 열어 출처와 예제를 그대로 가져가면 됩니다.

인용문은 2026-11-06 에 원문과 대조했습니다. 공식 문서와 소스를 `curl`·`go doc` 로 받아 159건을 맞춰 봤고, 어긋난 서술 1건(miniredis 의 `CLUSTER` 지원 범위)은 고쳤습니다.

출처 주소는 가능한 곳마다 버전이나 커밋을 고정했습니다. 고정 주소가 없는 페이지(Go 명세, Dockerfile reference, WHATWG, nginx 등)에는 `(2026-11-06 확인)` 을 붙였습니다. Go 예제는 go1.25.1 에서 `go vet`·빌드를 통과했지만, Kubernetes·Istio 내용은 클러스터에서 직접 돌려 보지 않았습니다.



## Go net/http

| 문서 | 다루는 것 |
|------|----------|
| [SSE 서버 — http.Flusher·text-event-stream·ping](./SSE%20서버%20—%20http.Flusher·text-event-stream·ping.md) | 연결을 열어 둔 채 이벤트를 밀어 보내는 서버, 프록시 버퍼링과 ping |
| [종료 신호 전파 — signal.NotifyContext·Server.BaseContext·Shutdown](./종료%20신호%20전파%20—%20signal.NotifyContext·Server.BaseContext·Shutdown.md) | 신호를 context 로 바꿔 서버 종료까지 잇는 법, BaseContext 함정 |
| [요청 본문 제한 — http.MaxBytesReader·MaxBytesHandler](./요청%20본문%20제한%20—%20http.MaxBytesReader·MaxBytesHandler.md) | 큰 요청 본문을 읽기 전에 끊는 법 |
| [HMAC 서명 쿠키 세션 — crypto-hmac](./HMAC%20서명%20쿠키%20세션%20—%20crypto-hmac.md) | 서버 저장소 없이 쿠키 변조를 막는 서명 세션 |



## Go 기타

| 문서 | 다루는 것 |
|------|----------|
| [최신값만 전달하는 채널 — 버퍼 1·drop-oldest](./최신값만%20전달하는%20채널%20—%20버퍼%201·drop-oldest.md) | 느린 소비자에게 가장 최근 값 하나만 넘기는 채널 패턴 |
| [Go 테스트 대역 — 시간 주입·fake clientset·miniredis·kfake](./Go%20테스트%20대역%20—%20시간%20주입·fake%20clientset·miniredis·kfake.md) | 시계·K8s API·Redis·Kafka 를 테스트에서 대신하는 도구 |
| [franz-go — kgo·kadm·컨슈머 lag](./franz-go%20—%20kgo·kadm·컨슈머%20lag.md) | Go Kafka 클라이언트의 소비 루프와 lag 계산 |
| [멀티 플랫폼 Go 이미지 빌드 — BUILDPLATFORM·TARGETARCH](./멀티%20플랫폼%20Go%20이미지%20빌드%20—%20BUILDPLATFORM·TARGETARCH.md) | amd64·arm64 이미지를 교차 컴파일로 한 번에 만드는 법 |



## Helm

| 문서 | 다루는 것 |
|------|----------|
| [Helm 템플릿 값 검증·차트 파일 읽기 — required·fail·Files.Get](./Helm%20템플릿%20값%20검증·차트%20파일%20읽기%20—%20required·fail·Files.Get.md) | 잘못된 values 를 렌더 단계에서 막는 법, 차트 안 파일 읽기 |
| [Helm 배포 동작 — checksum-config·resource-policy keep·reset-then-reuse-values](./Helm%20배포%20동작%20—%20checksum-config·resource-policy%20keep·reset-then-reuse-values.md) | 설정 변경 시 재시작, 삭제에서 리소스 지키기, upgrade 때 values 병합 |
| [Helm 렌더 결과 테스트 — helm template·helm lint·helm-unittest](./Helm%20렌더%20결과%20테스트%20—%20helm%20template·helm%20lint·helm-unittest.md) | 차트 렌더 결과를 시험하는 세 도구, lint 가 못 잡는 것 |



## Kubernetes·Istio

| 문서 | 다루는 것 |
|------|----------|
| [kubelet 통계 API — stats-summary·nodes-stats RBAC](./kubelet%20통계%20API%20—%20stats-summary·nodes-stats%20RBAC.md) | 노드·파드 자원 사용량을 kubelet 에서 직접 읽는 법과 권한 |
| [Istio VirtualService — delegate·매치 순서·rewrite·redirect](./Istio%20VirtualService%20—%20delegate·매치%20순서·rewrite·redirect.md) | 라우팅 규칙 위임, 규칙 평가 순서, 경로 바꾸기와 리다이렉트 |
| [Istio 사이드카 시동 순서 — holdApplicationUntilProxyStarts](./Istio%20사이드카%20시동%20순서%20—%20holdApplicationUntilProxyStarts.md) | 앱이 프록시보다 먼저 떠서 생기는 연결 실패와 그 해결 |
