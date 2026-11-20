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
  - ../../kubernetes/architecture/%EC%9D%B4%EB%AF%B8%EC%A7%80%20pull%C2%B7%ED%8F%90%EC%87%84%EB%A7%9D%20%EB%B0%98%EC%9E%85.md
  - ../../../../02_os/docs/cmd/isolate/nerdctl.md
updated: "2026-11-21"
---

# docker 참조 시트

---

> 컨테이너 이미지를 tar 아카이브로 묶어 내보내고 다른 호스트에 들이며, 압축·태그 복원·로컬 저장소 등록까지 다루는 docker 이미지 반입 명령을 따라 치면 그대로 나오는 실측 예제로 모았습니다.



## 개요

> docker save 와 docker load 는 중앙 레지스트리 없이 파일과 파이프로 이미지를 백업하고 옮기는 도구입니다.

`docker` 는 오픈소스 컨테이너 엔진의 공식 CLI 바이너리입니다. 이 시트는 반입 명령만 다루고 실행·조회 명령은 아직 없습니다.

이 시트의 출력은 OrbStack macOS Docker Engine 29.8.2(API 1.56, arm64)에서 받았습니다. 받는 호스트에는 OrbStack Ubuntu 26.04.1 LTS VM 의 Docker Engine 29.1.3(API 1.52, arm64)을 썼습니다.

`docker info` 의 DriverStatus 가 두 엔진 모두 `io.containerd.snapshotter.v1` 이라 containerd 이미지 저장소를 씁니다.

Docker 공식 릴리스 노트에서 2026-11-21 에 확인한 가장 새 버전은 29.10.0(2026-11-16 릴리스)입니다. 실측 엔진 두 대는 모두 이보다 낮은 마이너 버전입니다.[^env]



## 핵심 문법

> save 로 이미지를 파일이나 표준 출력으로 묶고, load 로 파일이나 표준 입력에서 풀어 엔진에 등록합니다.

```bash
# 호출 형태
# docker --help 와 하위 명령 --help 의 Usage 줄
docker save [OPTIONS] IMAGE [IMAGE...]
docker load [OPTIONS]
docker export [OPTIONS] CONTAINER
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
docker push [OPTIONS] NAME[:TAG]

# 이미지를 tar 파일로 묶어 저장한다 (이미지를 tar 로 내보내기)
docker save -o FILE IMAGE

# 표준 출력으로 이미지를 내보내 파이프로 전달한다 (표준 출력과 파이프로 내보내기)
docker save IMAGE > FILE

# 여러 이미지를 단일 tar 아카이브로 묶는다 (여러 이미지를 한 tar 로 묶기)
docker save -o FILE IMAGE1 IMAGE2

# tar 아카이브 파일에서 이미지를 불러온다 (tar 파일에서 이미지 들이기)
docker load -i FILE

# 표준 입력 리다이렉션으로 이미지를 복원한다 (tar 파일에서 이미지 들이기)
docker load < FILE

# save 출력을 gzip 으로 한 번 더 감싸고 load 로 그대로 읽는다 (gzip 으로 한 번 더 압축하기)
docker save IMAGE | gzip > FILE.tar.gz
docker load -i FILE.tar.gz

# 파이프로 다른 호스트의 docker 데몬에 즉시 넘긴다 (다른 호스트로 파이프 전송하기)
# 일반 형태는 ssh 이다. 이 시트에서는 ssh 를 실행하지 않았다
docker save IMAGE | ssh HOST docker load

# 이 시트의 실측 환경에서 받는 호스트로 들어가는 방법이다 (OrbStack Ubuntu VM 안의 docker)
docker save IMAGE | orb -m ubuntu sudo docker load

# 로컬 사설 저장소에 반입 이미지를 올린다 (반입한 이미지를 저장소에 올리기)
docker tag IMAGE REGISTRY/IMAGE:TAG
docker push REGISTRY/IMAGE:TAG

# 반입된 이미지의 고유 ID 와 digest 를 대조한다 (반입한 이미지의 정보 확인하기)
docker image inspect -f '{{.Id}}' IMAGE
docker image inspect -f '{{.RepoDigests}}' IMAGE
```

