# Ch13. Docker & WebAssembly - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Wasm과 컨테이너의 성능 비교는 실제로 어느 정도이며, 어떤 벤치마크가 의미 있는가?

### 왜 이 질문이 중요한가
"Wasm이 컨테이너보다 빠르다"는 주장은 흔하지만, 실제 성능 차이는 워크로드에 따라 크게 달라진다. 마케팅 수치가 아닌 실제 벤치마크를 이해하면, Wasm을 도입해야 할 상황과 그렇지 않은 상황을 구분할 수 있다. 또한 성능 측정 방법을 알면 자체 워크로드에서 검증 가능하다.

### 답변
**성능 비교의 세 가지 축**

1. **시작 시간(Cold Start)**: 첫 요청부터 응답까지 걸리는 시간
2. **실행 시간(Execution Time)**: 동일 작업을 수행하는 데 걸리는 시간
3. **메모리 사용량(Memory Footprint)**: 런타임이 소비하는 메모리

**시작 시간 벤치마크**

Wasm의 가장 큰 장점은 밀리초 단위 시작 시간이다.

실제 측정 결과 (Fastly 연구, 2019):
- **Linux 컨테이너**: 100ms~1s (이미지 크기, 초기화 로직에 따라 변동)
- **Wasm (Wasmtime)**: 1~5ms

예시 측정:
```bash
# 컨테이너 시작 시간
$ time docker run --rm alpine echo "Hello"
real    0m0.384s  # 384ms

# Wasm 시작 시간
$ time wasmtime hello.wasm
real    0m0.003s  # 3ms
```

차이의 원인:
- 컨테이너: 네임스페이스 생성, cgroups 설정, 파일시스템 마운트, 네트워크 설정 등 초기화 과정
- Wasm: 바이너리 로드 후 즉시 실행, OS 수준 격리 없음

**실행 시간 벤치마크**

실행 시간은 워크로드에 따라 크게 달라진다.

**케이스 1: CPU 집약적 작업 (암호화, 압축 등)**
- Native(C/Rust 바이너리): 100% (기준)
- Wasm (Wasmtime AOT): 95~105% (거의 동일)
- Wasm (Wasmtime JIT): 80~90% (JIT 오버헤드)
- 컨테이너 (Alpine + 네이티브 바이너리): 100% (컨테이너는 실행 시간에 거의 영향 없음)

**케이스 2: I/O 집약적 작업 (파일, 네트워크)**
- Native: 100%
- Wasm: 60~80% (WASI의 syscall 에뮬레이션 오버헤드)
- 컨테이너: 95~100% (overlay 네트워크 약간의 오버헤드)

**케이스 3: 메모리 집약적 작업**
- Native: 100%
- Wasm: 90~95% (선형 메모리 추상화 오버헤드)
- 컨테이너: 100%

**중요한 발견**: Wasm은 CPU 바운드 작업에서는 네이티브와 거의 동일하지만, I/O 작업에서는 현재 WASI 구현의 한계로 느리다.

**메모리 사용량 벤치마크**

간단한 HTTP 서버 예시:
- **Go 네이티브 바이너리**: 10MB 실행 파일, 5MB 런타임 메모리
- **Go 컨테이너 (scratch 기반)**: 10MB 이미지, 5MB 런타임 메모리
- **Go 컨테이너 (alpine 기반)**: 20MB 이미지, 5MB 런타임 메모리
- **Rust Wasm (Spin)**: 500KB 바이너리, 2MB 런타임 메모리

Wasm의 메모리 절감은 런타임보다 **배포 크기**에서 두드러진다.

**의미 있는 벤치마크 설계**

잘못된 벤치마크:
- "Hello World" 출력만 측정 (실제 워크로드와 무관)
- 컨테이너에 불필요한 OS 계층 포함 (scratch 대신 ubuntu 사용)
- 네트워크 I/O 미포함 (실제 마이크로서비스는 네트워크 호출 빈번)

올바른 벤치마크:
1. **실제 워크로드 사용**: 프로덕션 트래픽 패턴 재현
2. **End-to-End 측정**: 네트워크, 직렬화, 데이터베이스 접근 포함
3. **동일 조건**: 컨테이너도 scratch 기반, 네이티브 바이너리 사용
4. **반복 측정**: Warm-up 후 중앙값 사용

예시 벤치마크 시나리오:
```
서버리스 함수: 이미지 리사이징
1. 시작 시간: 첫 요청부터 응답까지
2. 실행 시간: 1MB 이미지를 100x100 썸네일로 변환
3. 메모리: 피크 메모리 사용량
4. 처리량: 초당 처리 가능한 이미지 수
```

**Wasm이 유리한 경우**:
- 서버리스 환경 (짧은 cold start 중요)
- 엣지 컴퓨팅 (제한된 메모리, 빠른 배포)
- CPU 집약적 워크로드 (암호화, 압축, AI 추론)

**컨테이너가 유리한 경우**:
- I/O 집약적 워크로드 (데이터베이스, 파일 처리)
- 복잡한 네트워킹 (HTTP/2, gRPC, 서비스 메시)
- 성숙한 생태계 필요 (라이브러리, 도구)

### 실무 적용
자체 워크로드 벤치마크 방법:
```bash
# 1. 컨테이너 버전 빌드
docker build -t myapp:container .
# 2. Wasm 버전 빌드
spin build && docker build --platform wasi/wasm -t myapp:wasm .
# 3. 시작 시간 측정
hyperfine --warmup 3 \
  'docker run --rm myapp:container' \
  'docker run --rm --runtime=io.containerd.spin.v2 --platform=wasi/wasm myapp:wasm'
# 4. 실행 시간 측정 (서버 실행 후)
ab -n 1000 -c 10 http://localhost:5000/api
```

결론: Wasm은 시작 시간에서 압도적 우위, 실행 시간은 워크로드 의존적. 프로덕션 도입 전 반드시 자체 벤치마크 필수.

---

## Q2. WasmEdge와 Wasmtime 런타임의 차이는 무엇이며, 어떤 상황에서 어떤 것을 선택해야 하는가?

