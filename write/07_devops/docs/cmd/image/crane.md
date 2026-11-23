---
title: "crane 참조 시트"
tags: ["devops", "command", "image", "crane", "oci", "registry"]
status: draft
source:
  - "crane v0.22.1 `crane --help` 와 하위 명령 `--help` 원문 (OrbStack Ubuntu 26.04.1 VM 실측)"
  - "https://github.com/google/go-containerregistry/blob/v0.22.1/cmd/crane/doc/crane.md"
  - "https://github.com/google/go-containerregistry/blob/v0.22.1/pkg/name/registry.go"
  - "https://github.com/google/go-containerregistry/blob/v0.22.1/cmd/crane/cmd/pull.go"
  - "https://github.com/google/go-containerregistry/blob/v0.22.1/cmd/crane/main.go"
related:
  - "../README.md"
  - "../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md"
  - "../../artifact/container/03-02.%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%86%B5%EC%8B%A0%EA%B3%BC%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EB%B0%98%EC%9E%85.md"
  - "../../../../08_cloud/docs/cmd/container/docker.md"
  - "../../../../02_os/docs/cmd/isolate/nerdctl.md"
updated: "2026-11-23"
---

# crane 참조 시트

---

> 컨테이너 데몬과 로컬 저장소 없이 레지스트리 HTTP API 를 직접 호출해 이미지를 조회·복사·태그·수정·삭제하는 `crane` 명령을 모았습니다.

## 개요

> `crane` 은 `docker pull` → `tag` → `push` 로 로컬 디스크를 거치던 작업을 원격 레지스트리 사이에서 바로 처리하는 CLI 입니다.

Google 의 `go-containerregistry` 프로젝트가 배포하는 단일 정적 바이너리입니다. 로컬 이미지 저장소나 백그라운드 데몬을 두지 않고 레지스트리와 직접 통신합니다. 같은 역할을 하는 다른 CLI 도구로 `skopeo` 가 있습니다.

```bash
# 두 도구가 레지스트리 작업을 처리하는 경로
# docker   docker CLI → dockerd → 로컬 이미지 저장소 → 레지스트리
# crane    crane CLI  ──────────────────────────────→ 레지스트리
```

이 시트의 출력은 OrbStack Ubuntu 26.04.1 LTS VM(aarch64)에서 실측했습니다. 실측 버전은 `crane` `v0.22.1` 이며, 2026-11-23 기준 GitHub 릴리스의 가장 새 버전도 `v0.22.1` 입니다.[^env]



## 핵심 문법

> `crane` 은 전역 플래그와 하위 명령으로 대상을 고르고, 이미지 이름·태그·digest 조합으로 원격 이미지를 가리킵니다.

```bash
# 호출 형태
crane [flags]
crane [command]

# 저장소의 리포지토리와 태그 목록을 본다 (저장소와 태그 목록 보기)
crane catalog REGISTRY
crane ls REPO

# 이미지를 받지 않고 digest·manifest·config 를 읽는다 (받지 않고 이미지 정보 읽기)
crane digest IMAGE
crane manifest IMAGE
crane config IMAGE

# 저장소 사이로 이미지를 직접 옮긴다 (저장소 사이 이미지 복사)
crane copy SRC DST

# 받지 않고 같은 리포지토리에 태그를 추가한다 (받지 않고 태그 추가하기)
crane tag IMG TAG

# 폐쇄망 반입용 아카이브로 내리거나 다시 올린다 (tar 로 내려받고 다시 올리기)
crane pull IMAGE TARBALL
crane push PATH IMAGE

# 이미지 파일시스템을 tar 스트림으로 꺼낸다 (컨테이너 없이 이미지 파일 꺼내기)
crane export IMAGE|- TARBALL|-

# 빌드 없이 설정을 바꾸거나 레이어를 추가한다 (빌드 없이 이미지 고치기)
crane mutate [flags] IMAGE
crane append -b BASE -f LAYER.tar -t NEW_TAG

# 자격 증명을 저장하고 원격 참조를 삭제한다 (인증 저장소 로그인하기, 태그와 이미지 지우기)
crane auth login [OPTIONS] [SERVER]
crane delete IMAGE
```

### 전역 옵션

```bash
# crane --help 에서 확인한 전역 플래그
# --platform platform                    대상 플랫폼(os/arch[/variant][:osversion]). 도움말 기본 표기는 all
# --insecure                             TLS 검증이나 HTTPS 없이 평문 HTTP 접속을 허용한다
# -v, --verbose                          디버그 로그를 켠다
# --allow-nondistributable-artifacts     배포 제한(foreign) 레이어의 push 를 허용한다
```



## 종료 코드

> 성공하면 0 으로 끝나고, 참조 형식 오류나 레지스트리 요청 실패가 나면 `Error:` 한 줄을 남기고 1 로 끝납니다.[^exit]

```bash
# 0  명령이 정상으로 끝났다
# 1  잘못된 참조·인증 실패·미지원 API 같은 오류가 발생했다
crane version > /dev/null; echo $?    # 0

# 잘못된 이미지 참조를 주면 오류 메시지와 함께 1 을 반환한다
crane digest invalid:::ref 2>&1; echo $?
```

