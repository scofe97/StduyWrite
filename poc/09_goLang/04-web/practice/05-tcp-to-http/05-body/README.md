# 05. Body - 본문 파싱

## 학습 목표

- Content-Length 기반 본문 파싱
- 상태 머신을 활용한 점진적 파싱
- 스트리밍 데이터 처리

## 핵심 개념

### 본문 크기 결정

1. **Content-Length 헤더**: 정확한 바이트 수 지정
2. **Chunked Encoding**: 청크 단위 전송 (크기 미리 알 수 없음)
3. **연결 종료**: 연결이 닫힐 때까지 읽기

## 실습 과제

### Task 1: 상태 머신 구현

```go
type ParserState string

const (
    StateInit    ParserState = "init"
    StateHeaders ParserState = "headers"
    StateBody    ParserState = "body"
    StateDone    ParserState = "done"
)
```

### Task 2: Request.Parse 메서드

```go
func (r *Request) Parse(data []byte) (int, error)
```

상태에 따라:
- `StateInit`: 요청 라인 파싱
- `StateHeaders`: 헤더 파싱
- `StateBody`: 본문 파싱
- `StateDone`: 완료

### Task 3: 본문 파싱 로직

```go
func (r *Request) parseBody(data []byte) (int, error) {
    length := getContentLength(r.Headers)
    if length == 0 {
        r.state = StateDone
        return 0, nil
    }

    remaining := length - len(r.Body)
    toRead := min(remaining, len(data))
    r.Body += string(data[:toRead])

    if len(r.Body) == length {
        r.state = StateDone
    }
    return toRead, nil
}
```

## 체크리스트

- [ ] 상태 전환 로직 구현
- [ ] Content-Length 파싱
- [ ] 불완전한 본문 처리
- [ ] 본문 없는 요청 처리
