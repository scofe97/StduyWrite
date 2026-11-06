---
title: SSE 서버 — http.Flusher·text-event-stream·ping
tags: [go, net-http, sse, flusher, responsecontroller, streaming]
status: draft
source:
  - https://html.spec.whatwg.org/multipage/server-sent-events.html  # (2026-11-06 확인)
  - https://raw.githubusercontent.com/golang/go/go1.25.1/src/net/http/server.go
  - https://raw.githubusercontent.com/golang/go/go1.25.1/src/net/http/responsecontroller.go
  - https://pkg.go.dev/net/http@go1.25.1
  - https://nginx.org/en/docs/http/ngx_http_proxy_module.html  # (2026-11-06 확인)
updated: 2026-11-06
---

# SSE 서버 — http.Flusher·text-event-stream·ping

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

## Go 서버가 SSE 스트림을 끊김 없이 흘려보내는 방법

> Server-Sent Events(SSE)는 응답을 끝내지 않고 이벤트를 계속 흘려보내는 HTTP 응답입니다. 서버는 `text/event-stream` 형식으로 쓰고 매번 Flush 하며, 주기적으로 주석 줄을 보내 유휴 연결을 살려 둡니다.

### 이 개념이 없으면 무엇이 깨지나

대시보드에 지표를 실시간으로 밀어 주려고 일반 핸들러처럼 `fmt.Fprintf(w, ...)` 만 하면 이벤트가 브라우저에 도착하지 않습니다. `ResponseWriter` 는 쓴 데이터를 버퍼에 모아 두었다가 핸들러가 끝나거나 버퍼가 차야 내보내기 때문입니다. Flush 를 해도 중간 문제가 세 가지 더 남아 있습니다.

- 서버의 `WriteTimeout` 이 스트림 연결을 잘라 버립니다.
- 사이에 낀 프록시가 유휴 연결을 끊거나 응답을 모아서 한꺼번에 내보냅니다.
- 탭을 닫은 클라이언트 쪽 연결을 서버가 모르고 고루틴과 타이머를 계속 붙들고 있습니다.

### 동작 원리

프로토콜 규격은 WHATWG HTML 표준의 Server-sent events 절입니다. 규격이 정한 약속은 다음과 같습니다.

- MIME 타입은 `text/event-stream` 이고 UTF-8 로 인코딩합니다. 브라우저의 `EventSource` 는 응답 상태가 200 이 아니거나 Content-Type 이 이 값이 아니면 연결을 실패로 처리합니다(§9.2.2).
- 이벤트는 `필드: 값` 줄의 묶음이고, 빈 줄이 오면 그 묶음을 하나의 이벤트로 전달합니다. 그래서 이벤트 끝에는 줄바꿈이 두 번 있어야 합니다.
- 필드는 `data`(본문, 여러 줄이면 `data:` 줄을 여러 번), `event`(이벤트 이름, 생략하면 기본값 `message`), `id`(마지막 이벤트 ID), `retry`(재연결 대기 시간, 정수)입니다.
- `:` 로 시작하는 줄은 주석이라 클라이언트가 무시합니다. 규격은 이 줄을 15초 정도마다 보내 프록시가 연결을 끊지 못하게 하라고 권합니다.
- 클라이언트는 연결이 닫히면 알아서 재연결합니다. 재연결을 멈추게 하려면 서버가 HTTP 204 를 돌려줍니다.

Go 쪽에서는 `http.Flusher` 의 `Flush()` 가 버퍼를 비웁니다. Go 1.20 에서 들어온 `http.NewResponseController(w)` 는 같은 일을 `rc.Flush()` 로 하면서 오류를 돌려줍니다. 지원하지 않는 `ResponseWriter` 이면 `ErrNotSupported` 에 해당하는 오류가 나옵니다.

끊긴 클라이언트는 `r.Context().Done()` 으로 알아챕니다. 핸들러의 `select` 에 이 채널을 넣어 두면 연결이 닫힐 때 루프를 빠져나와 타이머를 정리할 수 있습니다.