### 왜 이 질문이 중요한가
Wasm 런타임은 JVM이나 Node.js처럼 실행 환경을 제공하는 핵심 컴포넌트다. WasmEdge, Wasmtime, Wasmer, Spin 등 여러 선택지가 있으며, 각각 다른 성능 특성과 기능을 가진다. 올바른 런타임 선택은 애플리케이션 성능과 운영 편의성에 직접적인 영향을 미친다.

### 답변
**주요 Wasm 런타임 비교**

**1. Wasmtime (Bytecode Alliance)**

특징:
- Bytecode Alliance(Mozilla, Fastly, Intel 등) 주도의 레퍼런스 구현
- Cranelift JIT 컴파일러 사용 (Rust 기반)
- WASI(WebAssembly System Interface) 표준 선도
- 보안과 안정성에 중점

성능:
- 시작 시간: 매우 빠름 (1~5ms)
- 실행 속도: 중간~빠름 (네이티브의 80~95%)
- 메모리 효율: 우수

강점: 표준 준수, 보안, 문서화
약점: 특화 기능 부족, 클라우드 최적화 제한적

**2. WasmEdge (CNCF Sandbox)**

특징:
- CNCF(Cloud Native Computing Foundation) 프로젝트
- 클라우드 네이티브 및 엣지 컴퓨팅에 최적화
- LLVM AOT(Ahead-Of-Time) 컴파일러
- Kubernetes, Docker와 긴밀한 통합

독자 기능:
- **Tensorflow Lite 지원**: Wasm 내부에서 AI 모델 실행
- **Async I/O**: 비동기 네트워크 작업 최적화
- **Socket 지원**: TCP/UDP 소켓 직접 사용 (WASI 표준 외)
- **GPU 접근**: CUDA, OpenCL 실험적 지원

성능:
- 시작 시간: 빠름 (5~10ms, AOT 사용 시)
- 실행 속도: 매우 빠름 (네이티브의 90~98%)
- 메모리 효율: 우수

강점: 성능, 클라우드 네이티브 통합, AI 워크로드
약점: 표준 외 기능 사용 시 이식성 제한

**3. Wasmer**

특징:
- 플러그형 컴파일러 백엔드 (Cranelift, LLVM, Singlepass)
- 다양한 언어 바인딩 (Python, Ruby, Go 등)
- WASI 및 Emscripten 지원

컴파일러 전략:
- **Singlepass**: 초고속 컴파일, 느린 실행 (디버깅용)
- **Cranelift**: 빠른 컴파일, 빠른 실행 (프로덕션)
- **LLVM**: 느린 컴파일, 최고 성능 (AOT)

강점: 유연성, 언어 통합
약점: 클라우드 네이티브 통합 제한적

**4. Spin (Fermyon)**

특징:
- 서버리스 애플리케이션 프레임워크 (런타임이자 프레임워크)
- Wasmtime 기반
- HTTP, Redis, Key-Value Store 등 내장 API
- 개발자 경험 최적화

강점: 빠른 프로토타이핑, 서버리스 워크로드
약점: Spin 생태계 종속성

**선택 기준**

| 사용 사례 | 권장 런타임 | 이유 |
|----------|------------|------|
| 표준 준수, 보안 중시 | Wasmtime | Bytecode Alliance 레퍼런스, WASI 표준 선도 |
| 클라우드/Kubernetes | WasmEdge | CNCF 프로젝트, K8s 통합, 성능 |
| AI/ML 워크로드 | WasmEdge | TensorFlow Lite 네이티브 지원 |
| 엣지 디바이스 | WasmEdge | 경량, 빠른 실행, Async I/O |
| 언어 임베딩 (Python 등) | Wasmer | 다양한 언어 바인딩 |
| 서버리스 함수 | Spin | HTTP 핸들러 내장, 빠른 개발 |
| 범용 워크로드 | Wasmtime | 균형 잡힌 선택 |

**Docker Desktop의 런타임 지원**

Docker Desktop은 여러 런타임을 동시 지원:
```bash
io.containerd.wasmtime.v1   # Wasmtime
io.containerd.wasmedge.v1   # WasmEdge
io.containerd.wasmer.v1     # Wasmer
io.containerd.spin.v2       # Spin
```

실행 시 `--runtime` 플래그로 선택:
```bash
docker run --runtime=io.containerd.wasmedge.v1 \
  --platform=wasi/wasm myapp:wasm
```

**성능 벤치마크 (Fibonacci 계산, n=40)**

| 런타임 | 실행 시간 | 네이티브 대비 |
|--------|----------|--------------|
| Native C | 1.00s | 100% |
| WasmEdge (AOT) | 1.05s | 95% |
| Wasmtime (JIT) | 1.15s | 87% |
| Wasmer (LLVM) | 1.08s | 93% |
| Wasmer (Cranelift) | 1.20s | 83% |

**I/O 벤치마크 (HTTP 서버, 1000 req/sec)**

| 런타임 | 지연시간 (p99) |
|--------|---------------|
| Native Go | 5ms |
| WasmEdge | 8ms |
| Wasmtime | 12ms |
| Spin | 10ms |

WasmEdge가 I/O에서도 앞서는 이유: 비표준 Async I/O 최적화

**이식성 vs 성능 트레이드오프**

- **Wasmtime**: 완전한 WASI 표준 준수 → 어디서나 실행 가능
- **WasmEdge**: 비표준 확장 (Socket, Async) → 성능 우수, 이식성 제한

예시: WasmEdge의 Socket API 사용
```rust
use wasmedge_wasi_socket::TcpListener;  // 비표준!
let listener = TcpListener::bind("127.0.0.1:8080")?;
```

이 코드는 WasmEdge에서만 실행되며, Wasmtime에서는 컴파일 실패.

### 실무 적용
프로덕션 권장:
1. **Kubernetes 환경**: WasmEdge + runwasi (CNCF 통합)
2. **AWS Lambda 대체**: Spin (Fermyon Cloud와 호환)
3. **엣지 CDN**: WasmEdge (Fastly, Cloudflare Workers)
4. **범용 클라우드**: Wasmtime (이식성 우선)

