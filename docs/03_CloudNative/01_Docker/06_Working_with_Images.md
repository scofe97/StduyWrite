# Chapter 6: Working with Images

## 📌 핵심 요약

> **Docker 이미지는 애플리케이션 실행에 필요한 모든 것을 포함하는 읽기 전용 패키지다.**
> 이미지는 독립적인 레이어들의 스택으로 구성되며, 하나의 이미지로 여러 컨테이너를 생성할 수 있다.
> 이미지는 빌드 타임(build-time) 구조물이고, 컨테이너는 런타임(run-time) 구조물이다.

---

## 🎯 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- [ ] Docker 이미지의 개념과 구조 이해
- [ ] 이미지 Pull/Push 명령어 활용
- [ ] 레지스트리와 리포지토리 차이점 파악
- [ ] 이미지 태그와 다이제스트(Digest) 이해
- [ ] 레이어 구조와 공유 메커니즘 파악
- [ ] 멀티 아키텍처 이미지 개념 이해
- [ ] Docker Scout로 취약점 스캔 수행
- [ ] 이미지 삭제 및 관리

---

## 📖 본문 정리

### 1. Docker 이미지란?

#### 핵심 개념

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Image                             │
├─────────────────────────────────────────────────────────────┤
│  📦 애플리케이션 코드 (Application Code)                      │
│  📚 의존성 (Dependencies)                                    │
│  🖥️  최소한의 OS 구성요소 (Minimal OS Constructs)             │
│  📋 메타데이터 (Metadata)                                    │
└─────────────────────────────────────────────────────────────┘
```

💬 **비유**:
- **VM 템플릿**: 정지된 VM과 비슷 → 이미지는 정지된 컨테이너
- **클래스와 객체**: 클래스에서 여러 객체 생성 → 이미지에서 여러 컨테이너 생성

#### 이미지 특징

| 특징 | 설명 |
|------|------|
| **읽기 전용** | 이미지 자체는 수정 불가 |
| **레이어 구조** | 독립적인 레이어들의 스택 |
| **작은 크기** | NGINX ~80MB, Redis ~40MB |
| **커널 미포함** | 호스트 커널 사용 |

```
┌────────────────────────────────────────────────────────────┐
│                    Build vs Run                             │
├────────────────────────────────────────────────────────────┤
│                                                            │
│   ┌─────────┐         ┌─────────────┐                      │
│   │  Image  │ ──────► │ Container 1 │                      │
│   │ (Build  │         └─────────────┘                      │
│   │  Time)  │         ┌─────────────┐                      │
│   │         │ ──────► │ Container 2 │                      │
│   └─────────┘         └─────────────┘                      │
│                       ┌─────────────┐                      │
│               ──────► │ Container 3 │                      │
│                       └─────────────┘                      │
│                         (Run Time)                         │
└────────────────────────────────────────────────────────────┘
```

#### Slim 이미지

```
┌─────────────────────────────────────────────────────────────┐
│                   일반 이미지 vs Slim 이미지                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  일반 이미지:                    Slim 이미지:                │
│  ┌─────────────────┐            ┌─────────────────┐         │
│  │ 여러 Shell      │            │ 애플리케이션     │         │
│  │ 패키지 매니저    │            │ 필수 의존성만    │         │
│  │ 디버그 도구     │            │                 │         │
│  │ 애플리케이션    │            │                 │         │
│  └─────────────────┘            └─────────────────┘         │
│       ~500MB                         ~3MB                   │
│                                                             │
│  예: Alpine Linux = ~3MB (Shell, 패키지 매니저 최소화)        │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. 이미지 Pull

#### 기본 명령어

```bash
# 이미지 Pull
$ docker pull redis
Using default tag: latest              # 기본값: latest 태그
latest: Pulling from library/redis     # 기본값: Docker Hub
08df40659127: Download complete        # 레이어 다운로드
4f4fb700ef54: Already exists           # 이미 존재하는 레이어 (스킵)
...
Digest: sha256:76d5908f5e19...
Status: Downloaded newer image for redis:latest
docker.io/library/redis:latest         # docker.io = Docker Hub

# 로컬 이미지 확인
$ docker images
REPOSITORY   TAG     IMAGE ID        CREATED       SIZE
redis        latest  11c3e418c296    2 weeks ago   223MB
```

