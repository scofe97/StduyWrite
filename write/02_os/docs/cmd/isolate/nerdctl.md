---
title: "nerdctl 참조 시트"
tags: ["linux", "command", "isolate", "containerd", "nerdctl", "container"]
status: draft
source:
  - "nerdctl v2.4.2 `nerdctl --help` 와 하위 명령 `--help` 원문 (OrbStack Ubuntu 26.04 VM 실측)"
  - "https://github.com/containerd/nerdctl/releases/tag/v2.4.2"
  - "https://github.com/containernetworking/plugins/releases/tag/v1.10.0"
related:
  - "../README.md"
  - "../process/ps.md"
  - "../net/ss.md"
updated: "2026-11-20"
---

# nerdctl 참조 시트

---

> containerd 가 관리하는 컨테이너와 이미지를 docker 와 같은 문법으로 보고, 실행하고, namespace 를 가르고, tar 로 반입한 이미지를 저장소에 올리는 `nerdctl` 을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `nerdctl` 은 containerd 를 docker 와 같은 문법으로 다루는 CLI 입니다.

containerd 는 이미지를 받고 컨테이너를 실제로 띄우는 런타임이고, docker 는 그 앞에 `dockerd` 를 한 겹 더 둡니다. nerdctl 은 그 겹을 건너뛰고 containerd 에 바로 말을 겁니다.

```bash
# 세 CLI 가 containerd 에 닿는 길
# docker   docker  → dockerd → containerd
# nerdctl  nerdctl →            containerd
# crictl   crictl  → CRI     → containerd 또는 CRI-O
# ctr      containerd 에 딸린 저수준 CLI. 디버깅용이라 일상 작업에는 nerdctl 을 씁니다
```

CRI(Container Runtime Interface)는 Kubernetes 가 컨테이너 런타임에 말을 거는 규약입니다. crictl 은 Kubernetes 노드에서 쓰고, nerdctl 은 containerd 하나만 있으면 됩니다.

nerdctl 은 공식 GitHub 릴리스 바이너리 한 개(`/usr/local/bin/nerdctl`)입니다. 컨테이너 네트워크용 CNI 플러그인은 `/opt/cni/bin` 에 따로 받아 두며, 이 VM 에는 없어서 같이 받았습니다.

이 시트의 출력은 OrbStack Ubuntu 26.04.1 VM(aarch64)에서 받았습니다. 도구 버전은 nerdctl v2.4.2, containerd 2.2.2, runc 1.4.0, docker 29.1.3 입니다. 모든 명령은 root 셸(`sudo bash`)에서 돌렸습니다.[^env]



## 핵심 문법

> 명령은 docker 와 같은 이름으로 대상을 고르고, 어느 containerd namespace 를 볼지는 앞에 붙는 전역 옵션이 정합니다.

```bash
# 호출 형태
# nerdctl --help 의 Usage 줄
nerdctl [command]

# 전역 옵션을 앞에 붙이고 하위 명령을 부른다 (namespace 로 docker 컨테이너 찾기)
nerdctl [global flags] <command> [flags] [args...]

# 컨테이너와 이미지를 본다 (컨테이너와 이미지 보기)
nerdctl ps [-a]
nerdctl images

# 컨테이너를 띄우고 로그를 보고 들어간다 (실행·로그·들어가기)
nerdctl run -d --name NAME IMAGE
nerdctl logs [--tail N] CONTAINER
nerdctl exec [-it] CONTAINER COMMAND [ARG...]

# 다른 namespace 를 본다 (namespace 로 docker 컨테이너 찾기)
nerdctl -n NAMESPACE ps

# tar 로 옮긴 이미지를 저장소에 올린다 (tar 이미지를 저장소에 올리기)
nerdctl save -o FILE IMAGE
nerdctl load -i FILE
nerdctl tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
nerdctl push NAME[:TAG]

# 저장소에 로그인한다 (저장소 로그인)
nerdctl login [SERVER]
```

### 전역 옵션

