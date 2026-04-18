# Chapter 8: Containerizing an App

## 📌 핵심 요약

> **컨테이너화(Containerization)는 애플리케이션을 이미지로 패키징하고 컨테이너로 실행하는 과정이다.**
> Dockerfile에 빌드 지침을 작성하고, docker build로 이미지를 생성한다.
> Multi-stage 빌드를 사용하면 작고 안전한 프로덕션 이미지를 만들 수 있다.

---

## 🎯 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- [ ] Dockerfile 작성 및 이해
- [ ] docker init으로 Dockerfile 자동 생성
- [ ] docker build로 이미지 빌드
- [ ] 이미지를 Docker Hub에 Push
- [ ] Multi-stage 빌드로 최적화된 이미지 생성
- [ ] Buildx와 BuildKit 개념 이해
- [ ] Multi-architecture 이미지 빌드
- [ ] Build Cache 활용 전략

---

## 📖 본문 정리

### 1. 컨테이너화 프로세스

#### 5단계 워크플로우

```
┌─────────────────────────────────────────────────────────────┐
│                Containerization 워크플로우                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 애플리케이션 작성 & 의존성 목록 생성                       │
│         │                                                   │
│         ▼                                                   │
│  2. Dockerfile 생성 (빌드 지침 작성)                         │
│         │                                                   │
│         ▼                                                   │
│  3. docker build → 이미지 생성                              │
│         │                                                   │
│         ▼                                                   │
│  4. docker push → 레지스트리에 업로드 (선택)                  │
│         │                                                   │
│         ▼                                                   │
│  5. docker run → 컨테이너 실행                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. 단일 컨테이너 앱 빌드

#### 2.1 애플리케이션 코드 준비

```bash
# GitHub에서 소스 코드 클론
$ git clone https://github.com/nigelpoulton/ddd-book.git
$ cd ddd-book/node-app

# 디렉토리 구조 확인
$ ls -l
-rw-r--r--  app.js           # 애플리케이션 소스
-rw-r--r--  package.json     # 의존성 정의
-rw-r--r--  package-lock.json
drwxr-xr-x  node_modules/    # 설치된 패키지
drwxr-xr-x  views/           # 뷰 템플릿
```

#### 2.2 docker init으로 Dockerfile 생성

```bash
$ docker init
Welcome to the Docker Init CLI!

? What application platform does your project use? Node
? What version of Node do you want to use? 23.3.0
? Which package manager do you want to use? npm
? What command do you want to use to start the app? node app.js
? What port does your server listen on? 8080

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md
```

#### 2.3 Dockerfile 분석

```dockerfile
# 1. Base 이미지 지정 (ARG로 버전 변수화)
ARG NODE_VERSION=20.8.0
FROM node:${NODE_VERSION}-alpine

# 2. Node.js 프로덕션 모드 설정
ENV NODE_ENV production

# 3. 작업 디렉토리 설정
WORKDIR /usr/src/app

# 4. 의존성 설치 (바인드 마운트 & 캐시 활용)
RUN --mount=type=bind,source=package.json,target=package.json \
    --mount=type=bind,source=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci --omit=dev

# 5. 비root 사용자로 실행
USER node

# 6. 소스 코드 복사
COPY . .

# 7. 포트 문서화
EXPOSE 8080

# 8. 시작 명령
CMD node app.js
```

#### Dockerfile 지침별 역할

```
┌─────────────────────────────────────────────────────────────┐
│              Dockerfile 지침 분류                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  레이어 생성 (콘텐츠 추가):                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ FROM      - Base 이미지 Pull                        │   │
│  │ RUN       - 명령 실행 (패키지 설치 등)               │   │
│  │ COPY      - 파일 복사                               │   │
│  │ WORKDIR   - 작업 디렉토리 설정                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  메타데이터 추가 (레이어 미생성):                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ EXPOSE    - 포트 문서화                             │   │
│  │ ENV       - 환경 변수 설정                          │   │
│  │ CMD       - 기본 실행 명령                          │   │
│  │ ENTRYPOINT - 고정 실행 명령                         │   │
│  │ LABEL     - 메타데이터 라벨                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2.4 이미지 빌드

