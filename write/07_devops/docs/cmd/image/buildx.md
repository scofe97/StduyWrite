---
title: docker buildx 참조 시트
tags: [container, image-build, buildx, multi-platform, cross-compile, distroless, cli, reference]
status: draft
source:
  - https://github.com/docker/docs/blob/16e452c8eaea26cec842cbf1065037fb2015001f/content/manuals/build/building/multi-platform.md
  - https://docs.docker.com/reference/dockerfile/
  - https://github.com/golang/go/blob/go1.25.0/src/cmd/cgo/doc.go
  - https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/README.md
  - https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/base/README.md
  - docker buildx v0.37.2 의 `docker buildx build --help` 원문
related:
  - ../README.md
  - buildkit.md
  - ../../artifact/container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md
  - ../../../../08_cloud/book/cks-study-guide/06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md
updated: 2026-11-25
---

# docker buildx 참조 시트

---

> `docker buildx build` 로 amd64 와 arm64 이미지를 한 번에 만들 때 쓰는 `--platform` 과 `BUILDPLATFORM`·`TARGETARCH` 를 Go 크로스 컴파일 예제로 모았습니다.

## 개요

> `docker buildx build` 는 BuildKit 으로 빌드하는 `docker` 의 확장 명령이고, 이 시트는 그 가운데 멀티 플랫폼 빌드만 다룹니다.

`docker buildx` 는 `docker` CLI 의 플러그인이고 빌드는 BuildKit 이 합니다.[^docker-buildkit] 이 시트는 OrbStack 의 Docker Engine 29.8.2(linux/arm64)와 buildx v0.37.2 로 실측했습니다. 빌더는 `docker` 드라이버의 `orbstack` 이고 BuildKit 은 v0.33.1 입니다.

Go 멀티 스테이지 빌드와 distroless 최종 이미지가 왜 작고 안전한지는 [이미지 작게 만들고 미리 검사하기](../../../../08_cloud/book/cks-study-guide/06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md)가 다룹니다. 이 시트는 그 위에서 플랫폼 ARG 만 풉니다. `buildctl` 로 같은 BuildKit 을 직접 부르는 방법은 [buildctl·buildkitd 참조 시트](buildkit.md)가 맡습니다.



## 핵심 문법

> `--platform` 이 대상 플랫폼을 정하고, Dockerfile 의 `FROM --platform` 과 자동 ARG 가 빌드 단계를 어느 플랫폼에서 돌릴지 정합니다.

```bash
# 호출 형태. docker buildx build --help 의 Usage 줄
docker buildx build [OPTIONS] PATH | URL | -

# 두 플랫폼을 한 번에 빌드한다 (두 플랫폼 이미지 빌드)
docker buildx build --platform linux/amd64,linux/arm64 -t 이름:태그 .

# 한 플랫폼만 빌드해 로컬에 받는다 (플랫폼별로 실행 확인)
docker buildx build --platform linux/amd64 --load -t 이름:태그 .

# 빌드 중간 단계에서 멈춘다 (플랫폼 ARG 의 값 읽기)
docker buildx build --target 단계 .

# 만든 이미지를 레지스트리로 올린다. 이 시트는 돌리지 않았다 (레지스트리에 올리는 꼴)
docker buildx build --platform linux/amd64,linux/arm64 --push -t 레지스트리/이름:태그 .
```

### 자동 ARG

> BuildKit 이 빌드할 때 채워 주는 ARG 이며, 빌드를 돌리는 쪽과 결과물이 쓰일 쪽으로 나뉩니다.[^auto-arg]

```bash
# 이름              뜻                              예
# BUILDPLATFORM     빌드를 수행하는 노드의 플랫폼    linux/arm64
# TARGETPLATFORM    빌드 결과물의 플랫폼             linux/amd64, linux/arm/v7
# TARGETOS          TARGETPLATFORM 의 OS 부분        linux
# TARGETARCH        TARGETPLATFORM 의 구조 부분      amd64, arm64
# 이 밖에 BUILDOS·BUILDARCH·BUILDVARIANT·TARGETVARIANT 가 같은 방식으로 있다
```



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 만든 이미지와 파일만 씁니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 Go 예제와 Dockerfile 이 생깁니다. Docker 와 buildx 가 있는 macOS·Linux 에서 돌립니다.