```bash
# 결과
2026/11/23 21:11:52 HEAD request failed, falling back on GET: could not parse reference: invalid:::ref
Error: parsing reference "invalid:::ref": could not parse reference: invalid:::ref
1
```



## 유스케이스

> 아래 예제는 앞 절에서 띄운 로컬 저장소와 이미지를 이어 쓰므로 위에서 아래로 차례로 실행합니다.

### 실습 준비

> `crane` `v0.22.1` 바이너리의 체크섬을 검증해 설치하고, 테스트용 로컬 저장소 둘과 샘플 이미지를 준비합니다.

```bash
# 작업 디렉터리를 만들고 Linux arm64 묶음을 받아 체크섬을 맞춘 뒤 바이너리를 꺼낸다
mkdir -p /root/sheet-crane && cd /root/sheet-crane
curl -fsSL -o crane.tgz \
  https://github.com/google/go-containerregistry/releases/download/v0.22.1/go-containerregistry_Linux_arm64.tar.gz
curl -fsSL -o checksums.txt \
  https://github.com/google/go-containerregistry/releases/download/v0.22.1/checksums.txt
grep go-containerregistry_Linux_arm64.tar.gz checksums.txt \
  | sed 's/go-containerregistry_Linux_arm64.tar.gz/crane.tgz/' \
  | sha256sum -c -
tar -C /usr/local/bin -xzf crane.tgz crane
crane version
# crane.tgz: OK
# 0.22.1

# Docker Hub 속도 제한을 피하려고 미러에서 registry:2 를 받아 작업용 태그를 붙인다
docker pull -q mirror.gcr.io/library/registry:2    # mirror.gcr.io/library/registry:2
docker tag mirror.gcr.io/library/registry:2 sheet-crane/registry:2
docker rmi mirror.gcr.io/library/registry:2 > /dev/null

# 저장소 사이 복사와 인증 실습에 쓸 저장소 컨테이너 둘을 5101·5111 포트에 띄운다
docker run -d --name sheet-crane-reg -p 127.0.0.1:5101:5000 sheet-crane/registry:2
docker run -d --name sheet-crane-reg2 -p 127.0.0.1:5111:5000 sheet-crane/registry:2
sleep 1
# 682e80a54a670c7763cda763d50e36dd3d8526e0652b091c263c51808b01c929
# 69496c05ff8737c83168c1ed554716f4b39ce31cb30e42a4744fab6322608f28

# 첫 번째 저장소(5101)에 실습용 멀티 플랫폼 이미지(alpine:3.20)를 복사해 둔다 (전체 로그 끝 2줄만 표시)
crane copy mirror.gcr.io/library/alpine:3.20 localhost:5101/sheet-crane/alpine:3.20 2>&1 | tail -n 2
# 2026/11/23 21:12:07 localhost:5101/sheet-crane/alpine@sha256:ba51d55642345137ba4ebf1a15623cbd26493c258e4215391f608667387247aa: digest: sha256:ba51d55642345137ba4ebf1a15623cbd26493c258e4215391f608667387247aa size: 838
# 2026/11/23 21:12:07 localhost:5101/sheet-crane/alpine:3.20: digest: sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc size: 9226
```

### 저장소와 태그 목록 보기

> `catalog` 로 레지스트리의 리포지토리 이름을, `ls` 로 특정 리포지토리의 태그 목록을 조회합니다.

```bash
# 레지스트리에 들어 있는 리포지토리 목록을 본다
crane catalog localhost:5101    # sheet-crane/alpine

# 저장소 주소까지 붙여서 출력한다
#   --full-ref   레지스트리 호스트를 포함한 전체 참조 문자열로 출력한다
crane catalog --full-ref localhost:5101    # localhost:5101/sheet-crane/alpine

# 리포지토리의 태그 목록을 본다
crane ls localhost:5101/sheet-crane/alpine    # 3.20

# 전체 참조 형식으로 태그 목록을 본다
crane ls --full-ref localhost:5101/sheet-crane/alpine    # localhost:5101/sheet-crane/alpine:3.20
```

### 받지 않고 이미지 정보 읽기

> `digest`, `manifest`, `config` 는 이미지를 내려받지 않고 레지스트리에서 메타데이터 JSON 과 해시만 읽어 옵니다.

```bash
# 멀티 플랫폼 이미지의 인덱스 digest 를 읽는다
crane digest localhost:5101/sheet-crane/alpine:3.20
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# --platform 으로 특정 아키텍처의 매니페스트 digest 를 읽는다
crane digest --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20
# sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d

# amd64 매니페스트 digest 와 비교한다
crane digest --platform linux/amd64 localhost:5101/sheet-crane/alpine:3.20
# sha256:c64c687cbea9300178b30c95835354e34c4e4febc4badfe27102879de0483b5e
```

멀티 플랫폼 인덱스의 digest 와 각 플랫폼 매니페스트의 digest 는 서로 다른 객체의 해시라서 값이 다릅니다. 이 구조의 원리는 [이미지 구조와 digest](../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) 편에서 다룹니다.