### 옵션 목록

```bash
# docker 29.8.2 의 --help 원문에 실린 옵션 전체
# 기본값은 --help 나 공식 문서에 적힌 것만 쓰고, 적히지 않은 칸은 - 로 둔다

# docker save
# -o, --output string      기본값 STDOUT                        tar 아카이브를 파일에 씁니다
#     --platform strings   기본값 엔진에 있는 모든 플랫폼       지정한 플랫폼만 저장합니다. os[/arch[/variant]] 를 쉼표로 이어 씁니다

# docker load
# -i, --input string       기본값 STDIN                         tar 아카이브를 파일에서 읽습니다
#     --platform strings   기본값 아카이브에 있는 모든 플랫폼   지정한 플랫폼만 불러옵니다. 형식은 save 와 같습니다
# -q, --quiet              기본값 -                             --help 설명은 로드 출력을 숨긴다는 뜻입니다

# docker export
# -o, --output string      기본값 STDOUT                        컨테이너 파일시스템 tar 를 파일에 씁니다

# docker import
# -c, --change list       기본값 -                              만들어지는 이미지에 Dockerfile 명령을 적용합니다
# -m, --message string    기본값 -                              가져온 이미지에 커밋 메시지를 답니다
#     --platform string   기본값 -                              멀티 플랫폼을 지원하는 서버에서 플랫폼을 지정합니다
```



## 종료 코드

> 이 시트의 실측에서 성공은 0, 없는 이미지와 없는 파일은 모두 1로 끝났습니다.[^exit]

```bash
# 0  명령이 성공했다
# 1  없는 이미지 지정·없는 파일 읽기처럼 실패했다
docker save -o cmdsheet-alpine.tar alpine:3.20; echo $?
docker save -o cmdsheet-nonexistent.tar nosuchimage:nonexistent 2>&1; echo $?
docker load -i cmdsheet-nonexistent.tar 2>&1; echo $?
```

```bash
# 결과
0
Error response from daemon: No such image: nosuchimage:nonexistent
1
open cmdsheet-nonexistent.tar: no such file or directory
1
```



## 유스케이스

### 실습 준비

> 실습에 쓸 베이스 이미지 세 개를 받으며, 실행 환경은 OrbStack macOS Docker 데몬입니다.

```bash
# 실습에 쓸 경량 베이스 이미지를 미리 받는다
#   -q   다운로드 진행 상황을 숨기고 받은 이미지의 전체 이름만 출력한다
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

> docker save 에 -o 플래그를 주어 로컬 이미지를 단일 tar 아카이브 파일로 저장합니다.

```bash
# 이미지를 tar 아카이브 파일로 내보낸다
#   -o   표준 출력 대신 지정한 파일에 tar 아카이브를 쓴다
docker save -o cmdsheet-alpine.tar alpine:3.20

# 생성된 tar 파일의 크기를 바이트로 확인한다
#   -c   바이트 수를 센다
wc -c cmdsheet-alpine.tar    #  7910912 cmdsheet-alpine.tar

# tar 바깥 층에 있는 파일을 확인한다 (blobs 폴더 밖)
#   -t   아카이브 안의 파일 목록을 나열한다
#   -f   작업할 tar 파일 경로를 지정한다
tar -tf cmdsheet-alpine.tar | grep -v blobs
```

```bash
# 결과
index.json
manifest.json
oci-layout
```

tar 안에는 이미지의 레이어, 설정 JSON, 매니페스트가 `blobs/sha256/` 아래 파일로 들어 있습니다. 그 바깥에 `index.json`, `manifest.json`, `oci-layout` 세 파일이 있습니다. 이 구조는 containerd 이미지 저장소 엔진 두 대에서 본 모양입니다.

### 표준 출력과 파이프로 내보내기

> -o 옵션을 생략하면 표준 출력으로 스트림을 내보내므로 셸 리다이렉션이나 파이프로 전달할 수 있습니다.

```bash
# 표준 출력을 셸 리다이렉션(>)으로 받아 tar 파일로 저장한다
docker save alpine:3.20 > cmdsheet-alpine-stdout.tar