빌드가 `golang:1.25` 와 `gcr.io/distroless/static-debian13:nonroot` 를 공개 레지스트리에서 받습니다. 이 시트는 레지스트리로 push 하지 않습니다.

```bash
# 작업 폴더. 「두 플랫폼 이미지 빌드」 부터 여러 곳에서 쓴다
mkdir -p ~/buildx-lab && cd ~/buildx-lab

# 모듈 파일
cat > go.mod <<'EOF'
module hello

go 1.25
EOF

# OS 와 구조를 찍는 프로그램
cat > main.go <<'EOF'
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("hello from", runtime.GOOS, runtime.GOARCH)
}
EOF

# 빌드 단계는 빌더 플랫폼에 고정하고 최종 이미지는 distroless nonroot 로 만든다
cat > Dockerfile <<'EOF'
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM golang:1.25 AS build
ARG BUILDPLATFORM
ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
RUN echo "build=$BUILDPLATFORM target=$TARGETPLATFORM os=$TARGETOS arch=$TARGETARCH"
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -trimpath -ldflags="-s -w" -o /out/app .

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
EOF
```

### 두 플랫폼 이미지 빌드

> `--platform` 에 플랫폼 두 개를 쉼표로 주면 한 번의 빌드가 두 구조의 이미지를 만듭니다.

개발 장비와 운영 서버의 CPU 구조가 다른 일이 흔합니다. Apple 실리콘 노트북은 arm64 이고 클러스터 노드는 amd64 일 수 있어서, 한쪽 구조로만 만든 이미지는 다른 쪽에서 쓸 수 없습니다. 그래서 두 구조를 모두 담은 이미지가 필요합니다. Docker 문서가 드는 방법은 셋입니다. QEMU 에뮬레이션은 설정이 가장 쉽지만 느립니다. 네이티브 노드를 여러 개 두는 방법과 크로스 컴파일이 나머지입니다.[^mp-example] Go 는 컴파일러가 `GOOS` 와 `GOARCH` 로 대상 구조를 직접 받으므로 크로스 컴파일이 잘 맞습니다.

```bash
# amd64 와 arm64 를 함께 빌드해 buildx-lab:multi 로 받는다
#   --progress plain   진행을 줄 단위 로그로 찍는다
#   --platform 목록    쉼표로 이은 대상 플랫폼
#   -t 이름:태그       결과 이미지 이름 (--tag)
docker buildx build \
  --progress plain \
  --platform linux/amd64,linux/arm64 \
  -t buildx-lab:multi \
  .
```

```bash
#12 [linux/arm64->amd64 build 2/5] RUN echo "build=linux/arm64 target=linux/amd64 os=linux arch=amd64"
#13 [linux/arm64 build 2/5] RUN echo "build=linux/arm64 target=linux/arm64 os=linux arch=arm64"
#18 [linux/arm64 build 5/5] RUN CGO_ENABLED=0 GOOS=linux GOARCH=arm64     go build -trimpath -ldflags="-s -w" -o /out/app .
#19 [linux/arm64->amd64 build 5/5] RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64     go build -trimpath -ldflags="-s -w" -o /out/app .
```

위는 `grep -E 'RUN'` 으로 거른 줄입니다. 단계 이름 앞의 `linux/arm64->amd64` 는 arm64 빌더에서 amd64 결과를 만든다는 표시입니다. 두 `go build` 는 빌더 구조에서 네이티브로 돕니다.

### 플랫폼 ARG 의 값 읽기

> 같은 빌드를 `--no-cache` 로 다시 돌려 `RUN echo` 줄의 출력에서 ARG 가 무엇으로 채워졌는지 봅니다.