`WriteTimeout` 은 서버 전체에 걸리는 값이라 핸들러가 요청별로 정할 수 없습니다. 스트림 핸들러에서는 `rc.SetWriteDeadline(time.Time{})` 로 그 연결의 쓰기 기한만 풀 수 있습니다(영값은 기한 없음). `WriteTimeout` 자체를 키우거나 끄는 방법은 서버의 다른 엔드포인트 보호까지 약하게 하므로 권하지 않습니다.

nginx 뒤에 두면 응답 버퍼링이 켜져 있어(`proxy_buffering on` 이 기본값) 이벤트가 모여서 나갑니다. 응답 헤더 `X-Accel-Buffering: no` 로 그 응답만 버퍼링을 끌 수 있습니다. `proxy_read_timeout`(기본 60초)은 서버가 그 시간 동안 아무것도 보내지 않으면 연결을 닫기 때문에 ping 간격은 이 값보다 짧게 둡니다.

### 최소 예제

```go
package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
)

func events(w http.ResponseWriter, r *http.Request) {
	rc := http.NewResponseController(w)

	// 서버 전체 WriteTimeout 이 있어도 이 연결만 쓰기 기한을 푼다.
	if err := rc.SetWriteDeadline(time.Time{}); err != nil {
		log.Printf("write deadline: %v", err)
	}

	h := w.Header()
	h.Set("Content-Type", "text/event-stream")
	h.Set("Cache-Control", "no-cache")
	h.Set("X-Accel-Buffering", "no")
	w.WriteHeader(http.StatusOK)
	if err := rc.Flush(); err != nil {
		// 200 상태 줄은 이미 나갔으므로 http.Error 로 500 을 쓸 수 없다.
		log.Printf("flush: %v", err)
		return
	}

	events := time.NewTicker(2 * time.Second)
	defer events.Stop()
	ping := time.NewTicker(15 * time.Second)
	defer ping.Stop()

	id := 0
	for {
		select {
		case <-r.Context().Done():
			return
		case <-ping.C:
			if _, err := fmt.Fprint(w, ": ping\n\n"); err != nil {
				return
			}
		case t := <-events.C:
			id++
			if _, err := fmt.Fprintf(w, "id: %d\nevent: tick\ndata: %s\n\n", id, t.Format(time.RFC3339)); err != nil {
				return
			}
		}
		if err := rc.Flush(); err != nil {
			return
		}
	}
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /events", events)
	srv := &http.Server{Addr: ":8080", Handler: mux, ReadHeaderTimeout: time.Minute, WriteTimeout: 10 * time.Second}
	log.Fatal(srv.ListenAndServe())
}
```

Go 1.20 보다 오래된 코드는 `f, ok := w.(http.Flusher)` 로 타입 단언을 하고 `f.Flush()` 를 부릅니다. 이 예제는 Go 1.25.1 에서 `go vet`·`go build` 를 통과했고, `WriteTimeout` 10초 서버에서 `curl -N` 으로 13초 동안 이벤트가 이어지는 것도 확인했습니다.

### 흔한 함정

