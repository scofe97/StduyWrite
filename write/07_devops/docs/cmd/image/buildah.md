---
title: "buildah 참조 시트"
tags: ["devops", "command", "image", "buildah", "oci", "rootless"]
status: draft
source:
  - "buildah 1.42.1 (1.42.1+ds1-2build1) `buildah --help` 와 하위 명령 `--help` 원문 (OrbStack Ubuntu 26.04.1 VM 실측)"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-build.1.md"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-from.1.md"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-commit.1.md"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-push.1.md"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-mount.1.md"
  - "https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-unshare.1.md"
  - "https://github.com/podman-container-tools/buildah/releases/tag/v1.46.1"
related:
  - "../README.md"
  - "../../artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md"
  - "../../artifact/container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md"
  - "buildkit.md"
  - "../../../../08_cloud/docs/cmd/container/podman.md"
  - "../../../../08_cloud/docs/cmd/container/docker.md"
updated: "2026-11-23"
---

# buildah 참조 시트

---

> 데몬 없이 OCI 이미지를 만드는 `buildah` 로 Dockerfile 빌드, 셸 명령 단계별 빌드, 셸 없는 이미지 만들기, 저장소 올리기, 캐시와 격리 선택을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `buildah` 는 컨테이너 데몬 없이 OCI 이미지를 만드는 CLI 입니다.

이미지를 만드는 길이 둘입니다. 하나는 Dockerfile 을 읽는 `buildah build` 입니다. 다른 하나는 작업 컨테이너를 만들어 `from`·`run`·`copy`·`config`·`commit` 을 하나씩 부르는 길입니다. 빌더를 왜 고르는지는 「[이미지 빌더 종류와 선택](../../artifact/container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md)」, rootless 로 빌드가 되는 조건은 「[rootless 빌드의 조건](../../artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md)」 이 설명합니다.

이 시트의 출력은 OrbStack Ubuntu 26.04.1 VM(aarch64)에서 받았습니다. 실측 버전은 apt 로 받은 buildah 1.42.1(`1.42.1+ds1-2build1`)입니다. 가장 새 버전은 2026-11-11 에 나온 v1.46.1 이라서, 옵션 뜻은 1.42.1 의 `--help` 와 문서 기준입니다.[^env] 예는 일반 사용자 `dev` 로 돌렸고, docker 와 저장소 컨테이너를 다루는 곳만 root 입니다.



## 핵심 문법

> 이미지는 `build` 한 줄이나 작업 컨테이너를 고쳐 `commit` 하는 여러 줄로 만들고, 이미지를 내보낼 곳은 `전송방식:주소` 로 적습니다.

```bash
# 호출 형태
buildah [command]
buildah build [CONTEXT] [flags]

# Dockerfile 로 빌드한다 (Dockerfile 로 이미지 빌드하기)
buildah build -t NAME:TAG -f DOCKERFILE CONTEXT

# 이미지를 보고 안을 들여다본다 (만든 이미지와 설정 보기)
buildah images
buildah inspect --type image IMAGE

# 작업 컨테이너에서 한 단계씩 만든다 (셸 명령으로 한 단계씩 만들기)
buildah from --name NAME IMAGE
buildah run NAME -- COMMAND [ARG...]
buildah copy NAME SRC DEST
buildah config --env KEY=VALUE --cmd COMMAND NAME
buildah commit NAME IMAGE
buildah containers

# 빈 이미지의 루트 파일시스템에 파일을 직접 넣는다 (셸 없는 이미지 만들기)
buildah from scratch
buildah unshare COMMAND
buildah mount NAME

# 저장소나 tar 로 내보낸다 (저장소에 올리고 tar 로 내보내기)
buildah push IMAGE TRANSPORT:DESTINATION

# 캐시를 켜고 격리 방식을 고른다 (다시 빌드할 때 캐시 확인, 권한이 좁은 곳의 빌드 격리)
buildah build --layers ...
buildah build --isolation TYPE ...

# 이름을 찍어 지운다 (실습 정리)
buildah rm NAME
buildah rmi IMAGE
```

### 내보낼 곳 표기

```bash
# push 의 목적지는 전송방식:세부 주소 꼴이다. 전송방식을 빼면 docker (레지스트리)로 읽는다[^push]
# docker://localhost:5104/tiny:1                  레지스트리 (실측)
# oci-archive:FILE:NAME:TAG                       OCI 형식 tar 파일 (실측)
# docker-archive:FILE:NAME:TAG                    docker 형식 tar 파일 (실측)
# containers-storage, dir, docker-daemon, oci, sif   --help 에 나온 나머지 전송방식 (돌리지 않았다)
```



## 종료 코드

> 성공하면 0 이고, 이 시트에서 본 buildah 자체의 실패는 125 이며, `RUN` 단계가 실패하면 그 명령의 종료 코드가 그대로 나옵니다.[^exit]

```bash
# 0    성공
# 125  실측: 없는 작업 컨테이너를 지우거나 없는 Dockerfile 로 빌드한 경우
# 3    RUN 안 명령이 낸 코드 (「RUN 단계가 실패할 때」에서 본다)
buildah rm no-such-container; echo $?
buildah build -f app/NoSuchFile app > /dev/null 2>&1; echo $?
```

```bash
Error: removing container "no-such-container": container not known
125
125
```



## 유스케이스

### 실습 준비

> 아래 블록을 차례로 붙여 넣으면 buildah 설치와 이 시트의 예가 쓰는 소스·기준 이미지·저장소가 모두 생기며, 앞의 세 블록은 root 셸이고 그 뒤는 일반 사용자 `dev` 셸입니다.