#### Docker의 기본 가정

```
┌─────────────────────────────────────────────────────────────┐
│                   docker pull redis                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 태그 미지정 → latest 태그 가정                           │
│     docker pull redis = docker pull redis:latest            │
│                                                             │
│  2. 레지스트리 미지정 → Docker Hub 가정                       │
│     docker pull redis = docker pull docker.io/library/redis │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 3. 이미지 레지스트리

#### 레지스트리 아키텍처

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Registry (레지스트리)                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│   │  Repository   │  │  Repository   │  │  Repository   │          │
│   │    (nginx)    │  │   (redis)     │  │   (alpine)    │          │
│   ├───────────────┤  ├───────────────┤  ├───────────────┤          │
│   │ Image:latest  │  │ Image:latest  │  │ Image:latest  │          │
│   │ Image:1.25    │  │ Image:8.0     │  │ Image:3.19    │          │
│   │ Image:1.24    │  │ Image:7.2     │  │ Image:3.18    │          │
│   └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Build > Share > Run 파이프라인

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│     ┌───────┐      ┌────────────┐      ┌───────┐           │
│     │ Build │ ───► │  Registry  │ ───► │  Run  │           │
│     │       │      │            │      │       │           │
│     │ Dev   │      │  (Docker   │      │ Ops   │           │
│     │ Env   │      │   Hub)     │      │ Env   │           │
│     └───────┘      └────────────┘      └───────┘           │
│                                                             │
│         Push              Store              Pull           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 주요 레지스트리

| 레지스트리 | URL | 특징 |
|-----------|-----|------|
| **Docker Hub** | docker.io | 기본 레지스트리, Official Images |
| **GHCR** | ghcr.io | GitHub Container Registry |
| **GCR** | gcr.io | Google Container Registry |
| **ECR** | *.ecr.aws | AWS Container Registry |
| **ACR** | *.azurecr.io | Azure Container Registry |

#### Official vs Unofficial 리포지토리

```
┌─────────────────────────────────────────────────────────────┐
│              Official Repository (공식)                      │
├─────────────────────────────────────────────────────────────┤
│  URL: https://hub.docker.com/_/nginx                        │
│  특징:                                                       │
│  ✅ Docker와 벤더가 검증 및 큐레이션                          │
│  ✅ 최신 보안 패치                                           │
│  ✅ 좋은 문서화                                              │
│  ✅ 모범 사례 준수                                           │
│  ✅ Top-level namespace (library/)                          │
│  ✅ 녹색 "Docker Official Image" 배지                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│             Unofficial Repository (비공식)                   │
├─────────────────────────────────────────────────────────────┤
│  URL: https://hub.docker.com/r/nigelpoulton/gsd             │
│  특징:                                                       │
│  ⚠️  Second-level namespace (nigelpoulton/)                 │
│  ⚠️  품질 보장 없음                                          │
│  ⚠️  보안 검증 없음                                          │
│  ⚠️  기본적으로 신뢰하지 말 것                                │
└─────────────────────────────────────────────────────────────┘
```

---

### 4. 이미지 이름과 태그

#### 완전한 이미지 이름 구조 (FQIN)

```
┌─────────────────────────────────────────────────────────────┐
│           Fully Qualified Image Name (FQIN)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ghcr.io/regclient/regsync:latest                           │
│  ├──────┤ ├────────┤├──────┤├─────┤                         │
│  Registry  User/Org  Repo   Tag                             │
│                                                             │
│  ┌─────────────┬──────────────────────────────────────────┐ │
│  │ 구성요소     │ 설명                                     │ │
│  ├─────────────┼──────────────────────────────────────────┤ │
│  │ Registry    │ 레지스트리 DNS (기본: docker.io)          │ │
│  │ User/Org    │ 사용자/조직명 (Official은 library)        │ │
│  │ Repository  │ 리포지토리명                              │ │
│  │ Tag         │ 이미지 태그 (기본: latest)                │ │
│  └─────────────┴──────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### Pull 명령어 예시

