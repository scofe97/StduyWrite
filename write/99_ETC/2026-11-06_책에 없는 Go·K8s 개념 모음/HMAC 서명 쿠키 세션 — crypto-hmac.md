---
title: HMAC 서명 쿠키 세션 — crypto-hmac
tags: [go, crypto-hmac, cookie, session, net-http, security]
status: draft
source:
  - https://pkg.go.dev/crypto/hmac@go1.25.1
  - https://pkg.go.dev/net/http@go1.25.1#Cookie
  - https://pkg.go.dev/net/http@go1.25.1#SameSite
  - https://raw.githubusercontent.com/golang/go/go1.25.1/src/net/http/cookie.go
updated: 2026-11-06
---

# HMAC 서명 쿠키 세션 — crypto-hmac

---

> 임시 참고 문서입니다. 정본은 나중에 따로 만듭니다.

## 서버 저장소 없이 쿠키의 변조를 막는 방법

> 쿠키 값에 HMAC 서명을 붙이면 서버가 세션을 저장하지 않아도 클라이언트가 값을 바꿨는지 알 수 있습니다. 서명은 암호화가 아니므로 비밀 정보는 담지 않습니다.

### 이 개념이 없으면 무엇이 깨지나

쿠키는 클라이언트가 마음대로 고칠 수 있습니다. `user=alice` 를 그대로 믿으면 `user=admin` 으로 바꾼 쿠키가 통과합니다. 세션 ID 를 서버 저장소에 두면 해결되지만 저장소를 운영해야 합니다. HMAC 은 비밀 키를 가진 서버만 만들 수 있는 서명을 값에 붙이는 방식이라 저장소 없이 변조를 가려냅니다.

### 동작 원리

HMAC(Keyed-Hash Message Authentication Code)은 키를 쓰는 해시입니다. Go 문서는 "An HMAC is a cryptographic hash that uses a key to sign a message." 라고 설명합니다. `hmac.New(sha256.New, key)` 가 해시 객체를 만듭니다. `Write` 로 메시지를 넣고 `Sum(nil)` 로 서명(MAC)을 얻습니다. 해시 생성 함수는 호출할 때마다 새 `Hash` 를 돌려줘야 합니다.

쿠키 값은 `메시지.서명` 꼴로 만듭니다. 메시지에는 사용자 식별자와 만료 시각을 넣습니다. 만료 시각을 서명 대상에 포함해야 클라이언트가 만료 시각만 늘리는 변조를 막을 수 있습니다. 서버는 쿠키를 받으면 같은 키로 서명을 다시 계산해 비교합니다. 일치하고 만료 전이면 메시지를 믿습니다.

서명 비교에는 `hmac.Equal` 을 씁니다. 문서는 `Equal` 이 타이밍 정보를 흘리지 않고 MAC 을 비교한다고 설명합니다. 수신자는 타이밍 부채널(timing side-channel)을 피하려고 `Equal` 로 비교하라고도 안내합니다. 일반 비교는 처음 다른 바이트에서 멈출 수 있어 응답 시간 차이가 단서가 됩니다. 이 마지막 설명은 문서 문장이 아니라 일반적인 이유입니다.

쿠키 속성은 `http.Cookie` 구조체의 필드로 정합니다. `HttpOnly`, `Secure`, `SameSite`, `Expires`, `MaxAge`, `Path`, `Domain` 이 있습니다.

- `SameSite` 는 브라우저가 이 쿠키를 교차 사이트 요청에 실어 보내지 못하게 하는 속성입니다.
- 문서는 교차 출처 정보 유출 위험을 줄이고 CSRF 에 일부 보호를 준다고 설명합니다.
- 상수는 `SameSiteLaxMode`, `SameSiteStrictMode`, `SameSiteNoneMode` 입니다.
- `MaxAge` 는 0 이면 속성 없음, 0 보다 작으면 쿠키를 지금 삭제, 0 보다 크면 초 단위 수명입니다.

서명은 암호화가 아닙니다. 서명은 값이 바뀌지 않았음을 보장할 뿐 내용을 숨기지 않습니다. 아래 예제가 만든 쿠키의 앞부분은 base64 만 풀면 `사용자|만료시각` 평문이 그대로 나옵니다.

키 교체는 서명을 새 키로 만들되 검증은 현재 키와 이전 키를 모두 시도하는 방식으로 합니다. 이 부분은 Go 문서에 나오는 내용이 아니라 일반적인 설계 방식이어서 정본을 만들 때 별도 근거를 붙입니다.

### 최소 예제

