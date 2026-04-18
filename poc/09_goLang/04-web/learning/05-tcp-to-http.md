# From TCP to HTTP: Go Network Programming

> ThePrimeagen의 강의를 기반으로 한 실습 프로젝트

## 학습 목표

1. Go의 I/O 추상화 이해 (io.Reader/io.Writer)
2. TCP 서버 구현
3. HTTP 프로토콜 파싱
4. 상태 머신 패턴 적용
5. 완전한 HTTP 서버 구현
6. Chunked Encoding 및 Trailers

## 폴더 구조

```
04-tcp-to-http/
├── 01-io-basics/           # I/O 기초 - 파일 읽기
├── 02-tcp-server/          # TCP 리스너 구현
├── 03-http-parser/         # HTTP 요청 라인 파싱
├── 04-headers/             # 헤더 파싱
├── 05-body/                # 본문 파싱 (상태 머신)
├── 06-http-server/         # 완전한 HTTP 서버
└── 07-chunked-encoding/    # 청크 인코딩 및 트레일러
```

## 진행 방법

각 폴더의 README.md를 읽고 직접 코드를 작성하세요.

## 핵심 개념

### HTTP 메시지 구조

```
Start Line      GET /path HTTP/1.1\r\n
Field Lines     Header: Value\r\n
                Header: Value\r\n
Empty Line      \r\n
Body            <message body>
```

### 상태 머신 패턴

```
init → headers → body → done
         ↓         ↓
       error ← error
```

### 청크 인코딩

```
Transfer-Encoding: chunked

20\r\n          <- 크기 (16진수)
<32 bytes>\r\n  <- 데이터
0\r\n           <- 종료
\r\n
```

## 참고 자료

- RFC 9110: HTTP Semantics
- RFC 9112: HTTP/1.1
- Go net 패키지 문서
- Go io 패키지 문서
