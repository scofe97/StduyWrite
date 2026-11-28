---
title: "docker 참조 시트"
tags: ["cloud", "command", "container", "docker", "image"]
status: draft
source:
  - "Docker Engine v29.8.2 docker --help 와 하위 명령 --help 원문 (OrbStack macOS 실측)"
  - "https://docs.docker.com/reference/cli/docker/image/save/"
  - "https://docs.docker.com/reference/cli/docker/image/load/"
  - "https://docs.docker.com/reference/cli/docker/container/export/"
  - "https://docs.docker.com/reference/cli/docker/image/import/"
  - "https://docs.docker.com/engine/storage/containerd/"
  - "https://docs.docker.com/engine/release-notes/29/"
related:
  - ../README.md
  - ./docker%20컨테이너%20실행과%20조회.md
  - ../../kubernetes/architecture/%EC%9D%B4%EB%AF%B8%EC%A7%80%20pull%C2%B7%ED%8F%90%EC%87%84%EB%A7%9D%20%EB%B0%98%EC%9E%85.md
  - ../../../../02_os/docs/cmd/isolate/nerdctl.md
updated: "2026-11-21"
---

# docker 참조 시트

---

> 이미지를 tar 로 묶어 내보내고 들이며, 압축·태그 복원·저장소 등록까지 다루는 `docker` 반입 명령을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `docker save` 와 `docker load` 는 중앙 레지스트리 없이 파일과 파이프로 이미지를 백업하고 옮기는 명령입니다.

`docker` 는 Docker 공식 CLI 바이너리이고 이 시트는 이미지 반입 명령만 다룹니다. 출력은 OrbStack macOS 의 Docker Engine 29.8.2 에서 받았고 받는 호스트는 Ubuntu VM 의 29.1.3 입니다. 두 엔진은 `docker info` 의 DriverStatus 가 `io.containerd.snapshotter.v1` 이라 containerd 이미지 저장소를 씁니다. 가장 새 버전은 29.10.0 이고 overlay2 를 쓰는 엔진은 실측하지 않았습니다.[^env]



## 핵심 문법

> `save` 로 이미지를 파일이나 표준 출력으로 묶고, `load` 로 파일이나 표준 입력에서 풀어 엔진에 등록합니다.

```bash
# 호출 형태
# docker --help 와 하위 명령 --help 의 Usage 줄
docker save [OPTIONS] IMAGE [IMAGE...]
docker load [OPTIONS]
docker export [OPTIONS] CONTAINER
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
docker push [OPTIONS] NAME[:TAG]

# 이미지를 tar 파일로 묶어 저장한다 (이미지를 tar 로 내보내기)
docker save -o 파일 이미지

# 표준 출력으로 내보내 리다이렉션이나 파이프로 넘긴다 (표준 출력과 파이프로 내보내기)
docker save 이미지 > 파일

# 여러 이미지를 tar 하나로 묶는다 (여러 이미지를 한 tar 로 묶기)
docker save -o 파일 이미지1 이미지2

# tar 파일에서 이미지를 들인다 (tar 파일에서 이미지 들이기)
docker load -i 파일
docker load < 파일

# save 출력을 gzip 으로 한 번 더 압축하고 load 로 읽는다 (gzip 으로 한 번 더 압축하기)
docker save 이미지 | gzip > 파일.tar.gz
docker load -i 파일.tar.gz

# 파이프로 다른 호스트의 docker 에 바로 넘긴다 (다른 호스트로 파이프 전송하기)
docker save 이미지 | ssh 호스트 docker load

# 들인 이미지의 ID 와 digest 를 맞댄다 (반입한 이미지의 정보 확인하기)
docker image inspect -f '{{.Id}}' 이미지

# 플랫폼 하나만 골라 내보낸다 (플랫폼 지정하여 내보내기)
docker save --platform 플랫폼 -o 파일 이미지

# 들인 이미지를 저장소에 올린다 (반입한 이미지를 저장소에 올리기)
docker tag 이미지 저장소/이미지:태그
docker push 저장소/이미지:태그
```

### 이미지를 가리키는 표기

```bash
# IMAGE 자리에 쓰는 표기
# 이름:태그   저장소 이름과 태그. save 와 push 에 쓰며 태그가 아카이브에 남는다
# ID          이미지의 고유 해시. save 에 쓰면 manifest.json 의 RepoTags 가 null 이 된다
```

