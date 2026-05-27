# 01 - System Call Basics

시스템 콜의 기초를 배웁니다. 파일을 열고 읽는 것이 실제로 어떻게 동작하는지 체험합니다.

## 소크라테스 질문

실습을 시작하기 전에 다음 질문들을 생각해보세요.

### 질문 1: 시스템 콜 없이 파일을 읽을 수 있을까?

> **힌트**: 프로그램이 디스크에 직접 접근할 수 있을까요?
>
> 생각해볼 점:
> - 사용자 프로그램과 하드웨어 사이에는 무엇이 있나요?
> - 왜 운영체제가 중간에 개입해야 할까요?
> - 만약 모든 프로그램이 디스크에 직접 접근한다면 어떤 문제가 생길까요?

### 질문 2: fd가 단순한 숫자인 이유는?

> **힌트**: 파일을 열면 왜 3, 4, 5 같은 숫자가 반환될까요?
>
> 생각해볼 점:
> - 0, 1, 2는 어디에 쓰이고 있을까요?
> - 이 숫자가 가리키는 실제 정보는 어디에 있을까요?
> - 왜 파일 경로 대신 숫자를 사용할까요?

### 질문 3: Go의 os.Open()은 내부적으로 무엇을 호출할까?

> **힌트**: Go의 편리한 API 아래에는 무엇이 숨어있을까요?
>
> 생각해볼 점:
> - `os.Open()`과 `unix.Open()`의 차이는?
> - 추상화의 장단점은?
> - strace로 확인할 수 있을까요?

## 참고 문서

- [04_System_Calls.md](../../docs/04_System_Calls.md) - 시스템 콜 상세
- [03_OS_Fundamentals.md](../../docs/03_OS_Fundamentals.md) - OS 기초

## 실습 단계

### Step 1: unix.Open()과 unix.Read()로 파일 읽기

**목표**: 시스템 콜을 직접 호출하여 파일 읽기

**위치**: `step1_open_read/main.go`

**핵심 개념**:
- `unix.Open()` → `openat` 시스템 콜
- `unix.Read()` → `read` 시스템 콜
- `unix.Close()` → `close` 시스템 콜

**검증 방법**:
```bash
# Docker 컨테이너에서 실행
strace -e openat,read,close go run main.go
```

**기대 출력**:
```
openat(AT_FDCWD, "/etc/hostname", O_RDONLY) = 3
read(3, "container-id\n", 256) = 13
close(3) = 0
```

---

### Step 2: 파일 디스크립터(fd) 탐구

**목표**: fd가 프로세스별 테이블 인덱스임을 확인

**위치**: `step2_file_descriptor/main.go`

**핵심 개념**:
- fd 0, 1, 2는 stdin, stdout, stderr
- 새로 열린 파일은 사용 가능한 가장 작은 fd 할당
- `/proc/self/fd/`로 현재 프로세스의 fd 확인 가능

**검증 방법**:
```bash
# Docker 컨테이너에서
ls -la /proc/self/fd/

# 프로그램 실행 중 fd 확인
go run main.go
```

---

### Step 3: Go 표준 라이브러리 추적

**목표**: `os.Open()`이 내부적으로 호출하는 시스템 콜 확인

**위치**: `step3_strace/main.go`

**핵심 개념**:
- Go의 `os` 패키지는 내부적으로 `syscall` 패키지 사용
- 결국 같은 시스템 콜로 귀결됨
- 추상화 계층의 역할 이해

**검증 방법**:
```bash
# unix 패키지 직접 사용 vs os 패키지 사용 비교
strace -c go run main.go

# 시스템 콜 호출 횟수 비교
```

## 완료 체크리스트

- [ ] Step 1: `unix.Open()`, `unix.Read()`로 파일 읽기 성공
- [ ] Step 1: strace로 `openat`, `read`, `close` 확인
- [ ] Step 2: fd가 3부터 할당되는 것 확인
- [ ] Step 2: `/proc/self/fd/` 내용 확인
- [ ] Step 3: `os.Open()`과 `unix.Open()` 비교 완료
- [ ] 소크라테스 질문 3개 모두 답변 가능

## 핵심 인사이트

(실습 완료 후 작성하세요)

1. 시스템 콜이란...
2. fd의 역할은...
3. Go의 추상화가 주는 이점은...
