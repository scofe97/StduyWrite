---
title: buildctl·buildkitd 참조 시트
tags: [container, image-build, buildkit, buildctl, buildkitd, cli, reference]
status: draft
source:
  - https://github.com/moby/buildkit/blob/v0.34.1/README.md
  - https://github.com/moby/buildkit/blob/v0.34.1/docs/rootless.md
  - https://github.com/moby/buildkit/blob/v0.34.1/docs/buildkitd.toml.md
  - https://docs.docker.com/build/buildkit/
  - moby/buildkit:v0.34.1 이미지의 `buildctl --help`·`buildkitd --help` 원문
related:
  - 01-02.rootless 빌드의 조건.md
  - 01-03.이미지 빌더 종류와 선택.md
updated: 2026-11-15
---

# buildctl·buildkitd 참조 시트

---

> BuildKit 데몬을 띄우고 `buildctl` 로 Dockerfile 을 빌드해 registry·tar·폴더로 받고, 캐시를 주고받고, rootless 로 돌리는 방법을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `buildkitd` 는 빌드를 실행하는 데몬이고 `buildctl` 은 그 데몬에 빌드를 맡기고 결과를 받는 클라이언트입니다.

두 바이너리는 `moby/buildkit:v0.34.1` 이미지(Alpine Linux)에 들어 있습니다. `buildctl --version` 과 `buildkitd --version` 이 같은 `github.com/moby/buildkit v0.34.1 f5b59a1f2fb25a0cb7072c398cab9aed7835da4e` 를 찍습니다.

이 시트는 OrbStack 의 Docker Engine 29.8.2(linux/arm64)에서 이 이미지로 실측했습니다. `buildctl` 바이너리는 macOS·Windows 용도 있습니다. `buildkitd` 는 Linux 와 Windows 에서만 돌아서 macOS 에서는 컨테이너 안의 데몬에 붙여 씁니다.[^buildkit-os]

`docker build` 와 `docker buildx` 도 같은 BuildKit 을 빌더 백엔드로 쓰는 다른 앞단입니다.[^docker-buildkit] 이 시트는 buildx 를 다루지 않고 `buildctl` 만 다룹니다.



## 핵심 문법

> `buildctl` 은 서브커맨드로 동작을 정하고, `build` 는 frontend·`--local`·`--output` 세 가지로 입력과 결과를 정합니다.

```bash
# 호출 형태. buildctl --help 의 USAGE 줄
buildctl [global options] [command [command options]]

# buildkitd --help 의 USAGE 줄
buildkitd [global options]

# buildctl build --help 의 USAGE 예. $ 프롬프트를 빼고 줄만 나눴다
buildctl build \
  --frontend dockerfile.v0 \
  --opt target=foo \
  --opt build-arg:foo=bar \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=docker.io/username/image,push=true

# 데몬이 떠 있는지 워커를 본다 (데몬 주소와 워커 확인)
buildctl debug workers

# 다른 주소의 데몬에 붙는다 (데몬 주소와 워커 확인)
buildctl --addr 주소 debug workers

# Dockerfile 을 빌드해 이미지로 push 한다 (Dockerfile 빌드와 registry push)
buildctl build ... --output type=image,name=이름,push=true

# 빌드 메타데이터를 파일로 받는다 (빌드 결과 digest 받기)
buildctl build ... --metadata-file 경로

# 이미지를 tar 나 폴더로 받는다 (OCI tar 로 받기, 루트 파일시스템 폴더로 받기)
buildctl build ... --output type=oci,dest=파일
buildctl build ... --output type=local,dest=폴더

# ARG 값을 바꾸고 stage 를 고른다 (build-arg 로 값 바꾸기, target 으로 stage 하나만 빌드)
buildctl build ... --opt build-arg:이름=값
buildctl build ... --opt target=stage

# 데몬의 빌드 캐시를 본다 (캐시 크기 보기와 비우기)
buildctl du
buildctl prune --all

# 캐시를 registry 로 보내고 받아 온다 (registry 로 캐시 내보내기, 가져온 캐시로 다시 빌드)
buildctl build ... --export-cache type=registry,ref=이름
buildctl build ... --import-cache type=registry,ref=이름
```

### --output 의 type

> `--output` 은 빌드 결과를 어디에 어떤 모양으로 받을지 정하며, 본문에 나온 type 만 모았습니다.

뜻은 `buildctl build --help` 와 README 의 Output 절을 따랐습니다.[^buildkit-output]

```bash
# --output type=종류,키=값 꼴로 쓴다
# image   이미지를 만든다. name= 이미지 이름, push=true 면 push 까지 한다
# oci     이미지를 OCI 레이아웃 tar 파일 하나로 쓴다. dest= 으로 파일을 준다
# local   빌드가 끝난 파일시스템을 폴더로 푼다. dest= 이 없으면 오류가 난다
```



## 종료 코드

> `buildctl` 은 성공하면 0, `error:` 한 줄을 찍는 실패에는 1 을 돌려주고 모르는 서브커맨드에는 3 을 돌려줍니다.[^no-exit]