# 파일 크기를 확인한다
wc -c cmdsheet-alpine-stdout.tar    #  7910912 cmdsheet-alpine-stdout.tar

# -o 로 만든 파일과 바이트 단위로 같은지 비교한다
#   cmp   두 파일이 같으면 아무것도 출력하지 않고 0으로 끝난다
cmp cmdsheet-alpine.tar cmdsheet-alpine-stdout.tar && echo same    # same

# 파이프로 wc 에 연결해 출력되는 바이트 수를 확인한다
docker save alpine:3.20 | wc -c    # 7910912
```

리다이렉션으로 만든 파일과 `-o` 로 만든 파일은 이 실측에서 크기도 내용도 같았습니다.

### 여러 이미지를 한 tar 로 묶기

> save 뒤에 여러 이미지 이름을 나열하면 단일 tar 파일에 여러 이미지의 레이어와 매니페스트가 함께 묶입니다.

```bash
# 알파인과 비지박스 이미지를 단일 tar 파일로 한꺼번에 묶는다
docker save -o cmdsheet-bundle.tar alpine:3.20 busybox:1.36.0

# tar 아카이브 안에 manifest.json 이 존재하는지 확인한다
tar -tf cmdsheet-bundle.tar | grep manifest.json    # manifest.json

# manifest.json 의 항목마다 RepoTags 를 뽑아 본다
tar -xOf cmdsheet-bundle.tar manifest.json | python3 -I -c "import sys,json;print([m['RepoTags'] for m in json.load(sys.stdin)])"    # [['alpine:3.20'], ['busybox:1.36.0']]
```

아카이브 안의 `manifest.json` 은 묶인 이미지마다 항목 하나를 두고, 항목마다 `RepoTags` 에 저장할 때 준 이름이 들어갑니다.

### tar 파일에서 이미지 들이기

> docker load 에 -i 옵션이나 표준 입력을 주어 tar 파일에서 이미지와 태그를 복원합니다.

```bash
# tar 파일에서 이미지를 불러온다
#   -i   표준 입력 대신 지정한 파일에서 tar 아카이브를 읽는다
docker load -i cmdsheet-alpine.tar    # Loaded image: alpine:3.20

# 셸 리다이렉션(<)으로 표준 입력을 통해 이미지를 들인다
docker load < cmdsheet-alpine.tar    # Loaded image: alpine:3.20

# -q 를 붙여 본다
#   -q   --help 설명은 Suppress the load output 이다
docker load -q -i cmdsheet-alpine.tar    # Loaded image: alpine:3.20
```

이미 엔진에 있는 이미지를 다시 load 해도 오류 없이 같은 `Loaded image` 줄이 나왔습니다. `-q` 는 `--help` 에서 로드 출력을 숨긴다고 하지만, 이 실측에서는 `-q` 가 있어도 없어도 출력이 같았습니다. 받는 호스트에 없던 이미지를 새로 load 한 경우에도 같았습니다(「ID 로 내보낼 때의 태그 유실」 절).

### gzip 으로 한 번 더 압축하기

> save 출력을 gzip 에 넘겨도 7.5M 이 7.4M 으로 거의 줄지 않는 것은 tar 안의 레이어가 이미 gzip 이기 때문이고, load 는 gzip 파일을 그대로 읽습니다.

```bash
# save 출력을 gzip 으로 압축해 파일로 저장한다
docker save alpine:3.20 | gzip > cmdsheet-alpine.tar.gz

# 압축 파일의 크기를 바이트로 확인한다
wc -c cmdsheet-alpine.tar.gz    #  7727649 cmdsheet-alpine.tar.gz