### 이 시트가 실행하지 않은 옵션

```bash
# docker import 의 옵션이다. --help 원문만 옮겼고 실행하지 않았다
#   -c, --change   만들어지는 이미지에 Dockerfile 명령을 적용한다
#   -m, --message  가져온 이미지에 커밋 메시지를 단다
#   --platform     멀티 플랫폼을 지원하는 서버에서 플랫폼을 지정한다
```



## 종료 코드

> 성공하면 0, 없는 이미지나 아카이브 파일을 지정해 실패하면 1 입니다.[^exit]

```bash
# 0  이미지 저장이나 복원이 성공했을 때
# 1  없는 이미지를 지정하거나 없는 아카이브 파일을 읽으려 할 때
docker save -o cmdsheet-alpine.tar alpine:3.20 > /dev/null; echo $?    # 0
docker save -o cmdsheet-nonexistent.tar nosuchimage:nonexistent 2>&1; echo $?
# Error response from daemon: No such image: nosuchimage:nonexistent / 1

docker load -i cmdsheet-nonexistent.tar 2>&1; echo $?
# open cmdsheet-nonexistent.tar: no such file or directory / 1
```



## 유스케이스

> 예는 앞 예가 만든 상태를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 아래 블록을 한 번 붙여 넣으면 이 시트의 예가 쓰는 베이스 이미지 셋이 준비됩니다.

```bash
# 실습에 쓸 베이스 이미지를 미리 받는다
#   pull -q   다운로드 진행 상황을 숨기고 받은 이미지의 전체 이름만 출력한다
docker pull -q alpine:3.20
docker pull -q busybox:1.36.0
docker pull -q registry:2
```

```bash
# 결과
docker.io/library/alpine:3.20
docker.io/library/busybox:1.36.0
docker.io/library/registry:2
```

### 이미지를 tar 로 내보내기

> `docker save` 에 `-o` 를 주어 로컬 이미지를 단일 tar 아카이브 파일로 저장합니다.

```bash
# 이미지를 tar 파일로 내보낸다
#   save -o   표준 출력 대신 지정한 파일에 tar 아카이브를 쓴다
docker save -o cmdsheet-alpine.tar alpine:3.20

# 만든 파일의 크기를 바이트로 잰다
#   wc -c   바이트 수를 센다
wc -c cmdsheet-alpine.tar    #  7910912 cmdsheet-alpine.tar

# tar 바깥 층에 있는 파일을 본다 (blobs 폴더 밖)
#   tar -t   아카이브 안의 파일 목록을 나열한다
#   tar -f   작업할 tar 파일 경로를 지정한다
tar -tf cmdsheet-alpine.tar | grep -v blobs
```

```bash
# 결과
index.json
manifest.json
oci-layout
```

이미지 레이어와 설정 JSON, 매니페스트는 `blobs/sha256/` 아래에 있고 그 바깥에 위 세 파일이 놓입니다. 이 구조는 containerd 이미지 저장소를 쓰는 엔진 두 대에서 본 모양입니다.

### 표준 출력과 파이프로 내보내기

> `-o` 를 생략하면 표준 출력으로 스트림을 내보내므로 리다이렉션이나 파이프로 넘길 수 있습니다.

```bash
# 표준 출력을 리다이렉션(>)으로 받아 tar 파일로 저장한다
docker save alpine:3.20 > cmdsheet-alpine-stdout.tar

# 파일 크기를 잰다
wc -c cmdsheet-alpine-stdout.tar    #  7910912 cmdsheet-alpine-stdout.tar

# -o 로 만든 파일과 바이트 단위로 같은지 맞댄다
#   cmp   두 파일이 같으면 아무것도 출력하지 않고 0 으로 끝난다
cmp cmdsheet-alpine.tar cmdsheet-alpine-stdout.tar && echo same    # same

# 파이프로 wc 에 이어 출력되는 바이트 수를 센다
docker save alpine:3.20 | wc -c    # 7910912
```

리다이렉션으로 만든 파일과 `-o` 로 만든 파일은 크기도 내용도 같습니다.

### 여러 이미지를 한 tar 로 묶기