```bash
# 이미지 빌드 (마지막 . = 빌드 컨텍스트)
$ docker build -t ddd-book:ch8.node .

[+] Building 16.2s (12/12) FINISHED
 => [internal] load build definition from Dockerfile           0.0s
 => [stage-0 1/4] FROM docker.io/library/node:20.8.0-alpine    3s    # Base 레이어
 => [stage-0 2/4] WORKDIR /usr/src/app                         0.2s  # 새 레이어
 => [stage-0 3/4] RUN --mount=type=bind...npm ci --omit=dev    1.1s  # 새 레이어
 => [stage-0 4/4] COPY . .                                     0.1s  # 새 레이어
 => exporting to image                                         0.2s
 => => naming to docker.io/library/ddd-book:ch8.node

# 이미지 확인
$ docker images
REPO        TAG        IMAGE ID         SIZE
ddd-book    ch8.node   24dd040fa06b     242MB
```

#### 레이어 구조

```
┌─────────────────────────────────────────────────────────────┐
│              Dockerfile → Image Layers                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Dockerfile 지침              Image Layers                   │
│  ─────────────────────        ─────────────────────         │
│                                                             │
│  FROM node:23.3.0-alpine  →   ┌─────────────────┐           │
│                               │  Base Image     │  4 layers │
│                               │  (node:alpine)  │           │
│                               └────────┬────────┘           │
│                                        │                    │
│  WORKDIR /usr/src/app     →   ┌────────┴────────┐           │
│                               │  Layer 5        │           │
│                               └────────┬────────┘           │
│                                        │                    │
│  RUN npm ci --omit=dev    →   ┌────────┴────────┐           │
│                               │  Layer 6        │           │
│                               └────────┬────────┘           │
│                                        │                    │
│  COPY . .                 →   ┌────────┴────────┐           │
│                               │  Layer 7        │           │
│                               └─────────────────┘           │
│                                                             │
│  EXPOSE, ENV, CMD, USER   →   메타데이터만 추가 (레이어 없음) │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2.5 Docker Hub에 Push

```bash
# Docker Hub 로그인
$ docker login
Login Succeeded

# 이미지 태그 추가 (Docker ID 포함)
$ docker tag ddd-book:ch8.node nigelpoulton/ddd-book:ch8.node

# 태그 확인
$ docker images
REPO                    TAG         IMAGE ID         SIZE
nigelpoulton/ddd-book   ch8.node    24dd040fa06b     268MB
ddd-book                ch8.node    24dd040fa06b     268MB

# Docker Hub에 Push
$ docker push nigelpoulton/ddd-book:ch8.node
```

#### Push 대상 결정 로직

```
┌─────────────────────────────────────────────────────────────┐
│                  Image Tag → Push Target                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  nigelpoulton/ddd-book:ch8.node                             │
│  ├──────────┤├────────┤├───────┤                            │
│  Docker ID   Repo      Tag                                  │
│                                                             │
│  → Push 대상: docker.io/nigelpoulton/ddd-book:ch8.node      │
│                                                             │
│  ⚠️ Docker ID 없으면 Push 실패                               │
│     (ddd-book:ch8.node → docker.io/library/ddd-book 시도)   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2.6 컨테이너 실행 및 테스트

```bash
# 컨테이너 실행
$ docker run -d --name c1 \
  -p 5005:8080 \
  nigelpoulton/ddd-book:ch8.node

# 실행 확인
$ docker ps
ID    IMAGE              COMMAND           STATUS      PORTS                    NAMES
49..  ddd-book:ch8.node  "node ./app.js"   UP 6 secs   0.0.0.0:5005->8080/tcp   c1

# 브라우저에서 테스트
# http://localhost:5005
```

---

### 3. Multi-stage 빌드

#### 왜 Multi-stage인가?