```bash
# Official 리포지토리에서 Pull
$ docker pull redis:latest           # Docker Hub, latest 태그
$ docker pull redis:8.0-M02          # 특정 버전 태그
$ docker pull busybox:glibc          # glibc 태그
$ docker pull alpine                 # latest 태그 생략

# Unofficial 리포지토리에서 Pull
$ docker pull nigelpoulton/tu-demo:v2

# 다른 레지스트리에서 Pull
$ docker pull ghcr.io/regclient/regsync:latest
```

#### 하나의 이미지에 여러 태그

```bash
$ docker images
REPOSITORY               TAG       IMAGE ID       SIZE
nigelpoulton/tu-demo     latest    b4210d0aa52f   115MB  # 같은 이미지
nigelpoulton/tu-demo     v1        b4210d0aa52f   115MB  # 같은 이미지
nigelpoulton/tu-demo     v2        6ba12825d092   115MB  # 다른 이미지
```

⚠️ **주의**: `latest` 태그가 항상 최신 이미지를 가리키지 않음!

---

### 5. 이미지와 레이어

#### 레이어 스택 구조

```
┌─────────────────────────────────────────────────────────────┐
│                    이미지 레이어 구조                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌─────────────────┐                      │
│     Layer 4       │  App Source     │  <- 애플리케이션 코드  │
│                    └─────────────────┘                      │
│                           ▲                                 │
│                    ┌─────────────────┐                      │
│     Layer 3       │  Python 3.x     │  <- 런타임           │
│                    └─────────────────┘                      │
│                           ▲                                 │
│                    ┌─────────────────┐                      │
│     Layer 2       │  Dependencies   │  <- 의존성           │
│                    └─────────────────┘                      │
│                           ▲                                 │
│                    ┌─────────────────┐                      │
│     Layer 1       │  Ubuntu 24.04   │  <- Base Layer       │
│     (Base)        └─────────────────┘                      │
│                                                             │
│     ═══════════════════════════════════                     │
│           Unified View (단일 이미지)                         │
└─────────────────────────────────────────────────────────────┘
```

#### 레이어 확인 방법

```bash
# 1. Pull 시 레이어 확인
$ docker pull node:latest
latest: Pulling from library/node
952132ac251a: Pull complete    # Layer 1
82659f8f1b76: Pull complete    # Layer 2
c19118ca682d: Pull complete    # Layer 3
8296858250fe: Pull complete    # Layer 4
24e0251a0e2c: Pull complete    # Layer 5
Digest: sha256:f4691c96e6bbaa99d...
Status: Downloaded newer image for node:latest

# 2. docker inspect로 레이어 확인
$ docker inspect node:latest
"RootFS": {
    "Type": "layers",
    "Layers": [
        "sha256:c8a75145fc...",
        "sha256:c6f2b330b6...",
        "sha256:055757a193...",
        "sha256:4837348061...",
        "sha256:0cad5e07ba..."
    ]
}

# 3. docker history로 빌드 히스토리 확인
$ docker history node:latest
```

#### 레이어 파일 오버레이

```
┌─────────────────────────────────────────────────────────────┐
│                  레이어 파일 오버레이                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 3:  File 7 (수정됨)                                   │
│            ┌───────┐                                        │
│            │File 7 │  ← File 5의 업데이트 버전               │
│            └───────┘                                        │
│                                                             │
│  Layer 2:  File 4, File 5, File 6                           │
│            ┌───────┬───────┬───────┐                        │
│            │File 4 │File 5 │File 6 │  ← File 5는 가려짐      │
│            └───────┴───────┴───────┘                        │
│                                                             │
│  Layer 1:  File 1, File 2, File 3                           │
│            ┌───────┬───────┬───────┐                        │
│            │File 1 │File 2 │File 3 │                        │
│            └───────┴───────┴───────┘                        │
│                                                             │
│  ═══════════════════════════════════════════════════════    │
│  Unified View:                                              │
│  ┌───────┬───────┬───────┬───────┬───────┬───────┐         │
│  │File 1 │File 2 │File 3 │File 4 │File 6 │File 7 │         │
│  └───────┴───────┴───────┴───────┴───────┴───────┘         │
│                                                             │
│  → 총 6개 파일만 보임 (File 5는 File 7에 의해 가려짐)         │
└─────────────────────────────────────────────────────────────┘
```