```bash
# nerdctl --help 에서 찾은 전역 옵션 둘. 앞 두 줄은 이름·별칭·기본값
# --namespace, -n   기본값 default   containerd namespace. "moby" 는 Docker, "k8s.io" 는 Kubernetes
# --address, -a, -H, --host   기본값 /run/containerd/containerd.sock   containerd 소켓 주소
```



## 종료 코드

> 성공하면 0이고, 실패하면 `level=fatal` 로그 한 줄을 찍고 1로 끝납니다.[^exit]

```bash
# 0  명령이 성공했다
# 1  없는 컨테이너·권한 부족·push 거부처럼 실패했다
nerdctl ps; echo $?
```

```bash
CONTAINER ID    IMAGE    COMMAND    CREATED    STATUS    PORTS    NAMES
0
```

```bash
# 없는 컨테이너 이름을 주면 fatal 한 줄과 1이 나온다
nerdctl logs dk; echo $?
```

```bash
time="2026-11-20T13:12:41+09:00" level=fatal msg="no such container dk"
1
```



## 유스케이스

### 실습 준비

> 아래 블록을 차례로 붙여 넣으면 nerdctl 설치와 이 시트의 예가 쓰는 이미지·컨테이너가 모두 생기며, 실행 환경은 root 셸입니다.

```bash
# nerdctl 바이너리를 받아 푼다 (VM 이 aarch64 라서 arm64 파일이다. x86_64 면 amd64 로 바꾼다)
curl -fsSL -o nerdctl.tgz \
  https://github.com/containerd/nerdctl/releases/download/v2.4.2/nerdctl-2.4.2-linux-arm64.tar.gz
tar -C /usr/local/bin -xzf nerdctl.tgz nerdctl

# 컨테이너 네트워크용 CNI 플러그인을 받아 푼다
curl -fsSL -o cni.tgz \
  https://github.com/containernetworking/plugins/releases/download/v1.10.0/cni-plugins-linux-arm64-v1.10.0.tgz
mkdir -p /opt/cni/bin
tar -C /opt/cni/bin -xzf cni.tgz

# 설치된 버전과 CNI 플러그인 앞쪽 파일을 본다
nerdctl --version    # nerdctl version 2.4.2
ls /opt/cni/bin | head -n 5
```

```bash
LICENSE
README.md
bandwidth
bridge
dhcp
```

```bash
# 이미지를 받고(-q 는 진행 출력을 줄인다) 컨테이너 둘을 만든다
nerdctl pull -q nginx:alpine
nerdctl pull -q alpine:3.20
nerdctl run -d --name web nginx:alpine    # 8c993b973db6e3c6f27c78ac06e6fe4ed51ec392be73f05d8a2c416d98eeb19a
nerdctl run --name old alpine:3.20 echo done    # done
```

### 컨테이너와 이미지 보기

> `ps` 로 컨테이너를, `images` 로 이미지를 보고, `container ls`·`image ls` 가 같은 목록을 내는 별칭임을 확인합니다.

```bash
# 돌고 있는 컨테이너만 본다
nerdctl ps
```

```bash
CONTAINER ID    IMAGE                             COMMAND                   CREATED         STATUS    PORTS    NAMES
8c993b973db6    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    1 second ago    Up                 web
```

```bash
# 멈춘 컨테이너까지 본다
#   -a   멈춘 것까지 모두 보여 준다(기본은 돌고 있는 것만)
nerdctl ps -a
```

```bash
CONTAINER ID    IMAGE                             COMMAND                   CREATED                   STATUS                               PORTS    NAMES
1abdba9fec5f    docker.io/library/alpine:3.20     "echo done"               Less than a second ago    Exited (0) Less than a second ago             old
8c993b973db6    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    1 second ago              Up                                            web
```

```bash
# 이미지를 본다
nerdctl images
```

```bash
IMAGE           ID              DISK USAGE    CONTENT SIZE    EXTRA
alpine:3.20     d9e853e87e55    14.6MB        4.09MB          U
nginx:alpine    fb4658584bd9    94.4MB        26.3MB          U
```

```bash
# -q 는 ID 만 찍는다. container ls 는 ps, image ls 는 images 와 같은 결과를 낸다
nerdctl ps -q    # 8c993b973db6
nerdctl container ls -q    # 8c993b973db6
nerdctl images -q
nerdctl image ls -q
```