> `save` 뒤에 이미지 이름을 나열하면 tar 하나에 여러 이미지의 레이어와 매니페스트가 함께 묶입니다.

```bash
# 이미지 둘을 아카이브 하나로 묶어 한 번에 옮길 때 쓴다
docker save -o cmdsheet-bundle.tar alpine:3.20 busybox:1.36.0

# 아카이브 안에 manifest.json 이 있는지 본다
tar -tf cmdsheet-bundle.tar | grep manifest.json    # manifest.json

# manifest.json 의 항목마다 RepoTags 를 뽑아 본다
tar -xOf cmdsheet-bundle.tar manifest.json \
  | python3 -I -c \
  "import sys,json; print([m['RepoTags'] for m in json.load(sys.stdin)])"
```

```bash
# 결과
[['alpine:3.20'], ['busybox:1.36.0']]
```

`manifest.json` 은 묶인 이미지마다 항목 하나를 두고, 항목의 `RepoTags` 에 저장할 때 준 이름이 들어갑니다.

### tar 파일에서 이미지 들이기

> `docker load` 에 `-i` 나 표준 입력을 주어 tar 파일에서 이미지와 태그를 복원합니다.

```bash
# tar 파일에서 이미지를 들인다
#   load -i   표준 입력 대신 지정한 파일에서 tar 아카이브를 읽는다
docker load -i cmdsheet-alpine.tar    # Loaded image: alpine:3.20

# 리다이렉션(<)으로 표준 입력에 넘겨 들인다
docker load < cmdsheet-alpine.tar    # Loaded image: alpine:3.20

# 안내 출력을 숨기려고 -q 를 붙인다
#   load -q   --help 설명은 Suppress the load output 이다
docker load -q -i cmdsheet-alpine.tar    # Loaded image: alpine:3.20
```

엔진에 이미 있는 이미지를 다시 `load` 해도 오류 없이 같은 `Loaded image` 줄이 나옵니다. `-q` 는 출력을 숨긴다고 했지만 이 엔진에서는 있어도 없어도 출력이 같았습니다.

### gzip 으로 한 번 더 압축하기

> `save` 출력을 `gzip` 에 넘겨도 거의 줄지 않는 것은 tar 안의 레이어가 이미 gzip 이기 때문이고, `load` 는 gzip 파일을 그대로 읽습니다.

```bash
# save 출력을 gzip 으로 압축해 파일로 저장한다
docker save alpine:3.20 | gzip > cmdsheet-alpine.tar.gz

# 압축 파일의 크기를 잰다
wc -c cmdsheet-alpine.tar.gz    #  7727649 cmdsheet-alpine.tar.gz

# tar 안의 레이어 blob 이 어떤 형식인지 본다 (arm64 레이어와 amd64 레이어)
#   file -   표준 입력으로 받은 데이터의 형식을 알려 준다
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78 \
  2>/dev/null | file -    # /dev/stdin: gzip compressed data
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/25f1d6b1951ac8eb3740558fe94cb83d377bdadf95fd9f98b50d2e1b96130471 \
  2>/dev/null | file -    # /dev/stdin: gzip compressed data

# 레이어 둘의 합, 레이어 밖 바이트, gzip 으로 줄어든 바이트를 계산한다
python3 -I -c \
  "print(4092319 + 3630321, 7910912 - (4092319 + 3630321), 7910912 - 7727649)"    # 7722640 188272 183263

# gzip 으로 압축한 파일도 따로 풀지 않고 load 가 바로 읽는다
docker load -i cmdsheet-alpine.tar.gz    # Loaded image: alpine:3.20
```

7,910,912 바이트짜리 tar 에서 레이어 둘이 7,722,640 바이트이고 둘 다 gzip 이라, 줄어든 183,263 바이트는 레이어 밖 188,272 바이트(설정·매니페스트 JSON, tar 헤더와 패딩)에서 나온 것으로 계산됩니다. 크기를 크게 줄이려면 gzip 이 아니라 「플랫폼 지정하여 내보내기」 처럼 담을 플랫폼을 줄입니다.

공식 문서는 `load` 가 gzip, bzip2, xz, zstd 로 압축한 아카이브를 읽는다고 적습니다.[^load-compress] 이 시트에서 실행한 것은 gzip 뿐입니다.