```go
package main

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"
)

var key = []byte("replace-with-32-random-bytes-from-env") // 실제로는 환경변수·시크릿에서 읽는다

func sign(user string, exp time.Time) string {
	msg := user + "|" + strconv.FormatInt(exp.Unix(), 10)
	mac := hmac.New(sha256.New, key)
	mac.Write([]byte(msg))
	sig := base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
	return base64.RawURLEncoding.EncodeToString([]byte(msg)) + "." + sig
}

func verify(value string, now time.Time) (string, error) {
	msgB64, sigB64, ok := strings.Cut(value, ".")
	if !ok {
		return "", errors.New("malformed")
	}
	msg, err := base64.RawURLEncoding.DecodeString(msgB64)
	if err != nil {
		return "", errors.New("malformed")
	}
	got, err := base64.RawURLEncoding.DecodeString(sigB64)
	if err != nil {
		return "", errors.New("malformed")
	}
	mac := hmac.New(sha256.New, key)
	mac.Write(msg)
	if !hmac.Equal(got, mac.Sum(nil)) {
		return "", errors.New("bad signature")
	}
	user, expStr, ok := strings.Cut(string(msg), "|")
	if !ok {
		return "", errors.New("malformed")
	}
	exp, err := strconv.ParseInt(expStr, 10, 64)
	if err != nil || now.Unix() > exp {
		return "", errors.New("expired")
	}
	return user, nil
}

func login(w http.ResponseWriter, r *http.Request) {
	exp := time.Now().Add(time.Hour)
	http.SetCookie(w, &http.Cookie{
		Name:     "session",
		Value:    sign("alice", exp),
		Path:     "/",
		Expires:  exp,
		HttpOnly: true,
		Secure:   true,
		SameSite: http.SameSiteLaxMode,
	})
}

func me(w http.ResponseWriter, r *http.Request) {
	c, err := r.Cookie("session")
	if err != nil {
		http.Error(w, "no session", http.StatusUnauthorized)
		return
	}
	user, err := verify(c.Value, time.Now())
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnauthorized)
		return
	}
	fmt.Fprintln(w, user)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("POST /login", login)
	mux.HandleFunc("GET /me", me)
	log.Fatal(http.ListenAndServe(":8080", mux))
}
```

이 예제는 Go 1.25.1 에서 `go vet`·`go build` 를 통과했습니다. 로컬에서 로그인으로 받은 쿠키는 `/me` 가 `alice` 로 인정했고, 메시지를 `bob` 으로 바꾼 쿠키는 `bad signature` 로 거절했습니다.

### 흔한 함정

- 서명 비교를 `==` 로 하면 타이밍 부채널이 열립니다. `hmac.Equal` 을 씁니다.
- 만료 시각을 서명 밖에 두면 클라이언트가 늘려 쓸 수 있습니다. 서명 대상 메시지에 포함합니다.
- 서명만 있다고 비밀이 지켜지지 않습니다. 비밀번호나 개인정보를 쿠키에 담지 않습니다.
- 키를 소스에 적지 않습니다. 환경변수나 시크릿 저장소에서 읽습니다.
- 서버가 세션을 저장하지 않으니 이미 발급한 쿠키를 만료 전에 무효로 만들 방법이 없습니다. 로그아웃은 쿠키를 지울 뿐이고, 탈취된 쿠키를 막으려면 키를 바꾸거나 서버 쪽 폐기 목록이 필요합니다.
- 구분자(`|`)가 사용자 값에 들어 있으면 파싱이 어긋납니다. 사용자 값을 검증하거나 길이를 접두하는 방식으로 구분합니다.
- `HttpOnly`·`Secure` 가 실제로 하는 일은 net/http 문서에 설명이 없습니다. 필드가 있다는 사실만 확인했습니다.

### 공식 문서 근거

| 주장 | 출처 | 문장 일부 |
|------|------|-----------|
| HMAC 은 키로 메시지에 서명 | [crypto/hmac](https://pkg.go.dev/crypto/hmac@go1.25.1) | "An HMAC is a cryptographic hash that uses a key to sign a message." |
| 비교는 Equal 로 | crypto/hmac | "Receivers should be careful to use Equal to compare MACs in order to avoid timing side-channels" |
| Equal 은 타이밍을 흘리지 않음 | crypto/hmac Equal | "Equal compares two MACs for equality without leaking timing information." |
| New 에 sha256.New 를 쓸 수 있음 | crypto/hmac New | "New functions like crypto/sha256.New can be used as h. h must return a new Hash every time it is called." |
| SameSite 의 목적 | [net/http SameSite](https://pkg.go.dev/net/http@go1.25.1#SameSite) | "SameSite allows a server to define a cookie attribute making it impossible for the browser to send this cookie along with cross-site requests." |
| Cookie 는 Set-Cookie 헤더의 쿠키 | [net/http Cookie](https://pkg.go.dev/net/http@go1.25.1#Cookie) | "A Cookie represents an HTTP cookie as sent in the Set-Cookie header of an HTTP response" |
| MaxAge 의미 | [cookie.go (go1.25.1)](https://github.com/golang/go/blob/go1.25.1/src/net/http/cookie.go) | "MaxAge<0 means delete cookie now, equivalently 'Max-Age: 0'" |

`SameSite` 는 Go 1.11 에서 추가됐습니다. 문서는 IETF 초안 draft-ietf-httpbis-cookie-same-site-00 을 참조합니다. `hmac.Equal` 문서에는 "constant time" 이라는 표현이 없어 이 문서도 쓰지 않았습니다.

### 확인하지 못한 것

- `HttpOnly`·`Secure` 의 브라우저 동작은 net/http 문서에 설명이 없어 근거로 쓰지 못했습니다. 정본에서는 별도 문서로 확인합니다.
- 키 교체 방식은 일반 설계이며 공식 문서 근거가 없습니다.
- 구분자 충돌 방지 방식은 설계 의견이며 실행해 확인하지 않았습니다.
- 로그아웃 후 쿠키 재사용 가능성은 설명만 했고 실험하지 않았습니다.



## 관련 문서

> 같은 주제의 기존 문서입니다. 이 주제를 직접 다룬 기존 문서는 찾지 못해 net/http 서버 문서를 걸었습니다.

- [Server·ServeMux·Handler](../../01_language/docs/go/net-http/03-01.Server·ServeMux·Handler.md)