```
┌─────────────────────────────────────────────────────────────┐
│              큰 이미지의 문제점                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Big is Bad!                                                │
│                                                             │
│  ❌ 느림 (Pull/Push 시간 증가)                               │
│  ❌ 더 많은 잠재적 취약점                                    │
│  ❌ 더 큰 공격 표면 (Attack Surface)                         │
│                                                             │
│  목표: 프로덕션에 필요한 것만 포함한 Slim 이미지              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Multi-stage 빌드 개념

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Multi-stage Build 워크플로우                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Stage 0 (base):                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  FROM golang:1.23-alpine                                        │   │
│  │  • 컴파일 도구, 빌드 환경 포함 (~350MB)                          │   │
│  │  • 의존성 다운로드                                              │   │
│  │  • 소스 코드 복사                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                          │                                              │
│              ┌───────────┴───────────┐                                  │
│              ▼                       ▼                                  │
│  Stage 1 (build-client):   Stage 2 (build-server):                     │
│  ┌─────────────────────┐   ┌─────────────────────┐                     │
│  │  FROM base          │   │  FROM base          │    ← 병렬 실행      │
│  │  RUN go build       │   │  RUN go build       │                     │
│  │  → client 바이너리   │   │  → server 바이너리   │                     │
│  └──────────┬──────────┘   └──────────┬──────────┘                     │
│             │                         │                                 │
│             └───────────┬─────────────┘                                 │
│                         ▼                                               │
│  Stage 3 (prod):                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  FROM scratch                     ← 최소 이미지 (~0MB)           │   │
│  │  COPY --from=build-client /bin/client /bin/                     │   │
│  │  COPY --from=build-server /bin/server /bin/                     │   │
│  │  → 최종 프로덕션 이미지 (~27MB)                                  │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Multi-stage Dockerfile 예시

```dockerfile
# Stage 0: base - 빌드 환경 준비
FROM golang:1.23.4-alpine AS base
WORKDIR /src
COPY go.mod go.sum .
RUN go mod download
COPY . .

# Stage 1: build-client - 클라이언트 컴파일
FROM base AS build-client
RUN go build -o /bin/client ./cmd/client

# Stage 2: build-server - 서버 컴파일 (Stage 1과 병렬 실행)
FROM base AS build-server
RUN go build -o /bin/server ./cmd/server

# Stage 3: prod - 최종 프로덕션 이미지
FROM scratch AS prod
COPY --from=build-client /bin/client /bin/
COPY --from=build-server /bin/server /bin/
ENTRYPOINT [ "/bin/server" ]
```

#### 빌드 및 결과

```bash
# 빌드 실행
$ docker build -t multi:full .

[+] Building 14.6s (15/15) FINISHED
 => [build-client 1/1] RUN go build -o /bin/client ./cmd/client   5.1s  # 병렬
 => [build-server 1/1] RUN go build -o /bin/server ./cmd/server   5.1s  # 병렬

# 이미지 크기 비교
$ docker images
REPO    TAG       SIZE
multi   full      26.7MB    ← 최종 이미지 (350MB+ → 26.7MB)

# 레이어 확인
$ docker history multi:full
IMAGE          CREATED BY                          SIZE
a7a01440f2b5   ENTRYPOINT ["/bin/server"]          0B
<missing>      COPY /bin/server /bin/ # buildkit   8.64MB
<missing>      COPY /bin/client /bin/ # buildkit   8.53MB
```

#### Build Target으로 개별 이미지 생성

```dockerfile
# 별도의 prod-client, prod-server 스테이지 정의
FROM scratch AS prod-client
COPY --from=build-client /bin/client /bin/
ENTRYPOINT [ "/bin/client" ]

FROM scratch AS prod-server
COPY --from=build-server /bin/server /bin/
ENTRYPOINT [ "/bin/server" ]
```

```bash
# 각 타겟별로 개별 빌드
$ docker build -t multi:client --target prod-client -f Dockerfile-final .
$ docker build -t multi:server --target prod-server -f Dockerfile-final .