```bash
# 인덱스 매니페스트에서 unknown(증명 항목)을 빼고 플랫폼별 매니페스트 digest 를 뽑는다
crane manifest localhost:5101/sheet-crane/alpine:3.20 \
  | jq -r '.manifests[] | select(.platform.os != "unknown") | "\(.platform.os)/\(.platform.architecture)\t\(.digest)"'
```

```bash
# 결과
linux/amd64	sha256:c64c687cbea9300178b30c95835354e34c4e4febc4badfe27102879de0483b5e
linux/arm	sha256:37753b2965043543542cd9d48cba044151052ca14fa72e6cbec4edf2a1490599
linux/arm	sha256:bd05c4d38cbeb5cfb34883906276560353a6b0282fb5c4b9dd3bd40f5143d7c3
linux/arm64	sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
linux/386	sha256:4ec3ead63e75e791660b5abc4dc3bd85ebb6fc24a10d649ba05991bf34b5e80e
linux/ppc64le	sha256:80529c2d621d6271966cfa680d104ca55349a3b1fc7a567bc7e25349a1f2f6cb
linux/riscv64	sha256:c47cbcc0d9c7f68d8e19c8e4eb50252ff9722e504108d69e8c36d510e921fc26
linux/s390x	sha256:856b20bf4946b5c8f43fc5b2ce46f39109914d9213a2832eb24cc01c76f27bbe
```

```bash
# arm64 매니페스트에서 레이어 digest 목록을 뽑는다
crane manifest --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 | jq -r '.layers[].digest'
# sha256:3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78

# arm64 이미지 config 에서 아키텍처, OS, 기본 실행 명령, diff_ids 를 뽑는다
crane config --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 \
  | jq '{architecture, os, cmd: .config.Cmd, diff_ids: .rootfs.diff_ids}'
```

```bash
# 결과
{
  "architecture": "arm64",
  "os": "linux",
  "cmd": [
    "/bin/sh"
  ],
  "diff_ids": [
    "sha256:88b4fba61c4c714a2fc173ddf7e9324a257304696830bf41ad28ecc58c11c95f"
  ]
}
```

### 저장소 사이 이미지 복사

> `crane copy` 는 두 레지스트리 사이에서 블롭과 매니페스트를 직접 전송하며, `--platform` 유무에 따라 복사 범위와 digest 가 달라집니다.

```bash
# 플랫폼을 지정하지 않으면 멀티 플랫폼 인덱스 전체가 복사된다
crane copy localhost:5101/sheet-crane/alpine:3.20 localhost:5111/sheet-crane/alpine:3.20 2>&1 | tail -n 2
# 2026/11/23 21:12:08 localhost:5111/sheet-crane/alpine@sha256:ba51d55642345137ba4ebf1a15623cbd26493c258e4215391f608667387247aa: digest: sha256:ba51d55642345137ba4ebf1a15623cbd26493c258e4215391f608667387247aa size: 838
# 2026/11/23 21:12:08 localhost:5111/sheet-crane/alpine:3.20: digest: sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc size: 9226

# 복사본의 digest 가 원본 인덱스 digest 와 같다
crane digest localhost:5111/sheet-crane/alpine:3.20
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# --platform 을 주면 해당 플랫폼 매니페스트와 레이어만 복사된다
# 아래 existing blob 줄의 digest 는 실행마다 다를 수 있다(레이어와 config 중 마지막에 찍히는 쪽이 바뀐다).
crane copy --platform linux/arm64 \
  localhost:5101/sheet-crane/alpine:3.20 \
  localhost:5111/sheet-crane/alpine:3.20-arm64 2>&1 | tail -n 2
# 2026/11/23 21:12:08 existing blob: sha256:ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4
# 2026/11/23 21:12:08 localhost:5111/sheet-crane/alpine:3.20-arm64: digest: sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d size: 1026

# 단일 플랫폼만 복사했으므로 digest 가 arm64 매니페스트의 해시로 바뀐다
crane digest localhost:5111/sheet-crane/alpine:3.20-arm64
# sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
```

### 받지 않고 태그 추가하기

> 같은 리포지토리 안에서 태그만 하나 더 붙일 때는 `crane tag` 가 레이어 전송 없이 매니페스트 포인터만 추가합니다.[^tag]

```bash
# 3.20 이 가리키는 매니페스트에 v3.20 태그를 더한다
crane tag localhost:5101/sheet-crane/alpine:3.20 v3.20
# 2026/11/23 21:12:08 localhost:5101/sheet-crane/alpine:v3.20: digest: sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc size: 9226

# 추가된 태그와 digest 를 확인한다
crane ls localhost:5101/sheet-crane/alpine
# 3.20
# v3.20

# 두 태그가 같은 인덱스 digest 를 가리킨다
crane digest localhost:5101/sheet-crane/alpine:v3.20
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
```

### tar 로 내려받고 다시 올리기

> `crane pull` 은 이미지를 로컬 파일이나 디렉터리로 내려받고, `crane push` 는 그 결과물을 다른 저장소에 올립니다.