마이그레이션 고려: 초기에는 Wasmtime으로 시작해 표준 API만 사용. 성능 병목 발생 시 WasmEdge로 전환하되, 비표준 API는 feature flag로 격리.

결론: Wasmtime은 안전한 기본 선택, WasmEdge는 성능과 클라우드 통합이 중요한 경우, Wasmer는 언어 임베딩, Spin은 서버리스 프로토타이핑.

---

## Q3. WASI (WebAssembly System Interface) 표준은 무엇이며, 왜 Wasm의 미래에 중요한가?

### 왜 이 질문이 중요한가
Wasm은 원래 브라우저용으로 설계되어 시스템 리소스 접근이 제한적이었다. WASI는 Wasm을 브라우저 밖에서도 사용 가능하게 만드는 핵심 표준이다. WASI의 발전 방향을 이해하면, Wasm이 컨테이너를 대체할 수 있는 영역과 한계를 파악할 수 있다.

### 답변
**WASI의 탄생 배경**

초기 Wasm (브라우저 전용):
- 파일 시스템 접근 불가
- 네트워크 소켓 사용 불가
- 환경 변수, 커맨드 라인 인자 미지원
- 난수 생성기 없음

이는 브라우저 보안 모델에는 적합하지만, 서버 사이드 애플리케이션에는 치명적 제약이다.

**WASI의 목표**

> "Write once, run anywhere" - 하지만 JVM처럼 무거운 런타임 없이!

WASI는 Wasm이 다음을 가능하게 한다:
1. 파일 읽기/쓰기
2. 네트워크 통신
3. 환경 변수 접근
4. 시간, 난수 같은 시스템 리소스 사용
5. **플랫폼 독립성**: 동일한 .wasm 파일이 Linux, Windows, macOS, Raspberry Pi에서 실행

**WASI 아키텍처**

```
┌─────────────────────────────────────────────────┐
│         Wasm Application (hello.wasm)           │
│  ┌───────────────────────────────────────────┐  │
│  │  WASI API 호출 (파일, 네트워크 등)        │  │
│  └───────────────────┬───────────────────────┘  │
└──────────────────────┼──────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────┐
│           WASI Implementation (Runtime)         │
│  ┌──────────────┐  ┌──────────────┐             │
│  │ Wasmtime     │  │ WasmEdge     │             │
│  │ WASI Impl    │  │ WASI Impl    │             │
│  └──────┬───────┘  └──────┬───────┘             │
└─────────┼──────────────────┼────────────────────┘
          │                  │
          ▼                  ▼
┌─────────────────────────────────────────────────┐
│              Host OS (Linux, macOS, etc.)       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ syscall  │  │ syscall  │  │ syscall  │      │
│  │ open()   │  │ read()   │  │ socket() │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
```

**WASI의 핵심 인터페이스**

**WASI Preview 1 (안정화, 현재)**

기본 파일 시스템:
```rust
use std::fs::File;
use std::io::prelude::*;

fn main() -> std::io::Result<()> {
    // WASI를 통해 호스트 파일 시스템 접근
    let mut file = File::open("input.txt")?;
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    println!("{}", contents);
    Ok(())
}
```

컴파일:
```bash
rustc --target wasm32-wasip1 main.rs -o app.wasm
```

실행:
```bash
# 호스트의 /data를 Wasm의 루트로 마운트
wasmtime --dir=/data app.wasm
```

기본 API:
- `fd_read`, `fd_write`: 파일 디스크립터 읽기/쓰기
- `path_open`: 파일 열기
- `random_get`: 난수 생성
- `clock_time_get`: 시간 조회
- `environ_get`: 환경 변수 읽기

**WASI Preview 2 (개발 중, Component Model 기반)**

새로운 기능:
- **비동기 I/O**: async/await 네이티브 지원
- **네트워크 소켓**: TCP/UDP 표준화
- **HTTP**: 표준 HTTP 클라이언트/서버 API
- **스트림**: 효율적인 데이터 스트리밍

Component Model:
```wit
// WIT (WebAssembly Interface Types)
package example:http-handler;

interface http {
  record request {
    method: string,
    uri: string,
    headers: list<tuple<string, string>>,
    body: list<u8>,
  }

  record response {
    status: u16,
    headers: list<tuple<string, string>>,
    body: list<u8>,
  }

  handle: func(req: request) -> response;
}
```

이를 구현한 Wasm 컴포넌트는 **언어에 무관하게** 재사용 가능하다.

**WASI가 해결하는 문제**

**1. 이식성**

동일한 .wasm 파일이 다양한 환경에서 실행:
```bash
# Linux
wasmtime app.wasm

# macOS
wasmtime app.wasm

# Windows
wasmtime.exe app.wasm

# Raspberry Pi
wasmtime app.wasm
```

컨테이너와의 차이: 컨테이너는 Linux 커널에 의존 (macOS/Windows에서는 VM 필요)

**2. 보안 (Capability-based)**

WASI는 기본적으로 모든 권한이 거부되며, 명시적으로 허용해야 한다.

예:
```bash
# 아무 권한 없음 → 파일 접근 실패
wasmtime app.wasm

# /data 디렉토리만 읽기 허용
wasmtime --dir=/data::/data app.wasm

# /data 읽기, /output 쓰기 허용
wasmtime --dir=/data::/data --dir=/output::/output app.wasm

# 네트워크 접근 허용 (WASI Preview 2)
wasmtime --allow-network app.wasm
```

컨테이너와의 차이: Docker는 기본적으로 많은 권한 허용, 명시적 제한 필요

**3. 샌드박싱**

Wasm은 선형 메모리 모델로 메모리 안전성 보장:
- 버퍼 오버플로우 불가능
- Use-after-free 불가능
- 임의 메모리 접근 불가능

컨테이너는 프로세스 격리지만, 커널 취약점 공격 가능.

**WASI의 한계 (현재)**