# 결과 비교
$ docker images
REPOSITORY     TAG       SIZE
multi          full      26.7MB   # client + server
multi          server    11.7MB   # server만
multi          client    11.9MB   # client만
```

---

### 4. Buildx, BuildKit, Drivers

#### 빌드 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Docker Build Architecture                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌─────────────────┐                             │
│                         │    docker build │                             │
│                         │    (Buildx CLI) │                             │
│                         └────────┬────────┘                             │
│                                  │                                      │
│                    ┌─────────────┴─────────────┐                        │
│                    │                           │                        │
│                    ▼                           ▼                        │
│         ┌──────────────────┐        ┌──────────────────┐               │
│         │  Local Builder   │        │  Cloud Builder   │               │
│         │ (docker-container│        │ (Build Cloud)    │               │
│         │      driver)     │        │                  │               │
│         ├──────────────────┤        ├──────────────────┤               │
│         │   BuildKit       │        │   BuildKit       │               │
│         │   (Container)    │        │   (Remote)       │               │
│         └──────────────────┘        └──────────────────┘               │
│                                                                         │
│  Buildx: Docker의 최신 빌드 클라이언트 (CLI 플러그인)                    │
│  BuildKit: 실제 빌드를 수행하는 서버 (Builder)                          │
│  Driver: Builder가 실행되는 환경 (docker-container, cloud 등)           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Builder 관리

```bash
# 현재 Builder 목록 확인
$ docker buildx ls
NAME/NODE                  DRIVER/ENDPOINT         PLATFORMS
builder *                  docker-container
  builder0                 desktop-linux           linux/arm64, linux/amd64, linux/riscv64...
cloud-nigelpoulton-ddd     cloud
  linux-arm64              cloud://...             linux/arm64*
  linux-amd64              cloud://...             linux/amd64*

# 새 Builder 생성
$ docker buildx create --driver=docker-container --name=container

# 기본 Builder 설정
$ docker buildx use container

# Builder 상세 정보
$ docker buildx inspect cloud-nigelpoulton-ddd
```

| Driver | 설명 | 특징 |
|--------|------|------|
| **docker** | 기본 Docker 데몬 | 단순, 캐시 공유 |
| **docker-container** | 전용 BuildKit 컨테이너 | Multi-arch 지원, QEMU 에뮬레이션 |
| **cloud** | Docker Build Cloud | 빠름, 네이티브 하드웨어, 캐시 공유 |

---

### 5. Multi-architecture 빌드

#### 개념

```
┌─────────────────────────────────────────────────────────────┐
│              Multi-architecture Build                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  목표: 하나의 Dockerfile로 여러 아키텍처 이미지 생성          │
│                                                             │
│  ┌─────────────────┐                                        │
│  │   Dockerfile    │                                        │
│  └────────┬────────┘                                        │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────┐           │
│  │              docker buildx build             │           │
│  │  --platform=linux/amd64,linux/arm64         │           │
│  └─────────────────────────────────────────────┘           │
│           │                                                 │
│     ┌─────┴─────┐                                          │
│     ▼           ▼                                          │
│  ┌────────┐  ┌────────┐                                    │
│  │ AMD64  │  │ ARM64  │  → Docker Hub (동일 태그)           │
│  │ Image  │  │ Image  │                                    │
│  └────────┘  └────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 빌드 방법

```bash
# 로컬 Builder로 Multi-arch 빌드 (QEMU 에뮬레이션)
$ docker buildx build --builder=container \
  --platform=linux/amd64,linux/arm64 \
  -t nigelpoulton/ddd-book:ch8.1 --push .

[+] Building 79.3s (26/26) FINISHED
 => [linux/arm64 2/5] RUN apk add --update nodejs npm curl    19.0s
 => [linux/amd64 2/5] RUN apk add --update nodejs npm curl    17.4s
 ...
 => => pushing layers                                          31.5s
 => => pushing manifest for .../ddd-book:web0.2@sha256:...

# Docker Build Cloud로 빌드 (네이티브 하드웨어)
$ docker buildx build \
  --builder=cloud-nigelpoulton-ddd \
  --platform=linux/amd64,linux/arm64 \
  -t nigelpoulton/ddd-book:ch8.1 --push .
```

| 빌드 방식 | 장점 | 단점 |
|----------|------|------|
| **Local (QEMU)** | 무료, 많은 아키텍처 지원 | 느림, 불안정할 수 있음 |
| **Build Cloud** | 빠름, 안정적, 캐시 공유 | 유료 구독 필요 |

---

### 6. Best Practices

#### Build Cache 활용

