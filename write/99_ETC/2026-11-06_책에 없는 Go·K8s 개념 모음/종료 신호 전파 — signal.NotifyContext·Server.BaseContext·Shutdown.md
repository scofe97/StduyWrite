---
title: 종료 신호 전파 — signal.NotifyContext·Server.BaseContext·Shutdown
tags: [go, net-http, graceful-shutdown, signal, context, basecontext]
status: draft
source:
  - https://pkg.go.dev/os/signal@go1.25.1#NotifyContext
  - https://pkg.go.dev/net/http@go1.25.1#Server
  - https://pkg.go.dev/net/http@go1.25.1#Server.Shutdown
  - https://pkg.go.dev/net/http@go1.25.1#Server.RegisterOnShutdown
  - https://v1-36.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination
updated: 2026-11-06
---

# 종료 신호 전파 — signal.NotifyContext·Server.BaseContext·Shutdown

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

## 종료 신호를 요청 context 까지 전달하는 방법

> SIGTERM 을 받으면 `signal.NotifyContext` 의 context 가 닫히고, `Server.BaseContext` 로 그 context 를 요청의 뿌리로 삼으면 진행 중인 요청도 종료를 알아챕니다. 이어서 기한 있는 context 로 `Shutdown` 을 부릅니다.

### 이 개념이 없으면 무엇이 깨지나

쿠버네티스는 Pod 를 내릴 때 컨테이너에 SIGTERM 을 보냅니다. 프로세스가 신호를 처리하지 않으면 바로 종료돼 처리 중이던 요청이 끊깁니다. 신호를 받아 `Shutdown` 만 부르는 구조도 완전하지 않습니다. `Shutdown` 은 활성 연결이 유휴가 될 때까지 기다리는데, SSE 처럼 끝나지 않는 핸들러가 있으면 기한이 다 될 때까지 기다리다가 오류로 돌아옵니다. 핸들러가 종료를 알아야 스스로 끝낼 수 있습니다.

### 동작 원리

`signal.NotifyContext(parent, signals...)` 는 부모 context 의 복사본을 돌려줍니다. 나열한 신호가 도착하거나 `stop` 이 불리거나 부모가 닫히면 이 context 가 닫힙니다. Go 1.16 에서 추가됐습니다. `stop` 은 신호 처리를 해제하고 자원을 놓아 주므로, 문서는 작업이 끝나면 곧바로 `stop` 을 부르라고 합니다. 신호를 한 번 받은 뒤 `stop()` 을 부르면 두 번째 신호는 기본 동작(프로세스 종료)으로 돌아가 강제 종료 탈출구가 생깁니다.

`http.Server` 의 `BaseContext` 는 요청 context 의 뿌리를 정합니다. 문서에 따르면 nil 이면 기본값이 `context.Background()` 입니다. 이 필드가 제공하는 context 에서 연결별 `ConnContext`, 요청별 `r.Context()` 가 파생됩니다. 그래서 `BaseContext` 가 신호 context 를 돌려주면 SIGTERM 한 번으로 모든 요청의 `r.Context().Done()` 이 열립니다. `ConnContext` 는 새 연결의 context 를 바꾸는 훅이라, 연결 단위 값(원격 주소 등)을 context 에 싣고 싶을 때 씁니다.

`Server.Shutdown(ctx)` 는 리스너를 닫고 유휴 연결을 닫은 뒤 활성 연결이 유휴가 되기를 무기한 기다립니다. 넘긴 context 가 먼저 끝나면 그 context 의 오류를 돌려줍니다. `Shutdown` 을 부르면 `ListenAndServe` 가 즉시 `ErrServerClosed` 를 돌려줍니다. main 은 `Shutdown` 이 돌아올 때까지 기다려야 합니다. 이 부분의 자세한 동작과 타임아웃과의 관계는 기존 문서에 정리돼 있습니다.

`Shutdown` 은 하이재킹된 연결(WebSocket 등)은 닫지도 기다리지도 않습니다. `RegisterOnShutdown(f)` 로 등록한 함수가 `Shutdown` 시점에 불리므로, 거기서 장기 연결에 종료를 알리는 일을 시작합니다. 문서는 이 함수가 종료를 시작만 하고 끝날 때까지 기다리지는 말라고 적습니다.

### 최소 예제

```go
package main

import (
	"context"
	"errors"
	"log"
	"net"
	"net/http"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	// 종료 신호가 오면 ctx 가 닫힌다.
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	mux := http.NewServeMux()
	mux.HandleFunc("GET /stream", func(w http.ResponseWriter, r *http.Request) {
		select {
		case <-r.Context().Done(): // 서버 종료나 클라이언트 끊김
			log.Println("request ctx done:", context.Cause(r.Context()))
		case <-time.After(time.Minute):
		}
	})

	srv := &http.Server{
		Addr:              ":8080",
		Handler:           mux,
		ReadHeaderTimeout: time.Minute,
		// 모든 요청 context 의 뿌리를 신호 context 로 정한다.
		BaseContext: func(net.Listener) context.Context { return ctx },
	}
	srv.RegisterOnShutdown(func() { log.Println("shutdown started") })

	go func() {
		if err := srv.ListenAndServe(); !errors.Is(err, http.ErrServerClosed) {
			log.Fatal(err)
		}
	}()

	<-ctx.Done()
	stop() // 두 번째 신호는 기본 동작(즉시 종료)으로 돌린다.

	// 종료 기한은 이미 닫힌 ctx 가 아니라 새 context 로 준다.
	sctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := srv.Shutdown(sctx); err != nil {
		log.Printf("shutdown: %v", err)
	}
}
```