```bash
# buildah 와 podman 을 받고 버전을 본다 (uidmap 은 일반 사용자의 사용자 namespace 매핑에 쓴다)
DEBIAN_FRONTEND=noninteractive apt-get install -y buildah podman uidmap > /dev/null
buildah --version
dpkg -l buildah | grep '^ii'
```

```bash
buildah version 1.42.1 (image-spec 1.1.1, runtime-spec 1.2.1)
ii  buildah        1.42.1+ds1-2build1 arm64        CLI tool to facilitate building OCI images
```

```bash
# 일반 사용자 dev 를 만든다 (이미 있으면 그대로 쓴다. subuid·subgid 줄은 매핑 범위다)
id dev > /dev/null 2>&1 || useradd -m -s /bin/bash dev
id dev
grep '^dev:' /etc/subuid /etc/subgid
```

```bash
uid=1000(dev) gid=1000(dev) groups=1000(dev)
/etc/subuid:dev:100000:65536
/etc/subgid:dev:100000:65536
```

```bash
# 이미지를 올려 볼 저장소 컨테이너를 127.0.0.1:5104 에 띄운다 (「저장소에 올리고 tar 로 내보내기」에서 쓴다)
docker run -d --name sheet-buildah-reg -p 127.0.0.1:5104:5000 registry:2 | cut -c1-12
sleep 2
curl -s localhost:5104/v2/
```

```bash
# 예제 소스를 만든다 (「Dockerfile 로 이미지 빌드하기」부터 여러 곳에서 쓴다)
mkdir -p ~/sheet-buildah/app && cd ~/sheet-buildah
cat > app/hello.sh <<'EOF'
#!/bin/sh
echo "hello from buildah"
EOF
chmod +x app/hello.sh
cat > app/Dockerfile <<'EOF'
FROM localhost/sheet-buildah/alpine:3.20
RUN apk add --no-cache curl > /dev/null && echo built > /built.txt
COPY hello.sh /usr/local/bin/hello.sh
ENV GREETING=hi
CMD ["hello.sh"]
EOF
ls app
```

```bash
Dockerfile
hello.sh
```

```bash
# 기준 이미지를 받아 자기 이름으로 tag 한다 (이 뒤의 Dockerfile 이 이 이름을 FROM 에 쓴다)
buildah pull -q docker.io/library/alpine:3.20
buildah tag docker.io/library/alpine:3.20 localhost/sheet-buildah/alpine:3.20
buildah images
```

```bash
ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4
REPOSITORY                       TAG    IMAGE ID       CREATED        SIZE
localhost/sheet-buildah/alpine   3.20   ab3fe4defd29   7 months ago   9.12 MB
docker.io/library/alpine         3.20   ab3fe4defd29   7 months ago   9.12 MB
```

### Dockerfile 로 이미지 빌드하기

> `docker build` 와 같은 꼴로 빌드하되, 데몬 없이 로컬 저장소에 이미지를 쓰는 과정이 출력에 그대로 보입니다.

```bash
# Dockerfile 을 읽어 이미지를 만든다
#   -t   만들 이미지의 이름과 태그
#   -f   읽을 Dockerfile 경로
# 마지막 인자 app 은 COPY 가 파일을 찾는 컨텍스트 디렉터리다
buildah build -t localhost/sheet-buildah/app:1 -f app/Dockerfile app
```

```bash
STEP 1/5: FROM localhost/sheet-buildah/alpine:3.20
STEP 2/5: RUN apk add --no-cache curl > /dev/null && echo built > /built.txt
STEP 3/5: COPY hello.sh /usr/local/bin/hello.sh
STEP 4/5: ENV GREETING=hi
STEP 5/5: CMD ["hello.sh"]
COMMIT localhost/sheet-buildah/app:1
Getting image source signatures
Copying blob sha256:88b4fba61c4c714a2fc173ddf7e9324a257304696830bf41ad28ecc58c11c95f
Copying blob sha256:67262acc96433ae551eb3693fa4a8e3a9b687b7aae2e392bf2533bec97509542
Copying config sha256:c84284c48d81f33c978b348d51b8775438f5bed5d0c9578b3c2d43b1afbc279a
Writing manifest to image destination
--> c84284c48d81
Successfully tagged localhost/sheet-buildah/app:1
c84284c48d81f33c978b348d51b8775438f5bed5d0c9578b3c2d43b1afbc279a
```

`STEP N/5` 는 Dockerfile 줄이고 `COMMIT` 부터 이미지를 저장소에 씁니다. 마지막 줄의 값은 `Copying config` 에 찍힌 값과 같은 이미지 ID 입니다.

```bash
# 만든 이미지를 본다
buildah images
```

```bash
REPOSITORY                       TAG    IMAGE ID       CREATED                  SIZE
localhost/sheet-buildah/app      1      c84284c48d81   Less than a second ago   15.1 MB
localhost/sheet-buildah/alpine   3.20   ab3fe4defd29   7 months ago             9.12 MB
docker.io/library/alpine         3.20   ab3fe4defd29   7 months ago             9.12 MB
```

```bash
# buildah 는 이미지를 바로 실행하는 명령이 없어서, 같은 저장소를 읽는 podman 으로 돌려 본다
podman run --rm localhost/sheet-buildah/app:1    # hello from buildah
```

### 만든 이미지와 설정 보기

> `inspect` 로 이미지의 CMD·환경 변수·레이어 수를 `--format` 이나 `jq` 로 뽑습니다.

```bash
# 이미지의 아키텍처·CMD·환경 변수를 Go 템플릿으로 뽑는다
#   --type     container 대신 image 를 가리킨다
#   --format   출력할 필드를 Go 템플릿으로 고른다
buildah inspect --type image \
  --format '{{.OCIv1.Architecture}} {{.OCIv1.Config.Cmd}} {{.OCIv1.Config.Env}}' \
  localhost/sheet-buildah/app:1
```

