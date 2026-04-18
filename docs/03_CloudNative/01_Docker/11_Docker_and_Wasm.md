# Chapter 11: Docker and Wasm

## 📌 핵심 요약

> **Wasm(WebAssembly)**은 클라우드 컴퓨팅의 **세 번째 물결**을 이끄는 기술로, 기존 Linux 컨테이너보다 **더 작고, 빠르고, 안전하며, 이식성이 높다**. Docker Desktop은 여러 Wasm 런타임을 내장하고 있어, 익숙한 Docker 도구(`docker build`, `docker run`)로 Wasm 앱을 컨테이너화하고 실행할 수 있다.

---

## 🎯 학습 목표

- [ ] Wasm의 개념과 클라우드 컴퓨팅에서의 위치 이해
- [ ] Docker Desktop의 Wasm 지원 설정
- [ ] Spin 프레임워크로 Wasm 앱 작성 및 빌드
- [ ] Wasm 앱 컨테이너화 및 Docker Hub 배포
- [ ] Wasm 컨테이너 실행

---

## 📖 본문 정리

### 1. 클라우드 컴퓨팅의 세 가지 물결

#### 💬 비유로 이해하기
> VM은 **전체 집**을 통째로 옮기는 것, 컨테이너는 **가구만 포장**해서 옮기는 것, Wasm은 **필수품만 배낭에 넣어** 이동하는 것과 같다. 각 세대마다 더 가볍고, 빠르고, 유연해진다.

```
┌─────────────────────────────────────────────────────────────────┐
│              클라우드 컴퓨팅의 세 가지 물결                       │
└─────────────────────────────────────────────────────────────────┘

  1세대: VM                2세대: 컨테이너           3세대: Wasm
  ────────────             ────────────             ────────────
  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
  │     App      │         │     App      │         │     App      │
  ├──────────────┤         ├──────────────┤         │   (Wasm)     │
  │  Libraries   │         │  Libraries   │         └──────┬───────┘
  ├──────────────┤         └──────┬───────┘                │
  │  Guest OS    │                │                        │
  ├──────────────┤                │                        │
  │ Hypervisor   │         ┌──────┴───────┐         ┌──────┴───────┐
  └──────┬───────┘         │   Container  │         │    Wasm      │
         │                 │   Runtime    │         │   Runtime    │
         │                 └──────┬───────┘         └──────┬───────┘
         │                        │                        │
  ┌──────┴────────────────────────┴────────────────────────┴──────┐
  │                         Host OS                                │
  └────────────────────────────────────────────────────────────────┘

  크기:    큰 (GB)             중간 (MB)              작은 (KB)
  속도:    느림                 빠름                   매우 빠름
  보안:    중간                 중간                   높음
  이식성:  낮음                 높음                   매우 높음
```

#### 세대별 특징 비교

| 특성 | VM | 컨테이너 | Wasm |
|------|-----|----------|------|
| **크기** | GB 단위 | MB 단위 | KB 단위 |
| **시작 시간** | 분 | 초 | 밀리초 |
| **이식성** | 하이퍼바이저 의존 | OS 커널 의존 | 어디서나 실행 |
| **보안** | 하드웨어 격리 | 프로세스 격리 | 샌드박스 격리 |
| **유연성** | 매우 높음 | 높음 | 제한적 |

### 2. Wasm이란?

```
┌─────────────────────────────────────────────────────────────────┐
│                    Wasm 컴파일 및 실행 흐름                       │
└─────────────────────────────────────────────────────────────────┘

  Source Code                    Compilation Target
  ───────────                    ──────────────────

  ┌─────────────┐
  │    Rust     │─────┐
  └─────────────┘     │
                      │
  ┌─────────────┐     │         ┌─────────────────┐
  │     Go      │─────┼────────►│   .wasm 바이너리 │
  └─────────────┘     │         │  (WebAssembly)  │
                      │         └────────┬────────┘
  ┌─────────────┐     │                  │
  │    C/C++    │─────┘                  │
  └─────────────┘                        │
                                         │
                                         ▼
                           ┌─────────────────────────┐
                           │      Wasm Runtime       │
                           │  ┌─────┐ ┌─────┐ ┌────┐│
                           │  │spin │ │wasm │ │was ││
                           │  │time │ │edge │ │mer ││
                           │  └─────┘ └─────┘ └────┘│
                           └─────────────────────────┘
                                         │
                                         ▼
                               어디서나 실행 가능
                           (Mac, Windows, Linux, Edge...)
```