#### 레이어 공유

```
┌─────────────────────────────────────────────────────────────┐
│                    레이어 공유 메커니즘                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│    Image A              Image B              Local Storage  │
│  ┌─────────┐          ┌─────────┐          ┌─────────────┐ │
│  │ Layer 3 │          │ Layer 4 │          │   Layer 1   │ │
│  ├─────────┤          ├─────────┤          │   Layer 2   │ │
│  │ Layer 2 │──────────│ Layer 2 │──────────│   Layer 3   │ │
│  ├─────────┤   공유    ├─────────┤          │   Layer 4   │ │
│  │ Layer 1 │──────────│ Layer 1 │──────────│             │ │
│  └─────────┘          └─────────┘          └─────────────┘ │
│                                                             │
│  $ docker pull redis                                        │
│  4f4fb700ef54: Already exists  ← 공유 레이어, 다운로드 스킵   │
│                                                             │
│  ✅ 스토리지 절약                                            │
│  ✅ 네트워크 대역폭 절약                                     │
│  ✅ Pull/Push 속도 향상                                      │
└─────────────────────────────────────────────────────────────┘
```

#### Storage Driver

| 드라이버 | 설명 |
|---------|------|
| **overlay2** | 기본 드라이버, 대부분의 환경에서 사용 |
| **zfs** | ZFS 파일시스템 사용 시 |
| **btrfs** | Btrfs 파일시스템 사용 시 |
| **vfs** | 테스트용, 비효율적 |

---

### 6. 다이제스트(Digest)로 이미지 Pull

#### 태그의 문제점

```
┌─────────────────────────────────────────────────────────────┐
│                 태그의 문제점 (Mutable Tags)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  시나리오: golftrack:1.5 이미지에 취약점 발견                  │
│                                                             │
│  Before:                       After:                       │
│  golftrack:1.5 ────────►       golftrack:1.5 ────────►      │
│  (취약한 이미지)                 (수정된 이미지)               │
│                                                             │
│  ⚠️ 문제: 같은 태그, 다른 이미지!                             │
│  → 프로덕션에서 어떤 컨테이너가 취약한 버전인지 구분 불가       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 다이제스트 (Content Hash)

```
┌─────────────────────────────────────────────────────────────┐
│                     이미지 다이제스트                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Digest = 이미지 콘텐츠의 암호화 해시 (SHA256)                 │
│                                                             │
│  특징:                                                       │
│  ✅ Immutable (불변) - 내용이 바뀌면 해시도 바뀜              │
│  ✅ 고유성 보장 - 같은 다이제스트 = 같은 이미지               │
│  ✅ 변조 감지 가능                                           │
│                                                             │
│  예시:                                                       │
│  sha256:c5b1261d6d3e43071626931fc004f70149baeba2c8ec672...  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 다이제스트 확인 및 사용

```bash
# 로컬 이미지 다이제스트 확인
$ docker images --digests alpine
REPOSITORY   TAG       DIGEST                       IMAGE ID       SIZE
alpine       latest    sha256:c5b1261d...8e1ad6b    c5b1261d6d3e   11.8MB

# 리모트 이미지 다이제스트 확인 (Pull 전)
$ docker buildx imagetools inspect nigelpoulton/k8sbook:latest
Digest: sha256:13dd59a0c74e9a147800039b1ff4d61201375c008b96a29c5bd17244bce2e14b

# 다이제스트로 Pull (@ 사용)
$ docker pull nigelpoulton/k8sbook@sha256:13dd59a0c74e9a147800039b1ff4d61201375c008b96a29c5bd17244bce2e14b
```

#### Content Hash vs Distribution Hash