```bash
arm64 [hello.sh] [PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin GREETING=hi]
```

```bash
# JSON 전체를 jq 로 넘겨 레이어 수와 환경 변수를 뽑는다. 마지막 줄은 이름이 붙은 이미지 목록이다
buildah inspect --type image localhost/sheet-buildah/app:1 | jq '.OCIv1.rootfs.diff_ids | length'
buildah inspect --type image localhost/sheet-buildah/app:1 | jq -r '.OCIv1.config.Env[]'
buildah images --json | jq -r '.[].names[]' | grep app:1
```

```bash
2
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
GREETING=hi
localhost/sheet-buildah/app:1
```

레이어 수 `2` 는 기준 이미지 1층에 Dockerfile 의 `RUN`·`COPY` 가 더한 1층입니다. 이 수를 다음 두 유스케이스에서 견줍니다.

### 셸 명령으로 한 단계씩 만들기

> Dockerfile 없이 작업 컨테이너를 만들어 명령을 하나씩 실행하고 `commit` 해서 이미지로 굳힙니다.

작업 컨테이너는 `buildah from` 이 이미지 위에 만드는 고칠 수 있는 컨테이너입니다. 이름을 주지 않으면 `이미지이름-working-container` 로 붙습니다.[^from]

```bash
# 기준 이미지로 작업 컨테이너를 만든다
#   --name   작업 컨테이너의 이름
buildah from --name sb-step localhost/sheet-buildah/alpine:3.20
```

```bash
sb-step
```

```bash
# 컨테이너 안에서 명령을 실행하고 결과를 확인한다 (-- 뒤가 컨테이너 안 명령이다)
buildah run sb-step -- sh -c 'apk add --no-cache curl > /dev/null && echo built > /built.txt'; echo $?
buildah run sb-step -- cat /built.txt
```

```bash
0
built
```

```bash
# 호스트 파일을 컨테이너 안으로 복사하고 CMD·환경 변수를 정한다 (copy 는 복사된 내용의 해시를 찍는다)
#   --env   이미지에 넣을 환경 변수
#   --cmd   이미지의 기본 명령
buildah copy sb-step app/hello.sh /usr/local/bin/hello.sh | cut -c1-12
buildah config --env GREETING=hi --cmd hello.sh sb-step; echo $?
```

```bash
2cadb3f6b4c9
0
```

```bash
# 작업 컨테이너 목록을 본다
buildah containers
```

```bash
CONTAINER ID  BUILDER  IMAGE ID     IMAGE NAME                       CONTAINER NAME
16fe61f983fe     *     ab3fe4defd29 localhost/sheet-buildah/alpin... sb-step
```

```bash
# 작업 컨테이너를 이미지로 굳힌다
buildah commit sb-step localhost/sheet-buildah/app:2
```

```bash
Getting image source signatures
Copying blob sha256:88b4fba61c4c714a2fc173ddf7e9324a257304696830bf41ad28ecc58c11c95f
Copying blob sha256:81b46cd4dfe07e59c713c0251dc3667fb211b9c33b5a2b7e367a29068d0eb9ce
Copying config sha256:e5d8e127c3050ba10115642906a29c7ffa3a1c48920d2476d1cf66bb07cd9e12
Writing manifest to image destination
e5d8e127c3050ba10115642906a29c7ffa3a1c48920d2476d1cf66bb07cd9e12
```

```bash
# commit 뒤에도 작업 컨테이너는 남고, 새 이미지가 이름과 함께 목록에 오른다
buildah containers --format '{{.ContainerName}} {{.ImageName}}'
buildah images --format '{{.Name}}:{{.Tag}}' | grep sheet-buildah/app
```

```bash
sb-step   localhost/sheet-buildah/alpine:3.20
localhost/sheet-buildah/app:2
localhost/sheet-buildah/app:1
```

### 두 방식의 레이어 수 비교

> Dockerfile 로 만든 `app:1` 과 단계별로 만든 `app:2` 의 레이어 수를 같은 `jq` 로 셉니다.

```bash
# 이미지마다 레이어 수를 센다 (기준 이미지 alpine:3.20 은 1층이다)
for t in 1 2; do
  printf 'app:%s  ' $t
  buildah inspect --type image localhost/sheet-buildah/app:$t | jq '.OCIv1.rootfs.diff_ids | length'
done
printf 'alpine:3.20  '
buildah inspect --type image localhost/sheet-buildah/alpine:3.20 | jq '.OCIv1.rootfs.diff_ids | length'
```

```bash
app:1  2
app:2  2
alpine:3.20  1
```

두 방식 모두 기준 1층에 한 층이 더해진 2층입니다. `--layers` 를 켜면 달라지며, 그 결과는 「다시 빌드할 때 캐시 확인」 에서 봅니다.

### 셸 없는 이미지 만들기

> `scratch` 로 빈 작업 컨테이너를 만들어 루트 파일시스템에 파일을 직접 넣으면, 패키지 관리자도 `/bin/sh` 도 없는 이미지가 됩니다.

```bash
# 빈 이미지에서 작업 컨테이너를 만든다
buildah from --name sb-tiny scratch    # sb-tiny
```

```bash
# 일반 사용자는 mount 가 거부된다 (뒤의 숫자는 종료 코드다)
buildah mount sb-tiny; echo $?
```

```bash
Error: cannot mount using driver overlay in rootless mode. You need to run it in a `buildah unshare` session
125
```