### 다른 호스트로 파이프 전송하기

> `save` 의 표준 출력을 받는 호스트의 `docker load` 로 바로 이어 파일 저장 없이 반입합니다.

```bash
# 로컬 save 의 표준 출력을 Ubuntu VM 의 docker load 표준 입력으로 잇는다
#   orb -m ubuntu   OrbStack 의 ubuntu VM 안에서 뒤 명령을 실행한다
docker save alpine:3.20 | orb -m ubuntu sudo docker load    # Loaded image: alpine:3.20
```

폐쇄망이나 원격 운영 환경에서는 `orb -m ubuntu sudo` 자리에 `ssh 호스트` 를 두는 것이 일반 형태입니다. 이 시트에서는 ssh 를 실행해 보지 않았습니다.

### 반입한 이미지의 정보 확인하기

> `docker image inspect` 로 반입한 이미지의 ID, 저장소 digest, 아키텍처를 보고 받는 쪽 엔진의 ID 와 맞댑니다.

```bash
# 이미지 ID 를 읽어 받는 쪽과 맞댈 값으로 쓴다
#   inspect -f   Go 템플릿으로 출력할 필드를 정한다
docker image inspect -f '{{.Id}}' alpine:3.20
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# 저장소 digest 등록 목록을 본다
docker image inspect -f '{{.RepoDigests}}' alpine:3.20
# [alpine@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc]

# 아키텍처와 운영체제를 본다
docker image inspect -f '{{.Architecture}} {{.Os}}' alpine:3.20    # arm64 linux

# 받는 쪽(Ubuntu VM) 엔진에서 같은 이미지의 ID 를 읽어 위 값과 맞댄다
orb -m ubuntu sudo docker image inspect -f '{{.Id}}' alpine:3.20
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# ID 와 같은 이름의 blob 이 tar 안에 있고 그 내용의 SHA-256 이 ID 와 같은지 본다
#   shasum -a 256   입력의 SHA-256 해시를 낸다
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc \
  | shasum -a 256    # d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc  -

# 같은 blob 의 크기를 잰다
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc \
  | wc -c    # 9226
```

보낸 쪽과 받은 쪽의 ID 가 같습니다. 이 엔진에서 이미지 ID 는 tar 의 `blobs/sha256/d9e853e8…` 파일(9,226 바이트)의 digest 이고, 그 파일은 플랫폼 8개의 매니페스트를 적은 이미지 인덱스라서 save 와 load 로 옮겨도 ID 가 변하지 않습니다.

### 플랫폼 지정하여 내보내기

> `--platform` 으로 플랫폼 하나만 골라 내보내 아카이브 용량을 줄입니다.

```bash
# 엔진에 내용이 있는 linux/amd64 만 골라 tar 파일로 내보낸다
#   save --platform   저장할 플랫폼을 os[/arch[/variant]] 로 지정한다
docker save \
  --platform linux/amd64 \
  -o cmdsheet-amd64.tar \
  alpine:3.20

# 기본 save 와 크기를 맞댄다 (기본 save 는 7910912 바이트였다)
wc -c cmdsheet-amd64.tar    #  3722752 cmdsheet-amd64.tar

# tar 안의 설정 blob 에서 아키텍처를 직접 꺼낸다
tar -xOf cmdsheet-amd64.tar \
  blobs/sha256/bf8527eb54c3680e728d5b4b383a8ba730d72dae7236fbc8dff97ed6b224a731 \
  | python3 -I -c \
  "import sys,json; c=json.load(sys.stdin); print(c['architecture'], c['config']['Cmd'])"    # amd64 ['/bin/sh']

# 기본 save 한 tar 의 manifest.json 항목 수를 센다
tar -xOf cmdsheet-alpine.tar manifest.json \
  | python3 -I -c "import sys,json; print(len(json.load(sys.stdin)))"    # 1

# 기본 save 한 tar 의 이미지 인덱스에 적힌 플랫폼 목록을 본다 (증명 항목 unknown 은 거른다)
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc \
  | python3 -I -c "
import json, sys
data = json.load(sys.stdin)
for m in data['manifests']:
    p = m['platform']
    if p['os'] != 'unknown':
        v = p.get('variant', '')
        print('/'.join(filter(None, [p['os'], p['architecture'], v])))
"
```