```bash
d9e853e87e55
fb4658584bd9
```

두 `images -q` 는 같은 두 줄을 찍습니다.

### 실행·로그·들어가기

> 컨테이너를 띄우고, 끝 몇 줄의 로그를 보고, 안에서 명령을 하나 돌린 뒤 멈추고 지웁니다.

```bash
# 백그라운드로 띄운다
#   -d       백그라운드로 돌리고 컨테이너 ID 를 찍는다
#   --name   컨테이너에 이름을 붙인다
nerdctl run -d --name demo nginx:alpine    # 2a4d66696ada221c4a6f4b5639a1d0e9f6f42499b895be026bc7b75ca3d51173
```

```bash
# 끝 3줄만 본다
#   --tail   뒤에서 몇 줄만 보여 준다
nerdctl logs --tail 3 demo
```

```bash
2026/11/20 04:13:51 [notice] 1#1: start worker process 35
2026/11/20 04:13:51 [notice] 1#1: start worker process 36
2026/11/20 04:13:51 [notice] 1#1: start worker process 37
```

```bash
# 안에서 명령을 하나 돌리고 나온다
nerdctl exec demo sh -c 'cat /etc/alpine-release; id -u'
```

```bash
3.24.4
0
```

`exec -it CONTAINER sh` 로 셸에 들어가는 꼴은 터미널이 있어야 해서 이 시트의 자동 실측에서는 돌리지 못했습니다.

```bash
# 멈추고 지운다
nerdctl stop demo    # demo
nerdctl rm demo    # demo
```

### namespace 로 docker 컨테이너 찾기

> docker 로 띄운 컨테이너는 containerd 의 `moby` namespace 에 있어서, 기본 namespace 만 보는 `nerdctl ps` 에는 나오지 않습니다.

```bash
# 같은 VM 의 docker 로 컨테이너를 하나 띄운다
docker pull -q nginx:alpine    # docker.io/library/nginx:alpine
docker run -d --name dk nginx:alpine    # 1a66ccdf815ccf99783ae1f8d2dfe82b5ca12b4e85311c9a45456f731ff23cf6

# docker, 기본 namespace, moby namespace 가 각각 보는 컨테이너 ID
docker ps -q    # 1a66ccdf815c
nerdctl ps -q    # 8c993b973db6
nerdctl -n moby ps -q    # 1a66ccdf815c
```

앞의 `docker` 와 `-n moby` 가 같은 ID 를 보고, 기본 `nerdctl ps` 는 앞서 띄운 `web` 의 ID 만 봅니다.

```bash
# containerd 에 있는 namespace 와 각각의 컨테이너·이미지 수를 본다
nerdctl namespace ls
```

```bash
NAME       CONTAINERS    IMAGES    VOLUMES    LABELS
default    2             2         0              
moby       1             2         0              
```

```bash
# Kubernetes 노드의 컨테이너는 k8s.io namespace 에 있다
nerdctl -n k8s.io ps
```

```bash
CONTAINER ID    IMAGE    COMMAND    CREATED    STATUS    PORTS    NAMES
```

이 VM 에는 Kubernetes 가 없어 k8s.io 는 빈 목록입니다. kubelet 이 만든 컨테이너를 보는 것은 돌리지 못했습니다.[^ns]

### tar 이미지를 저장소에 올리기

> 인터넷이 되는 쪽에서 `save` 로 만든 tar 를 폐쇄망 서버로 옮기면, 그 서버에서 `load` → `tag` → `push` 로 사내 저장소에 올릴 수 있습니다.

```bash
# 저장소 역할을 할 레지스트리 이미지를 받는다
nerdctl pull -q registry:2

# 레지스트리를 localhost:5000 에 띄운다
#   -p   호스트 포트를 컨테이너 포트로 연결한다(호스트:컨테이너)
nerdctl run -d \
  --name reg \
  -p 5000:5000 \
  registry:2    # 78544af4ac0e6ad0fc266ad455043951e4cf46d1aba43a3f7a8b1c4015ecd7dd
```