# tar 안의 레이어 blob 이 어떤 형식인지 확인한다 (arm64 레이어와 amd64 레이어)
#   file -   표준 입력으로 받은 데이터의 형식을 알려 준다
tar -xOf cmdsheet-alpine.tar blobs/sha256/3f26bc2dec0b515f1c2818f6e13a8f1da1f88179a008445d4e587233386bff78 2>/dev/null | file -    # /dev/stdin: gzip compressed data
tar -xOf cmdsheet-alpine.tar blobs/sha256/25f1d6b1951ac8eb3740558fe94cb83d377bdadf95fd9f98b50d2e1b96130471 2>/dev/null | file -    # /dev/stdin: gzip compressed data

# 레이어 두 개의 합과 레이어 밖 바이트, gzip 으로 줄어든 바이트를 계산한다
python3 -I -c "print(4092319+3630321, 7910912-(4092319+3630321), 7910912-7727649)"    # 7722640 188272 183263

# docker load 는 gzip 압축된 tar.gz 파일도 별도 압축 해제 없이 바로 읽는다
docker load -i cmdsheet-alpine.tar.gz    # Loaded image: alpine:3.20
```

7,910,912 바이트짜리 tar 에서 레이어 blob 두 개가 7,722,640 바이트를 차지하고, 둘 다 `gzip compressed data` 였습니다. 이미 압축된 데이터는 gzip 으로 더 줄지 않습니다.

줄어든 183,263 바이트는 레이어 밖 188,272 바이트(설정·매니페스트 JSON, tar 헤더와 패딩)에서 나온 것으로 계산됩니다. 크기를 크게 줄이려면 gzip 이 아니라 `--platform` 으로 담을 플랫폼을 줄이는 쪽이 낫습니다(「containerd 와 멀티 플랫폼」 절).

공식 문서는 load 가 gzip, bzip2, xz, zstd 로 압축된 아카이브를 읽는다고 적습니다.[^load-compress] 이 시트에서 실행해 본 것은 gzip 뿐입니다.

### 다른 호스트로 파이프 전송하기

> save 의 표준 출력을 받는 호스트의 docker load 로 직접 파이프 연결해 파일 저장 없이 즉시 반입합니다.

```bash
# 로컬의 save 표준 출력을 OrbStack Ubuntu VM 의 docker load 표준 입력으로 파이프 연결한다
#   orb -m ubuntu   OrbStack 의 ubuntu VM 안에서 뒤 명령을 실행한다 (이 실측 환경의 진입 방법)
docker save alpine:3.20 | orb -m ubuntu sudo docker load    # Loaded image: alpine:3.20
```

폐쇄망이나 원격 운영 환경에서는 `orb -m ubuntu sudo` 자리에 `ssh HOST` 를 두는 것이 일반 형태입니다. 이 시트에서는 ssh 를 실행해 보지 않았습니다.

### 반입한 이미지를 저장소에 올리기

> 반입한 이미지에 사설 저장소 주소를 붙여 태깅하고 push 로 등록합니다.

```bash
# 테스트용 로컬 사설 레지스트리 컨테이너를 5000번 포트로 띄운다
#   -d       백그라운드에서 컨테이너를 실행한다
#   --name   컨테이너 이름을 지정한다
#   -p       호스트 포트와 컨테이너 포트를 바인딩한다
docker run -d --name cmdsheet-registry -p 5000:5000 registry:2

# 반입한 이미지에 로컬 레지스트리 태그를 단다
docker tag alpine:3.20 localhost:5000/cmdsheet-alpine:3.20

# 로컬 레지스트리로 이미지를 업로드한다
docker push localhost:5000/cmdsheet-alpine:3.20
```

```bash
# 결과
The push refers to repository [localhost:5000/cmdsheet-alpine]
3f26bc2dec0b: Unavailable
3f26bc2dec0b: Pushed
3.20: digest: sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d size: 1026

 Info -> Not all multiplatform-content is present and only the available single-platform image was pushed
         sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc -> sha256:45e09956dc667c5eff3583c9d94830261fb1ca0be10a0a7db36266edf5de9e1d
