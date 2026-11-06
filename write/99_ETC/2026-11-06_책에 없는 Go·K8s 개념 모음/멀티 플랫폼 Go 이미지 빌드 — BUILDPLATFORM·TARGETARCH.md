---
title: 멀티 플랫폼 Go 이미지 빌드 — BUILDPLATFORM·TARGETARCH
tags: [go, docker, buildx, multi-platform, cross-compile, distroless]
status: draft
source:
  - https://raw.githubusercontent.com/docker/docs/16e452c8eaea26cec842cbf1065037fb2015001f/content/manuals/build/building/multi-platform.md
  - https://docs.docker.com/reference/dockerfile/  # (2026-11-06 확인)
  - https://raw.githubusercontent.com/golang/go/go1.25.0/src/cmd/cgo/doc.go
  - https://go.dev/doc/install/source  # (2026-11-06 확인)
  - https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/README.md
  - https://github.com/GoogleContainerTools/distroless/blob/c3bf6a1d94037418960aa093212f11a943334266/base/README.md
updated: 2026-11-06
---

# 멀티 플랫폼 Go 이미지 빌드 — BUILDPLATFORM·TARGETARCH

---

> Go 이미지를 amd64 와 arm64 둘 다 만들 때는 빌드 단계를 빌더의 네이티브 플랫폼에 고정하고 `GOOS`·`GOARCH` 로 크로스 컴파일하면 에뮬레이션 없이 끝납니다. 임시 참고 문서이며 정본은 나중에 따로 만듭니다.

## 1. 크로스 컴파일 기반 멀티 플랫폼 빌드

> buildx 가 채워 주는 자동 ARG 로 빌더 플랫폼과 대상 플랫폼을 구분하고, 최종 이미지는 distroless `nonroot` 로 만듭니다.

### 풀려는 문제

개발 장비와 운영 서버의 CPU 구조가 다른 일이 흔합니다. Apple 실리콘 노트북은 arm64 이고 클러스터 노드는 amd64 일 수 있습니다. 한쪽 구조로만 만든 이미지는 다른 쪽에서 쓸 수 없으므로 두 구조를 모두 담은 이미지를 만들어야 합니다.

Docker 문서는 멀티 플랫폼 이미지를 만드는 방법을 세 가지로 나눕니다.

- 에뮬레이션: QEMU 로 다른 구조의 CPU 를 흉내 내서 빌드합니다.
- 네이티브 노드 여러 개: 구조마다 진짜 장비에서 빌드합니다.
- 크로스 컴파일: 멀티 스테이지 빌드에서 한 구조 장비가 다른 구조용 결과물을 만듭니다.

에뮬레이션은 설정이 가장 쉽지만 느립니다. 문서는 "Emulation with QEMU can be much slower than native builds" 라고 적고, 코드를 컴파일하는 것처럼 CPU 를 많이 쓰는 작업에서 특히 그렇다고 덧붙입니다. Go 는 컴파일러가 대상 구조를 직접 지원하므로 세 번째 방법이 잘 맞습니다.

이 문서가 쓴 환경은 Docker 29.8.2(OrbStack, BuildKit v0.33.1), Go 1.25 입니다.

### 자동 ARG 네 가지

BuildKit 은 빌드할 때 플랫폼 정보를 `ARG` 로 자동 설정합니다. Dockerfile 레퍼런스는 이 기능을 "only available when using the BuildKit backend" 라고 적습니다. 값은 빌드를 수행하는 노드(빌드 플랫폼)와 결과 이미지(대상 플랫폼) 두 쪽으로 나뉩니다.

| ARG | 뜻 | 예 |
|-----|----|----|
| `BUILDPLATFORM` | 빌드를 수행하는 노드의 플랫폼 | `linux/arm64` |
| `TARGETPLATFORM` | 빌드 결과물의 플랫폼 | `linux/amd64`, `linux/arm/v7` |
| `TARGETOS` | `TARGETPLATFORM` 의 OS 부분 | `linux` |
| `TARGETARCH` | `TARGETPLATFORM` 의 구조 부분 | `amd64`, `arm64` |

같은 문서는 이 외에도 `BUILDOS`, `BUILDARCH`, `BUILDVARIANT`, `TARGETVARIANT` 를 같은 방식으로 정의합니다. 대상 플랫폼은 `docker build` 의 `--platform` 플래그로 정합니다.