```bash
# 인터넷 쪽: 이미지를 tar 로 저장한다
#   -o   표준출력 대신 이 파일에 쓴다
nerdctl save -q -o nginx.tar nginx:alpine
ls -lh nginx.tar    # -rw-r--r--+ 1 root root 26M Nov 20 13:14 nginx.tar

# 폐쇄망 쪽을 흉내 내려고 이미지와 그 컨테이너를 지운다
nerdctl rm -f web    # web
nerdctl rmi nginx:alpine > /dev/null
nerdctl images
```

```bash
IMAGE          ID              DISK USAGE    CONTENT SIZE    EXTRA
alpine:3.20    d9e853e87e55    14.6MB        4.09MB          U
registry:2     a3d8aaa63ed8    37.7MB        9.47MB          U
```

```bash
# 폐쇄망 쪽: tar 를 읽어 들인다
#   -i   표준입력 대신 이 tar 파일을 읽는다
nerdctl load -q -i nginx.tar > /dev/null
nerdctl images
```

```bash
IMAGE           ID              DISK USAGE    CONTENT SIZE    EXTRA
alpine:3.20     d9e853e87e55    14.6MB        4.09MB          U
nginx:alpine    fb4658584bd9    94.4MB        26.3MB          
registry:2      a3d8aaa63ed8    37.7MB        9.47MB          U
```

`load -q` 도 터미널이 아니면 진행 줄을 찍어서 이 시트에서는 출력을 버렸습니다. 이미지는 목록에 다시 나옵니다.

```bash
# 저장소 주소를 앞에 붙인 이름을 달고 올린다 (줄은 120자에서 잘랐다)
nerdctl tag nginx:alpine localhost:5000/team/nginx:1.0
nerdctl push -q localhost:5000/team/nginx:1.0 2>&1 | cut -c1-120
```

```bash
time="2026-11-20T13:14:11+09:00" level=info msg="pushing as a reduced-platform image (application/vnd.oci.image.index.v1
localhost:5000/team/nginx:1.0
```

```bash
# 저장소 쪽에서 올라온 것을 확인한다
curl -s localhost:5000/v2/_catalog    # {"repositories":["team/nginx"]}
curl -s localhost:5000/v2/team/nginx/tags/list    # {"name":"team/nginx","tags":["1.0"]}
```

### 저장소가 살아 있는지 확인

> 저장소 컨테이너가 떠 있는지는 `ps` 로, 저장소가 요청에 답하는지는 `/v2/` 주소로 확인합니다.

```bash
# 저장소 컨테이너가 떠 있는지 본다
nerdctl ps | grep reg
```

```bash
78544af4ac0e    docker.io/library/registry:2    "/entrypoint.sh /etc…"    2 seconds ago    Up        0.0.0.0:5000->5000/tcp    reg
```

```bash
# Docker registry v2 API 의 루트 주소. 빈 JSON 과 200 이 오면 저장소가 답하는 것이다
curl -s localhost:5000/v2/    # {}
curl -s -o /dev/null -w '%{http_code}\n' localhost:5000/v2/    # 200
```

Nexus 3 의 상태 API(`/service/rest/v1/status`)는 이 VM 에 Nexus 를 설치하지 않아 돌리지 못했습니다.

### 저장소 로그인

> `login` 으로 저장소에 인증 정보를 저장하고 `logout` 으로 지웁니다.

```bash
# 비밀번호는 표준입력으로 준다
#   -u               사용자 이름
#   --password-stdin 표준입력에서 비밀번호를 읽는다
echo pass | nerdctl login -u user --password-stdin localhost:5000
```

```bash
WARNING! Your credentials are stored unencrypted in '/root/.docker/config.json'.
Configure a credential helper to remove this warning. See
https://docs.docker.com/go/credential-store/

Login Succeeded
```

```bash
# 저장한 인증 정보를 지운다
nerdctl logout localhost:5000
```

이 레지스트리는 인증을 걸지 않아서 아무 사용자·비밀번호로도 `Login Succeeded` 가 나옵니다. 인증이 걸린 저장소에서의 로그인과 거부는 돌리지 못했습니다.