```
┌─────────────────────────────────────────────────────────────┐
│              두 가지 해시 (Content vs Distribution)           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │   Content Hash   │      │Distribution Hash │            │
│  │  (비압축 상태)    │      │  (압축 상태)      │            │
│  └────────┬─────────┘      └────────┬─────────┘            │
│           │                         │                       │
│           ▼                         ▼                       │
│     로컬 저장 시                Push/Pull 시                 │
│     레이어 검증                 네트워크 전송 검증             │
│                                                             │
│  ⚠️ CLI 출력에서 해시가 다르게 보일 수 있음                   │
│     (Content Hash를 보는지, Distribution Hash를 보는지에 따라) │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. 멀티 아키텍처 이미지

#### Manifest List 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Multi-Architecture Image                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│                     ┌─────────────────────┐                         │
│                     │   Manifest List     │                         │
│                     │   (alpine:latest)   │                         │
│                     └──────────┬──────────┘                         │
│                                │                                    │
│          ┌─────────────────────┼─────────────────────┐              │
│          │                     │                     │              │
│          ▼                     ▼                     ▼              │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐       │
│  │   Manifest    │    │   Manifest    │    │   Manifest    │       │
│  │ linux/amd64   │    │ linux/arm64   │    │ linux/arm/v7  │       │
│  └───────┬───────┘    └───────┬───────┘    └───────┬───────┘       │
│          │                    │                    │                │
│          ▼                    ▼                    ▼                │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐       │
│  │    Layers     │    │    Layers     │    │    Layers     │       │
│  │   for amd64   │    │   for arm64   │    │   for arm/v7  │       │
│  └───────────────┘    └───────────────┘    └───────────────┘       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 지원 아키텍처 확인

```bash
$ docker buildx imagetools inspect alpine
Name:      docker.io/library/alpine:latest
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:c5b1261d...

Manifests:
  Platform:  linux/amd64
  Platform:  linux/arm/v6
  Platform:  linux/arm/v7
  Platform:  linux/arm64/v8
  Platform:  linux/386
  Platform:  linux/ppc64le

$ docker manifest inspect golang | grep 'architecture\|os'
"architecture": "amd64", "os": "linux"
"architecture": "arm64", "os": "linux"
"architecture": "amd64", "os": "windows"
```

#### 멀티 아키텍처 Pull 흐름

```
┌─────────────────────────────────────────────────────────────┐
│               Multi-Arch Pull 프로세스                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. docker pull alpine:latest                               │
│              │                                              │
│              ▼                                              │
│  2. Registry API에 Manifest List 요청                        │
│              │                                              │
│              ▼                                              │
│  3. 호스트 아키텍처 확인 (예: linux/arm64)                    │
│              │                                              │
│              ▼                                              │
│  4. Manifest List에서 해당 아키텍처 Manifest 찾기             │
│              │                                              │
│              ▼                                              │
│  5. Manifest에서 레이어 목록 추출                            │
│              │                                              │
│              ▼                                              │
│  6. 각 레이어 Pull 및 조립                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 멀티 아키텍처 빌드

```bash
# docker buildx로 멀티 아키텍처 빌드

# 1. Emulation (QEMU) - 느리지만 로컬에서 가능
$ docker buildx build \
  --platform=linux/amd64,linux/arm64 \
  -t myimage:latest --push .

# 2. Docker Build Cloud - 빠르고 네이티브 하드웨어 사용
$ docker buildx build \
  --builder=cloud-nigelpoulton-ddd-cloud \
  --platform=linux/amd64,linux/arm64 \
  -t nigelpoulton/tu-demo:latest --push .
```

| 빌드 방식 | 장점 | 단점 |
|----------|------|------|
| **Emulation** | 로컬에서 무료 | 느림, 캐시 공유 안됨 |
| **Build Cloud** | 빠름, 네이티브 | 유료 구독 필요 |

---

### 8. Docker Scout (취약점 스캔)

#### 빠른 개요 (Quickview)

```bash
$ docker scout quickview nigelpoulton/tu-demo:latest

    ✓ SBOM of image already cached, 66 packages indexed

  Target             │  nigelpoulton/tu-demo:latest  │    0C     1H     1M     0L
    digest           │  b4210d0aa52f                 │
  Base image         │  python:3-alpine              │    0C     1H     1M     0L

# C = Critical, H = High, M = Medium, L = Low
```

#### 상세 취약점 정보 (CVEs)