```bash
# 기본 형식(--format=tarball)은 Docker load 가 읽는 tar 파일을 만든다
crane pull --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 alpine-tarball.tar
tar -tf alpine-tarball.tar
```

```bash
# 결과
sha256:ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4
3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78.tar.gz
manifest.json
```

```bash
# --format=legacy 는 레이어별 디렉터리를 둔 구형 Docker tar 형식을 만든다
#   --format   저장 형식 지정("tarball", "legacy", "oci", 기본값 "tarball")
crane pull --platform linux/arm64 --format=legacy localhost:5101/sheet-crane/alpine:3.20 alpine-legacy.tar
tar -tf alpine-legacy.tar
```

```bash
# 결과
ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4.json
9bd18d68f92f3851e412df999eaaad1ec0fc70a24f5768ed56ffed916f38168d/layer.tar
9bd18d68f92f3851e412df999eaaad1ec0fc70a24f5768ed56ffed916f38168d/json
9bd18d68f92f3851e412df999eaaad1ec0fc70a24f5768ed56ffed916f38168d/VERSION
manifest.json
repositories
```

```bash
# --format=oci 는 tar 파일이 아니라 OCI 이미지 레이아웃 디렉터리를 만든다
crane pull --format=oci localhost:5101/sheet-crane/alpine:3.20 alpine-oci
ls -1 alpine-oci
```

```bash
# 결과
blobs
index.json
oci-layout
```

`--format=oci` 로 내릴 때 `--platform` 을 빼면 멀티 플랫폼 인덱스 전체가 디렉터리에 담깁니다.[^pull-oci]

```bash
# tarball 과 legacy 형식의 tar 는 docker load 로 바로 읽힌다 (실습 정리를 위해 즉시 태그 삭제)
docker load -i alpine-tarball.tar && docker rmi localhost:5101/sheet-crane/alpine:3.20 > /dev/null
# Loaded image: localhost:5101/sheet-crane/alpine:3.20

docker load -i alpine-legacy.tar && docker rmi localhost:5101/sheet-crane/alpine:3.20 > /dev/null
# Loaded image: localhost:5101/sheet-crane/alpine:3.20

# oci 형식은 디렉터리라서 docker load 가 읽지 못하고 오류를 낸다
docker load -i alpine-oci 2>&1; echo $?
# error during connect: Post "http://%2Fvar%2Frun%2Fdocker.sock/v1.52/images/load?quiet=1": read alpine-oci: is a directory
# 1
```

`tarball` 과 `legacy` 는 `docker load` 로 읽혔습니다. 반면 `oci` 디렉터리는 `is a directory` 오류로 실패했습니다. tar 로 반입하는 전체 절차는 [레지스트리 통신과 오프라인 반입](../../artifact/container/03-02.%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%86%B5%EC%8B%A0%EA%B3%BC%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EB%B0%98%EC%9E%85.md) 편과 [docker 참조 시트](../../../../08_cloud/docs/cmd/container/docker.md) 가 다룹니다.

```bash
# 두 번째 저장소(5111)로 tarball 파일과 oci 디렉터리를 각각 push 한다
crane push alpine-tarball.tar localhost:5111/sheet-crane/alpine-tar:3.20 2>&1 | tail -n 2
# 2026/11/23 21:12:09 localhost:5111/sheet-crane/alpine-tar:3.20: digest: sha256:0fc622c566ef5d44a668225fa2cfb201f9723197c1085fbe41d67e63f38c7fdf size: 427
# localhost:5111/sheet-crane/alpine-tar@sha256:0fc622c566ef5d44a668225fa2cfb201f9723197c1085fbe41d67e63f38c7fdf

crane push alpine-oci localhost:5111/sheet-crane/alpine-oci:3.20 2>&1 | tail -n 2
# 2026/11/23 21:12:09 localhost:5111/sheet-crane/alpine-oci:3.20: digest: sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc size: 9226
# localhost:5111/sheet-crane/alpine-oci@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# tarball 을 push 한 이미지는 형식이 바뀌어 새 digest 가 되고, oci 디렉터리는 원본 인덱스 digest 가 유지된다
crane digest localhost:5111/sheet-crane/alpine-tar:3.20
crane digest localhost:5111/sheet-crane/alpine-oci:3.20
# sha256:0fc622c566ef5d44a668225fa2cfb201f9723197c1085fbe41d67e63f38c7fdf
# sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
```

### 컨테이너 없이 이미지 파일 꺼내기

> `crane export` 는 이미지 레이어를 합친 루트 파일시스템을 tar 스트림으로 뽑아 컨테이너를 띄우지 않고 내용을 확인합니다.

```bash
# 파일시스템 tar 스트림을 표준 출력(-)으로 내보내 앞쪽 목록을 본다
crane export --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 - | tar -t | head -n 8
```

```bash
# 결과
bin
bin/arch
bin/ash
bin/base64
bin/bbconfig
bin/busybox
bin/cat
bin/chattr
```

```bash
# 이미지 안의 특정 파일(/etc/alpine-release)만 표준 출력으로 꺼내 읽는다
crane export --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 - \
  | tar -xOf - etc/alpine-release    # 3.20.10
```