아래 예는 「실습 준비」 에서 만든 환경으로 돌립니다.

```bash
# 0  성공. --version 도 0 이다
# 1  실패. 연결 실패, 빌드 실패, 모르는 옵션 모두 error: 로 시작하는 줄을 낸다
# 3  모르는 서브커맨드. No help topic for '이름' 을 낸다

# 성공
buildctl --version; echo $?    # buildctl github.com/moby/buildkit v0.34.1 f5b59a1... / 0

# 모르는 서브커맨드
buildctl nope; echo $?    # No help topic for 'nope' / 3

# 모르는 옵션
buildctl build --badflag 2>&1 | grep '^error'    # error: flag provided but not defined: -badflag
buildctl build --badflag > /dev/null 2>&1; echo $?    # 1

# 닿지 않는 데몬 주소
#   --addr 주소   붙을 buildkitd 주소
buildctl --addr tcp://nohost:1234 debug workers; echo $?
```

```bash
error: failed to list workers: Unavailable: connection error: desc = "transport: Error while dialing: dial tcp: lookup nohost on 127.0.0.11:53: no such host"
1
```

위 블록의 `/` 는 한 줄 출력과 종료 코드를 한 줄에 줄여 적은 것입니다. 스크립트에서는 `buildctl build ... || exit 1` 처럼 종료 코드로 빌드 실패를 가릅니다.



## 유스케이스

> 예는 위에서 아래로 따라 치게 놓았고, 뒤 예는 앞 예에서 푼 옵션과 만든 상태만 씁니다.

### 실습 준비

> 아래 블록을 셸에 한 번 붙여 넣으면 이 시트의 예가 쓰는 파일과 컨테이너가 모두 생깁니다.

Docker 가 있는 macOS·Linux 에서 실행합니다. 이 시트는 외부 registry 로 push 하지 않고 같은 docker 네트워크의 `registry:2` 로만 push 합니다. buildkitd 의 TCP 주소는 TLS 없이 열면 위험하고 실습의 격리된 네트워크 안에서만 씁니다.[^tcp-mtls]

```bash
# 작업 폴더. 「Dockerfile 빌드와 registry push」 부터 여러 곳에서 쓴다
mkdir -p ~/buildkit-lab/out && cd ~/buildkit-lab

# 빌드할 Dockerfile. stage 둘, ARG 하나, 2초 걸리는 RUN 하나다
cat > Dockerfile <<'EOF'
FROM alpine:3.20 AS base
ARG GREETING=hello
RUN sleep 2 && echo "$GREETING from base" > /greeting.txt

FROM base AS final
RUN echo "built by buildkit" > /who.txt
CMD ["cat", "/greeting.txt", "/who.txt"]
EOF

# 데몬 설정. HTTP 로 받는 registry:5000 에 push 를 허용한다
cat > buildkitd.toml <<'EOF'
[registry."registry:5000"]
  http = true
EOF

# 실습 전용 docker 네트워크
docker network create bk-lab

# 이 네트워크 안에서 registry:5000 으로 부를 registry
#   -d                       백그라운드로 띄운다 (--detach)
#   --rm                     멈추면 컨테이너를 지운다
#   --name 이름              컨테이너 이름
#   --network 네트워크       붙일 docker 네트워크
#   --network-alias 별칭     그 네트워크 안에서 부를 이름
docker run -d --rm \
  --name bk-registry \
  --network bk-lab \
  --network-alias registry \
  registry:2

# buildkitd. 이미지 이름 뒤는 buildkitd 의 옵션이다
#   --privileged             RUN 용 컨테이너를 만들 수 있게 권한 제한을 푼다
#   -v 호스트:컨테이너       폴더를 컨테이너와 공유한다 (--volume)
#   -w 경로                  컨테이너 안 작업 폴더 (--workdir)
#   --config 파일            buildkitd 설정 파일
#   --addr 주소              데몬이 듣는 주소. 소켓과 TCP 를 함께 연다
docker run -d --rm \
  --name bk-buildkitd \
  --network bk-lab \
  --network-alias buildkitd \
  --privileged \
  -v "$PWD":/work \
  -w /work \
  moby/buildkit:v0.34.1 \
  --config /work/buildkitd.toml \
  --addr unix:///run/buildkit/buildkitd.sock \
  --addr tcp://0.0.0.0:1234

# 호스트에는 buildctl 이 없어 같은 이름의 함수로 컨테이너 안의 buildctl 을 부른다
buildctl() { docker exec -w /work bk-buildkitd buildctl "$@"; }

# 데몬이 소켓을 열 때까지 기다린다
sleep 3
```

`out/` 은 결과를 받는 폴더입니다. `buildctl` 함수는 이 셸에서만 살아 있습니다. 이후 `buildctl` 은 모두 이 함수를 거쳐 컨테이너 안에서 실행됩니다.

### 데몬 주소와 워커 확인

> 데몬이 떠 있는지는 `buildctl debug workers` 가 워커 한 줄을 돌려주는지로 압니다.