```bash
# 결과 (인덱스에 적힌 플랫폼 8개)
linux/amd64
linux/arm/v6
linux/arm/v7
linux/arm64/v8
linux/386
linux/ppc64le
linux/riscv64
linux/s390x
```

이 엔진은 arm64 호스트이고 alpine:3.20 의 amd64 와 arm64 내용을 둘 다 가집니다. 그래서 기본 `save` 는 레이어 둘(4,092,319 바이트와 3,630,321 바이트)을 담지만 `manifest.json` 항목은 호스트 플랫폼 하나입니다. `--platform linux/amd64` 로 저장하면 3,722,752 바이트로 줄고 설정 blob 의 `architecture` 가 `amd64` 입니다.

`--platform` 은 28.0.0 에서 들어왔고 쉼표로 여러 플랫폼을 고르는 것은 29.0.0 부터입니다.[^platform-ver] 두 엔진이 모두 29 라서 28.0.0 보다 낮은 엔진은 돌려 보지 않았습니다.

### 반입한 이미지를 저장소에 올리기

> 반입한 이미지에 사설 저장소 주소를 붙여 태깅하고 `push` 로 등록합니다.

```bash
# 테스트용 로컬 사설 레지스트리를 5000번 포트로 띄운다
#   run -d       백그라운드에서 컨테이너를 실행한다
#   run --name   컨테이너 이름을 지정한다
#   run -p       호스트 포트와 컨테이너 포트를 묶는다
docker run -d --name cmdsheet-registry -p 5000:5000 registry:2

# 반입한 이미지에 로컬 레지스트리 주소를 태그로 단다
docker tag alpine:3.20 localhost:5000/cmdsheet-alpine:3.20

# 로컬 레지스트리로 이미지를 올린다
docker push localhost:5000/cmdsheet-alpine:3.20
```

```bash
# 결과
The push refers to repository [localhost:5000/cmdsheet-alpine]
3f26bc2dec0b: Pushed
3.20: digest: sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d size: 1026

 Info -> Not all multiplatform-content is present and only the available single-platform image was pushed
         sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc -> sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
```

멀티 플랫폼 이미지는 엔진에 내용이 있는 단일 플랫폼 이미지 하나(`size: 1026` 매니페스트)만 올라가고 위처럼 Info 줄이 붙습니다. 폐쇄망 내부 레지스트리로 배포할 때는 `load` 뒤에 `tag` 와 `push` 를 거쳐 워커 노드들이 가져가게 합니다.

### 실습 정리

> 유스케이스가 만든 컨테이너와 태그, tar 파일을 지웁니다.

```bash
# 테스트 레지스트리 컨테이너와 컨테이너에 연결된 익명 볼륨을 지운다
#   docker rm -f   실행 중인 컨테이너도 강제로 종료하고 지운다
#   docker rm -v   컨테이너에 연결된 익명 볼륨까지 지운다
docker rm -fv cmdsheet-registry

# 저장소 주소를 붙인 로컬 태그를 지운다
docker rmi localhost:5000/cmdsheet-alpine:3.20

# 유스케이스에서 만든 tar 아카이브와 압축 파일을 지운다
#   rm -f   없는 파일이어도 오류를 내지 않는다
rm -f \
  cmdsheet-alpine.tar \
  cmdsheet-alpine-stdout.tar \
  cmdsheet-bundle.tar \
  cmdsheet-alpine.tar.gz \
  cmdsheet-amd64.tar
```

```bash
# 결과
cmdsheet-registry
Untagged: localhost:5000/cmdsheet-alpine:3.20
```



## 주의사항과 동작 원리

### ID 로 내보낼 때의 태그 유실

> 이미지 ID 로 `save` 하면 `manifest.json` 의 `RepoTags` 가 `null` 이 되어 받는 쪽 기본 목록에서 빠집니다.

```bash
# 이미지 ID 를 읽어 ID 로 save 한다
docker image inspect -f '{{.Id}}' busybox:1.36.0
# sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

docker save \
  -o cmdsheet-by-id.tar \
  sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

# manifest.json 에서 RepoTags 를 본다
tar -xOf cmdsheet-by-id.tar manifest.json | python3 -m json.tool
```