```bash
# 캐시를 쓰지 않고 다시 빌드해 echo 의 출력 줄만 거른다
docker buildx build \
  --progress plain \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  -t buildx-lab:multi \
  . 2>&1 | grep 'build=linux'
```

```bash
#12 0.307 build=linux/arm64 target=linux/amd64 os=linux arch=amd64
#13 0.293 build=linux/arm64 target=linux/arm64 os=linux arch=arm64
```

`BUILDPLATFORM` 은 두 줄 모두 빌더의 `linux/arm64` 이고 `TARGET*` 만 플랫폼마다 달라집니다.

### 플랫폼별로 실행 확인

> `docker run --platform` 으로 구조를 골라 실행하면 같은 태그에서 구조별 바이너리가 나옵니다.

```bash
# 구조를 골라 실행한다
docker run --rm --platform linux/arm64 buildx-lab:multi    # hello from linux arm64
docker run --rm --platform linux/amd64 buildx-lab:multi    # hello from linux amd64

# 이미지의 사용자와 크기(바이트)
docker image inspect buildx-lab:multi --format '{{.Config.User}} {{.Size}}'    # nonroot:nonroot 9538212
```

이 맥에서는 두 플랫폼을 `--load` 로 한 번에 받는 빌드도 성공했습니다. `docker info` 의 스냅샷 드라이버가 `io.containerd.snapshotter.v1` 이었고, 이 저장소가 아닌 환경은 확인하지 않았습니다.

### 레지스트리에 올리는 꼴

> 멀티 플랫폼 결과를 레지스트리에 올리는 것은 `--push` 하나로 합니다. 이 시트는 돌리지 않았습니다.

```bash
# 두 플랫폼을 한 이미지 이름으로 올린다. 레지스트리 주소는 환경에 맞게 바꾼다
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t 레지스트리/이름:태그 \
  .
```

### 실습 정리

```bash
# 이 시트가 만든 이미지와 작업 폴더
docker image rm buildx-lab:multi
cd ~ && rm -rf ~/buildx-lab
```



## 주의사항과 동작 원리

### ARG 를 단계 안에서 다시 선언하는 일

> 자동 ARG 는 전역 스코프라서 빌드 단계 안에서는 값 없이 `ARG 이름` 을 다시 선언해야 보입니다.[^arg-scope]

단계 안에서 쓰려면 값 없이 다시 선언합니다.

```dockerfile
FROM alpine
ARG TARGETPLATFORM
RUN echo "I'm building for $TARGETPLATFORM"
```

선언하지 않은 경우를 echo 단계까지만 빌드해 값을 읽어 봅니다.

```bash
# 단계 안에서 ARG 를 선언하지 않은 Dockerfile 을 echo 단계까지만 빌드한다
cat > Dockerfile.noarg <<'EOF'
FROM --platform=$BUILDPLATFORM golang:1.25 AS build
RUN echo "arch=[$TARGETARCH] os=[$TARGETOS]"
FROM scratch
EOF
docker buildx build --progress plain --no-cache --target build --platform linux/amd64 -f Dockerfile.noarg . 2>&1 | grep 'arch='
```

```bash
#5 0.128 arch=[] os=[]
```

값이 비면 `GOARCH=${TARGETARCH}` 도 빈 값이 되고, 빈 `GOARCH` 에서 `go` 는 호스트 구조를 씁니다. `docker run --rm -e GOARCH= golang:1.25 go env GOARCH` 가 이 맥에서 `arm64` 를 찍었습니다. 그래서 amd64 를 요청했는데 arm64 바이너리가 들어가고 빌드 오류는 나지 않습니다.

### 에뮬레이션이 끼는 FROM

> 빌드 단계의 `FROM` 에 `--platform` 이 없으면 대상 플랫폼 이미지로 시작하므로, 빌더와 구조가 다를 때 `RUN` 이 에뮬레이션으로 돕니다.[^from-platform]