```bash
# 워커 목록. 워커가 나오면 데몬에 닿은 것이다
buildctl debug workers
```

```bash
ID                          PLATFORMS
aqv24ihizs1my2zmplupuql97   linux/arm64,linux/amd64,linux/amd64/v2,linux/riscv64,linux/ppc64le,linux/s390x,linux/386,linux/mips64le,linux/arm/v7,linux/arm/v6
```

ID 는 데몬을 띄울 때마다 달라지고 PLATFORMS 의 첫 항목은 이 시트를 돌린 arm64 호스트의 것입니다. 열 사이의 탭은 공백으로 적었습니다.

다른 컨테이너에서는 TCP 주소로 같은 데몬에 붙습니다.

```bash
# 데몬이 아니라 buildctl 만 담은 컨테이너를 띄워 TCP 주소로 붙는다
#   --entrypoint 실행파일   이미지의 기본 실행 파일 대신 이것을 실행한다
#   --addr 주소             buildkitd 주소. 기본값은 unix:///run/buildkit/buildkitd.sock
docker run --rm \
  --network bk-lab \
  --entrypoint buildctl \
  moby/buildkit:v0.34.1 \
  --addr tcp://buildkitd:1234 \
  debug workers
```

```bash
ID                          PLATFORMS
aqv24ihizs1my2zmplupuql97   linux/arm64,linux/amd64,linux/amd64/v2,linux/riscv64,linux/ppc64le,linux/s390x,linux/386,linux/mips64le,linux/arm/v7,linux/arm/v6
```

같은 워커 ID 가 나오므로 소켓으로 붙은 것과 TCP 로 붙은 것은 같은 데몬입니다. `--addr` 없이 이 컨테이너에서 부르면 기본 소켓이 없어 「종료 코드」 의 오류가 납니다.

### Dockerfile 빌드와 registry push

> Dockerfile 이 있는 폴더를 빌드해 같은 네트워크의 registry 로 push 하는 것이 `buildctl` 의 기본 용도입니다.

```bash
# 현재 폴더의 Dockerfile 을 빌드해 registry:5000/lab/app:v1 로 push 한다
#   build                      빌드를 시작한다
#   --frontend dockerfile.v0   입력을 Dockerfile 로 해석하는 frontend
#   --local context=폴더       빌드 컨텍스트 폴더. COPY·ADD 가 읽는다
#   --local dockerfile=폴더    Dockerfile 이 있는 폴더
#   --output 종류,키=값        결과를 받는 방식. type=image,push=true 는 push
#   --progress plain           진행을 줄 단위 로그로 찍는다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true \
  --progress plain
```

```bash
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 242B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/alpine:3.20
#2 DONE 2.1s
...
#5 [base 2/2] RUN sleep 2 && echo "hello from base" > /greeting.txt
#5 DONE 2.1s

#6 [final 1/1] RUN echo "built by buildkit" > /who.txt
#6 DONE 0.1s

#7 exporting to image
#7 exporting layers 0.2s done
#7 exporting manifest sha256:04973291fb5cafd7d45ea9f3ed52aec4a01e0d0f5f02f54c3b623a4c4d48820f done
#7 exporting config sha256:6a60364e8fe1ee1458b2523db3cb703f659fde97e5a40b8df0746eddba74e5f2 done
#7 pushing layers 0.1s done
#7 pushing manifest for registry:5000/lab/app:v1@sha256:04973291fb5cafd7d45ea9f3ed52aec4a01e0d0f5f02f54c3b623a4c4d48820f done
#7 DONE 0.2s
```

출력이 길어 가운데를 `...` 로 줄였습니다. `#5` 의 2.1s 가 `sleep 2` 라서 이 단계가 실제로 실행됐다는 표시입니다.

```bash
# registry 의 태그 목록으로 push 를 확인한다
#   -qO-   wget 의 -q 는 진행 표시를 끄고, -O- 는 응답을 표준 출력으로 보낸다
docker run --rm --network bk-lab --entrypoint wget moby/buildkit:v0.34.1 -qO- http://registry:5000/v2/lab/app/tags/list
# {"name":"lab/app","tags":["v1"]}
```

### 빌드 결과 digest 받기

> `--metadata-file` 은 push 한 이미지의 digest 를 JSON 파일로 남겨서 다음 단계가 읽을 수 있게 합니다.

```bash
# 같은 빌드를 다시 하면서 메타데이터를 out/meta.json 에 쓴다
#   --metadata-file 경로   빌드 메타데이터(이미지 digest 등)를 JSON 으로 쓴다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true \
  --metadata-file out/meta.json

cat out/meta.json
```

```bash
{
  "containerimage.config.digest": "sha256:6a60364e8fe1ee1458b2523db3cb703f659fde97e5a40b8df0746eddba74e5f2",
  "containerimage.descriptor": {
    "mediaType": "application/vnd.oci.image.manifest.v1+json",
    "digest": "sha256:04973291fb5cafd7d45ea9f3ed52aec4a01e0d0f5f02f54c3b623a4c4d48820f",
    "size": 857,
    "platform": {
      "architecture": "arm64",
      "os": "linux"
    }
  },
  "containerimage.digest": "sha256:04973291fb5cafd7d45ea9f3ed52aec4a01e0d0f5f02f54c3b623a4c4d48820f",
  "image.name": "registry:5000/lab/app:v1"
}
```