일반 사용자는 `buildah unshare` 로 만든 사용자 namespace 안에서만 `mount` 할 수 있습니다.[^unshare]

```bash
# unshare 안에서 두 작업 컨테이너를 mount 해 busybox 와 musl 로더를 옮기고 파일을 직접 만든다
# (musl 로더 이름은 aarch64 용이다. x86_64 에서는 ld-musl-x86_64.so.1 이다)
buildah unshare bash -c '
  tiny=$(buildah mount sb-tiny)
  base=$(buildah mount $(buildah from --name sb-src localhost/sheet-buildah/alpine:3.20))
  cp "$base/bin/busybox" "$tiny/busybox"
  mkdir -p "$tiny/lib"
  cp "$base/lib/ld-musl-aarch64.so.1" "$tiny/lib/"
  echo "hi from tiny" > "$tiny/hello.txt"
  cd "$tiny" && ls -R .
  buildah umount sb-tiny sb-src > /dev/null
'
buildah rm sb-src
```

```bash
.:
busybox
hello.txt
lib

./lib:
ld-musl-aarch64.so.1
99ef5d46ae3c5d76c378e166d19dd332e0aafca3ce2f3f35ca105cb899459ab7
```

```bash
# 시작 명령을 정하고 commit 한 뒤 크기를 본다
#   --entrypoint   JSON 배열로 주면 셸을 거치지 않는다
#   -q             commit 의 진행 출력을 줄이고 이미지 ID 만 찍는다
buildah config --entrypoint '["/busybox","cat","/hello.txt"]' sb-tiny
buildah commit -q sb-tiny localhost/sheet-buildah/tiny:1
buildah images --format '{{.Name}}:{{.Tag}} {{.Size}}' | grep tiny
```

```bash
a40522688bc6d2578f72315d2b71300f762d682599cbcf4d3d2ed912297e86d6
localhost/sheet-buildah/tiny:1        1.65 MB
```

```bash
# 실행해 보고, /bin/sh 를 지정하면 어떻게 되는지 본다 (오류 줄은 120자에서 잘랐다)
podman run --rm localhost/sheet-buildah/tiny:1
{ podman run --rm --entrypoint /bin/sh localhost/sheet-buildah/tiny:1; echo $?; } 2>&1 | cut -c1-120
```

```bash
hi from tiny
Error: runc: runc create failed: unable to start container process: error during container init: exec: "/bin/sh": stat /
127
```

`/bin/sh` 가 없어서 셸을 지정하면 runc 가 거부하고 `podman run` 은 127 로 끝납니다. 크기는 `busybox` 와 로더 파일만큼인 1.65 MB 입니다.

### 저장소에 올리고 tar 로 내보내기

> `push` 는 목적지의 `전송방식:` 으로 레지스트리와 tar 파일을 가르며, HTTP 로 답하는 로컬 저장소에는 `--tls-verify=false` 가 필요합니다.

```bash
# 옵션 없이 올리면 HTTPS 를 먼저 시도해 실패한다 (오류 줄의 뒷부분만 보고, 줄은 120자에서 잘랐다)
buildah push localhost/sheet-buildah/tiny:1 docker://localhost:5104/tiny:1 2>&1 | grep -o 'pinging container registry.*' | cut -c1-120
```

```bash
pinging container registry localhost:5104: Get "https://localhost:5104/v2/": http: server gave HTTP response to HTTPS cl
```

```bash
# 인증서 검증과 HTTPS 요구를 끄고 올린다
#   --tls-verify=false   HTTPS 를 요구하지 않고 인증서도 검증하지 않는다
buildah push --tls-verify=false localhost/sheet-buildah/tiny:1 docker://localhost:5104/tiny:1
```

```bash
Getting image source signatures
Copying blob sha256:421a5ffc0b579228b2d3db01945db3bafdba234aef117242bb6635f23b718a6a
Copying config sha256:a40522688bc6d2578f72315d2b71300f762d682599cbcf4d3d2ed912297e86d6
Writing manifest to image destination
```

`localhost` 도 예외가 아니었고, 기본값은 `--tls-verify` 가 켜진 쪽입니다.[^tls]

```bash
# 저장소 쪽에서 올라온 것을 확인한다
curl -s localhost:5104/v2/_catalog
curl -s localhost:5104/v2/tiny/tags/list
```

```bash
{"repositories":["tiny"]}
{"name":"tiny","tags":["1"]}
```

```bash
# 같은 이미지를 두 형식의 tar 로 내보내고 크기를 본다 (진행 출력은 버렸다)
buildah push localhost/sheet-buildah/tiny:1 oci-archive:tiny-oci.tar:localhost/sheet-buildah/tiny:1 > /dev/null 2>&1
buildah push localhost/sheet-buildah/tiny:1 docker-archive:tiny-docker.tar:sheet-buildah/tiny:1 > /dev/null 2>&1
ls -l tiny-oci.tar tiny-docker.tar
```

```bash
-rw-r--r-- 1 dev dev 1653760 Nov 23 21:38 tiny-docker.tar
-rw-r--r-- 1 dev dev  989696 Nov 23 21:38 tiny-oci.tar
```

```bash
# tar 안의 파일 목록을 본다
tar tf tiny-oci.tar
tar tf tiny-docker.tar
```