### 빌드 없이 이미지 고치기

> `crane mutate` 는 메타데이터와 실행 설정을 바꾸고, `crane append` 는 새 tar 레이어를 얹어 Dockerfile 빌드 없이 새 태그를 만듭니다.

```bash
# label, env, entrypoint 를 바꾼 새 태그(mutated)를 저장소에 만든다
#   -l, --label     이미지에 새 레이블을 추가한다
#   -e, --env       환경 변수를 추가한다
#   --entrypoint    기본 entrypoint 를 바꾼다
#   -t, --tag       결과 이미지를 올릴 태그를 지정한다
crane mutate \
  --platform linux/arm64 \
  -l env=prod \
  -e APP_ENV=prod \
  --entrypoint /bin/sh \
  -t localhost:5101/sheet-crane/alpine:mutated \
  localhost:5101/sheet-crane/alpine:3.20 2>&1 | tail -n 2
# 2026/11/23 21:12:09 localhost:5101/sheet-crane/alpine:mutated: digest: sha256:ea65b9ae2a7e76b49b7bfc9666faa22da464bebc24f943c0def75bffbaeb21d2 size: 902
# localhost:5101/sheet-crane/alpine@sha256:ea65b9ae2a7e76b49b7bfc9666faa22da464bebc24f943c0def75bffbaeb21d2

# digest 가 원본 arm64 매니페스트(45e09956...)에서 ea65b9ae... 로 바뀌었는지와 config 를 확인한다
crane digest localhost:5101/sheet-crane/alpine:mutated
crane config localhost:5101/sheet-crane/alpine:mutated \
  | jq '{labels: .config.Labels, env: .config.Env, entrypoint: .config.Entrypoint}'
```

```bash
# 결과
sha256:ea65b9ae2a7e76b49b7bfc9666faa22da464bebc24f943c0def75bffbaeb21d2
{
  "labels": {
    "env": "prod"
  },
  "env": [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "APP_ENV=prod"
  ],
  "entrypoint": [
    "/bin/sh"
  ]
}
```

```bash
# 추가할 파일 하나를 담은 tar 레이어를 만든다
mkdir -p layer/etc && echo "from-crane" > layer/etc/crane.txt
tar -cf layer.tar -C layer .

# 기존 이미지 위에 layer.tar 를 새 레이어로 얹어 appended 태그를 만든다
#   -b, --base      바탕이 될 원본 이미지 이름
#   -f, --new_layer 추가할 레이어 tar 파일 경로
#   -t, --new_tag   결과 이미지에 붙일 태그 이름
# 아래 digest 는 실행마다 다르다. 명령이 파일을 매번 다시 써서 tar 해시가 바뀌기 때문이다(tar --mtime=@0 으로 만들면 해시가 같다).
crane append \
  --platform linux/arm64 \
  -b localhost:5101/sheet-crane/alpine:3.20 \
  -f layer.tar \
  -t localhost:5101/sheet-crane/alpine:appended 2>&1 | tail -n 2
# 2026/11/23 21:12:10 localhost:5101/sheet-crane/alpine:appended: digest: sha256:aeb98d0dbf211785d6365a2ccbb9e171bc817d5a693907971140fceb33dd826d size: 1056
# localhost:5101/sheet-crane/alpine@sha256:aeb98d0dbf211785d6365a2ccbb9e171bc817d5a693907971140fceb33dd826d

# 새 digest 와 추가된 파일이 실제 파일시스템에 들어 있는지 확인한다
crane digest localhost:5101/sheet-crane/alpine:appended
crane export localhost:5101/sheet-crane/alpine:appended - | tar -t | grep crane.txt
# sha256:aeb98d0dbf211785d6365a2ccbb9e171bc817d5a693907971140fceb33dd826d
# etc/crane.txt
```

### 인증 저장소 로그인하기

> `crane auth login` 은 자격 증명을 검증한 뒤 `DOCKER_CONFIG` 경로의 `config.json` 에 저장하고, 이후 명령이 그 파일을 자동으로 읽습니다.

```bash
# htpasswd 인증과 삭제 허용을 켠 상태로 두 번째 저장소(5111)를 다시 띄운다
mkdir -p auth
docker pull -q mirror.gcr.io/library/httpd:2-alpine > /dev/null
docker tag mirror.gcr.io/library/httpd:2-alpine sheet-crane/httpd:2-alpine
docker rmi mirror.gcr.io/library/httpd:2-alpine > /dev/null
docker run --rm --entrypoint htpasswd sheet-crane/httpd:2-alpine -Bbn testuser testpass > auth/htpasswd
docker rm -fv sheet-crane-reg2 > /dev/null
docker run -d --name sheet-crane-reg2 -p 127.0.0.1:5111:5000 \
  -e REGISTRY_STORAGE_DELETE_ENABLED=true \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  -v /root/sheet-crane/auth:/auth:ro \
  sheet-crane/registry:2 > /dev/null
sleep 1

# 로그인 전에는 인증 오류가 나며 1 로 끝난다 (기존 ~/.docker/config.json 보호를 위해 DOCKER_CONFIG 분리)
DOCKER_CONFIG=/root/sheet-crane/dockercfg crane ls localhost:5111/sheet-crane/alpine 2>&1; echo $?
# Error: reading tags for localhost:5111/sheet-crane/alpine: GET http://localhost:5111/v2/sheet-crane/alpine/tags/list?n=1000: UNAUTHORIZED: authentication required; [map[Action:pull Class: Name:sheet-crane/alpine Type:repository]]
# 1
```