1. **네트워크 미성숙**: WASI Preview 1은 네트워크 소켓 미지원 (Preview 2에서 추가 예정)
2. **스레드 제한**: 멀티스레딩이 표준화되지 않음
3. **생태계 부족**: POSIX API와 완전히 호환되지 않아 기존 라이브러리 포팅 어려움

### 실무 적용
WASI 활용 사례:

**1. 플러그인 시스템**
```rust
// 호스트 애플리케이션
let engine = Engine::default();
let module = Module::from_file(&engine, "plugin.wasm")?;
let mut linker = Linker::new(&engine);
wasmtime_wasi::add_to_linker(&mut linker, |s| s)?;
let instance = linker.instantiate(&mut store, &module)?;
```

장점: 플러그인이 호스트 시스템을 해칠 수 없음, 언어 무관

**2. 서버리스 함수**
Fastly Compute@Edge, Cloudflare Workers는 WASI 기반:
```javascript
addEventListener('fetch', event => {
  // Wasm 모듈 호출
  const result = wasmModule.handle(event.request);
  event.respondWith(new Response(result));
});
```

**3. 엣지 디바이스**
IoT 디바이스에서 안전하게 서드파티 코드 실행:
```bash
# Raspberry Pi에서 WASI 앱 실행
wasmtime --dir=/sensors::/sensors sensor-app.wasm
```

미래 전망: WASI Preview 2가 안정화되면, Wasm은 "진정한 유니버설 바이너리"가 될 것. 하지만 POSIX 완전 호환까지는 여전히 시간이 필요하다.

---

## Q4. Spin과 wasm 런타임의 통합은 어떻게 이루어지며, 다른 Wasm 프레임워크는 무엇이 있는가?

### 왜 이 질문이 중요한가
Spin은 단순한 런타임이 아니라 서버리스 애플리케이션을 위한 프레임워크다. Wasm 생태계에는 Spin 외에도 다양한 프레임워크가 있으며, 각각 다른 사용 사례를 겨냥한다. 프레임워크의 역할과 선택 기준을 이해하면, Wasm 기반 애플리케이션 개발 시 올바른 도구를 선택할 수 있다.

### 답변
**Spin의 아키텍처**

Spin은 Wasmtime 위에 구축된 레이어드 아키텍처다:

```
┌─────────────────────────────────────────────────┐
│        Application (Rust/Go/JS/Python)          │
└─────────────────────┬───────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│              Spin SDK (언어별)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │spin_sdk  │  │spin-go   │  │spin-js   │       │
│  │(Rust)    │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────┬───────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│            Spin Runtime (Rust)                  │
│  ┌────────────────────────────────────────────┐ │
│  │ HTTP Trigger, Redis Trigger, etc.          │ │
│  ├────────────────────────────────────────────┤ │
│  │ Key-Value Store, SQL, Outbound HTTP        │ │
│  ├────────────────────────────────────────────┤ │
│  │ Configuration, Variables                   │ │
│  └────────────────────────────────────────────┘ │
└─────────────────────┬───────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│            Wasmtime (WASI Runtime)              │
└─────────────────────┬───────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│              Host Resources                      │
└─────────────────────────────────────────────────┘
```

**Spin의 핵심 개념**

**1. Triggers**

애플리케이션을 시작하는 이벤트 소스:
- `http`: HTTP 요청 (가장 흔함)
- `redis`: Redis pub/sub 메시지
- `timer`: 주기적 실행 (크론잡)

spin.toml:
```toml
spin_manifest_version = 2

[application]
name = "hello-world"

[[trigger.http]]
route = "/hello"
component = "hello"

[component.hello]
source = "target/wasm32-wasip1/release/hello.wasm"
allowed_outbound_hosts = ["https://api.example.com"]
[component.hello.build]
command = "cargo build --target wasm32-wasip1 --release"
```

**2. Components**

재사용 가능한 Wasm 모듈. 각 컴포넌트는:
- 독립적인 메모리 공간
- 명시적으로 허용된 리소스만 접근
- 상태 비저장 (stateless)

**3. Host Functions**

Spin이 제공하는 고수준 API:

Rust 예시:
```rust
use spin_sdk::{
    http::{Request, Response},
    http_component,
    key_value::Store,
};

#[http_component]
fn handle_request(req: Request) -> Result<Response> {
    // Key-Value Store 사용
    let store = Store::open_default()?;
    let count: u64 = store.get("counter")
        .unwrap_or(0)
        .parse()
        .unwrap_or(0);
    store.set("counter", &(count + 1).to_string())?;

    // Outbound HTTP 호출
    let external_data = spin_sdk::http::send(
        http::Request::builder()
            .uri("https://api.example.com/data")
            .method("GET")
            .body(None)?
    )?;

    Ok(http::Response::builder()
        .status(200)
        .body(format!("Visit count: {}", count))?)
}
```

이 코드는 WASI만으로는 구현 불가능 (Key-Value, Outbound HTTP는 Spin 확장)

**Spin과 Docker의 통합**

Docker Desktop의 `io.containerd.spin.v2` 런타임은 Spin을 containerd shim으로 통합한다:

```bash
docker run -d \
  --runtime=io.containerd.spin.v2 \
  --platform=wasi/wasm \
  -p 3000:80 \
  myapp:wasm
```

내부 동작:
1. containerd가 이미지를 pull하고 scratch 파일시스템 준비
2. Spin shim이 spin.toml과 .wasm 파일 로드
3. Spin이 Wasmtime으로 컴포넌트 실행
4. HTTP 트리거가 포트 80에서 요청 수신
5. 요청을 Wasm 핸들러로 라우팅

**다른 Wasm 프레임워크**

**1. Lunatic (Erlang-like Actor Model)**

특징:
- Actor 기반 동시성 (Erlang BEAM 영감)
- 경량 프로세스 (수백만 개 동시 실행 가능)
- Fault tolerance (supervisor 패턴)

예시:
```rust
use lunatic::process::spawn;

#[lunatic::main]
fn main() {
    let child = spawn!(|| {
        println!("Hello from actor!");
    });
    child.join();
}
```

적합 사례: 실시간 채팅, 게임 서버, IoT 디바이스 관리

**2. WasmCloud (Distributed Actor Platform)**