`containerimage.digest` 가 위 push 때 찍힌 manifest digest 와 같습니다. 같은 Dockerfile 을 같은 캐시로 다시 빌드해서 digest 도 같았습니다. 실습을 처음부터 다시 하면 digest 값은 달라집니다.

### OCI tar 로 받기

> `type=oci` 는 registry 없이 이미지를 OCI 레이아웃 tar 파일 하나로 받아서 파일로 옮기거나 검사하게 합니다.

```bash
# 이미지를 out/app-oci.tar 로 받고 안의 파일 목록을 본다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=oci,dest=out/app-oci.tar

tar -tf out/app-oci.tar
```

```bash
blobs/
blobs/sha256/
blobs/sha256/04973291fb5cafd7d45ea9f3ed52aec4a01e0d0f5f02f54c3b623a4c4d48820f
blobs/sha256/221345f78b56140307e1dce0b2a0663ddeb49e862f9da4830ccf4a7f309294a2
blobs/sha256/3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78
blobs/sha256/6a60364e8fe1ee1458b2523db3cb703f659fde97e5a40b8df0746eddba74e5f2
blobs/sha256/cfcaff80101ad21f5af9851681e376a62486342563790383873b0d0e798a609d
index.json
oci-layout
```

`index.json` 과 `oci-layout` 이 OCI 레이아웃의 표지입니다. 첫 blob 의 이름이 위 manifest digest 와 같습니다.

### 루트 파일시스템 폴더로 받기

> `type=local` 은 이미지가 아니라 빌드가 끝난 파일시스템을 폴더로 풀어 줘서 결과 파일을 바로 열어 보게 합니다.

```bash
# 최종 stage 의 파일시스템을 out/rootfs 폴더로 푼다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=local,dest=out/rootfs

ls out/rootfs | head -3
cat out/rootfs/greeting.txt out/rootfs/who.txt
```

```bash
bin
dev
etc
hello from base
built by buildkit
```

Dockerfile 의 `RUN` 이 쓴 두 파일이 Alpine 의 루트 파일시스템 위에 그대로 있습니다.

### build-arg 로 값 바꾸기

> `--opt build-arg:이름=값` 은 Dockerfile 의 `ARG` 기본값을 빌드 한 번 동안만 바꿉니다.

```bash
# GREETING 을 hola 로 바꿔 빌드하고 결과 파일을 읽는다
#   --opt 키=값   frontend 에 넘기는 옵션. build-arg:이름=값 은 ARG 값을 바꾼다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --opt build-arg:GREETING=hola \
  --output type=local,dest=out/arg

cat out/arg/greeting.txt    # hola from base
```

### target 으로 stage 하나만 빌드

> `--opt target=stage` 는 multi-stage Dockerfile 에서 그 stage 까지만 빌드합니다.

```bash
# base stage 까지만 빌드하면 final stage 의 who.txt 는 만들어지지 않는다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --opt target=base \
  --output type=local,dest=out/base

ls out/base | grep -E 'greeting|who'    # greeting.txt
```

없는 stage 이름을 주면 `error: failed to solve: target stage "nope" could not be found` 로 끝납니다. 종료 코드는 1 입니다.

### 캐시 크기 보기와 비우기

> `buildctl du` 는 데몬이 쌓아 둔 빌드 캐시를 보여 주고 `buildctl prune --all` 은 그것을 비웁니다.

```bash
# 위 빌드들이 쌓은 캐시 레코드를 본다
buildctl du
```

```bash
ID                                                                      RECLAIMABLE   SIZE      LAST ACCESSED
m0vi8tzi2t968bmwx9wpx9nj2*                                              true          0B
1k95coz1q3wsgarj3eqey3ej4                                               true          4.10kB
...
s1nv4h1588rq6okgasdm89qlr                                               true          14.55MB
Reclaimable:    14.57MB
Total:          14.57MB
```

레코드가 일곱 줄 나와 일부를 `...` 로 줄였고 열 사이의 탭은 공백으로 적었습니다.

```bash
# 내부 참조까지 모두 지우고 다시 본다
#   --all   내부·frontend 참조까지 포함해 지운다
buildctl prune --all
buildctl du
```

```bash
ID                                                                      RECLAIMABLE   SIZE      LAST ACCESSED
...
Total:  14.57MB
ID      RECLAIMABLE     SIZE    LAST ACCESSED
Reclaimable:    0B
Total:          0B
```

위 블록은 `prune` 이 지운 레코드 ID 목록의 끝과 합계, 그다음 `du` 의 빈 표를 이어 붙였습니다. 이후 예는 비운 캐시에서 시작합니다.

### registry 로 캐시 내보내기