```bash
# 비밀번호는 표준 입력으로 넘겨 로그인한다
#   -u                사용자 이름
#   --password-stdin  표준 입력에서 비밀번호를 읽는다
echo testpass | DOCKER_CONFIG=/root/sheet-crane/dockercfg \
  crane auth login localhost:5111 -u testuser --password-stdin 2>&1
```

```bash
# 결과

WARNING! Your credentials are stored unencrypted in '/root/sheet-crane/dockercfg/config.json'.
Configure a credential helper to remove this warning. See
https://docs.docker.com/go/credential-store/

2026/11/23 21:12:15 logged in via /root/sheet-crane/dockercfg/config.json
```

```bash
# 저장된 config.json 에는 auths 항목 아래 base64 로 인코딩된 계정 문자열이 들어간다
cat /root/sheet-crane/dockercfg/config.json
```

```bash
# 결과
{
	"auths": {
		"localhost:5111": {
			"auth": "dGVzdHVzZXI6dGVzdHBhc3M="
		}
	}
}
```

```bash
# 로그인한 상태에서는 복사 명령이 통과한다
DOCKER_CONFIG=/root/sheet-crane/dockercfg \
  crane copy localhost:5101/sheet-crane/alpine:mutated localhost:5111/sheet-crane/alpine:mutated 2>&1 | tail -n 2
# 2026/11/23 21:12:15 pushed blob: sha256:3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78
# 2026/11/23 21:12:15 localhost:5111/sheet-crane/alpine:mutated: digest: sha256:ea65b9ae2a7e76b49b7bfc9666faa22da464bebc24f943c0def75bffbaeb21d2 size: 902

# 작업이 끝나면 저장소 인증 정보를 지운다
DOCKER_CONFIG=/root/sheet-crane/dockercfg crane auth logout localhost:5111 2>&1
# 2026/11/23 21:12:15 logged out via /root/sheet-crane/dockercfg/config.json
```

### 태그와 이미지 지우기

> `crane delete` 는 레지스트리 서버가 삭제 API 를 허용해야 동작하며, `registry:2` 에서는 태그가 아니라 digest 참조를 주어야 지워집니다.

```bash
# 삭제 허용 옵션이 꺼진 5101 저장소는 UNSUPPORTED 오류를 낸다
crane delete localhost:5101/sheet-crane/alpine:mutated 2>&1; echo $?
# Error: DELETE http://localhost:5101/v2/sheet-crane/alpine/manifests/mutated: UNSUPPORTED: The operation is unsupported.
# 1

# 삭제를 켠 5111 저장소에 다시 로그인한 뒤, digest 를 뽑아 삭제한다
echo testpass | DOCKER_CONFIG=/root/sheet-crane/dockercfg \
  crane auth login localhost:5111 -u testuser --password-stdin > /dev/null 2>&1
D=$(DOCKER_CONFIG=/root/sheet-crane/dockercfg crane digest localhost:5111/sheet-crane/alpine:mutated)
DOCKER_CONFIG=/root/sheet-crane/dockercfg crane delete "localhost:5111/sheet-crane/alpine@$D"; echo $?    # 0

# 삭제 후 목록을 조회하면 태그가 사라져 아무 줄도 나오지 않는다
DOCKER_CONFIG=/root/sheet-crane/dockercfg crane ls localhost:5111/sheet-crane/alpine    # (출력 없음)
```

### 실습 정리

> 유스케이스에서 만든 저장소 컨테이너, 작업용 docker 이미지, 작업 디렉터리를 지웁니다.

```bash
# 컨테이너·볼륨·이미지·작업 폴더를 모두 정리한다 (crane 바이너리는 남긴다)
docker rm -fv sheet-crane-reg sheet-crane-reg2
docker rmi sheet-crane/registry:2 sheet-crane/httpd:2-alpine
rm -rf /root/sheet-crane
```

```bash
# 결과
sheet-crane-reg
sheet-crane-reg2
Untagged: sheet-crane/registry:2
Deleted: sha256:a3d8aaa63ed8681a604f1dea0aa03f100d5895b6a58ace528858a7b332415373
Untagged: sheet-crane/httpd:2-alpine
Deleted: sha256:32bd0639bcc4917ef1fd9363a1d9dd2dd9c498565118b062a10d51e43a5c3a24
```



## 주의사항과 동작 원리

### HTTP 저장소 접속 실패와 --insecure

> `crane` 은 `localhost:포트`, `*.localhost`, 루프백 IP, RFC 1918 사설 대역이 아닌 주소에는 기본적으로 HTTPS 로 접속해 HTTP 저장소에서 실패합니다.