특징:
- 분산 Actor 시스템
- Capability-based 보안
- 런타임에 컴포넌트 연결/재연결

예시 manifest:
```yaml
actors:
  - hello-actor
capabilities:
  - wascc:http_server
  - wascc:logging
links:
  - actor: hello-actor
    contract: wascc:http_server
    values:
      PORT: 8080
```

적합 사례: 마이크로서비스, 엣지 오케스트레이션

**3. Extism (Plug-in Framework)**

특징:
- 호스트 애플리케이션에 Wasm 플러그인 임베딩
- 다양한 언어 호스트 SDK (Python, Ruby, Go, .NET 등)

예시 (Python 호스트):
```python
from extism import Plugin

plugin = Plugin("plugin.wasm")
result = plugin.call("greet", b"World")
print(result)  # "Hello, World!"
```

적합 사례: 플러그인 시스템, 사용자 정의 함수

**4. Slight (SpiderLightning)**

특징:
- Distributed Application Runtime (Dapr와 유사)
- 클라우드 서비스 추상화 (S3, Redis, Pub/Sub)

예시:
```rust
#[slight::main]
async fn main() {
    let kv = slight::kv::get_default().await;
    kv.set("key", "value").await.unwrap();
}
```

적합 사례: 클라우드 네이티브 앱, 멀티 클라우드

**프레임워크 비교**

| 프레임워크 | 주요 특징 | 적합 사례 |
|-----------|----------|----------|
| **Spin** | HTTP/Redis 트리거, 서버리스 | 웹 API, 마이크로서비스 |
| **Lunatic** | Actor 모델, 동시성 | 실시간 시스템, 게임 |
| **WasmCloud** | 분산 Actor, Capability | 엣지 오케스트레이션 |
| **Extism** | 플러그인 호스팅 | 확장 가능 앱 |
| **Slight** | 클라우드 추상화 | 멀티 클라우드 앱 |

**통합 메커니즘**

모든 프레임워크는 Wasmtime/WasmEdge 위에서 실행되지만, 다음을 추가한다:
1. **Host Functions**: 프레임워크별 API (Spin의 Key-Value 등)
2. **Component Linking**: 여러 Wasm 모듈 연결
3. **Resource Management**: 메모리, 네트워크 등 리소스 추상화

### 실무 적용
프레임워크 선택 가이드:

**Spin**: 간단한 HTTP API, Fermyon Cloud 배포 계획
```bash
spin new http-rust myapp
cd myapp && spin build && spin up
```

**Lunatic**: 수천 개 동시 연결, WebSocket 서버
```bash
lunatic run server.wasm
```

**WasmCloud**: Kubernetes 대체, 엣지 배포
```bash
wash up  # WasmCloud 호스트 시작
wash ctl start actor myactor.wasm
```

**Extism**: 기존 앱에 플러그인 추가
```python
plugin = Plugin("user_script.wasm", wasi=True)
result = plugin.call("transform", user_data)
```

결론: Spin은 서버리스 웹 앱에 최적, Lunatic은 동시성 중심, WasmCloud는 분산 시스템, Extism은 플러그인 시스템. 각 프레임워크는 Wasm의 샌드박싱과 이식성을 유지하면서 고수준 추상화를 제공한다.

---

## Q5. Wasm의 보안 모델은 컨테이너와 어떻게 다르며, 실제로 더 안전한가?

### 왜 이 질문이 중요한가
보안은 클라우드 인프라의 최우선 과제다. Wasm이 "기본적으로 안전하다"는 주장은 흔하지만, 구체적인 보안 메커니즘과 한계를 이해해야 실무에 적용할 수 있다. 또한 컨테이너 탈출 공격 같은 실제 위협에 Wasm이 어떻게 대응하는지 파악하면, 보안 요구사항에 따라 올바른 기술을 선택할 수 있다.

### 답변
**컨테이너의 보안 모델**

컨테이너는 **프로세스 격리**를 통해 보안을 제공한다:

1. **네임스페이스**: PID, 네트워크, 파일시스템 등을 격리
2. **cgroups**: 리소스 사용량 제한
3. **Seccomp**: 허용된 syscall만 실행
4. **AppArmor/SELinux**: 강제 접근 제어
5. **Capabilities**: root 권한 세분화

하지만 여전히 같은 커널을 공유하므로 **커널 취약점**에 노출된다.

**컨테이너 탈출 공격 예시**

**CVE-2019-5736 (runc 취약점)**:
```bash
# 악의적인 컨테이너 이미지
FROM alpine
RUN echo '#!/bin/sh' > /bin/sh && \
    echo 'cat /proc/self/exe > /host_runc' >> /bin/sh && \
    echo 'chmod +x /host_runc' >> /bin/sh
```

이 공격은 runc 바이너리를 덮어써서 호스트를 장악한다. 수백만 개 컨테이너가 영향받았다.

**Dirty Pipe (CVE-2022-0847)**:
리눅스 커널 취약점으로, 컨테이너에서 읽기 전용 파일을 덮어쓸 수 있었다. 컨테이너 격리 무효화.

**Wasm의 보안 모델**

Wasm은 **언어 수준 샌드박싱**을 제공한다:

**1. 메모리 안전성**

Wasm의 선형 메모리 모델:
```
┌─────────────────────────────────────────┐
│   Wasm Linear Memory (컴파일 시 결정)   │
│  ┌─────────────────────────────────────┐│
│  │ 0x0000  ┌────────┐                  ││
│  │         │ Stack  │                  ││
│  │ 0x1000  ├────────┤                  ││
│  │         │  Heap  │                  ││
│  │ 0x5000  ├────────┤                  ││
│  │         │ (Unused)                  ││
│  │ 0xFFFF  └────────┘                  ││
│  └─────────────────────────────────────┘│
│  범위 밖 접근 → Trap (즉시 종료)        │
└─────────────────────────────────────────┘
```

모든 메모리 접근은 컴파일 시 검증되거나 런타임에 경계 체크:
```wasm
(memory 1)  ;; 1 페이지 (64KB) 할당
(func $safe_read (param $offset i32) (result i32)
  local.get $offset
  i32.load  ;; $offset이 64KB 넘으면 자동 Trap
)
```