```

```bash
# 테스트로 만든 태그와 레지스트리 컨테이너를 정리한다
#   -f   실행 중인 컨테이너를 강제로 종료하고 삭제한다
#   -v   컨테이너에 연결된 익명 볼륨까지 함께 지운다
docker rmi localhost:5000/cmdsheet-alpine:3.20    # Untagged: localhost:5000/cmdsheet-alpine:3.20
docker rm -fv cmdsheet-registry    # cmdsheet-registry
```

멀티 플랫폼 이미지를 push 하면 위처럼 Info 줄이 붙고 단일 플랫폼 이미지 하나(`size: 1026` 매니페스트)만 올라갑니다. 이 엔진에는 alpine:3.20 의 8개 플랫폼 중 일부 내용만 있기 때문입니다(「containerd 와 멀티 플랫폼」 절). 폐쇄망 내부 레지스트리로 이미지를 배포할 때는 load 뒤 tag 와 push 단계를 거쳐 워커 노드들이 가져갈 수 있게 만듭니다.

### 반입한 이미지의 정보 확인하기

> docker image inspect 로 반입된 이미지의 고유 ID, 저장소 digest, 플랫폼 아키텍처를 확인하고 받는 쪽 엔진의 ID 와 맞대 봅니다.

```bash
# 이미지의 고유 ID 해시값을 확인한다
#   -f   Go 템플릿 문법으로 출력 필드를 지정한다
docker image inspect -f '{{.Id}}' alpine:3.20    # sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc

# 저장소 digest 등록 목록을 확인한다
docker image inspect -f '{{.RepoDigests}}' alpine:3.20    # [alpine@sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc]

# 이미지의 아키텍처와 운영체제를 확인한다
docker image inspect -f '{{.Architecture}} {{.Os}}' alpine:3.20    # arm64 linux

# 받는 쪽(Ubuntu VM)의 엔진에서 같은 이미지의 ID 를 확인해 위 값과 맞댄다
orb -m ubuntu sudo docker image inspect -f '{{.Id}}' alpine:3.20    # sha256:d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc
```

보낸 쪽과 받은 쪽의 이미지 ID 가 같았습니다. `busybox:1.36.0` 도 같은 방식으로 비교했고 두 엔진의 ID 가 같았습니다(다음 절). 이 엔진에서 이미지 ID 는 save 한 tar 의 `blobs/sha256/d9e853e8…` 파일(9,226 바이트)의 digest 와 같은 값입니다. 그 파일을 열어 보면 8개 플랫폼의 매니페스트가 적힌 이미지 인덱스입니다. 그래서 저장소를 거치지 않고 save 와 load 로 옮겨도 ID 가 변하지 않았습니다.

### 실습 정리

```bash
# 실습 과정에서 생성된 모든 tar 아카이브와 압축 파일을 삭제한다
rm -f cmdsheet-alpine.tar cmdsheet-alpine-stdout.tar cmdsheet-bundle.tar cmdsheet-alpine.tar.gz cmdsheet-by-id.tar cmdsheet-by-name.tar cmdsheet-exported.tar cmdsheet-amd64.tar
```

받는 호스트에 이름 없이 들어간 실습 이미지는 ID 로 지웁니다(다음 절의 `docker rmi sha256:…`).



## 주의사항과 동작 원리

### ID 로 내보낼 때의 태그 유실

> 이름 대신 이미지 ID 로 save 하면 manifest.json 의 RepoTags 가 null 이 되고, 받는 호스트에서 load 한 이미지는 이름이 없어 기본 목록에서 빠집니다.

```bash
# 이미지 고유 ID 를 확인한다
docker image inspect -f '{{.Id}}' busybox:1.36.0    # sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