**Wasm의 특징**:
- 새로운 가상 머신 아키텍처
- 언어에 상관없이 동일한 바이너리로 컴파일
- Wasm 런타임만 있으면 어디서나 실행

**현재 적합한 워크로드**:
- ✅ AI 워크로드
- ✅ 서버리스 함수
- ✅ 플러그인
- ✅ 엣지 디바이스

**현재 부적합한 워크로드**:
- ❌ 복잡한 네트워킹
- ❌ 무거운 I/O 작업

### 3. 사전 요구사항

#### 필요한 도구

| 도구 | 버전 | 용도 |
|------|------|------|
| Docker Desktop | 4.37+ | Wasm 컨테이너 실행 |
| Rust | 1.82+ | Wasm 앱 개발 |
| Spin | 3.1+ | Wasm 프레임워크/런타임 |

#### Docker Desktop Wasm 설정

```
Docker Desktop → Settings
├── General
│   └── ☑ Use containerd for pulling and storing images
└── Features in development
    └── ☑ Enable Wasm
    → Apply & restart
```

#### Rust Wasm 타겟 설치

```bash
# Wasm 타겟 추가
$ rustup target add wasm32-wasip1
info: downloading component 'rust-std' for 'wasm32-wasip1'
info: installing component 'rust-std' for 'wasm32-wasip1'
```

### 4. Docker Desktop의 Wasm 런타임

```bash
# 설치된 Wasm 런타임 확인
$ docker run --rm -i --privileged --pid=host \
  jorgeprendes420/docker-desktop-shim-manager:latest

io.containerd.wasmtime.v1
io.containerd.wws.v1
io.containerd.slight.v1
io.containerd.wasmer.v1
io.containerd.spin.v2         # ← 이 장에서 사용
io.containerd.lunatic.v1
io.containerd.wasmedge.v1
```

```
┌─────────────────────────────────────────────────────────────────┐
│                Docker Desktop Wasm 런타임 구조                   │
└─────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                      containerd                              │
  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐ │
  │  │wasmtime │ │wasmedge │ │ wasmer  │ │  spin   │ │lunatic │ │
  │  │  .v1    │ │   .v1   │ │   .v1   │ │   .v2   │ │  .v1   │ │
  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └───┬────┘ │
  │       │           │           │           │          │      │
  │       └───────────┴─────┬─────┴───────────┴──────────┘      │
  │                         │                                    │
  │                         ▼                                    │
  │               ┌─────────────────┐                            │
  │               │  Wasm Container │                            │
  │               │  (.wasm binary  │                            │
  │               │   in scratch)   │                            │
  │               └─────────────────┘                            │
  └─────────────────────────────────────────────────────────────┘
```

### 5. Wasm 앱 작성 (Spin 사용)

#### 프로젝트 생성

```bash
# 새 Wasm 앱 생성
$ spin new hello-world -t http-rust
Description: Wasm app
HTTP path: /hello

# 디렉토리 구조
$ cd hello-world && tree
.
├── Cargo.toml      # Rust 패키지 설정
├── spin.toml       # Spin 앱 설정
└── src
    └── lib.rs      # 앱 소스 코드
```

#### 소스 코드 수정 (src/lib.rs)

```rust
use spin_sdk::http::{IntoResponse, Request, Response};
// ...
    Ok(http::Response::builder()
        .status(200)
        .header("content-type", "text/plain")
        .body("Docker loves Wasm")?)  // ← 응답 메시지 수정
        .build())
}
```

#### 빌드 및 로컬 테스트