```bash
# 재현을 위해 저장소 둘을 띄우고 /etc/hosts 에 registry.example.com 을 127.0.0.1 로 건다
mkdir -p /root/sheet-crane
docker pull -q mirror.gcr.io/library/registry:2 > /dev/null
docker tag mirror.gcr.io/library/registry:2 sheet-crane/registry:2
docker rmi mirror.gcr.io/library/registry:2 > /dev/null
docker run -d --name sheet-crane-reg -p 127.0.0.1:5101:5000 sheet-crane/registry:2 > /dev/null
docker run -d --name sheet-crane-reg2 -p 127.0.0.1:5111:5000 \
  -e REGISTRY_STORAGE_DELETE_ENABLED=true sheet-crane/registry:2 > /dev/null
sleep 1
crane copy --platform linux/arm64 \
  mirror.gcr.io/library/alpine:3.20 localhost:5101/sheet-crane/alpine:3.20 > /dev/null 2>&1
echo '127.0.0.1 registry.example.com' >> /etc/hosts

# 도메인 이름으로는 HTTPS 요청을 보내다 실패한다
crane ls registry.example.com:5101/sheet-crane/alpine 2>&1; echo $?
# Error: reading tags for registry.example.com:5101/sheet-crane/alpine: Get "https://registry.example.com:5101/v2/": http: server gave HTTP response to HTTPS client
# 1

# --insecure 를 주면 평문 HTTP 로 접속해 목록을 읽는다
crane ls --insecure registry.example.com:5101/sheet-crane/alpine    # 3.20

# 127.0.0.1 은 루프백 IP 로 판정되어 --insecure 없이도 HTTP 로 접속된다
crane ls 127.0.0.1:5101/sheet-crane/alpine    # 3.20

# 테스트를 위해 넣은 /etc/hosts 줄을 리터럴로 지운다
sed -i '/127\.0\.0\.1 registry\.example\.com/d' /etc/hosts
```