# 이름으로 한 번, ID 로 한 번 save 한다
docker save -o cmdsheet-by-name.tar busybox:1.36.0
docker save -o cmdsheet-by-id.tar sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

# 두 아카이브의 manifest.json 에서 RepoTags 를 비교한다
tar -xOf cmdsheet-by-name.tar manifest.json
tar -xOf cmdsheet-by-id.tar manifest.json
```

```bash
# 결과
[{"Config":"blobs/sha256/3596868f4ba86907dde5849edf4f426f4dc2110b1ace9e5969f5a21838ca9599","RepoTags":["busybox:1.36.0"],"Layers":["blobs/sha256/805f301826ef94301d30be8873f4c2f9a03fd5cad88b4d71808991046153eb86"]}]
[{"Config":"blobs/sha256/3596868f4ba86907dde5849edf4f426f4dc2110b1ace9e5969f5a21838ca9599","RepoTags":null,"Layers":["blobs/sha256/805f301826ef94301d30be8873f4c2f9a03fd5cad88b4d71808991046153eb86"]}]
```

```bash
# 이 이미지가 없는 받는 호스트(Ubuntu VM)에 ID 로 save 한 아카이브를 load 한다
cat cmdsheet-by-id.tar | orb -m ubuntu sudo docker load    # Loaded image ID: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112

# 기본 목록을 본다
#   --format   출력 모양을 Go 템플릿으로 정한다
orb -m ubuntu sudo docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}'

# -a 를 붙여 이름 없는 이미지까지 본다
orb -m ubuntu sudo docker images -a --format '{{.Repository}}:{{.Tag}} {{.ID}}'

# 이름 없는 이미지에 이름을 붙인다
orb -m ubuntu sudo docker tag sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112 cmdsheet-trap:1.0
```

```bash
# 결과 (기본 목록)
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
```

```bash
# 결과 (-a)
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
<none>:<none> 9e2bbca07938
```

```bash
# 결과 (tag 뒤 기본 목록)
alpine:3.20 d9e853e87e55
hello-world:latest c567b231f656
cmdsheet-trap:1.0 9e2bbca07938
```

```bash
# 받는 호스트의 실습 이미지를 지운다 (태그가 붙어 있으면 태그와 이미지가 함께 지워진다)
orb -m ubuntu sudo docker rmi sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
```

```bash
# 결과
Untagged: cmdsheet-trap:1.0
Deleted: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
```

ID 로 save 한 아카이브는 `RepoTags` 가 `null` 입니다. 이 아카이브를 이미지가 없는 호스트에 load 하면 이름이 붙지 않고, `docker images` 기본 목록에는 나타나지 않습니다. `-a` 를 주면 `<none>:<none>` 으로 보입니다.

반입했는데 목록에 없다고 놀랄 수 있으므로, 반입 대상은 ID 가 아니라 `repo:tag` 로 save 해야 이름이 함께 옮겨집니다.[^tag-loss] 이 확인은 containerd 이미지 저장소를 쓰는 엔진 두 대에서 한 것입니다. 그래프 드라이버 엔진의 목록 동작은 확인하지 않았습니다.

### export 와 save 의 층 차이

> export 는 컨테이너 파일시스템만 납작하게 묶으므로 이미지의 빌드 히스토리와 CMD 메타데이터가 사라집니다.

```bash
# 컨테이너를 하나 생성하고 export 로 파일시스템 전체를 tar 로 뺀다
docker create --name cmdsheet-export-demo alpine:3.20    # 5fd025fb81179838303eb0961e66769a5d6b246bc7cf58a354457e35ea83247a
docker export -o cmdsheet-exported.tar cmdsheet-export-demo

# export 로 추출한 tar 를 import 로 들여와 새 이미지를 만든다
docker import cmdsheet-exported.tar cmdsheet-imported:1.0    # sha256:5d84df57968b10af0e3835e8eb757650aa2aa5b641ce824064284469a82d320c