```bash
# 빌드 단계를 대상 플랫폼 이미지로 시작하는 Dockerfile
cat > Dockerfile.emu <<'EOF'
FROM golang:1.25 AS build
ARG TARGETOS
ARG TARGETARCH
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -trimpath -ldflags="-s -w" -o /out/app .
FROM scratch
COPY --from=build /out/app /app
ENTRYPOINT ["/app"]
EOF

# amd64 대상으로 go build 단계의 시간만 읽는다. 앞의 Dockerfile 도 같은 방식으로 돌린다
docker buildx build --progress plain --no-cache --platform linux/amd64 -f Dockerfile.emu . 2>&1 | grep -A3 'RUN CGO' | grep DONE
```

이 맥(arm64)에서 amd64 를 대상으로 `go build` 단계가 걸린 시간입니다.

```bash
# 빌드 단계를 대상 플랫폼 이미지로 시작한 Dockerfile.emu    9.4초, 10.0초 (두 번 잰 값)
# FROM --platform=$BUILDPLATFORM 을 쓴 Dockerfile           2.3초, 3.0초 (두 번 잰 값)
```

단계 이름도 `[linux/arm64->amd64 build 5/5]` 대신 `[build 5/5]` 로 찍혀 구별되지 않았습니다. Docker 문서는 QEMU 에뮬레이션이 네이티브 빌드보다 훨씬 느릴 수 있고 컴파일 같은 계산 작업에서 특히 그렇다고 적습니다.[^qemu-slow] 이 맥의 amd64 가 어떤 방식으로 실행되는지는 확인하지 않았고, 위 시간은 두 번씩 잰 값입니다.

### CGO_ENABLED=0 을 명시하는 이유

> 크로스 컴파일에서는 cgo 가 기본으로 꺼지고 같은 구조의 빌드에서는 켜질 수 있어서, Dockerfile 에 `0` 을 적어 두 경우를 맞춥니다.[^cgo-default]

```bash
# golang:1.25 (arm64) 안에서 cgo 기본값을 읽는다
docker run --rm golang:1.25 go env CGO_ENABLED                      # 1
docker run --rm -e GOARCH=amd64 golang:1.25 go env CGO_ENABLED      # 0
docker run --rm -e GOARCH=arm64 golang:1.25 go env CGO_ENABLED      # 1
```

arm64 빌더에서 arm64 대상은 켜지고 amd64 대상은 꺼졌습니다. cgo 로 링크한 바이너리는 libc 같은 시스템 라이브러리에 기대서 libc 가 없는 `static` 이미지에서는 돌지 않을 수 있습니다. libc 가 필요한 Go 앱은 distroless `base` 부터 시작하라고 안내합니다.[^distroless-static]

`static` 이미지에 든 것은 ca-certificates, root 사용자의 `/etc/passwd` 항목, `/tmp` 디렉터리, tzdata 입니다.[^distroless-static] 이 목록에 libc 는 없습니다.

cgo 가 필요한 의존성(예: 일부 SQLite 드라이버)이 있으면 `CGO_ENABLED=0` 으로는 빌드가 깨지거나 기능이 빠집니다. 길은 둘입니다. 구조별 C 크로스 컴파일러를 갖추거나, 대상 구조의 네이티브 노드에서 빌드하는 방식을 씁니다. 이 시트는 두 길의 절차를 열어 보지 않았습니다.

### 셸이 없는 distroless 이미지

> distroless 는 셸과 패키지 관리자가 없어서 `sh` 로 들어갈 수 없고, 디버깅할 때만 `:debug` 계열 태그를 씁니다.[^distroless-shell]

```bash
# 셸을 엔트리포인트로 바꿔 실행한다
docker run --rm --entrypoint /bin/sh buildx-lab:multi
```

```bash
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "/bin/sh": stat /bin/sh: no such file or directory
```

README 표가 `static-debian13` 에 적은 태그는 `latest`, `nonroot`, `debug`, `debug-nonroot` 넷입니다.[^distroless-shell]