한 가지 규칙을 꼭 알아야 합니다. 문서는 이렇게 적습니다.

> "These arguments are defined in the global scope so are not automatically available inside build stages or for your RUN commands."

단계 안에서 쓰려면 값 없이 다시 선언합니다.

```dockerfile
FROM alpine
ARG TARGETPLATFORM
RUN echo "I'm building for $TARGETPLATFORM"
```

### 에뮬레이션을 피하는 원리

핵심은 `FROM --platform=$BUILDPLATFORM` 입니다. Dockerfile 레퍼런스는 `FROM` 의 `--platform` 플래그를 설명하며 기본값을 이렇게 적습니다. "By default, the target platform of the build request is used." 즉 아무것도 쓰지 않으면 빌드 단계도 대상 플랫폼 이미지로 시작하고, 그것이 빌더와 다른 구조이면 `RUN` 이 에뮬레이션으로 실행됩니다.

`--platform=$BUILDPLATFORM` 을 주면 빌드 단계의 베이스 이미지가 빌더의 네이티브 플랫폼으로 고정됩니다. Docker 의 멀티 플랫폼 문서도 같은 형태를 보입니다. 그러면 `go build` 는 네이티브 속도로 돌고, 결과물의 구조만 `GOOS`·`GOARCH` 환경 변수로 정합니다.

Go 설치 문서는 이 두 변수를 이렇게 정의합니다. "The name of the target operating system and compilation architecture." `GOARCH` 의 기본값은 빌드 호스트 구조입니다. 그래서 `TARGETARCH` 를 `GOARCH` 에 넘기는 것이 크로스 컴파일의 전부입니다.

### CGO_ENABLED=0

`CGO_ENABLED=0` 은 C 코드 연결을 끕니다. cgo 문서는 기본 동작을 이렇게 적습니다.

> "It is disabled by default when cross-compiling as well as when the CC environment variable is unset and the default C compiler (typically gcc or clang) cannot be found on the system PATH."

크로스 컴파일이 아닌 빌드에서는 C 컴파일러가 있으면 기본으로 켜집니다. 같은 Dockerfile 이 빌드 환경에 따라 다르게 동작하지 않도록 기본값에 기대지 않고 `0` 을 명시합니다.

이 값이 중요한 이유는 최종 이미지입니다. 정적으로 링크된 Go 바이너리는 libc 가 없는 이미지에서도 실행됩니다. cgo 를 켜면 시스템 라이브러리에 의존하게 되어 아래 distroless `static` 이미지에서 실행되지 않을 수 있습니다.

### distroless nonroot 최종 이미지

distroless 는 실행에 필요한 것만 담은 이미지입니다. README 는 "They do not contain package managers, shells or any other programs" 라고 적습니다. 이미지가 작고 공격 면이 줄어드는 이유입니다.

정적 Go 바이너리용은 `static` 이미지입니다. base 문서는 이렇게 설명합니다.

> "Statically compiled applications (Go) that do not require libc can use the `gcr.io/distroless/static` image"

내용물은 ca-certificates, root 사용자의 `/etc/passwd` 항목, `/tmp` 디렉터리, tzdata 입니다. cgo 로 libc 가 필요한 Go 앱은 `base` 부터 시작하라고 안내합니다.

태그는 `latest`, `nonroot`, `debug`, `debug-nonroot` 가 있습니다. 이 문서가 열어 본 README 에서는 Debian 13 기반 태그(`static-debian13`)만 보였습니다. `nonroot` 태그를 내려받아 확인한 결과 기본 사용자는 UID 65532 였고 엔트리포인트는 비어 있었습니다.

### 최소 예제

일반 예제 프로그램입니다.

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Println("hello from", runtime.GOOS, runtime.GOARCH)
}
```

Dockerfile 은 다음과 같습니다.

```dockerfile
# syntax=docker/dockerfile:1

# 빌드 단계는 항상 빌더의 네이티브 플랫폼에서 돌립니다. QEMU 에뮬레이션을 쓰지 않습니다.
FROM --platform=$BUILDPLATFORM golang:1.25 AS build

# 전역 스코프의 자동 ARG 는 단계 안에서 값 없이 다시 선언해야 보입니다.
ARG TARGETOS
ARG TARGETARCH

WORKDIR /src
COPY go.mod ./
COPY main.go ./