**불가능한 공격**:
- 버퍼 오버플로우
- Use-after-free
- Double-free
- 임의 메모리 주소 접근

**2. 제어 흐름 무결성**

Wasm은 간접 호출을 테이블로 제한:
```wasm
(table 10 funcref)  ;; 함수 포인터 테이블 (크기 10)
(func $call_indirect (param $index i32)
  local.get $index
  call_indirect (type 0)  ;; 테이블 범위 체크, 타입 체크
)
```

테이블 범위 밖 호출 → Trap
타입 불일치 → Trap

컨테이너는 이런 보호 없음 (C/C++에서 함수 포인터 조작 가능)

**3. Capability-based 보안 (WASI)**

기본적으로 모든 권한 거부, 명시적 허용 필요:

```bash
# 권한 없음
wasmtime app.wasm
# → 파일 열기 시도 시 "Permission denied"

# /data 읽기만 허용
wasmtime --dir=/data::/ app.wasm
# → /data 외부 접근 시도 시 Trap

# 네트워크 허용 (WASI Preview 2)
wasmtime --allow-network app.wasm
```

컨테이너와의 차이:
```bash
# Docker는 기본적으로 많은 권한 허용
docker run myapp  # 네트워크, 파일시스템 접근 가능

# 제한하려면 명시적 설정 필요
docker run --network=none --read-only myapp
```

**4. 격리 수준**

| 항목 | 컨테이너 | Wasm |
|------|---------|------|
| **커널** | 공유 | 공유 (하지만 syscall 없음) |
| **메모리** | 프로세스 격리 | 언어 수준 샌드박스 |
| **파일시스템** | 네임스페이스 | Capability-based |
| **네트워크** | 네임스페이스 | 런타임 제어 |
| **syscall** | Seccomp 필터 | WASI 추상화 |

**Wasm이 더 안전한 이유**

1. **커널 취약점 무관**: Wasm은 syscall을 직접 호출하지 않고, WASI 추상화를 통해 접근. 런타임이 안전한 방식으로 syscall 변환.

2. **메모리 버그 불가능**: 컴파일 시 검증 + 런타임 경계 체크로 메모리 안전성 보장.

3. **공격 표면 축소**: Wasm 스펙은 수백 페이지, Linux syscall은 수천 개. 공격할 지점이 훨씬 적음.

**Wasm의 한계**

1. **사이드 채널 공격**: Spectre/Meltdown 같은 하드웨어 취약점에는 여전히 노출 (컨테이너도 동일)

2. **런타임 취약점**: Wasmtime/WasmEdge 자체에 버그가 있으면 탈출 가능 (하지만 훨씬 적은 코드베이스)

3. **Host Function 취약점**: 런타임이 제공하는 Host Function이 안전하지 않으면 위험

**실제 보안 비교**

**시나리오: 멀티테넌트 서버리스 플랫폼**

고객이 임의 코드를 업로드해 실행하는 환경:

**컨테이너 접근**:
- 각 고객에게 별도 VM 필요 (AWS Lambda 방식)
- 또는 gVisor/Kata Containers로 커널 격리
- 오버헤드: VM당 수백 MB, 시작 시간 초 단위

**Wasm 접근**:
- 같은 프로세스에서 수천 개 Wasm 모듈 실행 가능
- 메모리 격리는 언어 수준에서 보장
- 오버헤드: 모듈당 KB, 시작 시간 밀리초

**Shopify의 사례**: 상점 스크립트를 Wasm으로 실행
- 이전 (Ruby 샌드박스): 탈출 취약점 빈번
- 현재 (Wasm): 2년간 탈출 사례 0건

**Fastly Compute@Edge**: 수천 고객의 Wasm 앱을 같은 호스트에서 실행
- 격리는 Wasmtime의 샌드박싱에 의존
- 별도 VM/컨테이너 불필요

### 실무 적용
보안 요구사항별 권장:

**높은 보안 (금융, 의료)**:
- VM (Firecracker) + 컨테이너 + Wasm (다층 방어)
- 또는 Wasm 단독 (충분히 안전, 오버헤드 낮음)

**중간 보안 (일반 SaaS)**:
- gVisor + 컨테이너
- 또는 Wasm (멀티테넌트 환경)

**낮은 보안 (내부 도구)**:
- 표준 Docker 컨테이너

보안 감사 체크리스트:
- [ ] Wasm 런타임 버전 최신화 (보안 패치)
- [ ] Host Function 최소화 (공격 표면 축소)
- [ ] Capability 최소 권한 원칙 (--dir, --allow-network 엄격 설정)
- [ ] 메모리 제한 설정 (OOM 공격 방지)
- [ ] 실행 시간 제한 (무한 루프 방지)

결론: Wasm은 언어 수준 샌드박싱으로 컨테이너보다 본질적으로 더 안전하다. 특히 멀티테넌트 환경에서 Wasm은 VM/컨테이너보다 훨씬 경량이면서도 동등 이상의 보안을 제공한다.

---

## Q6. Wasm을 실제 프로덕션에서 사용하는 사례는 무엇이며, 각 사례에서 왜 Wasm을 선택했는가?

### 왜 이 질문이 중요한가
기술 도입 결정은 실제 성공 사례를 보고 내리는 경우가 많다. Wasm이 "미래 기술"이 아닌 "현재 사용 가능한 기술"임을 입증하려면, 프로덕션 사례와 선택 이유를 이해해야 한다. 각 사례에서 Wasm이 해결한 구체적인 문제를 파악하면, 자사 워크로드에 적용 가능한지 판단할 수 있다.

### 답변
**1. Shopify - 상점 스크립트 실행**

**문제**:
- Shopify 상점 주인이 Ruby로 커스텀 할인, 배송 로직을 작성
- 악의적 스크립트가 다른 상점 데이터 접근 위험
- Ruby 샌드박스 탈출 취약점 빈번