### 실습 정리

> 주의사항의 예가 위 컨테이너와 이미지를 이어 쓰므로 그 예까지 돌린 뒤에 실행합니다.

```bash
# 컨테이너·볼륨·이미지를 이름을 찍어 지운다
nerdctl rm -fv reg old
docker rm -fv dk
docker rmi nginx:alpine > /dev/null
nerdctl rmi -f \
  localhost:5000/team/nginx:1.0 \
  registry.example.com:5000/team/nginx:1.0 \
  nginx:alpine \
  registry:2 \
  alpine:3.20 > /dev/null

# 주의사항의 실측에서 넣은 hosts 줄과 임시 파일을 지운다
sed -i '/registry.example.com/d' /etc/hosts
rm -f nginx.tar nerdctl.tgz cni.tgz
```



## 주의사항과 동작 원리

### docker 와 nerdctl 의 이미지 분리

> docker 로 받은 이미지는 `moby` namespace 에 있어서 기본 `nerdctl images` 에는 나오지 않으며, `-n moby` 를 붙여야 보입니다.

```bash
# docker 가 가진 hello-world 이미지를 세 곳에서 센다
docker images --format '{{.Repository}}' | grep -c hello-world    # 1
nerdctl images --format '{{.Repository}}' | grep -c hello-world    # 0
nerdctl -n moby images --format '{{.Repository}}' | grep -c hello-world    # 1
```

이 VM 의 docker 는 이미지와 컨테이너를 모두 containerd 의 `moby` namespace 에 둡니다. 기본 namespace 에서 `0` 이 나온 것은 이미지가 없어서가 아니라 보는 namespace 가 달라서입니다.

### HTTP 저장소 push 거부

> nerdctl 은 저장소에 먼저 HTTPS 로 말을 걸어서, HTTP 만 쓰는 저장소에는 `--insecure-registry` 를 붙여야 올라갑니다.

```bash
# registry.example.com 은 실제 주소가 아니라서 VM 의 hosts 에 127.0.0.1 로 건다
echo '127.0.0.1 registry.example.com' >> /etc/hosts
nerdctl tag nginx:alpine registry.example.com:5000/team/nginx:1.0

# HTTP 저장소에 그냥 올린다 (줄은 120자에서 잘랐다)
nerdctl push -q registry.example.com:5000/team/nginx:1.0 2>&1 | cut -c1-120
```

```bash
time="2026-11-20T13:14:12+09:00" level=info msg="pushing as a reduced-platform image (application/vnd.oci.image.index.v1
time="2026-11-20T13:14:12+09:00" level=error msg="server \"registry.example.com:5000\" does not seem to support HTTPS" e
time="2026-11-20T13:14:12+09:00" level=info msg="Hint: you may want to try --insecure-registry to allow plain HTTP (if y
time="2026-11-20T13:14:12+09:00" level=fatal msg="failed to do request: Head \"https://registry.example.com:5000/v2/team
```

```bash
# 평문 HTTP 를 허용하고 올린다
nerdctl push -q \
  --insecure-registry \
  registry.example.com:5000/team/nginx:1.0 2>&1 | cut -c1-120
```

```bash
time="2026-11-20T13:14:12+09:00" level=info msg="pushing as a reduced-platform image (application/vnd.oci.image.index.v1
time="2026-11-20T13:14:12+09:00" level=warning msg="skipping verifying HTTPS certs for \"registry.example.com:5000\""
time="2026-11-20T13:14:12+09:00" level=warning msg="server \"registry.example.com:5000\" does not seem to support HTTPS,
registry.example.com:5000/team/nginx:1.0
```

같은 HTTP 저장소라도 `localhost:5000` 은 앞의 「tar 이미지를 저장소에 올리기」에서 플래그 없이 올라갔습니다. 다른 호스트 이름으로 건 HTTP 저장소에는 플래그가 필요했습니다.[^http]

### 앞뒤에서 뜻이 다른 -n

> `nerdctl` 바로 뒤의 `-n` 은 namespace 이고 `logs` 뒤의 `-n` 은 줄 수라서, 위치를 바꾸면 전혀 다른 일이 됩니다.