이 예제는 Go 1.25.1 에서 `go vet`·`go build` 를 통과했습니다.

### 흔한 함정

- `Shutdown` 에 신호 context 를 그대로 넘기면 이미 닫혀 있어서 기다리지 않고 바로 오류로 돌아옵니다. 기한은 `context.WithTimeout(context.Background(), ...)` 같은 새 context 로 줍니다.
- `BaseContext` 에 신호 context 를 쓰면 종료 신호가 오는 순간 모든 요청의 context 가 취소됩니다. 요청을 끝까지 처리하고 싶은 일반 API 서버에서는 요청을 중간에 자릅니다. 스트림 핸들러에만 쓰거나 핸들러가 별도 종료 채널을 보게 하는 편이 낫습니다.
- `ListenAndServe` 가 돌려주는 `ErrServerClosed` 는 정상 종료의 신호입니다. 이를 오류로 처리해 `log.Fatal` 하면 종료 중에 프로세스가 비정상 종료합니다.
- 고루틴에서 `ListenAndServe` 를 돌리고 main 이 바로 끝나면 `Shutdown` 을 기다리지 못합니다.
- 쿠버네티스의 종료 유예 시간은 기본 30초이고 지나면 SIGKILL 이 갑니다. `Shutdown` 기한은 이 유예 시간보다 짧게 둡니다.

### 공식 문서 근거

| 주장 | 출처 | 문장 일부 |
|------|------|-----------|
| 신호·stop·부모 종료 중 먼저 오는 것으로 닫힘 | [os/signal NotifyContext](https://pkg.go.dev/os/signal@go1.25.1#NotifyContext) | "marked done (its Done channel is closed) when one of the listed signals arrives, when the returned stop function is called, or when the parent context's Done channel is closed, whichever happens first." |
| stop 은 곧바로 호출 | os/signal NotifyContext | "code should call stop as soon as the operations running in this Context complete and signals no longer need to be diverted to the context." |
| BaseContext 기본값 | [net/http Server](https://pkg.go.dev/net/http@go1.25.1#Server) | "If BaseContext is nil, the default is context.Background()." |
| ConnContext 는 BaseContext 에서 파생 | net/http Server | "The provided ctx is derived from the base context and has a ServerContextKey value." |
| Shutdown 은 무기한 기다리고 context 만료 시 오류 | [Server.Shutdown](https://pkg.go.dev/net/http@go1.25.1#Server.Shutdown) | "If the provided context expires before the shutdown is complete, Shutdown returns the context's error" |
| Shutdown 은 하이재킹 연결을 다루지 않음 | Server.Shutdown | "Shutdown does not attempt to close nor wait for hijacked connections such as WebSockets." |
| 쿠버네티스는 TERM 을 보냄 | [Pod lifecycle](https://v1-36.docs.kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) | "The kubelet triggers the container runtime to send a TERM signal to process 1 inside each container." |
| 유예 시간 뒤 SIGKILL | Pod lifecycle | "When the grace period expires, if there is still any container running in the Pod, the kubelet triggers forcible shutdown." |
| RegisterOnShutdown 은 시작만 하고 기다리지 않음 | [Server.RegisterOnShutdown](https://pkg.go.dev/net/http@go1.25.1#Server.RegisterOnShutdown) | "This function should start protocol-specific graceful shutdown, but should not wait for shutdown to complete." |

도입 버전은 `NotifyContext` 가 Go 1.16, `BaseContext`·`ConnContext` 가 Go 1.13 입니다. `RegisterOnShutdown` 은 Go 1.9, `Shutdown` 은 Go 1.8 입니다. Go 1.25.1 의 `api/go1.*.txt` 로 확인했습니다. Server 의 필드·메서드 문장은 pkg.go.dev 를 통째로 읽지 못했습니다. 대신 Go 1.25.1 의 `go doc` 출력으로 대조했습니다.

### 확인하지 못한 것

- `preStop` 훅과 SIGTERM 의 순서는 다루지 않았습니다.
- `WithCancelCause` 계열로 신호를 사유까지 전달하는 방법은 다루지 않았습니다.
- `context.Cause` 출력 내용은 직접 실행해 확인하지 않았습니다.



## 관련 문서

> 같은 주제의 기존 문서입니다.

- [Server 타임아웃·Shutdown](../../01_language/docs/go/net-http/03-02.Server%20타임아웃·Shutdown.md)
- [Server·ServeMux·Handler](../../01_language/docs/go/net-http/03-01.Server·ServeMux·Handler.md)