```bash
# 결과
[
    {
        "Config": "blobs/sha256/3596868f4ba86907dde5849edf4f426f4dc2110b1ace9e5969f5a21838ca9599",
        "RepoTags": null,
        "Layers": [
            "blobs/sha256/805f301826ef94301d30be8873f4c2f9a03fd5cad88b4d71808991046153eb86"
        ]
    }
]
```

```bash
# 이 이미지가 없는 받는 호스트(Ubuntu VM)에 load 하면 이름 없는 이미지로 들어간다
cat cmdsheet-by-id.tar | orb -m ubuntu sudo docker load
# Loaded image ID: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

# 기본 목록에는 나타나지 않는다
#   images --format   출력 모양을 Go 템플릿으로 정한다
orb -m ubuntu sudo docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}'
```

```bash
# 결과
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
```

```bash
# -a 를 붙여야 <none>:<none> 으로 보인다
#   images -a   이름 없는 이미지까지 보인다
orb -m ubuntu sudo docker images -a --format '{{.Repository}}:{{.Tag}} {{.ID}}'
```

```bash
# 결과
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
<none>:<none> 9e2bbca07938
```

```bash
# 이름으로 save 하면 RepoTags 가 유지된다
docker save -o cmdsheet-by-name.tar busybox:1.36.0
tar -xOf cmdsheet-by-name.tar manifest.json | python3 -m json.tool
```

```bash
# 결과
[
    {
        "Config": "blobs/sha256/3596868f4ba86907dde5849edf4f426f4dc2110b1ace9e5969f5a21838ca9599",
        "RepoTags": [
            "busybox:1.36.0"
        ],
        "Layers": [
            "blobs/sha256/805f301826ef94301d30be8873f4c2f9a03fd5cad88b4d71808991046153eb86"
        ]
    }
]
```

```bash
# 이미 이름 없이 들인 이미지에는 tag 로 이름을 붙인다
orb -m ubuntu sudo docker tag \
  sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112 \
  cmdsheet-trap:1.0

# tag 뒤에는 기본 목록에 나타난다
orb -m ubuntu sudo docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}'
```

```bash
# 결과
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
cmdsheet-trap:1.0 9e2bbca07938
```

```bash
# 이 함정이 만든 받는 호스트의 이미지(붙인 태그도 함께 지워진다)와 tar 를 지운다
orb -m ubuntu sudo docker rmi \
  sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
rm -f cmdsheet-by-id.tar cmdsheet-by-name.tar
```

```bash
# 결과
Untagged: cmdsheet-trap:1.0
Deleted: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
```

ID 로 저장한 아카이브는 `RepoTags` 가 `null` 이라 이름 없이 들어오므로, 반입 대상은 ID 가 아니라 `저장소:태그` 로 지정해야 이름이 함께 옮겨집니다.[^tag-loss] 이 확인은 containerd 이미지 저장소를 쓰는 엔진 두 대에서 했고, 그래프 드라이버 엔진의 목록 동작은 확인하지 않았습니다.

### export 와 save 의 층 차이

> `export` 는 컨테이너 파일시스템만 납작하게 묶으므로 이미지의 빌드 히스토리와 `CMD` 메타데이터가 사라집니다.

```bash
# 컨테이너를 만들어 파일시스템 전체를 tar 로 내보낸다
#   export -o   표준 출력 대신 지정한 파일에 tar 를 쓴다
docker create --name cmdsheet-export-demo alpine:3.20
# ef4c6719a6fdc17c09f897b633cb92998875da82cb1df2ab3d29f05d8cd1e95c

docker export -o cmdsheet-exported.tar cmdsheet-export-demo

# 그 tar 를 import 로 들여 새 이미지를 만든다
docker import cmdsheet-exported.tar cmdsheet-imported:1.0
# sha256:414de12feaf7a640bebe80172d7d1a831e06352c6e46c26ec6451954798c9c43

# 히스토리가 Imported from - 한 층으로 평탄해졌는지 본다
docker history cmdsheet-imported:1.0
```

```bash
# 결과
IMAGE          CREATED                  CREATED BY   SIZE      COMMENT
414de12feaf7   Less than a second ago                10.4MB    Imported from -
```

