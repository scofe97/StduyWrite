---
title: 요청 본문 제한 — http.MaxBytesReader·MaxBytesHandler
tags: [go, net-http, maxbytesreader, request-body, security]
status: draft
source:
  - https://pkg.go.dev/net/http@go1.25.1#MaxBytesReader
  - https://pkg.go.dev/net/http@go1.25.1#MaxBytesHandler
  - https://pkg.go.dev/net/http@go1.25.1#MaxBytesError
  - https://raw.githubusercontent.com/golang/go/go1.25.1/src/io/io.go
updated: 2026-11-06
---

# 요청 본문 제한 — http.MaxBytesReader·MaxBytesHandler

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

## 요청 본문 크기를 제한하는 방법

> `http.MaxBytesReader` 는 요청 본문을 읽을 수 있는 최대 바이트 수를 정하고, 넘으면 `*http.MaxBytesError` 를 돌려줍니다. 경로 전체에 같은 한도를 씌울 때는 `http.MaxBytesHandler` 를 씁니다.

### 이 개념이 없으면 무엇이 깨지나

`json.NewDecoder(r.Body).Decode(&v)` 나 `io.ReadAll(r.Body)` 는 클라이언트가 보내는 만큼 읽습니다. 수 기가바이트 본문을 보내는 요청 하나로 서버 메모리가 바닥나거나, 느린 대용량 전송이 연결과 고루틴을 오래 붙잡습니다. 악의가 없어도 잘못된 클라이언트의 버그로 같은 일이 생깁니다. 본문 크기는 서버가 정해야 합니다.

### 동작 원리

`http.MaxBytesReader(w, r.Body, n)` 는 `r.Body` 를 감싼 `io.ReadCloser` 를 돌려줍니다. 누적으로 n 바이트를 넘겨 읽으려 하면 `Read` 가 `*http.MaxBytesError`(필드 `Limit`)를 돌려줍니다. `MaxBytesError` 는 Go 1.19 에서 들어왔습니다. 그 전에는 오류 메시지 문자열로만 구분할 수 있었습니다. 요청 핸들러에서는 `errors.As(err, &mbe)` 로 판별해 413 을 돌려줍니다.

`io.LimitReader` 와는 세 가지가 다릅니다.

- `LimitReader` 는 n 바이트에서 조용히 EOF 를 돌려줍니다. 잘린 본문이 정상 입력처럼 보입니다.
- `MaxBytesReader` 는 한도를 넘으면 오류를 돌려줍니다.
- `MaxBytesReader` 는 `ReadCloser` 라서 `Close` 가 원래 본문을 닫습니다.

가능하면 `ResponseWriter` 에게 한도 초과 뒤 연결을 닫도록 알리는 점도 다릅니다. 그래서 요청 본문에는 `MaxBytesReader` 를 씁니다.

`http.MaxBytesHandler(h, n)` 는 핸들러 `h` 를 실행하면서 `ResponseWriter` 와 `Request.Body` 를 감쌉니다. 감싼 아래의 핸들러는 모두 같은 한도를 받습니다. Go 1.18 에서 추가됐습니다.

JSON 과 함께 쓸 때는 `r.Body = http.MaxBytesReader(w, r.Body, limit)` 로 바꾼 뒤 디코더를 만듭니다. 디코더가 한도에서 읽기를 멈추면 디코더가 `*MaxBytesError` 를 그대로 돌려주므로 `errors.As` 로 잡을 수 있습니다.

### 최소 예제

```go
package main

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"
)

type payload struct {
	Name string `json:"name"`
}

func create(w http.ResponseWriter, r *http.Request) {
	r.Body = http.MaxBytesReader(w, r.Body, 1<<20) // 1 MiB

	var p payload
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		var mbe *http.MaxBytesError
		if errors.As(err, &mbe) {
			http.Error(w, "body too large", http.StatusRequestEntityTooLarge)
			return
		}
		http.Error(w, "bad json", http.StatusBadRequest)
		return
	}
	w.WriteHeader(http.StatusCreated)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /items", create)
	// 경로 전체에 같은 한도를 씌우는 방법
	mux.Handle("POST /bulk", http.MaxBytesHandler(http.HandlerFunc(create), 8<<20))
	log.Fatal(http.ListenAndServe(":8080", mux))
}
```