```bash
$ docker scout cves nigelpoulton/tu-demo:latest

## Packages and Vulnerabilities
   0C     1H     1M     0L  expat 2.5.0-r2

    ✗ HIGH CVE-2023-52425
      https://scout.docker.com/v/CVE-2023-52425
      Affected range : <2.6.0-r0
      Fixed version  : 2.6.0-r0    ← 수정 버전 안내
```

#### Docker Scout 통합

```
┌─────────────────────────────────────────────────────────────┐
│                   Docker Scout 통합 환경                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Docker    │    │   Docker    │    │   Docker    │     │
│  │    CLI      │    │   Desktop   │    │    Hub      │     │
│  │             │    │             │    │             │     │
│  │ docker scout│    │   GUI 뷰    │    │ 리포지토리   │     │
│  │  quickview  │    │  취약점     │    │   스캔      │     │
│  │  cves       │    │  대시보드   │    │             │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            ▼                                │
│                  ┌─────────────────┐                        │
│                  │ scout.docker.com│                        │
│                  │    포털         │                        │
│                  │  - 대시보드     │                        │
│                  │  - 정책 설정    │                        │
│                  │  - 통합 관리    │                        │
│                  └─────────────────┘                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 9. 이미지 삭제

#### 기본 삭제 명령어

```bash
# 이름으로 삭제
$ docker rmi redis:latest

# 짧은 ID로 삭제
$ docker rmi af111729d35a

# SHA로 삭제
$ docker rmi sha256:c5b1261d...f8e1ad6b

# 여러 이미지 한 번에 삭제
$ docker rmi redis:latest af111729d35a sha256:c5b1261d...

# 모든 이미지 삭제 (주의!)
$ docker rmi $(docker images -q) -f
```

#### 삭제 제한 사항

```
┌─────────────────────────────────────────────────────────────┐
│                    이미지 삭제 제한                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  삭제 불가 상황:                                             │
│  ❌ 컨테이너가 해당 이미지를 사용 중                          │
│  ❌ 여러 태그가 같은 이미지 참조 (모든 태그 삭제 필요)          │
│                                                             │
│  강제 삭제 (-f):                                             │
│  $ docker rmi -f myimage:latest                             │
│  ⚠️ 컨테이너가 사용 중인 이미지 강제 삭제 시                  │
│     → Dangling Image로 남음 (Untagged 상태)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 10. 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `docker pull <image>` | 이미지 다운로드 |
| `docker images` | 로컬 이미지 목록 |
| `docker images --digests` | 다이제스트 포함 목록 |
| `docker inspect <image>` | 이미지 상세 정보 |
| `docker history <image>` | 빌드 히스토리 |
| `docker manifest inspect <image>` | Manifest List 조회 |
| `docker buildx imagetools inspect <image>` | 멀티 아키텍처 정보 |
| `docker scout quickview <image>` | 취약점 빠른 개요 |
| `docker scout cves <image>` | 취약점 상세 정보 |
| `docker rmi <image>` | 이미지 삭제 |

---

## 🔍 심화 학습

### 핵심 개념 비교

| 개념 | 설명 | 비유 |
|------|------|------|
| **Image** | 읽기 전용 패키지 | 클래스, VM 템플릿 |
| **Layer** | 이미지 구성 단위 | 레이어 케이크 층 |
| **Tag** | 이미지 이름 (Mutable) | 별명 |
| **Digest** | 이미지 해시 (Immutable) | 주민등록번호 |
| **Manifest** | 레이어 목록 | 목차 |
| **Manifest List** | 아키텍처별 Manifest 목록 | 멀티 에디션 목록 |

### 추가 학습 자료

