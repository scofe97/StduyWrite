# Page Cache 코드 가이드

## 개요
OS Page Cache의 효과를 측정하는 Go 벤치마크 코드입니다.
Cold Read와 Warm Read의 성능 차이를 통해 Kafka가 Page Cache를 활용하는 이유를 체험합니다.

## 사용된 Go 문법

### 1. runtime 패키지 - 시스템 정보

```go
import "runtime"

// OS 및 아키텍처
runtime.GOOS      // "darwin", "linux", "windows"
runtime.GOARCH    // "amd64", "arm64"
runtime.NumCPU()  // CPU 코어 수

// 메모리 통계
var m runtime.MemStats
runtime.ReadMemStats(&m)
m.Alloc  // 현재 할당된 힙 메모리
m.Sys    // OS에서 획득한 총 메모리
```
- `GOOS`: 운영체제 식별
- `MemStats`: GC 및 메모리 상태 모니터링

### 2. 포인터와 주소 연산자

```go
var m runtime.MemStats
runtime.ReadMemStats(&m)  // &m: m의 메모리 주소 전달
```
- `&`: 주소 연산자 (포인터 생성)
- 함수가 값을 직접 수정해야 할 때 사용

### 3. Page Cache 비우기 시뮬레이션

```go
// 더미 파일로 캐시 밀어내기
dummyFile, _ := os.CreateTemp("", "dummy_*.dat")
defer os.Remove(dummyFile.Name())
defer dummyFile.Close()

// 500MB 더미 데이터로 캐시 교체
dummyData := make([]byte, 1024*1024)
for i := 0; i < 500; i++ {
    rand.Read(dummyData)
    dummyFile.Write(dummyData)
}
dummyFile.Sync()

// 읽기로 Page Cache에 로드
dummyFile.Seek(0, 0)
for i := 0; i < 500; i++ {
    dummyFile.Read(dummyData)
}
```
- 실제 `drop_caches`는 root 권한 필요
- 더미 데이터로 캐시를 밀어내는 방식으로 시뮬레이션

### 4. 파일 동기화

```go
file.Sync()  // 버퍼 → 디스크 강제 쓰기
```
- `Sync()`: fsync() 시스템 콜
- 데이터가 디스크에 확실히 기록되도록 보장

### 5. 파일 위치 이동

```go
file.Seek(0, 0)  // 파일 시작으로 이동
```
- 첫 번째 인자: offset
- 두 번째 인자: whence
  - 0: 파일 시작 기준 (SEEK_SET)
  - 1: 현재 위치 기준 (SEEK_CUR)
  - 2: 파일 끝 기준 (SEEK_END)

### 6. 무한 루프와 break

```go
for {
    n, err := file.Read(buffer)
    if err != nil {
        break  // EOF 또는 에러 시 종료
    }
    totalRead += n
}
```
- `for {}`: 무한 루프 (while true)
- `break`: 루프 탈출

### 7. 고루틴과 채널 (다중 Consumer 시뮬레이션)

```go
results := make(chan struct {
    id       int
    duration time.Duration
}, numConsumers)

// 여러 Consumer 동시 실행
for i := 0; i < numConsumers; i++ {
    go func(consumerID int) {
        // 파일 읽기 작업
        results <- struct {
            id       int
            duration time.Duration
        }{consumerID, time.Since(start)}
    }(i)
}

// 결과 수집
for i := 0; i < numConsumers; i++ {
    r := <-results
    fmt.Printf("Consumer %d: %v\n", r.id, r.duration)
}
```
- 익명 구조체를 채널로 전달
- 여러 고루틴이 같은 파일을 동시에 읽음
- Page Cache 공유 효과 시뮬레이션

### 8. 슬라이스 순회

```go
durations := make([]time.Duration, readIterations)

var totalRepeat time.Duration
for _, d := range durations {
    totalRepeat += d
}
avgRepeat := totalRepeat / time.Duration(len(durations))
```
- `range`: 슬라이스/맵 순회
- `_`: 인덱스 무시
- `len()`: 슬라이스 길이

## 핵심 개념

### Cold Read vs Warm Read

```
[Cold Read - Page Cache 미적중]
App → Kernel → Disk (물리적 I/O)
                ↓
            느림! (ms 단위)

[Warm Read - Page Cache 적중]
App → Kernel → Page Cache (메모리)
                ↓
            빠름! (us 단위)
```

### Kafka의 Page Cache 활용

```
[32GB 서버 메모리]
┌─────────────────┐
│ Kernel (~1GB)   │
├─────────────────┤
│ JVM Heap (~6GB) │ ← 작게 유지!
├─────────────────┤
│ Page Cache      │ ← 최대한 크게!
│ (~25GB)         │   OS가 자동 관리
└─────────────────┘
```

## Page Cache 확인 명령어

### macOS

```bash
# 메모리 통계 (페이지 단위, 4KB/page)
vm_stat

# 예시 출력 해석
# File-backed pages: 1234567  → 캐시된 파일 데이터
# Pages free: 234567          → 여유 메모리
```

### Linux

```bash
# Page Cache 확인
cat /proc/meminfo | grep -E "^(Cached|Buffers)"
free -h

# Page Cache 강제 비우기 (root 필요)
sync && echo 3 > /proc/sys/vm/drop_caches
```

## 실행 결과 해석

| 항목 | Cold Read | Warm Read | 이유 |
|------|-----------|-----------|------|
| 소스 | 디스크 | Page Cache (RAM) | 캐시 적중 |
| 속도 | 느림 | 빠름 (10x+) | 메모리 vs 디스크 |
| Latency | ms 단위 | us 단위 | 물리적 I/O 없음 |

## Kafka에서의 장점

1. **GC 없음**: Page Cache는 JVM 외부 → GC 대상 아님
2. **재시작 후 유지**: Kafka 프로세스 재시작해도 캐시 유지
3. **OS 자동 관리**: LRU, Read-ahead 자동 적용
4. **다중 Consumer 공유**: 같은 데이터를 여러 Consumer가 캐시에서 읽음