> `--export-cache` 는 빌드 캐시를 이미지와 따로 registry 에 올려서 캐시가 없는 다른 데몬이 받아 쓰게 합니다.[^buildkit-cache]

```bash
# 이미지를 push 하면서 캐시를 registry:5000/lab/cache:app 에 올린다
#   --export-cache 종류,키=값   캐시를 내보낸다. mode=max 는 중간 단계 레이어까지 올린다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true \
  --export-cache type=registry,ref=registry:5000/lab/cache:app,mode=max \
  --progress plain 2>&1 | grep -E 'exporting cache|writing cache'
```

```bash
#8 exporting cache to registry
#8 writing cache image manifest sha256:5fefcae140f1fb56aae1d78c315367b18dba8a39a5a4513de92dc623cace958c
#8 writing cache image manifest sha256:5fefcae140f1fb56aae1d78c315367b18dba8a39a5a4513de92dc623cace958c done
```

```bash
# registry 에 cache 저장소가 생겼는지 태그 목록으로 확인한다
docker run --rm --network bk-lab --entrypoint wget moby/buildkit:v0.34.1 -qO- http://registry:5000/v2/lab/cache/tags/list
# {"name":"lab/cache","tags":["app"]}
```

### 가져온 캐시로 다시 빌드

> `--import-cache` 로 registry 의 캐시를 가져오면 로컬 캐시가 비어 있어도 `RUN` 단계를 다시 실행하지 않습니다.

```bash
# 로컬 캐시를 비우고 캐시 없이 빌드해 CACHED 줄 수를 센다
buildctl prune --all > /dev/null

buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true \
  --progress plain 2>&1 | grep -c CACHED    # 0
```

```bash
# 다시 비우고 registry 의 캐시를 가져와 빌드한다
#   --import-cache 종류,키=값   registry 의 캐시를 가져온다
buildctl prune --all > /dev/null

buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true \
  --import-cache type=registry,ref=registry:5000/lab/cache:app \
  --progress plain 2>&1 | grep -E 'importing cache|CACHED'
```

```bash
#4 importing cache manifest from registry:5000/lab/cache:app
#6 CACHED
#7 CACHED
```

가져온 캐시로는 `RUN` 두 단계가 `CACHED` 이고 2초짜리 `sleep` 도 다시 돌지 않았습니다. 캐시 없이 빌드한 앞 블록은 `CACHED` 가 0줄입니다.

### registry 인증 정보 읽기

> `buildctl` 은 registry 로그인 정보를 `buildctl` 을 실행한 쪽의 docker 설정 파일에서 읽어 빌드 세션으로 데몬에 넘깁니다.[^buildkit-auth]

이 시트의 실습은 인증 없는 로컬 registry 로 돌려서 아래 블록은 실행하지 않았습니다. 근거는 각주의 소스와 문서입니다.

```bash
# registry.example.com 에 로그인하면 docker 설정 파일에 로그인 정보가 남는다
docker login registry.example.com

# buildctl 이 읽는 파일. 위치는 Linux 기준이다
# ~/.docker/config.json

# 설정 파일에 credential helper 를 두면 helper 가 비밀번호를 맡는다 (macOS 키체인 예)
# { "credsStore" : "osxkeychain" }
```

이 시트처럼 `buildctl` 을 컨테이너 안에서 실행하면 읽는 파일도 그 컨테이너 안의 설정 파일입니다. 호스트의 로그인 정보가 필요하면 그 파일을 컨테이너에 공유해야 합니다.

### 데몬 없이 컨테이너 하나로 빌드

> `buildctl-daemonless.sh` 는 컨테이너 안에서 임시 데몬을 띄워 빌드 한 번을 하고 함께 끝나서, 상시 데몬 없이 CI 한 단계로 빌드하게 합니다.[^daemonless]

```bash
# 임시 buildkitd 로 빌드하고 결과를 out/daemonless.tar 로 받는다
#   --entrypoint buildctl-daemonless.sh   임시 buildkitd 를 띄워 buildctl 을 한 번 실행한다
docker run --rm \
  --privileged \
  -v "$PWD":/work \
  --entrypoint buildctl-daemonless.sh \
  moby/buildkit:v0.34.1 \
  build \
  --frontend dockerfile.v0 \
  --local context=/work \
  --local dockerfile=/work \
  --output type=oci,dest=/work/out/daemonless.tar

ls out/daemonless.tar
```

```bash
out/daemonless.tar
```

이 컨테이너의 데몬은 빌드가 끝나면 사라지므로 `bk-buildkitd` 의 캐시를 쓰지 못합니다. 그래서 `#5` 의 `RUN sleep 2` 가 2.1s 걸려 새로 실행됐습니다.

### rootless buildkitd 띄우기

> rootless 이미지는 root 가 아닌 사용자로 buildkitd 를 띄우며, Docker 에서는 `--security-opt` 와 `--oci-worker-no-process-sandbox` 가 빠질 때마다 서로 다른 오류가 납니다.[^rootless-doc]

