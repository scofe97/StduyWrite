# 02 - Memory Management

mmap과 가상 메모리를 배웁니다. 파일을 메모리처럼 다루고, 프로세스 간 메모리를 공유하는 방법을 체험합니다.

## 소크라테스 질문

실습을 시작하기 전에 다음 질문들을 생각해보세요.

### 질문 1: mmap 없이 100GB 파일을 처리하려면?

> **힌트**: 메모리가 16GB인 시스템에서 100GB 파일을 읽으려면?
>
> 생각해볼 점:
> - read()로 100GB를 한 번에 읽을 수 있을까요?
> - 청크로 나눠서 읽으면 어떤 문제가 있을까요?
> - mmap은 이 문제를 어떻게 해결할까요?

### 질문 2: mmap한 영역에 쓰면 즉시 디스크에 저장될까?

> **힌트**: 메모리에 쓴 내용이 디스크에 반영되는 시점은?
>
> 생각해볼 점:
> - "페이지 캐시"란 무엇인가요?
> - `msync()`는 언제 필요할까요?
> - 컴퓨터가 갑자기 꺼지면 데이터는 안전할까요?

### 질문 3: 두 프로세스가 같은 메모리를 보려면?

> **힌트**: IPC(프로세스 간 통신)의 한 방법
>
> 생각해볼 점:
> - 프로세스마다 독립된 가상 주소 공간인데, 어떻게 공유?
> - 공유 메모리의 장단점은?
> - 동기화 문제는 어떻게 해결할까요?

## 참고 문서

- [03_OS_Fundamentals.md](../../docs/03_OS_Fundamentals.md) - 가상 메모리, 페이지
- [04_System_Calls.md](../../docs/04_System_Calls.md) - mmap 시스템 콜

## 실습 단계

### Step 1: mmap 기초

**목표**: mmap으로 익명 메모리 영역 할당하기

**위치**: `step1_mmap_basic/main.go`

**핵심 개념**:
- `unix.Mmap()` - 메모리 매핑 생성
- `unix.Munmap()` - 메모리 매핑 해제
- `MAP_ANONYMOUS` - 파일 없이 메모리만 할당
- `PROT_READ | PROT_WRITE` - 읽기/쓰기 권한

**검증 방법**:
```bash
strace -e mmap,munmap,mprotect go run main.go
```

---

### Step 2: 파일 mmap

**목표**: 파일을 메모리에 매핑하여 배열처럼 접근하기

**위치**: `step2_mmap_file/main.go`

**핵심 개념**:
- 파일 fd를 mmap에 전달
- 메모리 접근 = 파일 I/O (OS가 자동으로)
- Demand Paging - 실제 접근 시에만 메모리 로드
- `msync()` - 메모리 내용을 디스크에 동기화

**검증 방법**:
```bash
# 테스트용 대용량 파일 생성
dd if=/dev/zero of=testfile bs=1M count=100

# 프로그램 실행 및 메모리 사용량 관찰
go run main.go

# Page Fault 확인
strace -e mmap,munmap,read go run main.go
```

---

### Step 3: 공유 메모리

**목표**: 두 프로세스가 같은 메모리 영역을 공유하기

**위치**: `step3_shared_memory/main.go`

**핵심 개념**:
- `MAP_SHARED` - 변경 사항을 다른 프로세스와 공유
- `/dev/shm/` - tmpfs 기반 공유 메모리 파일 시스템
- 동기화가 없으면 데이터 경쟁 발생 가능

**검증 방법**:
```bash
# 터미널 1: 쓰기 프로세스
go run main.go write

# 터미널 2: 읽기 프로세스
go run main.go read
```

## 완료 체크리스트

- [ ] Step 1: mmap으로 익명 메모리 할당 성공
- [ ] Step 1: munmap으로 메모리 해제 확인
- [ ] Step 2: 파일을 mmap하여 배열처럼 접근
- [ ] Step 2: 대용량 파일도 작은 메모리로 처리 가능 확인
- [ ] Step 3: 두 프로세스 간 데이터 공유 성공
- [ ] 소크라테스 질문 3개 모두 답변 가능

## 핵심 인사이트

(실습 완료 후 작성하세요)

1. mmap의 핵심 원리는...
2. Demand Paging이란...
3. 공유 메모리의 주의점은...
