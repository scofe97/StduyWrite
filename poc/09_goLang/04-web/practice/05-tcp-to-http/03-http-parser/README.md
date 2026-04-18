# 03. HTTP Parser - 요청 라인 파싱

## 학습 목표

- HTTP 요청 메시지 구조 이해
- 요청 라인(Request Line) 파싱
- 상태 머신 패턴 적용

## 핵심 개념

### HTTP 요청 구조

```
Request Line    GET /coffee HTTP/1.1\r\n
Headers         Host: localhost\r\n
                Content-Type: text/plain\r\n
Empty Line      \r\n
Body            {"coffee": "americano"}
```

### CRLF

`\r\n` (Carriage Return + Line Feed)은 HTTP의 줄 구분자입니다.
- 암기 팁: "Registered Nurse" (RN)

## 실습 과제

### Task 1: Request 구조체 정의

```go
type RequestLine struct {
    Method        string
    RequestTarget string
    HttpVersion   string
}

type Request struct {
    RequestLine RequestLine
}
```

### Task 2: 요청 라인 파싱 함수

`parseRequestLine` 함수를 구현하세요:

입력: `GET /coffee HTTP/1.1\r\n...`
출력: `RequestLine{Method: "GET", RequestTarget: "/coffee", HttpVersion: "1.1"}`

## 구현 힌트

```go
// CRLF로 첫 번째 줄 찾기
idx := bytes.Index(data, []byte("\r\n"))
if idx == -1 {
    return nil, 0, nil  // 아직 완전한 줄이 없음
}

// 공백으로 분리
parts := bytes.Split(data[:idx], []byte(" "))
// parts[0]: Method, parts[1]: Target, parts[2]: HTTP/1.1
```

## 체크리스트

- [ ] CRLF 위치 찾기
- [ ] 공백으로 3개 부분 분리
- [ ] HTTP 버전 검증 (HTTP/1.1만 지원)
- [ ] 읽은 바이트 수 반환
