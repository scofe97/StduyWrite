# Sequential I/O 코드 가이드

## 개요
Sequential I/O와 Random I/O의 성능 차이를 측정하는 Go 벤치마크 코드입니다.

## 사용된 Go 문법

### 1. 상수 정의

```go
const (
    fileSize  = 500 * 1024 * 1024  // 500MB
    blockSize = 4 * 1024           // 4KB
    readCount = 50000              // 읽기 횟수
)
```
- `const`: 상수 선언
- 괄호로 여러 상수를 그룹화

### 2. 파일 생성 (임시 파일)

```go
file, err := os.CreateTemp("", "io_benchmark_*.dat")
if err != nil {
    panic(err)
}
```
- `os.CreateTemp(dir, pattern)`: 임시 파일 생성
- `*`는 랜덤 문자열로 대체됨
- 첫 번째 인자 `""`는 시스템 기본 임시 디렉토리 사용

### 3. F_NOCACHE - Page Cache 우회

```go
import "golang.org/x/sys/unix"

unix.FcntlInt(file.Fd(), unix.F_NOCACHE, 1)
```
- `file.Fd()`: 파일 디스크립터 (정수) 반환
- `F_NOCACHE`: macOS에서 Page Cache를 우회
- 실제 디스크 성능을 측정하기 위해 사용

### 4. 랜덤 데이터 생성

```go
import "crypto/rand"

data := make([]byte, 1024*1024)
rand.Read(data)  // 암호학적으로 안전한 랜덤 데이터
```
- `crypto/rand`: 암호학적 랜덤 생성기
- `math/rand`보다 진정한 랜덤값 생성

### 5. 큰 정수 랜덤 생성

```go
import (
    "crypto/rand"
    "math/big"
)

n, _ := rand.Int(rand.Reader, big.NewInt(maxBlocks))
offset := n.Int64() * blockSize
```
- `big.NewInt()`: 임의 정밀도 정수 생성
- `rand.Int()`: 0 ~ (max-1) 범위의 랜덤 정수

### 6. 파일 읽기

```go
buffer := make([]byte, blockSize)

// Sequential: 현재 위치에서 순차 읽기
n, err := file.Read(buffer)

// Random: 특정 위치로 이동 후 읽기
file.Seek(offset, 0)  // 0 = 파일 시작 기준
n, err := file.Read(buffer)
```
- `file.Read()`: 현재 위치에서 읽고 위치 이동
- `file.Seek(offset, whence)`: 파일 포인터 이동
  - `whence=0`: 파일 시작 기준
  - `whence=1`: 현재 위치 기준
  - `whence=2`: 파일 끝 기준

### 7. 시간 측정

```go
start := time.Now()
// ... 작업 수행 ...
duration := time.Since(start)

// 처리량 계산 (MB/s)
throughput := float64(totalBytes) / (1024 * 1024) / duration.Seconds()
```
- `time.Now()`: 현재 시간
- `time.Since(t)`: t 이후 경과 시간
- `duration.Seconds()`: Duration을 초 단위 float64로 변환

### 8. defer - 지연 실행

```go
testFile := createTestFile()
defer os.Remove(testFile)  // 함수 종료 시 파일 삭제
```
- `defer`: 함수 종료 시 실행 (LIFO 순서)
- 리소스 정리에 주로 사용

## 핵심 알고리즘

### Sequential Read
```
[Block 1][Block 2][Block 3][Block 4]...
    ↓       ↓       ↓       ↓
   Read    Read    Read    Read
   (OS Prefetch로 다음 블록 미리 로드)
```

### Random Read
```
[Block 1][Block 2][Block 3][Block 4]...
    ↑               ↑   ↑       ↑
   Seek           Seek Seek   Seek
   (매번 위치 이동 → 오버헤드)
```

## 실행 결과 해석

| 항목 | Sequential | Random | 이유 |
|------|------------|--------|------|
| 속도 | 빠름 | 느림 | Seek 오버헤드 없음 |
| OS 최적화 | Read-ahead 적용 | 불가능 | 순차 패턴 예측 가능 |
| SSD에서도 | 더 빠름 | 느림 | FTL 매핑 최적화 |
