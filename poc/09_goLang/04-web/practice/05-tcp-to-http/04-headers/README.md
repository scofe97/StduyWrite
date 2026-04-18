# 04. Headers - 헤더 파싱

## 학습 목표

- HTTP 헤더(Field Lines) 구조 이해
- 대소문자 무시(Case-Insensitive) 처리
- 중복 헤더 처리

## 핵심 개념

### 헤더 형식 (RFC 9110)

```
Field-Line = Field-Name ":" OWS Field-Value OWS CRLF
```

- OWS = Optional White Space (선택적 공백)
- 필드 이름과 콜론 사이에는 공백 불가
- 필드 값 앞뒤의 공백은 무시

### 예시

```
Host: localhost:42069\r\n
Content-Type: text/plain\r\n
Content-Length: 13\r\n
\r\n                        <- 빈 줄 = 헤더 종료
```

## 실습 과제

### Task 1: Headers 구조체

```go
type Headers struct {
    headers map[string]string
}

func NewHeaders() *Headers
func (h *Headers) Get(name string) (string, bool)
func (h *Headers) Set(name, value string)
```

### Task 2: 헤더 파싱 함수

```go
func (h *Headers) Parse(data []byte) (n int, done bool, err error)
```

- `n`: 소비한 바이트 수
- `done`: 빈 줄을 만나면 true
- `err`: 파싱 오류

## 주의사항

1. **대소문자 무시**: `Content-Type`과 `content-type`은 동일
2. **필드 값 트림**: 앞뒤 공백 제거
3. **중복 헤더**: 콤마로 연결 (`a, b`)
4. **유효한 토큰**: 필드 이름은 특정 문자만 허용

## 체크리스트

- [ ] 대소문자 무시 구현
- [ ] 값 앞뒤 공백 트림
- [ ] 빈 줄 감지 (헤더 종료)
- [ ] 중복 헤더 처리