```bash
blobs/
blobs/sha256/
blobs/sha256/a40522688bc6d2578f72315d2b71300f762d682599cbcf4d3d2ed912297e86d6
blobs/sha256/b8dee64bc39a016b67f4c4590ba1b7f2917e227904a516028e3fc1363f687b25
blobs/sha256/f753eaf51e7b94d16dbd66eaa414806dc4036e26c599cac0557bc91c3605498e
index.json
oci-layout
421a5ffc0b579228b2d3db01945db3bafdba234aef117242bb6635f23b718a6a.tar
a40522688bc6d2578f72315d2b71300f762d682599cbcf4d3d2ed912297e86d6.json
79174af510d0ecc61ece67a14fbda5063418c301df3562381623a51c79fa6d9b/layer.tar
79174af510d0ecc61ece67a14fbda5063418c301df3562381623a51c79fa6d9b/VERSION
79174af510d0ecc61ece67a14fbda5063418c301df3562381623a51c79fa6d9b/json
manifest.json
repositories
```

`oci-archive` 는 `index.json` 과 `blobs/` 로, `docker-archive` 는 `manifest.json` 으로 이루어집니다.

### 다시 빌드할 때 캐시 확인

> `--layers` 를 켜면 단계마다 중간 이미지가 남고, 같은 Dockerfile 을 다시 빌드할 때 `Using cache` 로 재사용합니다.

```bash
# 처음 빌드: 단계마다 --> 해시가 찍힌다
#   --layers   단계마다 중간 이미지를 남긴다
buildah build --layers -t localhost/sheet-buildah/app:3 -f app/Dockerfile app
```

```bash
STEP 1/5: FROM localhost/sheet-buildah/alpine:3.20
STEP 2/5: RUN apk add --no-cache curl > /dev/null && echo built > /built.txt
--> 62bc624e3446
STEP 3/5: COPY hello.sh /usr/local/bin/hello.sh
--> a70819ec3139
STEP 4/5: ENV GREETING=hi
--> 89ca138f9b78
STEP 5/5: CMD ["hello.sh"]
COMMIT localhost/sheet-buildah/app:3
--> c4e23ba8dc8d
Successfully tagged localhost/sheet-buildah/app:3
c4e23ba8dc8d408cc7a0a20ce4af49fc1758f895d0e502f83c275fba64af5cb1
```

```bash
# 같은 빌드를 한 번 더 한다
buildah build --layers -t localhost/sheet-buildah/app:3 -f app/Dockerfile app
```

```bash
STEP 1/5: FROM localhost/sheet-buildah/alpine:3.20
STEP 2/5: RUN apk add --no-cache curl > /dev/null && echo built > /built.txt
--> Using cache 62bc624e3446c097b2c50c0a5af4a9820e1621d656e76b99a978126f9b16d8e6
--> 62bc624e3446
STEP 3/5: COPY hello.sh /usr/local/bin/hello.sh
--> Using cache a70819ec3139997783914bd0e4700658e156ed29a3d3f2a274014f4d9298d4db
--> a70819ec3139
STEP 4/5: ENV GREETING=hi
--> Using cache 89ca138f9b7875e6c30a17f33cdc33b751c5f509762938fe51ab3cc915bf5667
--> 89ca138f9b78
STEP 5/5: CMD ["hello.sh"]
--> Using cache c4e23ba8dc8d408cc7a0a20ce4af49fc1758f895d0e502f83c275fba64af5cb1
COMMIT localhost/sheet-buildah/app:3
--> c4e23ba8dc8d
Successfully tagged localhost/sheet-buildah/app:3
c4e23ba8dc8d408cc7a0a20ce4af49fc1758f895d0e502f83c275fba64af5cb1
```

```bash
# 캐시 재사용 줄 수와 레이어 수를 센다 (진행 출력은 stderr 라서 2>&1 로 합쳤다)
# 위: --layers 없이, 가운데: --layers 로 다시 빌드, 아래: app:3 의 레이어 수
buildah build -t localhost/sheet-buildah/app:1 -f app/Dockerfile app 2>&1 | grep -c 'Using cache'
buildah build --layers -t localhost/sheet-buildah/app:3 -f app/Dockerfile app 2>&1 | grep -c 'Using cache'
buildah inspect --type image localhost/sheet-buildah/app:3 | jq '.OCIv1.rootfs.diff_ids | length'
```

```bash
0
4
3
```

`--layers` 없이 빌드하면 앞서 만든 중간 이미지가 있어도 재사용하지 않아 `0` 입니다. 켜면 단계 4개를 모두 재사용해 `4` 입니다. `app:3` 은 `RUN`·`COPY` 가 각각 한 층이라 기준 1층까지 3층이며, 이 옵션의 기본값은 `false` 입니다.[^layers]

### 권한이 좁은 곳의 빌드 격리

> `--isolation` 은 `RUN` 단계를 어떤 격리로 실행할지 정하고, 환경 변수 `BUILDAH_ISOLATION` 으로도 바꿀 수 있습니다. 일반 사용자의 기본값은 `rootless` 입니다.[^isol]

```bash
# RUN 안에서 namespace 번호를 찍는 Dockerfile 을 만들고, 호스트(dev 셸)의 번호도 찍는다
mkdir -p iso
cat > iso/Dockerfile <<'EOF'
FROM localhost/sheet-buildah/alpine:3.20
RUN echo ns net=$(readlink /proc/self/ns/net) pid=$(readlink /proc/self/ns/pid) uts=$(readlink /proc/self/ns/uts)
EOF
echo "host net=$(readlink /proc/self/ns/net) pid=$(readlink /proc/self/ns/pid) uts=$(readlink /proc/self/ns/uts)"
```

```bash
host net=net:[4026532503] pid=pid:[4026532501] uts=uts:[4026532499]
```

```bash
# 세 가지 격리로 같은 Dockerfile 을 빌드해 RUN 이 찍은 줄만 본다
#   --isolation   oci, rootless, chroot 중 하나
for i in oci rootless chroot; do
  echo "isolation=$i"
  buildah build --isolation $i -t localhost/sheet-buildah/iso:$i iso 2>&1 | grep '^ns '
done
```