`go-containerregistry` 의 `Registry.Scheme()` 은 `--insecure` 외에 일부 주소만 `http` 로 보냅니다. `localhost:`, `*.localhost`, `127.0.0.1`, `::1` 이 해당합니다. 사설 대역(`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)도 포함되며 그 밖은 `https` 를 씁니다.[^http-scheme]

### 움직이는 태그와 digest 고정 참조

> 태그는 새 이미지가 push 되면 언제든 다른 매니페스트를 가리키도록 덮어써지므로, 변하지 않는 이미지를 가리킬 때는 `이름@sha256:…` 를 씁니다.

```bash
# moving 태그에 alpine arm64 를 걸고 digest 를 확인한다
crane tag localhost:5101/sheet-crane/alpine:3.20 moving
crane digest localhost:5101/sheet-crane/alpine:moving
# 2026/11/23 21:12:23 localhost:5101/sheet-crane/alpine:moving: digest: sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d size: 1026
# sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d

# 같은 moving 태그에 busybox:1.36.0 을 덮어쓰면 같은 태그의 digest 가 바뀐다
crane copy --platform linux/arm64 \
  mirror.gcr.io/library/busybox:1.36.0 localhost:5101/sheet-crane/alpine:moving > /dev/null 2>&1
crane digest localhost:5101/sheet-crane/alpine:moving    # sha256:1af0a016aaa24dd9ddf2ff0771160a68d6394eff88c9c0d5239c93a21ea06f9f

# 태그 대신 원래 digest 를 직접 적으면 태그가 바뀐 뒤에도 같은 매니페스트를 가리킨다
crane digest localhost:5101/sheet-crane/alpine@sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
# sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
```

### 태그 이름으로 crane delete 가 거부되는 오류

> `registry:2` 는 삭제가 켜져 있어도 태그 이름에 대한 `DELETE` 요청을 거부하고, digest 참조만 삭제합니다.

```bash
# 삭제가 켜진 5111 저장소에 이미지를 올리고 태그 이름으로 지워 본다
crane copy localhost:5101/sheet-crane/alpine:3.20 localhost:5111/sheet-crane/alpine:3.20 > /dev/null 2>&1
crane delete localhost:5111/sheet-crane/alpine:3.20 2>&1; echo $?
# Error: DELETE http://localhost:5111/v2/sheet-crane/alpine/manifests/3.20: DIGEST_INVALID: provided digest did not match uploaded content
# 1
```

삭제 설정이 꺼져 있으면 「태그와 이미지 지우기」 처럼 `UNSUPPORTED` 가 나옵니다. 켜져 있어도 태그를 주면 `DIGEST_INVALID` 오류가 나므로 `crane digest` 로 얻은 `@sha256:…` 를 넘겨야 합니다.

### copy 와 pull·push 의 digest 차이

> `crane copy` 는 원격 매니페스트를 그대로 옮겨 digest 를 보존하지만, `crane pull` 로 tar 를 거친 뒤 `crane push` 하면 형식이 바뀌어 digest 가 달라집니다.

```bash
# copy 한 이미지(3.20)와 tar 로 pull 후 push 한 이미지(from-tar)의 digest 를 비교한다
mkdir -p /root/sheet-crane && cd /root/sheet-crane
crane pull --platform linux/arm64 localhost:5101/sheet-crane/alpine:3.20 alpine-trap.tar
crane push alpine-trap.tar localhost:5111/sheet-crane/alpine:from-tar > /dev/null 2>&1
crane digest localhost:5111/sheet-crane/alpine:3.20
crane digest localhost:5111/sheet-crane/alpine:from-tar
# sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
# sha256:0fc622c566ef5d44a668225fa2cfb201f9723197c1085fbe41d67e63f38c7fdf

# 주의사항 실습에서 띄운 저장소와 작업 디렉터리를 정리한다
docker rm -fv sheet-crane-reg sheet-crane-reg2 > /dev/null
docker rmi sheet-crane/registry:2 > /dev/null
rm -rf /root/sheet-crane
```

`crane copy` 는 `--platform` 을 안 주면 인덱스 전체를 복제해 인덱스 digest 를 유지합니다. `--platform` 을 주면 해당 플랫폼 매니페스트만 복사해 그 매니페스트 digest 가 됩니다. 기본 `crane pull` 은 Docker tarball 형식으로 바꾸므로, 원본 digest 를 유지하려면 `--format=oci` 를 씁니다.[^pull-format]



## 관련 문서

> 이 시트와 이어서 읽을 DevOps·컨테이너 문서와 이웃 명령어 시트입니다.

- [DevOps 명령어 시트](../README.md) — 빌드·배포 도구 시트 목록
- [이미지 구조와 digest](../../artifact/container/03-01.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EA%B5%AC%EC%A1%B0%EC%99%80%20digest.md) — index·manifest·config·layer 가 digest 로 이어지는 구조
- [레지스트리 통신과 오프라인 반입](../../artifact/container/03-02.%EB%A0%88%EC%A7%80%EC%8A%A4%ED%8A%B8%EB%A6%AC%20%ED%86%B5%EC%8B%A0%EA%B3%BC%20%EC%98%A4%ED%94%84%EB%9D%BC%EC%9D%B8%20%EB%B0%98%EC%9E%85.md) — 토큰 인증·HTTP 저장소·폐쇄망 반입 절차
- [docker 참조 시트](../../../../08_cloud/docs/cmd/container/docker.md) — `docker save`·`docker load`·`docker export` 명령과 형식 차이
- [nerdctl 참조 시트](../../../../02_os/docs/cmd/isolate/nerdctl.md) — containerd 환경에서 `nerdctl load`·`tag`·`push` 로 반입하는 방법



## 참고 자료

> 실측 환경 정보와 공식 문서·소스 근거입니다.

- 검증 환경: OrbStack Ubuntu 26.04.1 LTS VM(aarch64), Docker Engine, `jq`
- 실측·최신 버전: `crane` `v0.22.1` (2026-11-23 GitHub `releases/latest` 확인)
- [crane v0.22.1 공식 문서](https://github.com/google/go-containerregistry/blob/v0.22.1/cmd/crane/doc/crane.md)
- [go-containerregistry v0.22.1 pkg/name/registry.go](https://github.com/google/go-containerregistry/blob/v0.22.1/pkg/name/registry.go)

[^env]: `crane version` 출력 `0.22.1` 과 GitHub API `https://api.github.com/repos/google/go-containerregistry/releases/latest` 의 `tag_name: v0.22.1` 을 2026-11-23 에 확인했습니다.
[^exit]: `go-containerregistry` `v0.22.1` `cmd/crane/main.go` 는 `if err := cmd.Root.ExecuteContext(ctx); err != nil { cancel(); os.Exit(1) }` 로 오류 시 1 을 반환합니다.
[^tag]: `crane tag --help` 는 `"We can skip layer existence checks because we know the manifest already exists. This makes \"tag\" slightly faster than \"copy\"."` 라고 설명합니다.
[^pull-oci]: `go-containerregistry` `v0.22.1` `cmd/crane/cmd/pull.go` 는 `if format == "oci" && rmt.MediaType.IsIndex() && o.Platform == nil` 일 때 인덱스 전체를 레이아웃에 저장하고, 그 외에는 `remote.defaultPlatform`(`linux/amd64`) 또는 `--platform` 지정 플랫폼의 단일 이미지를 가져옵니다.
[^http-scheme]: `go-containerregistry` `v0.22.1` `pkg/name/registry.go` 의 `Scheme()` 함수는 `r.insecure`, `r.isRFC1918()`(`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), `strings.HasPrefix(r.Name(), "localhost:")`, `reLocal`(`.*\.localhost(?::\d{1,5})?$`), `reLoopback`(`^127\.0\.0\.1(?::\d{1,5})?$`), `reipv6Loopback`(`^(::1|\[::1\](?::\d{1,5})?)$`) 에 해당하면 `"http"` 를, 그 외는 `"https"` 를 반환합니다.
[^pull-format]: `crane pull --help` 는 `--format` 값으로 `"tarball"`, `"legacy"`, `"oci"`(기본값 `"tarball"`)를 지원하며, `crane push --help` 는 `"If the PATH is a directory, it will be read as an OCI image layout. Otherwise, PATH is assumed to be a docker-style tarball."` 라고 설명합니다.