**Wasm 도입 전 (Ruby VM)**:
- 각 스크립트를 별도 Ruby 프로세스에서 실행
- 메모리 사용량: 스크립트당 50MB
- 시작 시간: 100~200ms
- 탈출 취약점: 연간 5~10건

**Wasm 도입 후 (AssemblyScript → Wasm)**:
- 같은 프로세스에서 수천 개 Wasm 모듈 실행
- 메모리 사용량: 스크립트당 1~2MB
- 시작 시간: 5ms
- 탈출 시도: 모두 Trap으로 차단

**결과**:
- 인프라 비용 60% 절감
- 체크아웃 속도 30% 향상
- 보안 사고 제로

**왜 Wasm인가**: 멀티테넌트 보안 + 경량 격리 + 빠른 시작

---

**2. Fastly - Compute@Edge CDN**

**문제**:
- 고객이 엣지 로케이션에서 커스텀 로직 실행 필요 (A/B 테스트, 개인화 등)
- 엣지 서버는 리소스 제한적 (컨테이너/VM 부담)
- Cold start 지연 허용 불가 (CDN은 밀리초 단위 응답)

**Wasm 도입 이유**:
- **극단적 시작 속도**: 35μs (마이크로초!)
- **밀도**: 단일 서버에서 수천 고객 격리 실행
- **보안**: Wasmtime 샌드박싱으로 고객 간 격리

**아키텍처**:
```
User Request → Fastly Edge
              ↓
        Wasm Module (고객 코드)
              ↓
        Origin Server (필요 시)
```

**성능**:
- 처리량: 단일 코어에서 100,000 req/sec
- 지연시간: p99 < 10ms
- 메모리: 동시 실행 1000개 모듈 = 2GB

**결과**: Viceroy (로컬 Wasm 개발 도구) 오픈소스화, 수천 고객 Compute@Edge 사용

**왜 Wasm인가**: 엣지 환경의 리소스 제약 + 멀티테넌트 보안 + 초저지연

---

**3. Cloudflare Workers - 서버리스 플랫폼**

**문제**:
- V8 Isolate로 JavaScript 실행 중이었지만, 다른 언어 지원 필요
- 고객이 Rust, C++로 작성한 코드를 엣지에서 실행 요청

**Wasm 도입**:
- JavaScript 외에 Rust, C, C++, Go를 Wasm으로 컴파일 지원
- 동일한 V8 엔진에서 JS와 Wasm 혼용 실행

**성능 비교**:
- JavaScript (JIT): cold start 5ms
- Wasm (AOT): cold start 0.5ms

**사용 사례**:
- 이미지 리사이징 (C++ Wasm)
- 암호화 (Rust Wasm)
- API 게이트웨이 (JS + Wasm 하이브리드)

**결과**: 월 수조 개 요청 처리, Wasm 워크로드 30% 차지

**왜 Wasm인가**: 다중 언어 지원 + V8과의 통합 + 성능

---

**4. BBC - iPlayer 개인화**

**문제**:
- iPlayer (영국 BBC 스트리밍 서비스) 사용자별 추천 로직
- 서버 사이드 렌더링 시 개인화 적용 필요
- 대규모 트래픽 (수백만 동시 사용자)

**Wasm 도입**:
- 추천 알고리즘을 Rust로 작성, Wasm으로 컴파일
- Node.js 서버에서 Wasm 모듈 로드

**성능**:
- Native Rust: 10ms
- Wasm (Wasmtime): 12ms (20% 오버헤드)
- JavaScript 구현: 50ms

**결과**:
- 서버 대수 40% 감소
- 응답 시간 60% 개선
- Rust의 메모리 안전성으로 런타임 에러 90% 감소

**왜 Wasm인가**: 성능 + 메모리 안전성 + 기존 Node.js 인프라 활용

---

**5. Adobe - Photoshop Web**

**문제**:
- 데스크탑 Photoshop (C++)을 브라우저로 이식
- 수백만 줄 레거시 C++ 코드

**Wasm 도입**:
- Emscripten으로 C++ 코드를 Wasm으로 컴파일
- 브라우저에서 네이티브 수준 성능

**성능**:
- 필터 적용: Wasm 500ms vs JavaScript 3000ms
- 메모리: Wasm은 C++ 포인터 그대로 사용 (GC 없음)

**결과**: Photoshop, Illustrator, Premiere Pro 웹 버전 출시

**왜 Wasm인가**: 레거시 C++ 재사용 + 브라우저 성능

---

**6. Figma - 다중 플레이어 디자인 도구**

**문제**:
- 실시간 협업 편집 시 렌더링 성능 중요
- JavaScript만으로는 60fps 유지 어려움

**Wasm 도입**:
- C++로 작성된 렌더링 엔진을 Wasm으로 컴파일
- 브라우저에서 네이티브 앱 수준 성능

**성능**:
- 복잡한 문서 렌더링: Wasm 16ms (60fps) vs JavaScript 100ms

**결과**: 수백만 사용자, 실시간 협업에서도 부드러운 경험

**왜 Wasm인가**: 브라우저에서 네이티브 수준 렌더링 성능

---

**공통 패턴**

모든 사례에서 Wasm을 선택한 이유는 다음 중 하나 이상:

1. **멀티테넌트 보안**: Shopify, Fastly, Cloudflare
2. **극단적 성능**: Figma, Adobe, BBC
3. **엣지/서버리스**: Fastly, Cloudflare
4. **레거시 코드 재사용**: Adobe, Photoshop
5. **리소스 효율**: Shopify, Fastly

### 실무 적용
Wasm 도입 검토 체크리스트:

**Wasm이 적합한 경우**:
- [ ] 멀티테넌트 환경에서 고객 코드 실행
- [ ] 엣지/서버리스에서 cold start가 중요
- [ ] CPU 집약적 워크로드 (암호화, 압축, AI)
- [ ] 브라우저에서 네이티브 수준 성능 필요
- [ ] C/C++ 레거시 코드를 웹으로 이식