```bash
isolation=oci
ns net=net:[4026533071] pid=pid:[4026533069] uts=uts:[4026533066]
isolation=rootless
ns net=net:[4026533067] pid=pid:[4026533065] uts=uts:[4026533063]
isolation=chroot
ns net=net:[4026532503] pid=pid:[4026532501] uts=uts:[4026533064]
```

`chroot` 만 net 과 pid 가 호스트와 같고 uts 는 달랐습니다. `oci` 와 `rootless` 는 셋 다 호스트와 달랐습니다. 문서는 `rootless` 가 호스트의 network·UTS 를 재사용한다고 적었는데, 이 VM 의 일반 사용자 실측은 그와 어긋났습니다.[^isol]

```bash
# 옵션 대신 환경 변수로 같은 값을 준다. chroot 와 같은 모양이 나온다
BUILDAH_ISOLATION=chroot buildah build -t localhost/sheet-buildah/iso:env iso 2>&1 | grep '^ns '
```

```bash
ns net=net:[4026532503] pid=pid:[4026532501] uts=uts:[4026533066]
```

권한이 좁은 컨테이너 안에서 이 값들을 돌려 보는 일은 이 VM 에서 하지 않았습니다.

### 실습 정리

> 아래 「주의사항과 동작 원리」 의 예는 필요한 것을 스스로 다시 만들고 스스로 지우므로, 이 블록은 먼저 돌려도 됩니다.

```bash
# dev 의 작업 컨테이너와 이미지를 이름을 찍어 지운다. 남은 중간 이미지는 <none> 으로 보이니 목록을 보고 ID 로 지운다
buildah rm sb-step sb-tiny
buildah rmi \
  localhost/sheet-buildah/app:1 \
  localhost/sheet-buildah/app:2 \
  localhost/sheet-buildah/app:3 \
  localhost/sheet-buildah/tiny:1 \
  localhost/sheet-buildah/iso:oci \
  localhost/sheet-buildah/iso:rootless \
  localhost/sheet-buildah/iso:chroot \
  localhost/sheet-buildah/iso:env > /dev/null
buildah rmi localhost/sheet-buildah/alpine:3.20 docker.io/library/alpine:3.20 > /dev/null
buildah images -a
# 주의: 바로 아래 줄은 이 사용자의 저장소 이미지를 전부 지우며 podman 으로 받은 이미지도 같은 저장소라 함께 지워지니, 실습 전용 사용자가 아니면 돌리지 말고 위 목록의 <none> 이미지 ID 를 찍어 지운다
buildah rmi $(buildah images -a -q) > /dev/null
rm -rf /home/dev/sheet-buildah/app /home/dev/sheet-buildah/iso
rm -f /home/dev/sheet-buildah/tiny-oci.tar /home/dev/sheet-buildah/tiny-docker.tar
buildah images -a -q | wc -l
buildah containers -q | wc -l
```

```bash
16fe61f983fe07ab0719998711c93f0eafd978104ee2554ab59bb6c50b619565
975bfba29f4e2355a148938266dc8eef34e75ad3004465e05d8a570778a3f9a2
REPOSITORY   TAG      IMAGE ID       CREATED         SIZE
<none>       <none>   c84284c48d81   7 seconds ago   15.1 MB
0
0
```

```bash
# root 쪽: 저장소 컨테이너를 지우고 작업 폴더를 정리한다
docker rm -fv sheet-buildah-reg
rm -rf /home/dev/sheet-buildah
```

```bash
sheet-buildah-reg
```



## 주의사항과 동작 원리

> 「실습 정리」 에서 기준 이미지와 작업 폴더를 지웠으므로, 아래 예는 먼저 그 둘을 다시 만듭니다.

```bash
buildah pull -q docker.io/library/alpine:3.20 > /dev/null && buildah tag docker.io/library/alpine:3.20 localhost/sheet-buildah/alpine:3.20
mkdir -p ~/sheet-buildah && cd ~/sheet-buildah
```

### 일반 사용자의 mount 실패

> 일반 사용자의 `buildah mount` 는 `buildah unshare` 밖에서 거부되므로, 같은 명령을 unshare 로 감싸 실행합니다.

```bash
# 증상: 거부된다 (빈 작업 컨테이너 sb-tiny 를 먼저 만든다)
# 고치는 꼴: buildah unshare 로 감싸면 mount 경로가 나온다 (경로 앞부분은 줄여 적었다)
buildah from --name sb-tiny scratch > /dev/null
buildah mount sb-tiny 2>&1 | cut -c1-110
buildah unshare buildah mount sb-tiny | sed 's|^.*storage/|.../storage/|'
buildah rm sb-tiny > /dev/null
```

```bash
Error: cannot mount using driver overlay in rootless mode. You need to run it in a `buildah unshare` session
.../storage/overlay/41907dbe160170e1978a7542f9990fcc6f03088347736a9ca7162493072ec233/merged
```

mount 는 unshare 가 만든 mount namespace 안에서만 보이므로, 파일을 넣는 작업도 그 안에서 끝내야 합니다.[^unshare]

### 기본 OCI 형식에서 사라지는 설정

> `buildah` 의 기본 형식은 OCI 라서 docker 용 `HEALTHCHECK` 는 버려지며, 이 설정이 필요하면 `--format docker` 를 줍니다.

```bash
# HEALTHCHECK 가 든 Dockerfile 을 기본 형식(oci)과 docker 형식으로 빌드한다
#   --format   이미지 manifest·설정 형식. 기본값은 oci
mkdir -p hc
printf 'FROM localhost/sheet-buildah/alpine:3.20\nHEALTHCHECK CMD true\n' > hc/Dockerfile
buildah build -t localhost/sheet-buildah/hc:oci hc 2>&1 | grep -i warning | cut -c1-160
buildah build -q --format docker -t localhost/sheet-buildah/hc:docker hc | cut -c1-12
```