보안 옵션 없이 띄우면 데몬이 시작도 하지 못합니다.

```bash
# 보안 옵션 없이 rootless 이미지를 띄운다
docker run --rm \
  --name bk-rootless \
  --network bk-lab \
  moby/buildkit:v0.34.1-rootless
echo "rc=$?"
```

```bash
[rootlesskit:parent] error: failed to start the child: fork/exec /proc/self/exe: operation not permitted
rc=1
```

`seccomp=unconfined` 를 주면 데몬은 뜨지만 `RUN` 단계가 실패합니다. 아래 `rbuild` 는 rootless 데몬의 소켓 경로로 빌드하는 이 유스케이스 전용 함수입니다.

```bash
# rootless 데몬은 /run/user/1000/... 소켓에서 듣는다. 인자는 그대로 buildctl build 로 넘어간다
rbuild() {
  docker exec -w /work bk-rootless buildctl \
    --addr unix:///run/user/1000/buildkit/buildkitd.sock \
    build \
    --frontend dockerfile.v0 \
    --local context=. \
    --local dockerfile=. \
    --output type=local,dest=/tmp/out "$@"
}

# seccomp 프로필만 푼 rootless 데몬을 띄워 빌드한다
#   --security-opt 값   컨테이너의 보안 옵션. seccomp=unconfined 는 시스템 콜 제한을 푼다
docker run -d --rm \
  --name bk-rootless \
  --network bk-lab \
  -v "$PWD":/work \
  -w /work \
  --security-opt seccomp=unconfined \
  moby/buildkit:v0.34.1-rootless

sleep 4
rbuild 2>&1 | grep -m1 'runc run failed'

docker rm -fv bk-rootless
```

```bash
#5 0.084 runc run failed: unable to start container process: error during container init: error mounting "proc" to rootfs at "/proc": mount src=proc, dst=/proc, dstFd=/proc/thread-self/fd/15, flags=MS_NOSUID|MS_NODEV|MS_NOEXEC: operation not permitted
```

`0.084` 와 `fd/15` 는 실행마다 달라지는 값입니다. 이 오류는 `RUN` 마다 새 `/proc` 을 마운트하지 못해서 납니다. 두 가지 방법으로 피합니다.

```bash
# 방법 1. buildkitd 의 --oci-worker-no-process-sandbox. RUN 이 호스트의 /proc 을 쓴다
docker run -d --rm \
  --name bk-rootless \
  --network bk-lab \
  -v "$PWD":/work \
  -w /work \
  --security-opt seccomp=unconfined \
  moby/buildkit:v0.34.1-rootless \
  --oci-worker-no-process-sandbox

sleep 4
rbuild --progress plain 2>&1 | tail -1    # #7 DONE 0.1s
docker exec bk-rootless id -u    # 1000

docker rm -fv bk-rootless
```

```bash
# 방법 2. systempaths=unconfined 로 컨테이너의 /proc 마스크를 푼다
docker run -d --rm \
  --name bk-rootless \
  --network bk-lab \
  -v "$PWD":/work \
  -w /work \
  --security-opt seccomp=unconfined \
  --security-opt apparmor=unconfined \
  --security-opt systempaths=unconfined \
  moby/buildkit:v0.34.1-rootless

sleep 4
rbuild --progress plain 2>&1 | tail -1    # #7 DONE 0.1s
docker exec bk-rootless id -u    # 1000

docker rm -fv bk-rootless
```

두 방법 모두 빌드가 성공했고 데몬의 사용자 ID 는 1000 입니다. `apparmor=unconfined` 는 AppArmor 를 쓰는 호스트에서만 필요합니다.[^rootless-doc] 이 호스트의 `docker info` 보안 옵션에는 apparmor 가 없습니다. 문서는 방법 1 을 권하지 않습니다. Kubernetes 에는 방법 2 에 해당하는 설정이 없어서 그곳의 예제는 방법 1 을 씁니다.

### 실습 정리

```bash
# 컨테이너와 네트워크를 지운다 (「rm -f 뒤에 남는 익명 볼륨」)
#   -f   실행 중이어도 지운다 (--force)
#   -v   컨테이너의 익명 볼륨까지 지운다 (--volumes)
docker rm -fv bk-buildkitd bk-registry
docker network rm bk-lab

# buildctl 함수와 작업 폴더를 지운다. 받은 이미지는 지우지 않는다
unset -f buildctl rbuild
cd ~ && rm -rf ~/buildkit-lab
```



## 주의사항과 동작 원리

### HTTP registry push 의 HTTPS 시도

> 설정 없는 데몬은 registry 에 HTTPS 로 먼저 말을 걸어서 HTTP 만 받는 registry 로 push 하지 못합니다.

```bash
# 설정 파일 없이 데몬을 하나 더 띄운다
docker run -d --rm \
  --name bk-nocfg \
  --network bk-lab \
  --privileged \
  -v "$PWD":/work \
  -w /work \
  moby/buildkit:v0.34.1

sleep 3

# 설정 없는 데몬으로 push
docker exec -w /work bk-nocfg buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true 2>&1 | tail -1
```