**컨테이너가 더 나은 경우**:
- [ ] I/O 집약적 워크로드 (데이터베이스, 파일 처리)
- [ ] 복잡한 네트워킹 (gRPC, 서비스 메시)
- [ ] POSIX API 완전 호환 필요
- [ ] 성숙한 생태계 필요 (Kubernetes, Helm 등)

결론: Wasm은 이미 Shopify, Fastly, Cloudflare, Adobe, Figma 같은 대기업 프로덕션에서 입증되었다. 특히 멀티테넌트, 엣지, 고성능 웹 애플리케이션에서 강점을 보인다.

---

## Q7. Wasm과 컨테이너를 함께 사용하는 하이브리드 아키텍처는 어떤 모습이며, 언제 이런 접근이 필요한가?

### 왜 이 질문이 중요한가
Wasm과 컨테이너는 경쟁 관계가 아니라 상호 보완적이다. 각 기술의 장점을 결합한 하이브리드 아키텍처는 실무에서 더 흔하다. 언제 Wasm을 쓰고, 언제 컨테이너를 쓰며, 어떻게 통합할지 이해하면 최적의 시스템을 설계할 수 있다.

### 답변
**하이브리드 아키텍처의 필요성**

단일 기술만 사용하는 것은 비현실적이다:
- Wasm은 I/O 집약적 워크로드에 약함
- 컨테이너는 멀티테넌트 격리에 무거움
- 기존 인프라(Kubernetes)는 컨테이너 중심

**하이브리드 패턴들**

**패턴 1: 컨테이너 내부에서 Wasm 실행**

컨테이너는 배포/오케스트레이션 단위, Wasm은 실행 단위.

아키텍처:
```
┌─────────────────────────────────────────┐
│         Kubernetes Pod                  │
│  ┌────────────────────────────────────┐ │
│  │      Container                     │ │
│  │  ┌──────────────────────────────┐  │ │
│  │  │  Wasmtime Runtime            │  │ │
│  │  │  ┌────────┐  ┌────────┐      │  │ │
│  │  │  │Wasm    │  │Wasm    │      │  │ │
│  │  │  │Module1 │  │Module2 │      │  │ │
│  │  │  └────────┘  └────────┘      │  │ │
│  │  └──────────────────────────────┘  │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

**장점**:
- Kubernetes의 스케줄링, 네트워킹 활용
- Wasm의 보안 샌드박싱 활용
- 플러그인 업데이트 시 컨테이너 재시작 불필요

**사용 사례**: API 게이트웨이 + Wasm 플러그인 (Kong, Envoy)

---

**패턴 2: Sidecar Wasm**

메인 앱은 컨테이너, 부가 기능은 Wasm.

**장점**:
- 메인 앱은 기존 언어(Python, Node.js) 유지
- 보안 민감 로직(인증, 암호화)만 Wasm으로 격리
- 플러그인 동적 업데이트 (ConfigMap 변경)

**사용 사례**: 인증/인가 플러그인, 로깅/메트릭 수집기

---

**패턴 3: 워크로드 분리**

스테이트풀/I/O는 컨테이너, 스테이트리스/CPU는 Wasm.

**배치 전략**:
- **Wasm 노드**: 경량, 많은 수, 빠른 스케일링
  - HTTP API 핸들러
  - 서버리스 함수
  - 엣지 프록시
- **컨테이너 노드**: 안정적, 스테이트풀
  - 데이터베이스
  - 메시지 큐
  - 파일 스토리지

**장점**:
- 각 워크로드를 최적 기술로 실행
- 리소스 효율 극대화
- 통합 관리 (Kubernetes)

**사용 사례**: 대규모 마이크로서비스 플랫폼

---

**패턴 4: Wasm을 빌드 아티팩트로**

컨테이너 이미지 안에 Wasm 바이너리 포함, 런타임에 선택.

**장점**:
- 단일 이미지로 네이티브/Wasm 양쪽 지원
- A/B 테스트 용이
- 점진적 마이그레이션

**사용 사례**: Wasm 마이그레이션 중 폴백 옵션 유지

---

**패턴 5: 엣지 Wasm + 클라우드 컨테이너**

엣지에는 Wasm, 중앙에는 컨테이너.

**엣지 Wasm 역할**:
- 캐싱, CDN 퍼지
- A/B 테스트 라우팅
- 간단한 인증
- 정적 콘텐츠 변환

**클라우드 컨테이너 역할**:
- 비즈니스 로직
- 데이터베이스 접근
- 복잡한 워크플로우

**장점**:
- 엣지에서 지연시간 최소화
- 클라우드에서 복잡한 로직 처리
- 트래픽 오프로딩 (엣지에서 80% 처리)

**사용 사례**: 글로벌 전자상거래, 스트리밍 플랫폼

---

**하이브리드 선택 가이드**

| 요구사항 | 권장 패턴 |
|---------|----------|
| 플러그인 시스템 필요 | 패턴 1 (컨테이너 내 Wasm) |
| 보안 민감 로직 격리 | 패턴 2 (Sidecar Wasm) |
| 대규모 멀티테넌트 | 패턴 3 (워크로드 분리) |
| 점진적 마이그레이션 | 패턴 4 (빌드 아티팩트) |
| 글로벌 엣지 배포 | 패턴 5 (엣지 Wasm + 클라우드) |

### 실무 적용
하이브리드 도입 로드맵:

**Phase 1 (1~3개월)**: 컨테이너 내 Wasm 실험
- 기존 앱에 Wasm 플러그인 추가
- 성능/보안 검증

**Phase 2 (3~6개월)**: Sidecar 패턴 적용
- 인증/로깅을 Wasm Sidecar로 분리
- Kubernetes와 통합

**Phase 3 (6~12개월)**: 워크로드 분리
- 새 서비스는 Wasm 우선
- 레거시는 컨테이너 유지

**Phase 4 (12개월+)**: 엣지 확장
- Wasm을 CDN 엣지에 배포
- 클라우드는 데이터 레이어만

결론: Wasm과 컨테이너는 "어느 것을 선택할까"가 아닌 "어떻게 결합할까"의 문제다. 하이브리드 아키텍처는 각 기술의 장점을 극대화하며, 실무에서 가장 현실적인 접근이다.