```bash
time="2026-11-23T21:39:00+09:00" level=warning msg="HEALTHCHECK is not supported for OCI image format and will be ignored. Must use `docker` format"
4583bfd26caf
```

```bash
# 두 이미지가 가진 healthcheck 설정을 본다
for t in oci docker; do
  printf '%s  ' $t
  buildah inspect --type image localhost/sheet-buildah/hc:$t | jq -c '.Docker.config.Healthcheck'
done
```

```bash
oci  null
docker  {"Test":["CMD-SHELL","true"]}
```

OCI 형식 이미지에는 `HEALTHCHECK` 를 담을 자리가 없어서 빌드 때 경고와 함께 버려집니다. docker 형식으로 만들면 설정이 남습니다.[^fmt]

### buildah bud 라는 이름의 글

> 예전 글에 나오는 `buildah bud` 는 `buildah build` 의 별칭이라 같은 명령입니다.

```bash
# build 의 별칭 목록
buildah build --help | grep -A1 '^Aliases'
```

```bash
Aliases:
  build, build-using-dockerfile, bud
```

문서의 SYNOPSIS 도 `buildah build` 와 `buildah bud` 를 나란히 적습니다.[^bud]

### 사용자마다 따로인 이미지 저장소

> 이미지 저장소는 사용자마다 따로라서, `dev` 가 만든 이미지는 root 의 `buildah images` 에 나오지 않습니다.

```bash
# root 의 저장소 위치와, 이름에 sheet-buildah 가 든 이미지 수
buildah info --format '{{.store.GraphRoot}}{{"\n"}}'
buildah images --format '{{.Name}}' | grep sheet-buildah | wc -l
```

```bash
/var/lib/containers/storage
0
```

```bash
# dev 의 저장소 위치와 같은 수
buildah info --format '{{.store.GraphRoot}}{{"\n"}}'
buildah images --format '{{.Name}}' | grep sheet-buildah | wc -l
```

```bash
/home/dev/.local/share/containers/storage
3
```

반대 방향, 곧 root 가 만든 이미지가 dev 에 안 보이는지는 돌리지 않았습니다.

### 쌓이는 작업 컨테이너

> `buildah from` 은 `commit` 하지 않아도 작업 컨테이너를 남기므로, 목록에서 보고 이름으로 지웁니다.

```bash
# 이름 없이 두 번 만들면 -working-container 이름이 붙고, 앞의 두 줄은 from 이 찍은 이름이다
buildah from localhost/sheet-buildah/alpine:3.20
buildah from localhost/sheet-buildah/alpine:3.20
buildah containers --format '{{.ContainerName}}'
```

```bash
alpine-working-container
alpine-working-container-1
alpine-working-container
alpine-working-container-1
```

```bash
# 이름을 찍어 지우고 남은 목록을 본다
buildah rm alpine-working-container alpine-working-container-1
buildah containers --format '{{.ContainerName}}'
```

```bash
6cffb52346e3e80a1c5ad071e863dcbbdc5d626de21ac697820e6dd2f5a8c89d
a48f5eee12de92c87210ec7b2a9c146415cd184553d1eea2f3484bf65b85b72b
```

### RUN 단계가 실패할 때

> `RUN` 안 명령이 실패하면 빌드가 그 단계에서 멈추고, buildah 는 그 명령의 종료 코드를 그대로 돌려줍니다.

```bash
# RUN 단계가 실패하는 Dockerfile (줄 바꿈은 printf 가 만든다)
mkdir -p fail
printf 'FROM localhost/sheet-buildah/alpine:3.20\nRUN exit 3\n' > fail/Dockerfile
buildah build fail 2>&1 | tail -3
buildah build fail > /dev/null 2>&1; echo $?
rm -rf fail
```

```bash
STEP 1/2: FROM localhost/sheet-buildah/alpine:3.20
STEP 2/2: RUN exit 3
Error: building at STEP "RUN exit 3": while running runtime: exit status 3
3
```

### podman 으로 만든 이미지가 buildah 에 보임

> `podman build` 로 만든 이미지가 `buildah images` 에 나오고, buildah 의 작업 컨테이너도 `podman ps --external` 에 나옵니다.

```bash
# podman 으로 빌드한 이미지 이름을 buildah 로 찾고, buildah 의 작업 컨테이너를 podman 으로 본다
#   --external   podman 이 만들지 않은(buildah 등의) 컨테이너까지 보여 준다
buildah from --name sb-pm localhost/sheet-buildah/alpine:3.20 > /dev/null
mkdir -p pm && printf 'FROM localhost/sheet-buildah/alpine:3.20\n' > pm/Dockerfile
podman build -q -t localhost/sheet-buildah/frompodman:1 -f pm/Dockerfile pm | cut -c1-12
buildah images --format '{{.Name}}:{{.Tag}}' | grep frompodman
podman ps -a --external --format '{{.Names}}'
```

```bash
ab3fe4defd29
localhost/sheet-buildah/frompodman:1
sb-pm
```

두 도구가 같은 저장소를 읽는다는 것은 이 시트의 실측으로만 확인했고, 공식 문서 근거는 찾아 대조하지 않았습니다.

```bash
buildah rm sb-pm > /dev/null
buildah rmi localhost/sheet-buildah/frompodman:1 localhost/sheet-buildah/hc:oci localhost/sheet-buildah/hc:docker localhost/sheet-buildah/alpine:3.20 docker.io/library/alpine:3.20 > /dev/null
cd ~ && rm -rf ~/sheet-buildah
```