- [Docker Hub Official Images](https://hub.docker.com/search?q=&type=image&image_filter=official)
- [OCI Image Specification](https://github.com/opencontainers/image-spec)
- [Docker Scout Documentation](https://docs.docker.com/scout/)

---

## 💡 실무 적용 포인트

### 면접 대비 질문

1. **Q: Docker 이미지와 컨테이너의 차이점은?**
   > A: 이미지는 빌드 타임 구조물로 읽기 전용 패키지이고, 컨테이너는 런타임 구조물로 이미지를 실행한 인스턴스입니다. 하나의 이미지에서 여러 컨테이너를 생성할 수 있으며, 컨테이너가 삭제되기 전까지 해당 이미지는 삭제할 수 없습니다.

2. **Q: 이미지 태그와 다이제스트의 차이점은?**
   > A: 태그는 Mutable(변경 가능)하여 같은 태그가 다른 이미지를 가리킬 수 있습니다. 다이제스트는 이미지 콘텐츠의 SHA256 해시로 Immutable(불변)하여 이미지 무결성을 보장합니다. 프로덕션에서는 다이제스트를 사용하여 정확한 이미지를 지정하는 것이 안전합니다.

3. **Q: 이미지 레이어 공유가 주는 이점은?**
   > A: 스토리지 공간 절약, 네트워크 대역폭 절약, Pull/Push 속도 향상입니다. Docker는 이미 로컬에 있는 레이어는 다시 다운로드하지 않고, 레지스트리도 동일한 레이어를 한 번만 저장합니다.

4. **Q: 멀티 아키텍처 이미지는 어떻게 동작하나요?**
   > A: Manifest List가 각 아키텍처별 Manifest를 가리킵니다. docker pull 시 호스트 아키텍처를 확인하고, Manifest List에서 해당 아키텍처의 Manifest를 찾아 적절한 레이어를 다운로드합니다. 사용자는 아키텍처 신경 쓰지 않고 같은 태그로 pull할 수 있습니다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] 이미지 = 읽기 전용 패키지 (코드 + 의존성 + OS + 메타데이터)
- [ ] 이미지 : 컨테이너 = 클래스 : 객체 관계 이해
- [ ] 빌드 타임(이미지) vs 런타임(컨테이너) 구분
- [ ] Slim 이미지 개념 (최소한의 구성요소)

### 레지스트리와 리포지토리
- [ ] Registry > Repository > Image 계층 구조
- [ ] Docker Hub가 기본 레지스트리
- [ ] Official vs Unofficial 리포지토리 구분
- [ ] FQIN (Fully Qualified Image Name) 구조

### 이미지 이름과 태그
- [ ] Tag는 Mutable (변경 가능)
- [ ] `latest` 태그가 항상 최신이 아닐 수 있음
- [ ] 하나의 이미지에 여러 태그 가능

### 레이어 구조
- [ ] 이미지는 독립적 레이어들의 스택
- [ ] Storage Driver가 레이어를 단일 뷰로 제공
- [ ] 상위 레이어가 하위 파일 오버라이드 가능
- [ ] 레이어 공유로 스토리지/네트워크 효율화

### 다이제스트
- [ ] Digest = 이미지 콘텐츠의 SHA256 해시
- [ ] Immutable (불변) - 콘텐츠 변경 시 해시도 변경
- [ ] `@sha256:...` 형식으로 정확한 이미지 지정
- [ ] Content Hash vs Distribution Hash 차이

### 멀티 아키텍처
- [ ] Manifest List가 각 아키텍처 Manifest 참조
- [ ] 같은 태그로 다양한 아키텍처 지원
- [ ] `docker buildx`로 멀티 아키텍처 빌드

### 취약점 스캔
- [ ] Docker Scout로 이미지 스캔
- [ ] `docker scout quickview` - 빠른 개요
- [ ] `docker scout cves` - 상세 CVE 정보

### 명령어
- [ ] `docker pull` - 이미지 다운로드
- [ ] `docker images` - 로컬 이미지 목록
- [ ] `docker inspect` - 상세 정보
- [ ] `docker rmi` - 이미지 삭제
- [ ] `docker manifest inspect` - Manifest 조회

---

## 🔗 참고 자료

- **공식 문서**
  - [Docker Hub](https://hub.docker.com/)
  - [Docker Scout](https://docs.docker.com/scout/)
  - [OCI Image Spec](https://github.com/opencontainers/image-spec)

- **관련 명령어**
  - `docker pull`, `docker images`, `docker inspect`
  - `docker history`, `docker manifest inspect`
  - `docker buildx imagetools inspect`
  - `docker scout quickview`, `docker scout cves`
  - `docker rmi`

---

## 다음 챕터 예고

> **Chapter 7**: 컨테이너에 대한 심층 학습 - 이미지의 런타임 형제
