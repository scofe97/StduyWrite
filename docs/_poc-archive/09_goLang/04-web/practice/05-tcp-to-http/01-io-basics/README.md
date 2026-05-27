# 01. I/O Basics - 파일 읽기

## 학습 목표

- Go의 `io.Reader` 인터페이스 이해
- 바이트 단위 파일 읽기
- 버퍼 크기에 따른 읽기 동작 이해

## 핵심 개념

Go에서 파일과 네트워크 연결은 동일한 인터페이스(`io.Reader`)를 사용합니다.

```go
type Reader interface {
    Read(p []byte) (n int, err error)
}
```

## 실습 과제

### Task 1: 8바이트씩 파일 읽기

`main.go` 파일을 작성하세요:

1. `messages.txt` 파일 생성 (내용: "Hello, World! This is a test.")
2. 8바이트 버퍼로 파일 읽기
3. 각 읽기 결과 출력

### 예상 출력

```
Read 8 bytes: Hello, W
Read 8 bytes: orld! Th
Read 8 bytes: is is a
Read 6 bytes: test.
EOF reached
```

## 힌트

```go
f, err := os.Open("messages.txt")
defer f.Close()

buf := make([]byte, 8)
for {
    n, err := f.Read(buf)
    if err == io.EOF {
        break
    }
    // 읽은 데이터 처리
}
```

## 체크리스트

- [ ] 파일 열기/닫기 이해
- [ ] Read 메서드 반환값 이해 (n, error)
- [ ] io.EOF 처리
- [ ] 버퍼 슬라이싱 (`buf[:n]`)