## 관련 문서

> 빌더를 고르는 기준과 rootless 조건, 같은 저장소를 쓰는 podman 시트, 데몬 없이 BuildKit 으로 빌드하는 시트입니다.

- [DevOps 명령어 시트](../README.md) — 같은 폴더 지도
- [rootless 빌드의 조건](../../artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md) — 일반 사용자 빌드가 되는 사용자 namespace 와 매핑의 원리
- [이미지 빌더 종류와 선택](../../artifact/container/01-03.%EC%9D%B4%EB%AF%B8%EC%A7%80%20%EB%B9%8C%EB%8D%94%20%EC%A2%85%EB%A5%98%EC%99%80%20%EC%84%A0%ED%83%9D.md) — buildah 와 다른 빌더 중 무엇을 고를지
- [buildctl·buildkitd 참조 시트](buildkit.md) — BuildKit 으로 같은 이미지를 빌드할 때
- [podman 참조 시트](../../../../08_cloud/docs/cmd/container/podman.md) — 같은 저장소의 이미지를 실행하고 관리할 때
- [docker 참조 시트](../../../../08_cloud/docs/cmd/container/docker.md) — tar 로 내보낸 이미지를 docker 로 불러올 때



## 참고 자료

> 검증 환경과 근거 자료, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04.1 LTS(aarch64) — 2026-11-23 실측
- 도구 버전: buildah 1.42.1(`1.42.1+ds1-2build1`), podman 5.7.0, docker 29.1.3
- [buildah-build(1) v1.42.1](https://github.com/podman-container-tools/buildah/blob/v1.42.1/docs/buildah-build.1.md)
- [buildah v1.46.1 릴리스](https://github.com/podman-container-tools/buildah/releases/tag/v1.46.1)

[^env]: `buildah --version` 출력 "buildah version 1.42.1 (image-spec 1.1.1, runtime-spec 1.2.1)" 와 `dpkg -l buildah` 의 `1.42.1+ds1-2build1` 은 이 시트의 실측입니다. 가장 새 버전은 GitHub 릴리스 API 의 `tag_name` "v1.46.1" 과 `published_at` "2026-11-11T16:23:39Z" 입니다.
[^exit]: buildah 의 종료 코드 표는 `--help` 에 없습니다. 위 값은 `buildah rm no-such-container; echo $?` 와 `buildah build -f app/NoSuchFile app; echo $?` 가 낸 125, `RUN exit 3` 이 낸 3, 정상 실행의 0 이 이 시트의 실측입니다. buildah-commit(1) 은 "On error, 1 is returned" 라고 적어서 125 와 어긋나지만, 이 시트에서 commit 실패는 재현하지 않았습니다.
[^from]: buildah-from(1) — "Creates a new working container, either from scratch or using a specified image as a starting point." `-working-container` 이름은 이 시트의 실측입니다.
[^unshare]: buildah-unshare(1) — "Executing `buildah mount` fails for unprivileged users unless the user is running inside a `buildah unshare` session." buildah-mount(1) 의 "To be able to access the file system mounted, you might need to create the mount namespace separately as part of `buildah unshare`." 도 같은 말을 합니다.
[^push]: buildah-push(1) — "If no transport is specified, the `docker` (i.e., container registry) transport is used." `buildah push --help` 의 "Supported transports: containers-storage,dir,docker,docker-archive,docker-daemon,oci,oci-archive,sif".
[^tls]: buildah-push(1) — "Require HTTPS and verification of certificates when talking to container registries (defaults to true)." 오류 줄의 "http: server gave HTTP response to HTTPS client" 는 이 시트의 실측입니다.
[^layers]: buildah-build(1) — "Cache intermediate images during the build process (Default is `false`)." `buildah build --help` 의 `--layers` 줄에는 기본값 표기가 없고 "Use BUILDAH_LAYERS environment variable to override." 만 있습니다.
[^isol]: buildah-build(1) — "Recognized types include *oci* (OCI-compatible runtime, the default), *rootless* (OCI-compatible runtime invoked using a modified configuration, with *--no-new-keyring* added to its *create* invocation, reusing the host's network and UTS namespaces, and creating private IPC, PID, mount, and user namespaces; the default for unprivileged users), and *chroot* (an internal wrapper that leans more toward chroot(1) than container technology, reusing the host's control group, network, IPC, and PID namespaces, and creating private mount and UTS namespaces, and creating user namespaces only when they're required for ID mapping)." 같은 문서에는 `BUILDAH_ISOLATION` 환경 변수 설명이 있습니다. `buildah build --help` 의 기본값은 실행한 사용자에 따라 찍힙니다. root 로 돌리면 `--isolation` 이 (default "oci") 이고, 일반 사용자 `dev` 로 돌리면 (default "rootless") 입니다. `--format` 은 두 사용자 모두 (default "oci") 입니다. 문서의 "the default for unprivileged users" 와 맞습니다.
[^fmt]: buildah-build(1) — "Recognized formats include *oci* (OCI image-spec v1.0, the default) and *docker* (version 2, using schema format 2 for the manifest)." `buildah build --help` 도 `--format` 을 "(default "oci")" 로 적습니다. 경고 "HEALTHCHECK is not supported for OCI image format and will be ignored. Must use `docker` format" 은 이 시트의 실측입니다.
[^bud]: `buildah build --help` 의 "Aliases: build, build-using-dockerfile, bud" 와 buildah-build(1) 의 SYNOPSIS 두 줄 "**buildah build** [*options*] [*context*]", "**buildah bud** [*options*] [*context*]".