`nonroot` 태그의 기본 사용자는 UID 65532 이고 엔트리포인트는 비어 있었습니다. `docker image inspect` 의 `Config.User`·`Config.Entrypoint` 로 읽었습니다.

이 사용자로 돌아서 바이너리가 쓸 경로는 `/tmp` 나 볼륨으로 따로 마련해야 합니다.

### 최종 단계의 --platform

> 빌드 단계에만 `--platform=$BUILDPLATFORM` 을 쓰고 최종 이미지 단계에는 쓰지 않는 것이 Docker 문서의 예와 같은 형태입니다.[^mp-example]

최종 단계에 `--platform=$BUILDPLATFORM` 을 쓰면 무엇이 빌더 구조가 되는지 알파인 베이스로 쟀습니다. 두 Dockerfile 은 `FROM alpine` 한 줄과 `FROM --platform=$BUILDPLATFORM alpine` 한 줄입니다. 둘 다 `docker buildx build --platform linux/amd64 --load` 로 빌드했습니다.

```bash
# 이미지에서 /bin/busybox 를 docker create 와 docker cp 로 꺼내 file 로 읽었다
#                                        Architecture   uname -m   /bin/busybox
# FROM alpine                            amd64          x86_64     x86-64
# FROM --platform=$BUILDPLATFORM alpine  amd64          aarch64    ARM aarch64
```

`docker image inspect` 의 `Architecture` 는 두 이미지 모두 `amd64` 였습니다. 그런데 `BUILDPLATFORM` 쪽은 `docker run --platform linux/amd64` 로 돌려도 `uname -m` 이 `aarch64` 였습니다. busybox 의 ELF machine 값은 `FROM alpine` 이 `0x3e`(x86-64)였습니다. `BUILDPLATFORM` 쪽은 `0xb7`(arm64)이었습니다.

알파인 베이스로 잰 결과로는, 이미지 설정의 구조 칸은 요청한 플랫폼으로 적히고 베이스 계층에서 온 실행 파일만 빌더 구조가 됩니다. arm64 호스트 한 대에서 각 한 번 잰 값입니다.

`--platform` 없이 `docker run` 하면 두 이미지가 같은 경고를 냈습니다.

```bash
WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested
```

이 경고로는 두 이미지를 구별할 수 없었습니다. 앞서 distroless `static` 으로 쟀을 때는 `Architecture` 값과 Go 바이너리 출력만 봤고 차이가 없었습니다. Go 바이너리는 빌드 단계에서 `TARGETARCH` 로 만들어 요청한 구조였기 때문입니다.

`static` 안의 다른 파일 구조는 재지 않았고, BuildKit 소스에서 이 동작의 근거 문장은 찾지 않았습니다. 알파인 베이스에서는 구조 표시와 안의 실행 파일이 어긋난 이미지가 나왔으므로, 최종 단계에는 쓰지 않습니다.

### -ldflags 의 -s -w

> `-s -w` 는 심벌 테이블과 DWARF 디버그 정보를 지워 크기를 줄이는 링커 옵션이고, 줄인 만큼 스택 추적의 정보와 디버거 지원이 줄어듭니다.

이 시트의 예제는 `-trimpath -ldflags="-s -w"` 로 만든 이미지가 9538212바이트였습니다. 옵션을 빼고 비교한 크기는 재지 않았습니다.



## 관련 문서

> 같은 BuildKit 을 다른 앞단으로 쓰는 시트와 빌더 선택·Go 멀티 스테이지 개념 노트입니다.