```bash
# import 한 이미지의 기본 실행 명령(Cmd)이 비어 있다
docker image inspect -f '{{.Config.Cmd}}' cmdsheet-imported:1.0    # []

# 원본 이미지를 save 한 tar 의 설정 JSON 에는 Cmd 가 남아 있다 (arm64 설정 blob)
docker save -o cmdsheet-alpine.tar alpine:3.20
tar -xOf cmdsheet-alpine.tar \
  blobs/sha256/ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4 \
  | python3 -I -c \
  "import sys,json; c=json.load(sys.stdin); print(c['architecture'], c['config']['Cmd'])"    # arm64 ['/bin/sh']

# 이 함정이 만든 컨테이너와 이미지, tar 를 지운다
docker rm -fv cmdsheet-export-demo
docker rmi cmdsheet-imported:1.0
rm -f cmdsheet-exported.tar cmdsheet-alpine.tar
```

```bash
# 결과
cmdsheet-export-demo
Untagged: cmdsheet-imported:1.0
Deleted: sha256:414de12feaf7a640bebe80172d7d1a831e06352c6e46c26ec6451954798c9c43
```

이미지의 빌드 구조와 실행 설정을 보존하려면 `export` 가 아니라 `save` 와 `load` 를 써야 합니다.[^export-save]

### 엔진에 없는 플랫폼을 지정할 때의 오류

> 엔진에 내용이 없는 플랫폼을 지정하면 `save` 도 `load` 도 오류를 내고 아카이브가 만들어지지 않습니다.

```bash
# 인덱스에는 있어도 엔진에 내용이 없는 플랫폼을 고르면 오류가 난다
docker save \
  --platform linux/s390x \
  -o cmdsheet-s390x.tar \
  alpine:3.20; echo $?

docker save \
  --platform linux/amd64 \
  -o cmdsheet-bb-amd64.tar \
  busybox:1.36.0; echo $?
```

```bash
# 결과
Error response from daemon: no suitable export target found: image with reference alpine:3.20 was found but does not provide the specified platform (linux/s390x)
1
Error response from daemon: no suitable export target found: image with reference busybox:1.36.0 was found but does not provide the specified platform (linux/amd64)
1
```

```bash
# 엔진에 내용이 있는 플랫폼을 고르면 정상으로 끝난다
docker save \
  --platform linux/amd64 \
  -o cmdsheet-amd64.tar \
  alpine:3.20; echo $?    # 0
```

```bash
# load 도 같은 규칙이다. arm64 내용만 든 busybox 아카이브에서 amd64 를 고르면 오류가 난다
#   load --platform   불러올 플랫폼을 지정한다
docker save -o cmdsheet-bb.tar busybox:1.36.0
cat cmdsheet-bb.tar \
  | orb -m ubuntu sudo docker load --platform linux/amd64

# 내용이 있는 플랫폼은 들인다
cat cmdsheet-bb.tar \
  | orb -m ubuntu sudo docker load --platform linux/arm64    # Loaded image: busybox:1.36.0
```

```bash
# 결과 (amd64)
requested platform(s) ([linux/amd64]) found, but some content is missing: NotFound: content digest sha256:086417a48026173aaadca4ce43a1e4b385e8e62cc738ba79fc6637049674cac0: not found
```

```bash
# 이 함정이 만든 받는 호스트의 이미지와 tar 를 지운다
orb -m ubuntu sudo docker rmi busybox:1.36.0
rm -f cmdsheet-amd64.tar cmdsheet-bb.tar
```

```bash
# 결과
Untagged: busybox:1.36.0
Deleted: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
```

`docker save` 는 엔진에 레이어 데이터가 실제로 있는 플랫폼만 내보낼 수 있어서, 인덱스에 이름이 있어도 내용이 없으면 오류가 납니다.[^multiplatform] 위 예에서 오류가 난 것은 alpine 의 s390x 와 busybox 의 amd64 이고 tar 파일은 만들어지지 않았습니다.



## 관련 문서

> 이 시트와 이어지는 문서입니다.

