# Kafka 성능 원리 실습 (Go)

Kafka가 빠른 3가지 핵심 원리를 Go 코드로 직접 체험합니다.

## 📁 디렉토리 구조

```
go/
├── go.mod
├── go.sum
├── README.md
├── sequential-io/
│   ├── main.go         # Sequential I/O vs Random I/O 벤치마크
│   └── CODE_GUIDE.md   # Go 문법 및 코드 설명
├── zero-copy/
│   ├── main.go         # Zero-Copy vs Traditional Copy 벤치마크
│   └── CODE_GUIDE.md   # Go 문법 및 코드 설명
└── page-cache/
    ├── main.go         # Page Cache 효과 측정
    └── CODE_GUIDE.md   # Go 문법 및 코드 설명
```

> 각 폴더의 `CODE_GUIDE.md`에서 Go 문법과 코드 상세 설명을 확인할 수 있습니다.

## 🚀 실행 방법

### 사전 준비

```bash
# 의존성 설치 (최초 1회)
cd go
go mod download

# 또는 직접 설치
go get golang.org/x/sys/unix
```

### 1. Sequential I/O vs Random I/O

```bash
cd sequential-io
go run main.go
```

**주요 명령어 설명**:

| 명령어 | 설명 |
|--------|------|
| `go run main.go` | Go 소스 코드를 컴파일하고 즉시 실행 |
| `go build -o benchmark main.go` | 실행 파일로 컴파일 (재사용 가능) |

**코드 핵심 설명**:

```go
// F_NOCACHE: Page Cache를 우회하여 실제 디스크 성능 측정
unix.FcntlInt(file.Fd(), unix.F_NOCACHE, 1)

// Sequential Read: 연속된 블록을 순서대로 읽음
file.Read(buffer)  // 현재 위치에서 다음 블록 읽기

// Random Read: 랜덤 위치로 이동 후 읽기 (Seek 오버헤드 발생)
file.Seek(randomOffset, 0)  // 랜덤 위치로 이동
file.Read(buffer)           // 해당 위치에서 읽기
```

**학습 포인트**:
- Append-Only 로그 구조의 장점 이해
- 디스크 헤드 이동(Seek)이 성능에 미치는 영향
- Kafka가 Sequential I/O를 선택한 이유

**예상 결과**:
```
Sequential I/O: 50ms
Random I/O:     500ms
🏆 Sequential이 10x 더 빠름!
```

### 2. Zero-Copy vs Traditional Copy

```bash
cd zero-copy
go run main.go
```

**주요 명령어 설명**:

```go
// Traditional Copy: User Space를 거쳐 복사 (4회 복사)
buffer := make([]byte, bufferSize)
srcFile.Read(buffer)      // Kernel → User Space (1차 복사)
dstFile.Write(buffer)     // User Space → Kernel (2차 복사)

// Zero-Copy (시뮬레이션): io.Copy 사용
io.Copy(dstFile, srcFile)  // 내부적으로 최적화된 복사 사용
```

**시스템 콜 확인** (macOS):

```bash
# dtrace로 시스템 콜 확인 (root 필요)
sudo dtruss -c go run main.go 2>&1 | grep -E "read|write|sendfile"
```

**학습 포인트**:
- sendfile() 시스템 콜의 원리
- User Space를 거치는 복사의 오버헤드
- Broker가 압축을 해제하지 않는 이유

**예상 결과**:
```
Traditional Copy: 200ms
Zero-Copy:        80ms
🏆 Zero-Copy가 2.5x 더 빠름!
```

### 3. Page Cache 효과

```bash
cd page-cache
go run main.go
```

**주요 명령어 설명**:

```go
// Cold Read: Page Cache가 비어있을 때 (디스크에서 직접 읽기)
dropPageCache()     // 캐시 비우기 시도
file.Read(buffer)   // 디스크 → Kernel → User Space

// Warm Read: Page Cache에 데이터가 있을 때 (메모리에서 읽기)
file.Read(buffer)   // Page Cache → User Space (디스크 접근 없음)
```

**Page Cache 확인 명령어**:

```bash
# macOS: 메모리 통계 확인
vm_stat | grep "File-backed"

# macOS: 특정 파일의 캐시 상태
sudo fs_usage -f filesys | grep "PAGE"

# Linux: Page Cache 확인
cat /proc/meminfo | grep -E "^(Cached|Buffers)"
free -h

# Linux: Page Cache 강제 비우기 (root 필요)
sync && echo 3 > /proc/sys/vm/drop_caches
```

**학습 포인트**:
- Cold Read vs Warm Read 성능 차이
- OS Page Cache의 자동 관리
- 여러 Consumer가 캐시를 공유하는 효과

**예상 결과**:
```
Cold Read (디스크): 500ms
Warm Read (캐시):   50ms
🏆 Page Cache로 10x 더 빠름!
```

## 📊 핵심 개념 정리

### 1️⃣ Sequential I/O

```
[Kafka Log Structure]
Block 1 → Block 2 → Block 3 → Block 4 → ...
   ↑
   순차적으로만 쓰기/읽기
   헤드 이동 최소화
```

- HDD: Seek Time(~10ms) + Rotational Latency(~4ms) 제거
- SSD: FTL 매핑 조회 최적화 + OS Prefetch 활용

### 2️⃣ Zero-Copy (sendfile)

```
[Traditional - 4 Copy]
Disk → Kernel Buffer → User Buffer → Socket Buffer → NIC
                       ⚠️ CPU Copy   ⚠️ CPU Copy

[Zero-Copy - 2 Copy]
Disk → Kernel Buffer(Page Cache) → NIC
       ✅ User Space 우회!
```

### 3️⃣ Page Cache

```
[32GB RAM]
┌─────────────────┐
│ Kernel (~1GB)   │
├─────────────────┤
│ JVM Heap (~6GB) │ ← 작게 유지!
├─────────────────┤
│ Page Cache      │ ← OS가 자동 관리
│ (~25GB) ⭐      │    GC 없음, 재시작해도 유지
└─────────────────┘
```

## 🔗 관련 문서

- [06_Performance_면접정리.md](../../../docs/카프카/06_Performance_면접정리.md)
- [Kafka Documentation - Design](https://kafka.apache.org/documentation/#design)
- [IBM Developer - Zero-Copy](https://developer.ibm.com/articles/j-zerocopy/)

## 💡 면접 팁

**Q: Kafka가 빠른 이유는?**

1. **Sequential I/O**: Append-Only 로그 구조로 순차 쓰기/읽기만 사용. Random I/O 대비 10~100배 빠름.

2. **Zero-Copy**: sendfile() 시스템 콜로 User Space 복사 생략. 복사 4회 → 2회, Context Switch 감소.

3. **Page Cache**: JVM Heap 대신 OS Page Cache 활용. GC 없음, 재시작해도 캐시 유지, 다중 Consumer 캐시 공유.