```bash
# Wasm 바이너리로 컴파일
$ spin build
Building component hello-world with `cargo build --target wasm32-wasip1 --release`
Finished building all Spin components

# 빌드 결과 확인
$ tree target/wasm32-wasip1/release/
└── hello_world.wasm    # ← Wasm 바이너리 (104KB)

# 로컬 실행 테스트
$ spin up
Serving http://127.0.0.1:3000
Available Routes:
  hello-world: http://127.0.0.1:3000/hello

# 브라우저에서 http://127.0.0.1:3000/hello 접속
# → "Docker loves Wasm" 표시
```

### 6. Wasm 앱 컨테이너화

#### Dockerfile 작성

```dockerfile
FROM scratch                                        # 빈 베이스 이미지 (OS 불필요)
COPY /target/wasm32-wasip1/release/hello_world.wasm .  # Wasm 바이너리 복사
COPY spin.toml .                                    # Spin 설정 파일 복사
```

#### spin.toml 수정

```toml
# 변경 전
[component.hello-world]
source = "target/wasm32-wasip1/release/hello_world.wasm"

# 변경 후 (이미지 내 경로에 맞춤)
[component.hello-world]
source = "hello_world.wasm"
```

#### 이미지 빌드 및 푸시

```bash
# Wasm 이미지 빌드
$ docker build \
  --platform wasi/wasm \
  --provenance=false \
  -t myuser/ddd-book:wasm .

# 이미지 확인
$ docker images
REPOSITORY       TAG    SIZE
myuser/ddd-book  wasm   104kB    # ← 매우 작은 크기!

# Docker Hub에 푸시
$ docker push myuser/ddd-book:wasm
```

```
┌─────────────────────────────────────────────────────────────────┐
│                  Wasm 컨테이너 이미지 구조                        │
└─────────────────────────────────────────────────────────────────┘

  일반 Linux 컨테이너                    Wasm 컨테이너
  ─────────────────────                 ─────────────────────

  ┌─────────────────────┐               ┌─────────────────────┐
  │       App           │               │   hello_world.wasm  │
  ├─────────────────────┤               ├─────────────────────┤
  │    Libraries        │               │     spin.toml       │
  ├─────────────────────┤               ├─────────────────────┤
  │   Base Image        │               │      scratch        │
  │   (alpine 등)       │               │      (비어있음)      │
  └─────────────────────┘               └─────────────────────┘
       ~50MB+                                ~104KB

  • Guest OS 포함                        • OS 없음
  • 라이브러리 포함                       • Wasm 바이너리만
  • 취약점 스캔 가능                      • 취약점 스캔 불가 (아직)
```

### 7. Wasm 컨테이너 실행

```bash
# Wasm 컨테이너 실행
$ docker run -d --name wasm-ctr \
  --runtime=io.containerd.spin.v2 \   # Spin Wasm 런타임 지정
  --platform=wasi/wasm \              # Wasm 플랫폼 지정
  -p 5556:80 \                        # 포트 매핑
  myuser/ddd-book:wasm /

# 컨테이너 상태 확인
$ docker ps
CONTAINER ID   IMAGE                  STATUS    PORTS
abc123...      myuser/ddd-book:wasm   Up        0.0.0.0:5556->80/tcp

# 브라우저에서 http://localhost:5556/hello 접속
# → "Docker loves Wasm" 표시
```

#### 명령어 플래그 설명

| 플래그 | 설명 |
|--------|------|
| `--runtime=io.containerd.spin.v2` | Spin Wasm 런타임 사용 |
| `--platform=wasi/wasm` | Wasm 플랫폼 지정 |
| `-p 5556:80` | 호스트 5556 → 컨테이너 80 포트 매핑 |

### 8. 정리

```bash
# 컨테이너 삭제
$ docker rm wasm-ctr -f

# 로컬 이미지 삭제
$ docker rmi myuser/ddd-book:wasm
```

---

## 🔍 심화 학습

### Wasm 생태계
- **WASI (WebAssembly System Interface)**: Wasm이 시스템 리소스에 접근하기 위한 표준 인터페이스
- **Component Model**: Wasm 모듈 간 상호작용을 위한 새로운 표준

### 주요 Wasm 런타임 비교

