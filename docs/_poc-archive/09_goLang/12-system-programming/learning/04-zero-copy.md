# 04 - Zero-Copy

불필요한 메모리 복사를 제거하는 기술을 배웁니다. 전통적인 read/write와 sendfile의 차이를 체험하고, Go가 내부적으로 어떻게 최적화하는지 이해합니다.

## 소크라테스 질문

실습을 시작하기 전에 다음 질문들을 생각해보세요.

### 질문 1: 파일을 소켓으로 보낼 때 왜 두 번 복사가 필요한가?

> **힌트**: read()와 write()의 동작을 생각해보세요.
>
> 생각해볼 점:
> - read()는 데이터를 어디에 저장하나요?
> - write()는 데이터를 어디서 가져오나요?
> - 커널 버퍼와 유저 버퍼의 경계는 어디인가요?

### 질문 2: sendfile은 어떻게 복사를 줄이는가?

> **힌트**: 데이터가 유저 공간을 거치지 않는다면?
>
> 생각해볼 점:
> - sendfile의 시그니처: `sendfile(out_fd, in_fd, offset, count)`
> - 유저 버퍼가 없다는 것의 의미는?
> - 커널 내에서 직접 전송하면 어떤 이점이?

### 질문 3: io.Copy(conn, file)은 sendfile을 사용할까?

> **힌트**: Go는 내부적으로 최적화를 수행합니다.
>
> 생각해볼 점:
> - io.Copy의 소스 코드를 보면?
> - net.TCPConn.ReadFrom() 메서드는?
> - strace로 확인할 수 있을까요?

## 참고 문서

- [04_System_Calls.md](../../docs/04_System_Calls.md) - sendfile 시스템 콜
- [05_Go_System_Integration.md](../../docs/05_Go_System_Integration.md) - Go의 최적화

## 실습 단계

### Step 1: 전통적인 read + write

**목표**: 표준 방식의 파일 전송과 복사 횟수 이해

**위치**: `step1_traditional/main.go`

**핵심 개념**:
- read(): 커널 버퍼 → 유저 버퍼 (1회 복사)
- write(): 유저 버퍼 → 커널 버퍼 (1회 복사)
- 총 4회 복사 (DMA 포함)

**검증 방법**:
```bash
# 테스트 파일 생성
dd if=/dev/urandom of=/tmp/testfile bs=1M count=100

# 서버 실행
go run main.go server

# 클라이언트 실행 (다른 터미널)
go run main.go client

# strace로 확인
strace -e read,write,sendfile go run main.go server
```

---

### Step 2: sendfile 시스템 콜

**목표**: sendfile로 복사 횟수 줄이기

**위치**: `step2_sendfile/main.go`

**핵심 개념**:
- sendfile(): 커널 내 직접 전송
- 유저 공간 복사 제거
- 2회 복사로 감소 (DMA만)

**검증 방법**:
```bash
# strace로 sendfile 확인
strace -e sendfile,read,write go run main.go

# 시간 측정
time go run main.go
```

---

### Step 3: Go io.Copy의 내부 동작

**목표**: Go가 자동으로 sendfile을 사용하는지 확인

**위치**: `step3_io_copy/main.go`

**핵심 개념**:
- io.Copy()는 ReaderFrom 인터페이스 확인
- net.TCPConn은 ReadFrom()에서 sendfile 사용
- 투명한 최적화

**검증 방법**:
```bash
# io.Copy vs sendfile 비교
strace -e sendfile,read,write go run main.go iocopy
strace -e sendfile,read,write go run main.go manual
```

## 완료 체크리스트

- [ ] Step 1: read + write로 파일 전송 구현
- [ ] Step 1: strace에서 read, write 시스템 콜 확인
- [ ] Step 2: sendfile로 파일 전송 구현
- [ ] Step 2: strace에서 sendfile 시스템 콜 확인
- [ ] Step 3: io.Copy가 sendfile을 사용하는지 확인
- [ ] Step 3: 성능 차이 측정
- [ ] 소크라테스 질문 3개 모두 답변 가능

## 핵심 인사이트

(실습 완료 후 작성하세요)

1. Zero-copy의 핵심은...
2. sendfile의 제약 사항은...
3. Go의 투명한 최적화란...