# 원본과 달리 히스토리가 Imported from - 단일 층으로 평탄화되었는지 확인한다
docker history cmdsheet-imported:1.0
```

```bash
# 결과
IMAGE          CREATED         CREATED BY   SIZE      COMMENT
5d84df57968b   2 seconds ago                10.4MB    Imported from -
```

```bash
# 컨테이너 실행에 필요한 기본 실행 명령(Cmd)이 비어 있는지 확인한다
docker image inspect -f '{{.Config.Cmd}}' cmdsheet-imported:1.0    # []

# save 한 tar 의 설정 JSON 에서는 Cmd 가 남아 있는지 확인한다 (arm64 설정 blob)
tar -xOf cmdsheet-alpine.tar blobs/sha256/ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4 | python3 -I -c "import sys,json;c=json.load(sys.stdin);print(c['architecture'],c['config']['Cmd'])"    # arm64 ['/bin/sh']

# 테스트용 컨테이너와 가져온 이미지를 정리한다
docker rm -fv cmdsheet-export-demo    # cmdsheet-export-demo
docker rmi cmdsheet-imported:1.0
```

```bash
# 결과
Untagged: cmdsheet-imported:1.0
Deleted: sha256:5d84df57968b10af0e3835e8eb757650aa2aa5b641ce824064284469a82d320c
```

`docker save` 한 tar 의 설정 JSON 에는 기본 실행 명령 `['/bin/sh']` 이 남아 있었습니다.

반면 `docker export` 로 만든 tar 는 파일시스템만 담습니다. 그래서 `import` 한 이미지는 히스토리가 `Imported from -` 한 줄로 줄었습니다. `Config.Cmd` 도 `[]` 가 되었습니다.[^export-save]

### containerd 와 멀티 플랫폼

> containerd 이미지 저장소 엔진에서 save 는 엔진에 내용이 있는 플랫폼을 모두 담고, --platform 으로 하나만 골라 담을 수 있으며, 엔진에 없는 플랫폼을 고르면 오류가 납니다.

```bash
# 엔진에 내용이 있는 linux/amd64 플랫폼만 골라 tar 파일로 내보낸다
#   --platform   저장할 플랫폼을 os[/arch[/variant]] 로 지정한다
docker save --platform linux/amd64 -o cmdsheet-amd64.tar alpine:3.20

# 기본 save 와 크기를 맞댄다 (기본 save 는 7910912 바이트였다)
wc -c cmdsheet-amd64.tar    #  3722752 cmdsheet-amd64.tar

# tar 안의 설정 blob 에서 아키텍처를 직접 꺼낸다
tar -xOf cmdsheet-amd64.tar blobs/sha256/bf8527eb54c3680e728d5b4b383a8ba730d72dae7236fbc8dff97ed6b224a731 | python3 -I -c "import sys,json;c=json.load(sys.stdin);print(c['architecture'],c['config']['Cmd'])"    # amd64 ['/bin/sh']

# 기본 save 한 tar 의 이미지 인덱스에 적힌 플랫폼 목록을 본다 (인덱스는 blobs/sha256/d9e853e8… 파일, 증명 항목 unknown 은 거른다)
tar -xOf cmdsheet-alpine.tar blobs/sha256/d9e853e87e55526f6b2917df91a2115c36dd7c696a35be12163d44e6e2a4b6bc | python3 -I -c "import sys,json;[print('/'.join([m['platform']['os'],m['platform']['architecture'],m['platform'].get('variant','')]).rstrip('/')) for m in json.load(sys.stdin)['manifests'] if m['platform']['os']!='unknown']"
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

```bash
# 엔진에 내용이 없는 플랫폼을 고르면 어떻게 되는지 본다
docker save --platform linux/s390x -o cmdsheet-s390x.tar alpine:3.20; echo $?
docker save --platform linux/amd64 -o cmdsheet-bb-amd64.tar busybox:1.36.0; echo $?
```