```bash
# logs 뒤의 -n 1 은 끝 1줄 (줄은 80자에서 잘랐다)
nerdctl logs -n 1 reg | cut -c1-80
```

```bash
10.4.0.1 - - [20/Nov/2026:04:14:12 +0000] "HEAD /v2/team/nginx/manifests/1.0 HTT
```

```bash
# 앞의 -n k8s.io 는 namespace 라서 그 안에 reg 가 없다고 답한다
nerdctl -n k8s.io logs reg
```

```bash
time="2026-11-20T13:14:12+09:00" level=fatal msg="no such container reg"
```

### moby 컨테이너의 빈 이름과 로그

> `-n moby` 로 docker 컨테이너가 보여도 NAMES 열은 비고, `nerdctl logs` 는 그 컨테이너를 찾지 못합니다.

```bash
# docker 로 띄운 컨테이너를 moby namespace 에서 본다
nerdctl -n moby ps
```

```bash
CONTAINER ID    IMAGE                             COMMAND                   CREATED           STATUS    PORTS    NAMES
1a66ccdf815c    docker.io/library/nginx:alpine    "/docker-entrypoint.…"    15 seconds ago    Up                 
```

```bash
# 이름으로도 못 찾는다 (줄은 130자에서 잘랐다)
nerdctl -n moby logs dk 2>&1 | cut -c1-130
```

```bash
time="2026-11-20T13:14:12+09:00" level=warning msg="Currently, `nerdctl logs` only supports containers created with `nerdctl run -
time="2026-11-20T13:14:12+09:00" level=fatal msg="no such container dk"
```

docker 로 만든 컨테이너의 이름과 로그는 nerdctl 에서 읽히지 않았으니 `docker ps`·`docker logs` 로 봅니다.[^logs]

### 사용 중인 이미지의 rmi 거부

> 컨테이너가 쓰는 이미지는 `rmi` 가 거부하므로 컨테이너를 먼저 지워야 합니다.

```bash
# nginx:alpine 을 쓰는 컨테이너를 띄우고 이미지를 지워 본다 (줄은 150자에서 잘랐다)
nerdctl run -d --name tmp nginx:alpine    # 393e9c720f46673a6fb8a09ad0a0f419c322eda8d8212eda67af5a53fb99ef5e
nerdctl rmi nginx:alpine 2>&1 | cut -c1-150
```

```bash
time="2026-11-20T13:14:13+09:00" level=fatal msg="1 errors:\nconflict: unable to delete nginx:alpine (cannot be forced) - image is being used by runni
```

```bash
# 컨테이너를 먼저 지우면 이미지도 지울 수 있다
nerdctl rm -f tmp    # tmp
```

### 플랫폼 하나만 올라간 이미지

> 여러 CPU 용 이미지를 받아도 이 VM 은 arm64 만 받아 저장해서, 올린 이미지에는 arm64 만 들어 있어 amd64 로 받으면 거부됩니다.

```bash
# 올라간 이미지 index 에 들어 있는 플랫폼
curl -s -H 'Accept: application/vnd.oci.image.index.v1+json' \
  localhost:5000/v2/team/nginx/manifests/1.0 \
  | grep -o '"architecture": *"[a-z0-9]*"'    # "architecture":"arm64"