```bash
error: failed to solve: failed to push registry:5000/lab/app:v1: failed to do request: Head "https://registry:5000/v2/lab/app/blobs/sha256:3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78": http: server gave HTTP response to HTTPS client
```

```bash
# 이 push 한 번에만 HTTP 를 허용한다
#   registry.insecure=true   --output 의 키. HTTP registry 로 push 한다
docker exec -w /work bk-nocfg buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --output type=image,name=registry:5000/lab/app:v1,push=true,registry.insecure=true 2>&1 | tail -1    # #7 DONE 0.1s

docker rm -fv bk-nocfg
```

`buildkitd.toml` 의 `http = true` 는 그 registry 로 가는 모든 빌드에 적용됩니다. `registry.insecure=true` 는 그 출력에만 적용됩니다.[^registry-insecure]

### 결과를 받지 않는 빌드

> `--output` 이 없으면 빌드는 성공하지만 결과가 데몬 안에만 남고 어디에도 내보내지 않습니다.

```bash
# --output 없이 빌드하고 exporting 단계가 몇 줄 나왔는지 센다
buildctl build \
  --frontend dockerfile.v0 \
  --local context=. \
  --local dockerfile=. \
  --progress plain 2>&1 | grep -c exporting    # 0
```

종료 코드는 0 이라서 CI 에서 성공으로 읽히지만 push 도 파일도 없습니다.[^buildkit-output]

### 클라이언트 쪽 경로

> `--local` 과 `type=oci,dest=` 의 경로는 데몬이 아니라 `buildctl` 을 실행한 쪽 파일시스템 기준입니다.

```bash
# 데몬 컨테이너에는 없는 /src 를 클라이언트 컨테이너에만 공유해 빌드한다
docker run --rm \
  --network bk-lab \
  -v "$PWD":/src \
  --entrypoint buildctl \
  moby/buildkit:v0.34.1 \
  --addr tcp://buildkitd:1234 \
  build \
  --frontend dockerfile.v0 \
  --local context=/src \
  --local dockerfile=/src \
  --output type=oci,dest=/src/out/client.tar

ls out/client.tar    # out/client.tar
docker exec bk-buildkitd ls /src    # ls: /src: No such file or directory
```

빌드 컨텍스트는 클라이언트가 세션으로 데몬에 보내고 결과 tar 도 클라이언트 쪽에 쓰이므로, 데몬 컨테이너에 같은 폴더를 공유하지 않아도 됩니다.[^local-flag]


### rm -f 뒤에 남는 익명 볼륨

> `--rm` 으로 띄운 컨테이너도 `docker rm -f` 로 지우면 이미지가 선언한 익명 볼륨이 남고, `-v` 를 붙여야 함께 지워집니다.

```bash
# -f 만 준 경우. 컨테이너가 쓰던 볼륨 이름을 먼저 적어 둔다
docker run -d --rm --name bk-vol --privileged moby/buildkit:v0.34.1
sleep 2
vol=$(docker inspect -f '{{range .Mounts}}{{.Name}}{{end}}' bk-vol)
docker rm -f bk-vol
docker volume ls -q | grep -c "$vol"    # 1
docker volume rm "$vol"

# -fv 를 준 경우
docker run -d --rm --name bk-vol --privileged moby/buildkit:v0.34.1
sleep 2
vol=$(docker inspect -f '{{range .Mounts}}{{.Name}}{{end}}' bk-vol)
docker rm -fv bk-vol
docker volume ls -q | grep -c "$vol"    # 0
```

`moby/buildkit` 이미지는 `/var/lib/buildkit` 을 볼륨으로 선언해서 컨테이너마다 익명 볼륨이 하나씩 생깁니다. `docker stop` 으로 멈추면 `--rm` 이 이 볼륨도 함께 지웁니다.[^volume-rm]



## 관련 문서

> 이 시트의 예와 이어지는 개념 편과 K8s 쪽 실측 노트입니다.

- [이미지 빌더 종류와 선택](01-03.이미지%20빌더%20종류와%20선택.md) — BuildKit 을 다른 빌더와 견주는 기준
- [rootless 빌드의 조건](01-02.rootless%20빌드의%20조건.md) — user namespace·seccomp 가 rootless 빌드에 필요한 이유
- [Image Builder — 클러스터 안에서 이미지를 빌드하기](../../../../08_cloud/book/kubernetes-patterns/30-01.Image%20Builder%20—%20클러스터%20안에서%20이미지를%20빌드하기.md) — Pod 안에서 BuildKit rootless 로 빌드한 실측
- [컨테이너 이미지 빌드](../../../02_Jenkins/03_agent/01-04.컨테이너%20이미지%20빌드.md) — Kaniko 와 daemon-free 빌드의 비교



## 참고 자료

> 검증 환경, 공식 자료, 각주 정의입니다.