- 이벤트 끝의 빈 줄을 빼먹으면 클라이언트가 이벤트를 전달하지 않습니다. 줄 끝은 `\n\n` 입니다.
- 헤더를 쓴 뒤에는 상태 코드를 바꿀 수 없습니다. `WriteHeader` 나 첫 `Flush` 뒤에 `http.Error` 로 500 을 써도 나가지 않고 `superfluous WriteHeader` 경고만 남습니다. 예제는 Flush 실패 시 로그만 남기고 돌아갑니다.
- Flush 를 한 번만 하고 끝내면 첫 이벤트만 도착합니다. 쓸 때마다 Flush 합니다.
- 미들웨어가 `ResponseWriter` 를 감싸면 `Flusher` 를 구현하지 않을 수 있습니다. Go 문서도 "Handlers should always test for this ability at runtime" 이라고 적고 있습니다. `ResponseController` 는 감싼 writer 가 `Unwrap() ResponseWriter` 를 제공하면 원래 writer 까지 따라갑니다.
- 클라이언트와 서버 사이에 HTTP 프록시가 있으면 Flush 해도 응답이 끝날 때까지 도착하지 않을 수 있습니다. 이 한계는 Go 문서에도 적혀 있습니다.
- `r.Context().Done()` 를 보지 않으면 클라이언트가 떠난 뒤에도 타이머가 도는 고루틴이 남습니다. 쓰기 오류(`Fprintf` 가 돌려주는 error)를 확인해 루프를 끝내는 것도 같은 목적입니다.
- 기존 문서에도 다뤘듯 `Server.WriteTimeout` 을 짧게 두면 스트림이 중간에 끊깁니다. 서버 전역 값을 올리지 말고 연결별 `SetWriteDeadline` 으로 푸는 편이 낫습니다.

### 공식 문서 근거

| 주장 | 출처 | 문장 일부 |
|------|------|-----------|
| MIME 타입은 `text/event-stream` | [WHATWG SSE §9.2.5](https://html.spec.whatwg.org/multipage/server-sent-events.html) (2026-11-06 확인) | "This event stream format's MIME type is text/event-stream." |
| 주석 줄은 무시되고 빈 줄이 이벤트를 전달 | WHATWG SSE §9.2.6 | "If the line starts with a U+003A COLON character (:)" → "Ignore the line." / "If the line is empty (a blank line)" → "Dispatch the event" |
| 프록시 끊김을 막으려면 주석 줄을 주기적으로 | WHATWG SSE §9.2.7 | "Legacy proxy servers are known to, in certain cases, drop HTTP connections after a short timeout." |
| Flusher 는 런타임에 확인, 프록시 뒤에서는 지연 가능 | [server.go (go1.25.1)](https://github.com/golang/go/blob/go1.25.1/src/net/http/server.go) | "Handlers should always test for this ability at runtime." |
| WriteTimeout 은 서버 전역 | server.go (go1.25.1) | "Like ReadTimeout, it does not let Handlers make decisions on a per-request basis." |
| 영값 쓰기 기한은 기한 없음 | [responsecontroller.go (go1.25.1)](https://github.com/golang/go/blob/go1.25.1/src/net/http/responsecontroller.go) | "A zero value means no deadline." |
| nginx 응답 버퍼링을 헤더로 끔 | [nginx proxy 모듈](https://nginx.org/en/docs/http/ngx_http_proxy_module.html) (2026-11-06 확인) | "Buffering can also be enabled or disabled by passing "yes" or "no" in the "X-Accel-Buffering" response header field." |
| nginx 읽기 타임아웃 기본 60초 | nginx proxy 모듈 | "If the proxied server does not transmit anything within this time, the connection is closed." |

`NewResponseController` 는 Go 1.20 에서 추가됐습니다(Go 1.25.1 `api/go1.20.txt` 확인).

### 확인하지 못한 것

- `http.ResponseController` 의 Go 1.20 도입 문구는 소스 주석에 없어 `api/go1.20.txt` 로 갈음했습니다.
- `WriteTimeout` 없이 같은 코드가 끊기지 않는지의 대조 실험은 하지 않았습니다.



## 관련 문서

> 같은 주제의 기존 문서입니다.

- [Server 타임아웃·Shutdown](../../01_language/docs/go/net-http/03-02.Server%20타임아웃·Shutdown.md)
- [Server·ServeMux·Handler](../../01_language/docs/go/net-http/03-01.Server·ServeMux·Handler.md)
- [Go HTTP 서버는 타임아웃을 정하고 핸들러에 의존성을 주입하며 httptest 로 시험한다](../../02_os/book/npg_network-programming-with-go/09-01.Go%20HTTP%20서버는%20타임아웃을%20정하고%20핸들러에%20의존성을%20주입하며%20httptest%20로%20시험한다.md)
