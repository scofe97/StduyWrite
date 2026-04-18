# 02. TCP Server - TCP 리스너 구현

## 학습 목표

- TCP 리스너 생성
- 연결 수락 및 처리
- 네트워크 데이터 읽기

## 핵심 개념

TCP는 연결 지향 프로토콜로:
- 3-way handshake로 연결 수립
- 순서 보장 (패킷이 순서대로 도착)
- 신뢰성 있는 전송 (ACK 확인)

## 실습 과제

### Task 1: 기본 TCP 리스너

`main.go` 파일을 작성하세요:

1. 포트 42069에서 TCP 리스너 시작
2. 연결 수락
3. 연결에서 데이터 읽기
4. 수신 데이터 출력

### 테스트 방법

```bash
# 터미널 1: 서버 실행
go run main.go

# 터미널 2: 클라이언트로 테스트
echo "Hello, TCP!" | nc localhost 42069
```

## 구현 가이드

```go
// 1. 리스너 생성
listener, err := net.Listen("tcp", ":42069")

// 2. 연결 수락 (블로킹)
conn, err := listener.Accept()

// 3. 데이터 읽기
buf := make([]byte, 1024)
n, err := conn.Read(buf)
```

## 체크리스트

- [ ] net.Listen 사용법 이해
- [ ] listener.Accept의 블로킹 동작 이해
- [ ] conn이 io.Reader를 구현함을 이해
- [ ] 리소스 정리 (defer conn.Close())