```
┌─────────────────────────────────────────────────────────────┐
│                    Build Cache 동작                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  각 Dockerfile 지침마다:                                     │
│  1. 캐시에 동일 레이어 존재? → Cache Hit (사용)              │
│  2. 없음? → Cache Miss (새로 빌드)                          │
│                                                             │
│  ⚠️ Cache Miss 발생 시 → 이후 모든 지침 재빌드              │
│                                                             │
│  예시:                                                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ FROM alpine           ← Cache Hit                   │   │
│  │ RUN apk add nodejs    ← Cache Hit                   │   │
│  │ COPY . /src           ← Cache Miss (파일 변경)      │   │
│  │ WORKDIR /src          ← 재빌드 (Cache 무효화됨)     │   │
│  │ RUN npm install       ← 재빌드                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Dockerfile 최적화 전략

```dockerfile
# ❌ 나쁜 예: 소스 변경 시 npm install도 재실행
FROM alpine
RUN apk add nodejs npm
COPY . /src              # 소스 변경 → Cache Miss
WORKDIR /src
RUN npm install          # 불필요하게 재실행

# ✅ 좋은 예: 의존성 파일만 먼저 복사
FROM alpine
RUN apk add nodejs npm
WORKDIR /src
COPY package*.json .     # 의존성 파일만 먼저
RUN npm install          # 의존성 변경 시만 재실행
COPY . .                 # 소스는 마지막에
```

#### 핵심 최적화 규칙

```
┌─────────────────────────────────────────────────────────────┐
│                  Dockerfile 최적화 규칙                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 변경 빈도가 낮은 지침을 앞에 배치                         │
│     (FROM → 패키지 설치 → 의존성 → 소스 코드)                │
│                                                             │
│  2. 필수 패키지만 설치                                       │
│     apt: --no-install-recommends 플래그 사용                │
│                                                             │
│  3. 레이어 수 최소화                                         │
│     여러 RUN을 하나로 합치기 (&&)                            │
│                                                             │
│  4. Multi-stage 빌드 사용                                   │
│     빌드 도구 제외, 실행 파일만 프로덕션 이미지에             │
│                                                             │
│  5. Official/Verified Publisher 이미지 사용                 │
│     보안 및 품질 보장                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 7. 주요 Dockerfile 지침 정리

| 지침 | 설명 | 레이어 생성 |
|------|------|------------|
| `FROM` | Base 이미지 지정 | ✅ |
| `RUN` | 명령 실행 | ✅ |
| `COPY` | 파일 복사 | ✅ |
| `ADD` | 파일 복사 (tar 자동 해제, URL 지원) | ✅ |
| `WORKDIR` | 작업 디렉토리 설정 | ✅ (작은 레이어) |
| `ENV` | 환경 변수 설정 | ❌ |
| `EXPOSE` | 포트 문서화 | ❌ |
| `CMD` | 기본 실행 명령 | ❌ |
| `ENTRYPOINT` | 고정 실행 명령 | ❌ |
| `USER` | 실행 사용자 설정 | ❌ |
| `ARG` | 빌드 시 변수 | ❌ |
| `LABEL` | 메타데이터 라벨 | ❌ |

---

### 8. 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `docker init` | Dockerfile 자동 생성 |
| `docker build -t <tag> .` | 이미지 빌드 |
| `docker build -f <file>` | Dockerfile 지정 |
| `docker build --target <stage>` | 특정 스테이지만 빌드 |
| `docker build --no-cache` | 캐시 무시 |
| `docker tag <src> <dst>` | 이미지 태그 추가 |
| `docker push <image>` | 레지스트리에 Push |
| `docker history <image>` | 빌드 히스토리 확인 |
| `docker buildx ls` | Builder 목록 |
| `docker buildx create` | Builder 생성 |
| `docker buildx use` | 기본 Builder 설정 |
| `docker buildx build --platform` | Multi-arch 빌드 |

---

## 🔍 심화 학습

### 핵심 개념 비교

| 개념 | 설명 |
|------|------|
| **Build Context** | 빌드에 포함할 파일들이 있는 디렉토리 |
| **Dockerfile** | 빌드 지침이 담긴 파일 |
| **Layer** | 이미지 구성 단위 (콘텐츠 추가 지침마다 생성) |
| **Multi-stage** | 여러 FROM을 사용해 최종 이미지 최소화 |
| **Buildx** | Docker 빌드 CLI 플러그인 |
| **BuildKit** | 실제 빌드 수행 서버 (Builder) |
| **Build Cache** | 빌드 속도 향상을 위한 레이어 캐싱 |