# amd64 로 받아 본다 (줄은 120자에서 잘랐다)
nerdctl pull -q --platform amd64 localhost:5000/team/nginx:1.0 2>&1 | cut -c1-120
```

```bash
time="2026-11-20T13:14:13+09:00" level=fatal msg="no match for platform in manifest sha256:06f4baf572ade5151cbe79b218654
```

앞의 push 가 `pushing as a reduced-platform image` 라고 알려 준 것이 이 뜻입니다. `--help` 에는 `--all-platforms` 가 `pull`·`save`·`load`·`push` 에 있다고 나옵니다. 그 흐름은 돌리지 못했습니다.[^platform]

### 일반 사용자의 containerd 접근 실패

> 일반 사용자가 `nerdctl ps` 를 치면 root 의 containerd 대신 rootless containerd 를 찾다가 실패합니다.

```bash
# 일반 사용자 셸에서 (줄은 150자에서 잘랐다)
nerdctl ps 2>&1 | cut -c1-150
```

```bash
time="2026-11-20T13:14:13+09:00" level=fatal msg="rootless containerd not running? (hint: use `containerd-rootless-setuptool.sh install` to start root
```

이 시트는 root 셸에서 실측했습니다. rootless containerd 를 설치해 일반 사용자로 쓰는 방법은 돌리지 못했습니다.[^root]



## 관련 문서

> 같은 폴더 지도와, 컨테이너 안팎의 프로세스·포트를 이어서 볼 시트입니다.

- [리눅스 명령어 시트](../README.md) — 다른 명령 시트 목록
- [ps 참조 시트](../process/ps.md) — 컨테이너 프로세스가 호스트에서 어떻게 보이는지 확인할 때
- [ss 참조 시트](../net/ss.md) — `-p 5000:5000` 으로 연 포트가 호스트에서 듣고 있는지 확인할 때



## 참고 자료

> 검증 환경과 근거 자료, 각주 정의입니다.

- 검증 환경: OrbStack Linux VM, Ubuntu 26.04.1 LTS(aarch64) — 2026-11-20 실측
- 도구 버전: nerdctl v2.4.2, containerd 2.2.2, runc 1.4.0-0ubuntu1, docker 29.1.3, CNI plugins v1.10.0
- [nerdctl v2.4.2 릴리스](https://github.com/containerd/nerdctl/releases/tag/v2.4.2)
- [CNI plugins v1.10.0 릴리스](https://github.com/containernetworking/plugins/releases/tag/v1.10.0)

[^env]: `nerdctl --help` 첫 줄 "nerdctl is a command line interface for containerd", `nerdctl --version` 출력 "nerdctl version 2.4.2"(이 시트의 실측). 바이너리와 CNI 플러그인은 위 두 릴리스 페이지의 `nerdctl-2.4.2-linux-arm64.tar.gz` 와 `cni-plugins-linux-arm64-v1.10.0.tgz` 입니다.
[^exit]: nerdctl 의 종료 코드 표는 `--help` 에 없습니다. 위 값은 `nerdctl logs dk; echo $?` 로 읽은 1과 `nerdctl ps; echo $?` 로 읽은 0, 그리고 주의사항에서 `rmi`·`push`·일반 사용자 실행이 낸 `level=fatal` 줄이 이 시트의 실측입니다.
[^ns]: `nerdctl --help` — "--namespace string  containerd namespace, such as "moby" for Docker, "k8s.io" for Kubernetes [$CONTAINERD_NAMESPACE] (aliases: -n) (default "default")". `nerdctl namespace --help` — "Unrelated to Linux namespaces and Kubernetes namespaces".
[^http]: `push` 가 HTTPS 시도 후 낸 로그는 `server "registry.example.com:5000" does not seem to support HTTPS` 와 `Hint: you may want to try --insecure-registry to allow plain HTTP (if you are in a trusted network)` 이고, 이는 이 시트의 실측입니다. `localhost:5000` 이 플래그 없이 올라간 것도 이 VM 의 실측이며, 그 이유를 밝힌 문서는 찾아 대조하지 않았습니다.
[^logs]: `nerdctl -n moby logs dk` 가 낸 경고 "Currently, `nerdctl logs` only supports containers created with `nerdctl run -d` or CRI" 와 `-n moby ps` 의 빈 NAMES 열은 이 시트의 실측입니다.
[^platform]: `nerdctl push --help` — "--all-platforms  Push content for all platforms", "--platform strings  Push content for a specific platform". `nerdctl load --help`·`save --help`·`pull` 에도 같은 이름의 플래그가 있습니다. `pull --platform amd64` 가 낸 "no match for platform in manifest" 는 이 시트의 실측입니다.
[^root]: 일반 사용자의 `nerdctl ps` 오류 "rootless containerd not running? (hint: use `containerd-rootless-setuptool.sh install` to start rootless containerd)" 는 이 시트의 실측입니다.