# 크로스 컴파일: 실행 플랫폼은 BUILDPLATFORM, 결과물 플랫폼은 TARGETOS/TARGETARCH 입니다.
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -trimpath -ldflags="-s -w" -o /out/app .

# 최종 이미지는 --platform 을 쓰지 않아 대상 플랫폼 이미지가 선택됩니다.
FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

빌드 명령은 Docker 문서의 형태를 따릅니다.

```bash
docker buildx build --platform linux/amd64,linux/arm64 .
```

이 문서의 환경(arm64 호스트)에서 두 플랫폼 빌드는 성공했습니다. 빌드 로그에서 `RUN` 단계가 `[linux/arm64->amd64 build 5/5]` 와 `[linux/arm64 build 5/5]` 로 나타났고, 각각 `GOARCH=amd64`, `GOARCH=arm64` 로 실행됐습니다. `linux/arm64->amd64` 표기는 arm64 빌더에서 amd64 결과를 만든다는 뜻입니다.

arm64 이미지를 로컬에 불러와 실행하면 `hello from linux arm64` 가 출력됩니다. 이미지의 사용자는 `nonroot:nonroot`, 크기는 약 9.5MB 였습니다. 셸이 없다는 것도 확인했습니다. `--entrypoint /bin/sh` 로 실행하면 `exec: "/bin/sh": stat /bin/sh: no such file or directory` 오류가 납니다. 안을 들여다봐야 하면 `:debug` 태그를 씁니다. README 는 "The `:debug` image set for each language provides a busybox shell to enter." 라고 적습니다.

### 흔한 함정

- 단계 안에서 `ARG TARGETARCH` 를 다시 선언하지 않으면 값이 비어 `GOARCH` 가 호스트 구조로 정해집니다. 문서가 "not automatically available inside build stages" 라고 경고한 부분입니다.
- 최종 단계에 `--platform=$BUILDPLATFORM` 을 쓰면 결과 이미지가 빌더 구조가 됩니다. 최종 단계에는 쓰지 않습니다.
- cgo 가 필요한 의존성(예: 일부 SQLite 드라이버)이 있으면 `CGO_ENABLED=0` 으로 빌드가 깨지거나 기능이 빠집니다. 크로스 컴파일에서는 cgo 가 기본으로 꺼진다는 점이 이를 뒷받침합니다. 이 경우 구조별 C 크로스 컴파일러를 갖추거나 네이티브 노드 방식을 쓰는 것이 길인데, 이 문서는 그 절차를 열어 보지 않았습니다.
- `nonroot` 이미지에서 바이너리가 쓰기를 해야 하면 권한 오류가 납니다. 쓰기 경로는 `/tmp` 나 볼륨으로 따로 마련합니다.
- 셸이 없어서 `docker exec ... sh` 로 들어갈 수 없습니다. 디버깅 때만 `:debug-nonroot` 같은 태그로 바꿔 씁니다.
- `-ldflags="-s -w"` 는 디버그 정보를 지워 크기를 줄입니다. 대신 스택 추적의 정보가 줄고 디버거로 보기 어렵습니다.

### 공식 문서 근거

| 출처 | 확인한 문장 | 이 문서에서 쓴 곳 |
|------|------------|------------------|
| Docker multi-platform | "Emulation with QEMU can be much slower than native builds" | 에뮬레이션 비용 |
| Docker multi-platform | "docker buildx build --platform linux/amd64,linux/arm64 ." | 빌드 명령 |
| Dockerfile 레퍼런스 | "These arguments are defined in the global scope so are not automatically available inside build stages or for your RUN commands." | ARG 재선언 |
| Dockerfile 레퍼런스 | "By default, the target platform of the build request is used." | FROM --platform |
| Go 설치 문서 | "The name of the target operating system and compilation architecture." | GOOS·GOARCH |
| cmd/cgo | "It is disabled by default when cross-compiling" | CGO_ENABLED |
| distroless README | "They do not contain package managers, shells or any other programs" | 최종 이미지 |
| distroless base README | "Statically compiled applications (Go) that do not require libc can use the `gcr.io/distroless/static` image" | static 선택 |

distroless 문서는 main 브랜치에서 열었고 커밋 해시로 고정하지 못했습니다. 위 모든 주소는 frontmatter 의 `source` 와 같습니다.