### 추가 학습 자료

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Build Cloud](https://docs.docker.com/build-cloud/)

---

## 💡 실무 적용 포인트

### 면접 대비 질문

1. **Q: Dockerfile에서 레이어를 생성하는 지침은?**
   > A: FROM, RUN, COPY, ADD, WORKDIR 등 콘텐츠를 추가하는 지침이 레이어를 생성합니다. ENV, EXPOSE, CMD, ENTRYPOINT 등은 메타데이터만 추가하고 레이어를 생성하지 않습니다.

2. **Q: Multi-stage 빌드의 장점은?**
   > A: 빌드 도구와 컴파일러 등을 포함한 큰 빌드 이미지에서 컴파일 후, 실행 파일만 작은 프로덕션 이미지로 복사합니다. 이렇게 하면 이미지 크기를 크게 줄일 수 있고(350MB → 27MB), 보안 취약점도 줄어듭니다. 또한 의존성 없는 스테이지는 병렬 실행됩니다.

3. **Q: Build Cache를 효과적으로 활용하는 방법은?**
   > A: 변경 빈도가 낮은 지침을 Dockerfile 앞에 배치합니다. 예를 들어 패키지 설치 → 의존성 파일 복사 → npm install → 소스 코드 복사 순서로 작성하면, 소스 코드만 변경 시 앞의 레이어들은 캐시에서 재사용됩니다. Cache Miss가 발생하면 이후 모든 지침이 재빌드되므로 순서가 중요합니다.

4. **Q: Buildx와 BuildKit의 관계는?**
   > A: Buildx는 Docker의 빌드 클라이언트(CLI 플러그인)이고, BuildKit은 실제 빌드를 수행하는 서버입니다. Buildx는 여러 BuildKit 인스턴스(Builder)와 통신할 수 있으며, 로컬 컨테이너나 Docker Build Cloud 등 다양한 환경에서 빌드를 실행할 수 있습니다.

---

## ✅ 체크리스트

### 컨테이너화 프로세스
- [ ] 5단계: 앱 작성 → Dockerfile → Build → Push → Run
- [ ] Build Context = 앱 파일이 있는 디렉토리
- [ ] docker init으로 Dockerfile 자동 생성

### Dockerfile
- [ ] FROM: Base 이미지 지정
- [ ] RUN: 명령 실행 (레이어 생성)
- [ ] COPY: 파일 복사 (레이어 생성)
- [ ] WORKDIR: 작업 디렉토리
- [ ] EXPOSE: 포트 문서화 (메타데이터)
- [ ] CMD/ENTRYPOINT: 실행 명령 (메타데이터)

### Multi-stage 빌드
- [ ] 여러 FROM = 여러 스테이지
- [ ] COPY --from=<stage>로 다른 스테이지에서 복사
- [ ] 최종 스테이지만 프로덕션 이미지
- [ ] 의존성 없는 스테이지는 병렬 실행

### Build Cache
- [ ] Cache Hit = 캐시된 레이어 재사용
- [ ] Cache Miss = 이후 모든 지침 재빌드
- [ ] 변경 적은 지침을 앞에 배치

### Buildx & Multi-arch
- [ ] Buildx = 빌드 클라이언트
- [ ] BuildKit = 빌드 서버 (Builder)
- [ ] --platform으로 Multi-arch 빌드
- [ ] docker-container driver = QEMU 에뮬레이션
- [ ] cloud driver = Docker Build Cloud

### 명령어
- [ ] docker build, docker push
- [ ] docker tag, docker history
- [ ] docker buildx ls, create, use

---

## 🔗 참고 자료

- **공식 문서**
  - [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
  - [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
  - [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/)
  - [Docker Build Cloud](https://docs.docker.com/build-cloud/)

- **관련 명령어**
  - `docker init`, `docker build`, `docker push`
  - `docker tag`, `docker history`, `docker inspect`
  - `docker buildx ls`, `docker buildx create`, `docker buildx use`

---

## 다음 챕터 예고

> **Chapter 9**: Docker Compose - 멀티 컨테이너 애플리케이션 관리