- [buildctl·buildkitd 참조 시트](buildkit.md) — buildx 와 같은 BuildKit 을 `buildctl` 로 직접 부르는 방법
- [DevOps 명령어 시트](../README.md) — 같은 폴더 지도
- [이미지 빌더 종류와 선택](../../artifact/container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md) — 빌더를 고르는 기준
- [이미지 작게 만들고 미리 검사하기](../../../../08_cloud/book/cks-study-guide/06-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EC%9E%91%EA%B2%8C%20%EB%A7%8C%EB%93%A4%EA%B3%A0%20%EB%AF%B8%EB%A6%AC%20%EA%B2%80%EC%82%AC%ED%95%98%EA%B8%B0%20%E2%80%94%20%EB%B2%A0%EC%9D%B4%EC%8A%A4%20%EC%9D%B4%EB%AF%B8%EC%A7%80%C2%B7%EB%A9%80%ED%8B%B0%20%EC%8A%A4%ED%85%8C%EC%9D%B4%EC%A7%80%C2%B7Hadolint%C2%B7Kubesec.md) — Go 멀티 스테이지·distroless static 이미지



## 참고 자료

> 검증 환경, 공식 자료, 각주 정의입니다.

- 검증 환경: OrbStack Docker 29.8.2(linux/arm64), docker buildx v0.37.2, BuildKit v0.33.1
- 사용한 이미지: `golang:1.25`(go1.25.14), `gcr.io/distroless/static-debian13:nonroot`
- [Docker Docs — Multi-platform builds (고정 커밋)](https://github.com/docker/docs/blob/16e452c8eaea26cec842cbf1065037fb2015001f/content/manuals/build/building/multi-platform.md)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [cmd/cgo 문서 (go1.25.0)](https://github.com/golang/go/blob/go1.25.0/src/cmd/cgo/doc.go)
- [distroless README](https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/README.md)
- [distroless base README](https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/base/README.md)

[^docker-buildkit]: Docker Docs, BuildKit (2026-11-15 확인). "BuildKit is the builder backend used by Docker." <https://docs.docker.com/build/buildkit/>
[^auto-arg]: Docker Dockerfile reference (2026-11-25 확인). 이 기능은 "only available when using the BuildKit backend" 입니다. <https://docs.docker.com/reference/dockerfile/>
[^arg-scope]: Docker Dockerfile reference (2026-11-25 확인). "These arguments are defined in the global scope so are not automatically available inside build stages or for your RUN commands." 단계 안에서는 `ARG TARGETPLATFORM` 처럼 값 없이 다시 선언합니다. <https://docs.docker.com/reference/dockerfile/>
[^from-platform]: Docker Dockerfile reference (2026-11-25 확인). `FROM` 의 `--platform` 은 "By default, the target platform of the build request is used." 입니다. <https://docs.docker.com/reference/dockerfile/>
[^qemu-slow]: Docker Docs, Multi-platform builds (고정 커밋). "Emulation with QEMU can be much slower than native builds, especially for compute-heavy tasks like compilation and compression or decompression." <https://github.com/docker/docs/blob/16e452c8eaea26cec842cbf1065037fb2015001f/content/manuals/build/building/multi-platform.md>
[^mp-example]: Docker Docs, Multi-platform builds (고정 커밋). 멀티 플랫폼 빌드 방법은 에뮬레이션·여러 네이티브 노드·크로스 컴파일 셋이고, 크로스 컴파일 예가 `FROM --platform=$BUILDPLATFORM golang:alpine AS build` 로 `FROM` 을 빌더 플랫폼에 고정하고 `docker buildx build --platform linux/amd64,linux/arm64 .` 로 빌드합니다. <https://github.com/docker/docs/blob/16e452c8eaea26cec842cbf1065037fb2015001f/content/manuals/build/building/multi-platform.md>
[^cgo-default]: Go cmd/cgo 문서 (go1.25.0). "It is disabled by default when cross-compiling as well as when the CC environment variable is unset and the default C compiler (typically gcc or clang) cannot be found on the system PATH." <https://github.com/golang/go/blob/go1.25.0/src/cmd/cgo/doc.go>
[^distroless-static]: distroless base README (고정 커밋). "Statically compiled applications (Go) that do not require libc can use the `gcr.io/distroless/static` image" <https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/base/README.md>
[^distroless-shell]: distroless README (고정 커밋). "They do not contain package managers, shells or any other programs you would expect to find in a standard Linux distribution." 그리고 "The `:debug` image set for each language provides a busybox shell to enter." <https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/README.md>