| 런타임 | 특징 | 용도 |
|--------|------|------|
| **Wasmtime** | Bytecode Alliance 공식 | 범용, 안정적 |
| **Wasmer** | 가장 빠른 실행 속도 | 성능 중시 |
| **WasmEdge** | 클라우드 네이티브 최적화 | K8s, 서버리스 |
| **Spin** | 서버리스 프레임워크 | 마이크로서비스 |

### 추가 학습 주제
- Spin 고급 기능 (key-value store, SQL 등)
- Kubernetes에서 Wasm 워크로드 실행
- WasmCloud, Fermyon Cloud 등 Wasm PaaS

---

## 💡 실무 적용 포인트

### 면접 대비 질문

**Q1: Wasm이 클라우드 컴퓨팅의 '세 번째 물결'이라 불리는 이유는?**
> **A**: 첫 번째 물결(VM)은 하드웨어 가상화, 두 번째 물결(컨테이너)은 OS 수준 가상화를 도입했다. Wasm은 더 작고, 빠르고, 안전하며, 진정한 "한 번 컴파일, 어디서나 실행" 이식성을 제공하는 세 번째 진화이다.

**Q2: Wasm 컨테이너가 일반 Linux 컨테이너보다 작은 이유는?**
> **A**: Wasm 컨테이너는 `scratch`(빈) 베이스 이미지를 사용하고 Guest OS나 라이브러리가 필요 없다. Wasm 바이너리와 설정 파일만 포함하므로 KB 단위의 매우 작은 크기를 유지한다.

**Q3: Docker에서 Wasm 컨테이너를 실행할 때 `--runtime` 플래그가 필요한 이유는?**
> **A**: Docker Desktop은 여러 Wasm 런타임(spin, wasmtime, wasmer 등)을 지원한다. `--runtime` 플래그로 어떤 Wasm 런타임을 사용할지 지정해야 하며, 각 런타임은 다른 기능과 성능 특성을 가진다.

**Q4: 현재 Wasm이 적합한/부적합한 워크로드는?**
> **A**: Wasm은 AI 워크로드, 서버리스 함수, 플러그인, 엣지 디바이스에 적합하다. 하지만 복잡한 네트워킹이나 무거운 I/O 작업에는 아직 제한적이다. 이는 WASI 표준이 계속 발전하면서 개선될 예정이다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Wasm의 개념과 클라우드 컴퓨팅 세대별 비교 설명 가능
- [ ] Wasm이 언어에 독립적인 컴파일 타겟인 이유 이해
- [ ] Wasm 컨테이너와 일반 Linux 컨테이너 차이점 파악
- [ ] Wasm의 적합/부적합 워크로드 구분

### 환경 설정
- [ ] Docker Desktop에서 containerd 및 Wasm 활성화
- [ ] Rust wasm32-wasip1 타겟 설치
- [ ] Spin 프레임워크 설치 및 버전 확인
- [ ] Docker Desktop의 Wasm 런타임 목록 확인

### Wasm 앱 개발
- [ ] `spin new`로 프로젝트 생성
- [ ] `spin build`로 Wasm 바이너리 컴파일
- [ ] `spin up`으로 로컬 테스트

### 컨테이너화 및 실행
- [ ] `FROM scratch` 기반 Dockerfile 작성
- [ ] `--platform wasi/wasm` 플래그로 이미지 빌드
- [ ] Docker Hub에 Wasm 이미지 푸시
- [ ] `--runtime=io.containerd.spin.v2`로 컨테이너 실행

### 실무 적용
- [ ] 서버리스/엣지 워크로드에 Wasm 적용 검토
- [ ] 기존 컨테이너 vs Wasm 컨테이너 선택 기준 수립

---

## 🔗 참고 자료

- [Docker Desktop Wasm 공식 문서](https://docs.docker.com/desktop/wasm/)
- [Fermyon Spin](https://developer.fermyon.com/spin)
- [WebAssembly.org](https://webassembly.org/)
- [WASI (WebAssembly System Interface)](https://wasi.dev/)
- [Bytecode Alliance](https://bytecodealliance.org/)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 11