- 검증 환경: OrbStack Docker 29.8.2(linux/arm64), `moby/buildkit:v0.34.1`(rootless 태그 포함), `registry:2`(2.8.3), `alpine:3.20`
- [BuildKit README (v0.34.1)](https://github.com/moby/buildkit/blob/v0.34.1/README.md)
- [BuildKit rootless 문서 (v0.34.1)](https://github.com/moby/buildkit/blob/v0.34.1/docs/rootless.md)
- [buildkitd.toml 문서 (v0.34.1)](https://github.com/moby/buildkit/blob/v0.34.1/docs/buildkitd.toml.md)
- [Docker Docs — BuildKit](https://docs.docker.com/build/buildkit/)

[^buildkit-os]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "While the `buildctl` client is available for Linux, macOS, and Windows, the `buildkitd` daemon is only available for Linux and *Windows currently." <https://github.com/moby/buildkit/blob/v0.34.1/README.md>
[^docker-buildkit]: Docker Docs, BuildKit (2026-11-15 확인). "BuildKit is the builder backend used by Docker." <https://docs.docker.com/build/buildkit/>
[^tcp-mtls]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "Enabling TCP without mTLS is dangerous because the executor containers (aka Dockerfile `RUN` containers) can call BuildKit API as well." <https://github.com/moby/buildkit/blob/v0.34.1/README.md>
[^buildkit-output]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "By default, the build result and intermediate cache will only remain internally in BuildKit. An output needs to be specified to retrieve the result." `buildctl build --help` 는 `--output string, -o string  Define exports for build result, e.g. --output type=image,name=docker.io/username/image,push=true` 로 적습니다. <https://github.com/moby/buildkit/blob/v0.34.1/README.md>
[^no-exit]: `buildctl` 은 man 페이지가 없고 `--help` 와 README 에도 종료 코드 설명이 없습니다. 아래 값은 컨테이너에서 해당 호출을 돌려 `echo $?` 로 읽은 것입니다.
[^buildkit-cache]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "`mode=<min|max>`: specify cache layers to export (default: `min`)" / "`max`: export all the layers of all intermediate steps" <https://github.com/moby/buildkit/blob/v0.34.1/README.md>
[^buildkit-auth]: Moby BuildKit, cmd/buildctl/build.go (v0.34.1, 2026-11-15 확인). `dockerConfig := config.LoadDefaultConfigFile(os.Stderr)` 가 `buildctl` 안에서 호출되고 그 결과가 `authprovider.NewDockerAuthProvider(...)` 로 빌드 세션에 붙습니다. Docker Docs 는 설정 파일을 "$HOME/.docker/config.json on Linux" 라고 적고, 매뉴얼에 `{ "credsStore" : "osxkeychain" }` 예가 있습니다. <https://github.com/moby/buildkit/blob/v0.34.1/cmd/buildctl/build.go> <https://docs.docker.com/reference/cli/docker/login/>
[^daemonless]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "To run the client and an ephemeral daemon in a single container ("daemonless mode"):" 이미지 안 `/usr/bin/buildctl-daemonless.sh` 의 머리 주석은 "buildctl-daemonless.sh spawns ephemeral buildkitd for executing buildctl." 입니다. <https://github.com/moby/buildkit/blob/v0.34.1/README.md>
[^rootless-doc]: Moby BuildKit, docs/rootless.md (v0.34.1, 2026-11-15 확인). "`seccomp=unconfined`: For allowing several syscalls such as `unshare` (used by runc) and `mount` (used by snapshotters, etc)." / "`apparmor=unconfined`: ... This flag is not needed when the host operating system does not use AppArmor." / "`systempaths=unconfined`: For disabling the masks for the `/proc` mount in the container" / "Using `--oci-worker-no-process-sandbox` is discouraged" <https://github.com/moby/buildkit/blob/v0.34.1/docs/rootless.md>
[^registry-insecure]: Moby BuildKit, README.md (v0.34.1, 2026-11-15 확인). "`registry.insecure=true`: push to insecure HTTP registry" 설정 파일 쪽은 docs/buildkitd.toml.md 의 `[registry."yourmirror.local:5000"]` 아래 `http = true` 예입니다. <https://github.com/moby/buildkit/blob/v0.34.1/README.md> <https://github.com/moby/buildkit/blob/v0.34.1/docs/buildkitd.toml.md>
[^volume-rm]: `docker rm --help` (Docker 29.8.2)에서 `-v, --volumes  Remove anonymous volumes associated with the container` 입니다. `docker image inspect moby/buildkit:v0.34.1 --format '{{.Config.Volumes}}'` 는 `map[/var/lib/buildkit:{}]` 를 돌려줍니다(실측). `registry:2` 이미지도 `/var/lib/registry` 를 같은 방식으로 선언합니다.
[^local-flag]: `buildctl build --help` (v0.34.1). "`--local string [ --local string ]  Allow build access to the local directory`" 이 옵션은 데몬이 아니라 `buildctl` 이 읽는 로컬 디렉터리를 빌드에 연다는 뜻이며, 아래 실측이 데몬 컨테이너에 없는 `/src` 로 빌드가 성공함을 보여 줍니다.