```bash
# 결과
Error response from daemon: no suitable export target found: image with reference alpine:3.20 was found but does not provide the specified platform (linux/s390x)
1
Error response from daemon: no suitable export target found: image with reference busybox:1.36.0 was found but does not provide the specified platform (linux/amd64)
1
```

이 실측 엔진은 arm64 호스트이고, alpine:3.20 의 amd64 와 arm64 내용이 둘 다 있습니다. 그래서 기본 `docker save` 는 레이어 blob 두 개를 모두 담았습니다. arm64 레이어는 4,092,319 바이트, amd64 레이어는 3,630,321 바이트였습니다.

기본 `save` 로 만든 tar 의 `manifest.json` 에는 호스트 플랫폼인 arm64 항목 하나만 있었습니다. 그래도 `blobs/` 에는 두 플랫폼의 레이어가 모두 들어 있었습니다.

`--platform linux/amd64` 로 저장하면 크기가 3,722,752 바이트로 줄었습니다. 설정 blob 의 `architecture` 가 `amd64` 로 나와, amd64 이미지가 실제로 담겼음을 확인했습니다.

인덱스에는 있어도 엔진에 내용이 없는 플랫폼을 고르면 오류가 났고 tar 파일은 만들어지지 않았습니다. alpine 의 s390x 와 busybox 의 amd64 가 그런 경우였습니다. 이 동작은 공식 문서의 설명과 같습니다.[^multiplatform]

받는 쪽에서 load 할 때도 같은 규칙이 적용됩니다. 아래는 arm64 내용만 든 `busybox:1.36.0` 을 ID 로 save 한 아카이브를 Ubuntu VM 에 load 한 실측입니다.

```bash
# 아카이브에 내용이 없는 플랫폼을 load 하려 하면 오류가 난다
#   --platform   불러올 플랫폼을 지정한다
cat cmdsheet-by-id.tar | orb -m ubuntu sudo docker load --platform linux/amd64

# 내용이 있는 플랫폼은 불러온다
cat cmdsheet-by-id.tar | orb -m ubuntu sudo docker load --platform linux/arm64
```

```bash
# 결과
requested platform(s) ([linux/amd64]) found, but some content is missing: NotFound: content digest sha256:086417a48026173aaadca4ce43a1e4b385e8e62cc738ba79fc6637049674cac0: not found
Loaded image ID: sha256:9e2bbca079387d7965c3a9cee6d0c53f4f4e63ff7637877a83c4c05f2a666112
```

두 번째 load 로 들어간 이미지는 앞 절의 `docker rmi sha256:…` 로 지웠습니다.

`--platform` 은 엔진 버전을 탑니다. 릴리스 노트는 `save`·`load` 의 `--platform` 이 28.0.0 에서 들어왔고, 쉼표로 여러 플랫폼을 고르는 것은 29.0.0 부터라고 적습니다.[^platform-ver]

이 시트의 두 엔진은 모두 29 버전입니다. 28.0.0 보다 낮은 엔진에서는 돌려 보지 않았습니다.



## 관련 문서

> 이어서 볼 시트와 관련 문서를 모았습니다.

- [클라우드 명령어 시트](../README.md) — 컨테이너와 쿠버네티스 도구의 시트 모음
- [이미지 pull과 폐쇄망 반입](../../kubernetes/architecture/%EC%9D%B4%EB%AF%B8%EC%A7%80%20pull%C2%B7%ED%8F%90%EC%87%84%EB%A7%9D%20%EB%B0%98%EC%9E%85.md) — ctr images import 와 nerdctl load, k8s.io 네임스페이스 반입 절차
- [nerdctl 참조 시트](../../../../02_os/docs/cmd/isolate/nerdctl.md) — containerd 환경에서 이미지 반입과 저장소 push 를 다루는 시트



## 참고 자료

> 실측에 쓴 두 엔진의 버전과 대조한 Docker 공식 문서 페이지를 모았습니다.

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