이 예제는 Go 1.25.1 에서 `go vet`·`go build` 를 통과했습니다. 로컬에서 2MB 본문은 413, 작은 JSON 은 201 로 응답하는 것을 `curl` 로 확인했습니다.

### 흔한 함정

- `ReadAll` 이나 디코더를 만들기 전에 `MaxBytesReader` 로 바꾸지 않으면 한도가 적용되지 않습니다. 본문 읽기보다 먼저 적용합니다.
- 한도를 `MaxBytesHandler` 와 핸들러 안의 `MaxBytesReader` 두 곳에 쓰면 어느 값이 적용되는지 헷갈립니다. 한 곳에서만 정합니다.
- 오류를 문자열로 비교하지 말고 `errors.As` 로 `*http.MaxBytesError` 를 판별합니다.
- 413 은 핸들러가 직접 써야 합니다. `MaxBytesReader` 는 오류만 돌려줍니다.
- `MaxBytesReader` 의 `Read` 는 읽은 바이트 수만 세므로 `Content-Length` 가 큰 요청도 본문을 읽기 시작해야 오류가 납니다(Go 1.25.1 `request.go` 확인).

### 공식 문서 근거

| 주장 | 출처 | 문장 일부 |
|------|------|-----------|
| 본문 크기 제한 목적 | [MaxBytesReader](https://pkg.go.dev/net/http@go1.25.1#MaxBytesReader) | "MaxBytesReader prevents clients from accidentally or maliciously sending a large request and wasting server resources." |
| LimitReader 와의 차이 | MaxBytesReader | "In contrast to io.LimitReader, MaxBytesReader's result is a ReadCloser, returns a non-nil error of type *MaxBytesError for a Read beyond the limit, and closes the underlying reader when its Close method is called." |
| 연결 닫기 | MaxBytesReader | "If possible, it tells the ResponseWriter to close the connection after the limit has been reached." |
| LimitReader 는 EOF | [io.LimitReader](https://raw.githubusercontent.com/golang/go/go1.25.1/src/io/io.go) | "LimitReader returns a Reader that reads from r but stops with EOF after n bytes." |
| MaxBytesHandler 는 Body 를 감쌈 | [MaxBytesHandler](https://pkg.go.dev/net/http@go1.25.1#MaxBytesHandler) | "MaxBytesHandler returns a Handler that runs h with its ResponseWriter and [Request.Body] wrapped by a MaxBytesReader." |
| 오류 타입 | [MaxBytesError](https://pkg.go.dev/net/http@go1.25.1#MaxBytesError) | "MaxBytesError is returned by MaxBytesReader when its read limit is exceeded." |

`MaxBytesHandler` 는 Go 1.18, `MaxBytesError` 는 Go 1.19 에서 추가됐습니다. Go 1.25.1 의 `api/go1.*.txt` 로 확인했습니다. `MaxBytesReader` 문장은 pkg.go.dev 와 `go doc` 출력에서 함께 확인했습니다.

### 확인하지 못한 것

- `encoding/json` 디코더가 `*MaxBytesError` 를 어떻게 돌려주는지는 소스를 읽지 않았습니다. `errors.As` 로 413 이 나가는 것을 `curl` 로 확인했을 뿐입니다.
- 한도를 넘은 뒤 실제로 연결이 닫히는지는 확인하지 않았습니다.
- `MaxBytesHandler` 와 `MaxBytesReader` 를 겹쳐 쓴 동작은 실행하지 않았습니다.



## 관련 문서

> 같은 주제의 기존 문서입니다.

- [Server·ServeMux·Handler](../../01_language/docs/go/net-http/03-01.Server·ServeMux·Handler.md)
- [Server 타임아웃·Shutdown](../../01_language/docs/go/net-http/03-02.Server%20타임아웃·Shutdown.md)