- [클라우드 명령어 시트](../README.md) — 컨테이너와 쿠버네티스 도구의 시트 모음
- [docker 컨테이너 실행과 조회](./docker%20컨테이너%20실행과%20조회.md) — 반입한 이미지로 컨테이너를 띄우고 `ps`·`logs`·`exec`·`stop` 으로 다루는 시트
- [이미지 pull과 폐쇄망 반입 — 노드는 이미지를 어디서 누구의 자격으로 받는가](../../kubernetes/architecture/이미지%20pull·폐쇄망%20반입.md) — ctr images import 와 nerdctl load, k8s.io 네임스페이스 반입 절차
- [nerdctl 참조 시트](../../../../02_os/docs/cmd/isolate/nerdctl.md) — containerd 환경에서 이미지 반입과 저장소 push 를 다루는 시트



## 참고 자료

> 검증 환경과 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack macOS Docker Engine 29.8.2 (API 1.56, arm64)
- 받는 호스트: OrbStack Ubuntu 26.04.1 LTS VM, Docker Engine 29.1.3 (API 1.52, arm64)
- 릴리스 노트에서 확인한 가장 새 버전: Docker Engine 29.10.0 (2026-11-16)
- [docker image save](https://docs.docker.com/reference/cli/docker/image/save/)
- [docker image load](https://docs.docker.com/reference/cli/docker/image/load/)
- [docker container export](https://docs.docker.com/reference/cli/docker/container/export/)
- [docker image import](https://docs.docker.com/reference/cli/docker/image/import/)
- [containerd image store](https://docs.docker.com/engine/storage/containerd/)
- [Docker Engine 29 릴리스 노트](https://docs.docker.com/engine/release-notes/29/)

[^env]: 릴리스 노트 29 페이지의 첫 항목이 `29.10.0`, 날짜가 `2026-11-16` 입니다. 2026-11-21 에 직접 읽었고 같은 값이 릴리스 노트 인덱스에도 있습니다. https://docs.docker.com/engine/release-notes/29/ containerd 이미지 저장소는 29.0 이후 새로 설치한 엔진의 기본 저장소이고, 이전 버전에서 올린 엔진은 켜기 전까지 overlay2 를 쓴다고 적혀 있습니다. https://docs.docker.com/engine/storage/containerd/
[^exit]: 이 시트의 실측에서 본 값입니다. `echo $?` 가 성공에서 0, 없는 이미지와 없는 파일에서 1이었습니다. 다른 실패 유형의 종료 코드는 확인하지 않았습니다.
[^load-compress]: load 문서의 설명에 "Load an image or repository from a tar archive (even if compressed with gzip, bzip2, xz or zstd) from a file or STDIN. It restores both images and tags." 라고 적혀 있습니다. https://docs.docker.com/reference/cli/docker/image/load/
[^tag-loss]: save 문서는 아카이브에 "all tags + versions, or specified repo:tag, for each argument provided" 가 담긴다고 적습니다. https://docs.docker.com/reference/cli/docker/image/save/ ID 로 저장했을 때 `RepoTags` 가 `null` 이 된다는 것은 위 실측의 `manifest.json` 에서 직접 확인했습니다.
[^export-save]: 이 설명은 위 실측의 `docker history` 와 `Config.Cmd` 에서 나온 것입니다. export 문서는 볼륨 내용을 export 하지 않는다는 점을 적고 있으며 레이어 히스토리에 대한 설명은 없습니다. https://docs.docker.com/reference/cli/docker/container/export/
[^multiplatform]: save 문서에 "By default, docker save saves all platform variants that are present in the daemon's image store." 와 "An error is produced if the given platform is not present in the local image store." 가 적혀 있습니다. https://docs.docker.com/reference/cli/docker/image/save/ load 문서에도 "By default, docker load loads all platform variants that are present in the archive." 가 있습니다. https://docs.docker.com/reference/cli/docker/image/load/
[^platform-ver]: 28.0.0 릴리스 노트에 "now support a `--platform` flag allowing you to choose a specific platform for single-platform operations on multi-platform images" 가 있습니다. https://docs.docker.com/engine/release-notes/28/ 29.0.0 릴리스 노트에는 "now supports multiple platform selection via `--platform` flag" 가 있습니다. https://docs.docker.com/engine/release-notes/29/ tar 안의 `blobs/` 구조와 관련해서는 25.0.0 릴리스 노트가 "The `docker image save` tarball output is now OCI compliant." 라고 적습니다. https://docs.docker.com/engine/release-notes/25.0/
