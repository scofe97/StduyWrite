---
title: "podman 참조 시트"
tags: ["cloud", "command", "container", "podman", "rootless"]
status: draft
source:
  - "podman 5.7.0 (5.7.0+ds2-3build1) podman --help 와 하위 명령 --help·man 페이지 원문 (OrbStack Ubuntu 26.04 VM 실측)"
  - "https://docs.podman.io/en/v5.7.0/markdown/podman.1.html"
  - "https://docs.podman.io/en/v5.7.0/markdown/podman-systemd.unit.5.html"
  - "https://docs.podman.io/en/v5.7.0/markdown/podman-generate-systemd.1.html"
  - "https://docs.podman.io/en/v5.7.0/markdown/podman-build.1.html"
  - "https://docs.podman.io/en/v5.7.0/markdown/podman-system-service.1.html"
  - "https://github.com/podman-container-tools/podman/releases/tag/v6.2.0"
related:
  - ../README.md
  - ./docker.md
  - ../../../../02_os/docs/cmd/isolate/nerdctl.md
  - ../../../../07_devops/docs/artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md
  - ../../../../07_devops/docs/cmd/image/buildah.md
updated: "2026-11-23"
---

# podman 참조 시트

---

> 백그라운드 데몬 없이 컨테이너와 pod 를 띄우고 일반 사용자 권한으로도 돌리는 `podman` 명령을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `podman` 은 데몬 없이 CLI 가 직접 OCI 런타임을 호출해 컨테이너와 pod 를 관리하는 도구입니다.

`docker` 와 하위 명령 꼴이 같아 실행·조회·로그 확인 명령은 대부분 그대로 씁니다. 다만 중앙 데몬 대신 사용자마다 별도 저장소를 쓰고 일반 사용자 권한으로 컨테이너를 띄울 수 있습니다.

```bash
# docker 와 podman 이 각각 컨테이너에 닿는 길
# docker   docker → dockerd(root 데몬) → containerd → runc
# podman   podman → conmon + runc (데몬 없음, root 또는 일반 사용자)
```

이 시트의 출력은 OrbStack Ubuntu 26.04.1 LTS VM(aarch64)에서 실측했습니다. 실측 버전은 `podman 5.7.0`(`5.7.0+ds2-3build1`)입니다. 공식 GitHub 릴리스 기준 가장 새 버전은 `v6.2.0`(2026-11-10)입니다.[^env]



## 핵심 문법

> `docker` 와 같은 문법으로 대상을 고르지만 백그라운드 데몬이 없으므로 사용자·pod·Quadlet 단위를 구분해 써야 합니다. 아래 꼴은 `NAME`·`POD`·`FILE` 같은 자리표시자를 바꿔 쓰는 꼴이라 그대로 실행하지 않습니다.

```bash
# 호출 형태 (podman --help 의 Usage 줄)
podman [options] [command]

# 컨테이너를 띄우고 보고 들어간다 (컨테이너 실행·조회·로그·접속·삭제)
podman run -d --name NAME -p HOST:CONTAINER IMAGE
podman ps [-a]
podman logs [--tail N] CONTAINER
podman exec CONTAINER COMMAND [ARG...]
podman stop [-t SEC] CONTAINER
podman rm CONTAINER

# 일반 사용자의 user namespace 안에서 명령을 돌린다 (일반 사용자 실행과 UID 매핑 확인)
podman unshare COMMAND [ARG...]

# 사용자별 저장소 경로와 이미지 목록을 확인한다 (사용자별 이미지·컨테이너 저장소 분리)
podman info --format '{{.Store.GraphRoot}}'
podman images

# 여러 컨테이너를 한 네트워크·IPC 네임스페이스로 묶는다 (Pod 생성과 컨테이너 간 localhost 통신)
podman pod create --name POD -p HOST:CONTAINER
podman run -d --pod POD --name NAME IMAGE
podman pod ps

# pod 를 Kubernetes YAML 로 내보내고 다시 띄운다 (Kubernetes YAML 생성과 재실행)
podman kube generate POD > FILE.yaml
podman kube play FILE.yaml
podman kube play --down FILE.yaml

# Docker 호환 소켓 API 를 연다 (Docker 소켓과 system service)
podman system service [--time=SEC] URI
```

### 주요 설정과 저장소 경로

```bash
# 실행 주체별로 갈리는 저장소·레지스트리·Quadlet 경로
# root 저장소       /var/lib/containers/storage      root 이미지·컨테이너 저장 위치
# 일반 사용자 저장소 ~/.local/share/containers/storage  사용자별 이미지·컨테이너 저장 위치
# 레지스트리 설정   /etc/containers/registries.conf    unqualified-search-registries 정의
# short-name 별칭   /etc/containers/registries.conf.d/shortnames.conf  짧은 이름과 전체 주소 매핑
# root Quadlet      /etc/containers/systemd/           시스템 systemd 유닛 생성 원본
# 사용자 Quadlet    ~/.config/containers/systemd/      사용자 systemd 유닛 생성 원본
```



## 종료 코드

> 성공하면 0 이고, podman 자체 오류·실행 불가·명령 없음은 chroot 관례를 따라 125·126·127 로 나뉘며, 그 밖의 실패는 컨테이너 안 명령의 종료 코드를 그대로 돌려줍니다.[^exit]

```bash
# 0    명령이 성공했다
podman run -q --rm docker.io/library/alpine:3.20 true; echo $?    # 0

# 125  잘못된 플래그처럼 podman 자체에서 오류가 났다
podman run --nosuchflag docker.io/library/alpine:3.20 2>&1; echo $?
```

```bash
# 결과 (125)
Error: unknown flag: --nosuchflag
See 'podman run --help'
125
```

```bash
# 126  컨테이너 안의 명령을 실행할 수 없다 (디렉터리 지정·권한 부족)
podman run -q --rm docker.io/library/alpine:3.20 /etc 2>&1; echo $?
```

```bash
# 결과 (126)
Error: OCI runtime error: runc: runc create failed: unable to start container process: error during container init: exec: "/etc": is a directory
126
```

```bash
# 127  컨테이너 안에서 실행할 명령을 찾지 못했다
podman run -q --rm docker.io/library/alpine:3.20 nosuchcmd 2>&1; echo $?
```

```bash
# 결과 (127)
Error: runc: runc create failed: unable to start container process: error during container init: exec: "nosuchcmd": executable file not found in $PATH: OCI runtime attempted to invoke a command that was not found
127
```

```bash
# 그 외  컨테이너 안 명령이 낸 종료 코드를 그대로 반환한다
podman run -q --rm docker.io/library/alpine:3.20 sh -c 'exit 3'; echo $?    # 3
```



## 유스케이스

> 아래 예는 `root` 와 일반 사용자 `dev` 를 오가며 실행하므로, 실행 계정이 섞이지 않게 주의하며 위에서 아래로 돌립니다.

### 실습 준비

> apt 로 `podman` 을 설치하고 일반 사용자 `dev` 와 작업 폴더·실습 이미지를 준비합니다.

```bash
# podman 패키지를 설치하고 버전을 확인한다 (컨테이너 실행·조회·로그·접속·삭제부터 여러 곳)
DEBIAN_FRONTEND=noninteractive apt-get install -y podman >/dev/null
podman --version
dpkg -l podman | grep '^ii'
```

```bash
# 결과
podman version 5.7.0
ii  podman         5.7.0+ds2-3build1 arm64        tool to manage containers and pods
```

```bash
# 일반 사용자 dev 를 만들고 UID 를 확인한다 (일반 사용자 실행과 UID 매핑 확인부터 여러 곳)
id dev >/dev/null 2>&1 || useradd -m -s /bin/bash dev
id dev
```

```bash
# 결과
uid=1000(dev) gid=1000(dev) groups=1000(dev)
```

```bash
# 작업 폴더를 만들고 이동한다 (Kubernetes YAML 생성과 재실행)
mkdir -p /root/sheet-podman && cd /root/sheet-podman && pwd    # /root/sheet-podman
```

```bash
# 실습에 쓸 작은 이미지를 받고 sp- 접두 태그를 붙인다 (컨테이너 실행·조회·로그·접속·삭제부터 여러 곳)
#   pull -q   받는 동안의 출력 정보를 숨긴다 (--quiet)
podman pull -q docker.io/library/alpine:3.20
podman pull -q docker.io/library/nginx:alpine
podman tag docker.io/library/alpine:3.20 localhost/sp-alpine:3.20
podman tag docker.io/library/nginx:alpine localhost/sp-nginx:alpine
```

```bash
# 결과
ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4
7db22640b020292f56a05da2a1ccdf7d44c1f321b71444ffca55192dae23f664
```

### 컨테이너 실행·조회·로그·접속·삭제

> `docker` 를 쓰던 방식 그대로 컨테이너를 띄우고 목록·로그·내부 명령 실행 뒤 멈추고 지웁니다.

```bash
# 백그라운드로 웹 컨테이너를 띄운다
#   -d       컨테이너를 백그라운드로 돌리고 ID 를 찍는다
#   --name   컨테이너 이름을 지정한다
#   -p       호스트 포트와 컨테이너 포트를 잇는다 (호스트:컨테이너)
podman run -d --name sp-web -p 8301:80 localhost/sp-nginx:alpine    # 1d72b08bd26b08b003ecb67ef5c559d3ffe4c569780e28823fa33ef518d6fc52

# 실행 중인 컨테이너 목록을 본다
podman ps
```

```bash
# 결과
CONTAINER ID  IMAGE                      COMMAND               CREATED                 STATUS                 PORTS                 NAMES
1d72b08bd26b  localhost/sp-nginx:alpine  nginx -g daemon o...  Less than a second ago  Up Less than a second  0.0.0.0:8301->80/tcp  sp-web
```

```bash
# 끝 3줄 로그를 읽는다
#   --tail   로그 끝에서 지정한 줄 수만 출력한다
podman logs --tail 3 sp-web
```

```bash
# 결과
2026/11/23 12:13:15 [notice] 1#1: start worker process 35
2026/11/23 12:13:15 [notice] 1#1: start worker process 36
2026/11/23 12:13:15 [notice] 1#1: start worker process 37
```

```bash
# 컨테이너 안에서 명령을 실행한다
podman exec sp-web sh -c 'cat /etc/alpine-release; id -u'
```

```bash
# 결과
3.24.4
0
```

```bash
# 컨테이너를 멈추고 지운다
#   stop -t   정지를 기다릴 초를 지정한다. 그 시간이 지나면 컨테이너를 강제로 죽인다
podman stop -t 1 sp-web && podman rm sp-web
```

```bash
# 결과
sp-web
sp-web
```

### 일반 사용자 실행과 UID 매핑 확인

> 일반 사용자 `dev` 가 띄운 컨테이너의 root 프로세스는 호스트에서 `dev` 자신으로, 그 밖의 컨테이너 UID 는 `/etc/subuid` 의 하위 UID 로 매핑됩니다.[^uidmap]

```bash
# dev 사용자에게 위임된 하위 UID·GID 범위를 본다
grep '^dev:' /etc/subuid /etc/subgid
```

```bash
# 결과
/etc/subuid:dev:100000:65536
/etc/subgid:dev:100000:65536
```

```bash
# dev 의 user namespace 안팎 UID 매핑 표를 본다
su - dev -c 'podman unshare cat /proc/self/uid_map'
```

```bash
# 결과 (컨테이너 안 UID, 호스트 UID, 개수)
         0       1000          1
         1     100000      65536
```

컨테이너 안 UID 0 은 호스트 UID 1000(`dev`)에 매핑되고, UID 1 부터는 호스트 100000 번대 65536 개에 매핑됩니다. 자세한 커널 조건은 [rootless 빌드의 조건](../../../../07_devops/docs/artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md) 에서 다룹니다.

```bash
# dev 권한으로 nginx 컨테이너를 띄운다
su - dev -c 'podman pull -q docker.io/library/nginx:alpine >/dev/null && podman run -d --name sp-dev-web -p 8302:80 docker.io/library/nginx:alpine'    # eac1e036db735aee4c2652ccc57d11747215eedcdfb20206f77784206f33e11d

# 호스트에서 conmon 과 nginx 프로세스의 소유자·UID 를 본다 (기동 직후에는 워커가 아직 없을 수 있어 1초 기다린다. 줄은 110자에서 잘랐다)
#   ps -eo   출력할 열을 사용자·UID·PID·명령으로 고른다
sleep 1 && ps -eo user:10,uid,pid,cmd | grep -E 'conmon|nginx' | grep -v grep | cut -c1-110
```

```bash
# 결과
dev         1000   41218 /usr/bin/conmon --api-version 1 -c eac1e036db735aee4c2652ccc57d11747215eedcdfb20206f7
dev         1000   41232 nginx: master process nginx -g daemon off;
100100     100100  41269 nginx: worker process
100100     100100  41270 nginx: worker process
100100     100100  41271 nginx: worker process
100100     100100  41272 nginx: worker process
100100     100100  41273 nginx: worker process
100100     100100  41274 nginx: worker process
100100     100100  41275 nginx: worker process
100100     100100  41276 nginx: worker process
```

컨테이너 안 root 로 도는 `nginx: master` 는 호스트의 `dev`(1000) 소유로 보입니다. 컨테이너 안 UID 101 로 도는 `nginx: worker` 는 호스트 UID 100100 으로 보입니다.

### 사용자별 이미지·컨테이너 저장소 분리

> `podman` 은 데몬을 공유하지 않고 실행 사용자마다 `GraphRoot` 와 `RunRoot` 를 따로 두므로 `root` 와 `dev` 의 이미지 목록이 서로 보이지 않습니다.

```bash
# root 와 dev 의 이미지 저장소(GraphRoot)와 실행 상태 경로(RunRoot)를 비교한다
podman info --format 'root: {{.Store.GraphRoot}} | {{.Store.RunRoot}}'
su - dev -c "podman info --format 'dev:  {{.Store.GraphRoot}} | {{.Store.RunRoot}}'"
```

```bash
# 결과
root: /var/lib/containers/storage | /run/containers/storage
dev:  /home/dev/.local/share/containers/storage | /run/user/1000/containers
```

```bash
# root 가 가진 이미지 목록을 본다
podman images --format '{{.Repository}}:{{.Tag}} {{.ID}}'
```

```bash
# 결과
localhost/sp-nginx:alpine 7db22640b020
docker.io/library/nginx:alpine 7db22640b020
localhost/sp-alpine:3.20 ab3fe4defd29
docker.io/library/alpine:3.20 ab3fe4defd29
```

```bash
# dev 가 가진 이미지 목록을 본다
su - dev -c "podman images --format '{{.Repository}}:{{.Tag}} {{.ID}}'"    # docker.io/library/nginx:alpine 7db22640b020
```

`root` 는 `/var/lib/containers/storage` 에서 4개 태그를 봅니다. 반면 `dev` 는 자기 홈 아래에서 `nginx:alpine` 한 개만 봅니다.

### 저장소 주소 없는 이름과 short-name

> 저장소 주소 없이 짧은 이름을 주면 `shortnames.conf` 별칭을 먼저 찾고, 별칭에도 없고 `unqualified-search-registries` 도 비어 있으면 실패합니다.[^shortname]

```bash
# 이 VM 의 레지스트리 검색 목록과 alpine 별칭 설정을 본다
grep -E 'unqualified-search-registries|^  "alpine"' /etc/containers/registries.conf /etc/containers/registries.conf.d/shortnames.conf
```

```bash
# 결과
/etc/containers/registries.conf:# unqualified-search-registries = ["example.com"]
/etc/containers/registries.conf.d/shortnames.conf:  "alpine" = "docker.io/library/alpine"
```

```bash
# 별칭에도 없는 짧은 이름 nginx 를 터미널 입력 없이 받아 본다
podman pull nginx 2>&1; echo "exit=$?"
```

```bash
# 결과
Error: short-name "nginx" did not resolve to an alias and no unqualified-search registries are defined in "/etc/containers/registries.conf"
exit=125
```

```bash
# shortnames.conf 에 별칭이 있는 alpine 은 주소 없이도 받아진다
podman pull -q alpine:3.20    # ab3fe4defd29ba6231229a4d41440ac8bde8218e85870e53876277faa24b35c4
```

이 VM 은 `unqualified-search-registries` 가 주석 처리돼 있고 `shortnames.conf` 에 `nginx` 별칭이 없습니다. 그래서 `nginx` 대신 `docker.io/library/nginx` 처럼 저장소 전체 주소를 주어야 받아집니다.

### Pod 생성과 컨테이너 간 localhost 통신

> 같은 pod 에 묶인 컨테이너들은 기본적으로 `ipc`·`net`·`uts` 네임스페이스를 함께 쓰므로 `localhost` 로 바로 통신합니다.[^pod-share]

```bash
# 포트를 연 빈 pod 를 만든다
podman pod create --name sp-pod -p 8303:80    # c8dcd1552d1d8204ffb297c33fc1b876b30ce049a8a371970aae921a71673373

# pod 안에 웹 서버와 클라이언트 컨테이너를 넣고 localhost 로 호출한다
#   --pod   기존 pod 의 네임스페이스를 공유해 컨테이너를 띄운다
podman run -d --pod sp-pod --name sp-pod-web localhost/sp-nginx:alpine
podman run --rm --pod sp-pod --name sp-pod-cli localhost/sp-alpine:3.20 wget -qO- http://localhost:80 | head -n 4
```

```bash
# 결과
c8dcd1552d1d8204ffb297c33fc1b876b30ce049a8a371970aae921a71673373
8a15953d409f77a94a9b20cc7908f31a69614539b1866e211cb780d0bdf9ac1b
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```

```bash
# pod 목록과 포함된 컨테이너 수(infra 컨테이너 포함)를 본다
podman pod ps
```

```bash
# 결과
POD ID        NAME        STATUS      CREATED                 INFRA ID      # OF CONTAINERS
c8dcd1552d1d  sp-pod      Running     Less than a second ago  d9a76cc88c4e  2
```

### Kubernetes YAML 생성과 재실행

> 실행 중인 pod 를 `kube generate` 로 Kubernetes YAML 파일로 내보내고, 그 파일로 pod 를 다시 띄우고 내립니다.[^kube]

```bash
# 실행 중인 sp-pod 를 Kubernetes YAML 로 저장하고 앞부분을 본다
podman kube generate sp-pod > /root/sheet-podman/sp-pod.yaml
head -n 28 /root/sheet-podman/sp-pod.yaml
```

```bash
# 결과
# Save the output of this file and use kubectl create -f to import
# it into Kubernetes.
#
# Created with podman-5.7.0
apiVersion: v1
kind: Pod
metadata:
  annotations:
    io.kubernetes.cri-o.SandboxID/sp-pod-web: d9a76cc88c4e35e37e8aea63b76c13844eead812fcf96cf7acca08f868f38417
  creationTimestamp: "2026-11-23T12:13:22Z"
  labels:
    app: sp-pod
  name: sp-pod
spec:
  containers:
  - args:
    - nginx
    - -g
    - daemon off;
    image: localhost/sp-nginx:alpine
    name: sp-pod-web
    ports:
    - containerPort: 80
      hostPort: 8303
```

```bash
# 기존 pod 를 지운 뒤 YAML 로 다시 띄우고 목록을 확인한다
podman pod rm -f -t 0 sp-pod
podman kube play /root/sheet-podman/sp-pod.yaml
podman pod ps
```

```bash
# 결과
c8dcd1552d1d8204ffb297c33fc1b876b30ce049a8a371970aae921a71673373
Pod:
af932dba00220b6aff21c9bb50b12c1cf2f317f7d1cddeb79bd1205373b5b605
Container:
058e5971cf0d2f42f06101ec1b9bd8971f65d6c35cc3df3f972a738857b19c2f

POD ID        NAME        STATUS      CREATED                 INFRA ID      # OF CONTAINERS
af932dba0022  sp-pod      Running     Less than a second ago  8f75f454b4b5  2
```

```bash
# YAML 에 정의된 pod 와 자원을 한 번에 내린다
#   kube play --down   YAML 파일로 만든 pod 를 멈추고 지운다 (play --help 목록에는 없는 플래그라 아래 출력으로 확인한다)
podman kube play --down /root/sheet-podman/sp-pod.yaml
```

```bash
# 결과
Pods stopped:
af932dba00220b6aff21c9bb50b12c1cf2f317f7d1cddeb79bd1205373b5b605
Pods removed:
af932dba00220b6aff21c9bb50b12c1cf2f317f7d1cddeb79bd1205373b5b605
Secrets removed:
Volumes removed:
```

### Quadlet 으로 systemd 서비스 등록

> podman 5.7 공식 문서는 deprecated 된 `podman generate systemd` 대신 Quadlet(`.container` 파일)을 systemd 에 두는 방식을 권합니다.[^quadlet] 이 절은 일반 사용자 `dev` 의 Quadlet 경로 `~/.config/containers/systemd/` 로 띄웁니다.

```bash
# dev 의 Quadlet 경로에 컨테이너 유닛 파일을 만든다 (root 가 쓰고 dev 소유로 넘긴다)
#   Image       dev 저장소에 받아 둔 이미지를 전체 주소로 적는다
#   WantedBy    사용자 systemd 는 default.target 에 붙는다
mkdir -p /home/dev/.config/containers/systemd
cat <<'EOF' > /home/dev/.config/containers/systemd/sp-quadlet.container
[Container]
Image=docker.io/library/nginx:alpine
ContainerName=sp-quadlet
PublishPort=8304:80

[Service]
Restart=always

[Install]
WantedBy=default.target
EOF
chown -R dev:dev /home/dev/.config/containers
```

이 VM 의 `su - dev` 셸에는 `XDG_RUNTIME_DIR` 과 사용자 D-Bus 가 잡혀 있습니다. 그래서 사용자 systemd 인스턴스를 그대로 쓸 수 있습니다.

```bash
# dev 의 systemd 사용자 인스턴스에서 설정을 다시 읽고 서비스를 시작한 뒤 상태를 본다
su - dev -c 'systemctl --user daemon-reload && systemctl --user start sp-quadlet.service && systemctl --user status sp-quadlet.service --no-pager | head -n 10'
```

```bash
# 결과
● sp-quadlet.service
     Loaded: loaded (/home/dev/.config/containers/systemd/sp-quadlet.container; generated)
     Active: active (running) since Mon 2026-11-23 21:21:26 KST; 5ms ago
 Invocation: 9d4c1e5679e04edabfd06c5a7a6a9b9d
   Main PID: 54680 (conmon)
      Tasks: 18 (limit: 9641)
     Memory: 80.8M (peak: 95.4M)
        CPU: 106ms
     CGroup: /user.slice/user-1000.slice/user@1000.service/app.slice/sp-quadlet.service
             ├─libpod-payload-43af82485732ca5ce310d71e46b9d7057563e0c35e596316f30677c5c9c67ae3
```

```bash
# Quadlet 이 띄운 컨테이너의 8304 포트 응답을 확인한다
curl -s http://localhost:8304 | head -n 4
```

```bash
# 결과
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```

### 실습 정리

> 유스케이스에서 만든 Quadlet 유닛·컨테이너·이미지·YAML 파일을 모두 지웁니다.

```bash
# Quadlet 서비스와 파일, root 와 dev 의 sp- 컨테이너·이미지, YAML 파일과 작업 폴더를 지운다
su - dev -c 'systemctl --user stop sp-quadlet.service; rm -f /home/dev/.config/containers/systemd/sp-quadlet.container; systemctl --user daemon-reload; podman rm -f -t 0 sp-quadlet sp-dev-web >/dev/null 2>&1 || true; podman rmi -f docker.io/library/nginx:alpine >/dev/null 2>&1 || true'
podman rm -f -t 0 sp-web >/dev/null 2>&1 || true
podman rmi -f localhost/sp-alpine:3.20 localhost/sp-nginx:alpine docker.io/library/alpine:3.20 docker.io/library/nginx:alpine >/dev/null 2>&1 || true
rm -f /root/sheet-podman/sp-pod.yaml
rmdir /root/sheet-podman
```



## 주의사항과 동작 원리

### 일반 사용자의 낮은 포트 바인딩 실패

> 일반 사용자가 1024 미만 포트를 호스트에 열면 커널의 `ip_unprivileged_port_start` 제한에 걸려 실패하므로 1024 이상 포트로 바꿉니다.[^unpriv-port]

```bash
# 커널이 일반 사용자에게 허용하는 최소 포트 번호를 확인한다
sysctl net.ipv4.ip_unprivileged_port_start    # net.ipv4.ip_unprivileged_port_start = 1024

# dev 로 호스트 80번 포트를 열려 하면 거부된다
su - dev -c 'podman run -q -d --name sp-p80 -p 80:80 docker.io/library/nginx:alpine 2>&1 || true'
```

```bash
# 결과
Error: pasta failed with exit code 1:
Listen failed for HOST TCP port */80: Permission denied
Couldn't listen on requested TCP ports
```

```bash
# 1024 이상인 8305 포트를 주면 정상으로 뜬다
su - dev -c 'podman run -q -d --name sp-p8305 -p 8305:80 docker.io/library/nginx:alpine'    # 82d5692234218acf8d917fc269b1a9cf3eb1a5885aa601e26c30b09e6ad4aab0

# 실패한 컨테이너와 테스트 컨테이너·이미지를 지운다
su - dev -c 'podman rm -f -t 0 sp-p80 sp-p8305 >/dev/null && podman rmi -f docker.io/library/nginx:alpine >/dev/null'
```

실패해도 `sp-p80` 컨테이너 메타데이터는 생성된 상태로 남으므로 정리할 때 함께 지워야 합니다.

### sudo podman ps 와 podman ps 차이

> `sudo` 로 `podman` 을 부르면 `root` 저장소를 조회하므로 일반 사용자 계정이 띄운 컨테이너가 보이지 않습니다.

```bash
# dev 계정으로 컨테이너를 하나 띄운다
su - dev -c 'podman run -q -d --name sp-dev-only docker.io/library/alpine:3.20 sleep 30 >/dev/null'

# dev 로 조회하면 컨테이너가 나온다
su - dev -c 'podman ps --format "{{.Names}} {{.Status}}"'    # sp-dev-only Up Less than a second

# root(sudo) 로 조회하면 빈 목록이 나온다
sudo podman ps    # CONTAINER ID  IMAGE       COMMAND     CREATED     STATUS      PORTS       NAMES

# 테스트 컨테이너와 이미지를 지운다
su - dev -c 'podman rm -f -t 0 sp-dev-only >/dev/null && podman rmi -f docker.io/library/alpine:3.20 >/dev/null'
```

컨테이너가 갑자기 사라진 것처럼 보이면 앞의 「사용자별 이미지·컨테이너 저장소 분리」 처럼 명령을 실행한 계정이 같은지 먼저 확인합니다.

### Docker 소켓과 system service

> `/var/run/docker.sock` 을 찾는 도구에는 `podman system service` 로 Docker v1.40 호환 API 소켓을 열어 연결합니다.[^socket]

```bash
# 5초 동안 소켓을 열고 docker CLI 로 서버 버전과 목록을 조회한 뒤 소켓을 지운다
#   --time   요청이 없을 때 소켓 서비스가 종료되기까지 기다릴 초(0 은 무제한)
podman system service --time=5 unix:///run/sp-podman.sock &
sleep 1
DOCKER_HOST=unix:///run/sp-podman.sock docker version --format '{{.Server.Platform.Name}} {{.Server.Version}}'
DOCKER_HOST=unix:///run/sp-podman.sock docker ps -a
wait
rm -f /run/sp-podman.sock
```

```bash
# 결과
linux/arm64/ubuntu-26.04 5.7.0
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

운영 환경에서는 `systemctl enable --now podman.socket` 을 켭니다. 그러면 `/run/podman/podman.sock` 이 소켓 활성화로 열립니다.

### 로그아웃 시 일반 사용자 컨테이너 종료

> 일반 사용자가 마지막 로그인 세션을 닫으면 `systemd --user` 인스턴스가 내려가며 사용자 컨테이너도 함께 멈출 수 있으므로, 상시 실행에는 `loginctl enable-linger <사용자>` 가 필요합니다.[^linger]

공식 `podman-generate-systemd(1)` 문서는 마지막 세션이 닫힐 때 systemd 사용자 인스턴스가 멈춘다고 적습니다. 부팅 시 시작해 로그아웃 뒤에도 살려 두려면 `loginctl enable-linger <username>` 을 실행합니다.[^linger] 실제 대화형 로그아웃에 따른 컨테이너 종료 동작은 이 VM 환경에서 재현하지 않았습니다.

### podman build 의 Buildah 내부 호출

> `podman build` 는 내부적으로 Buildah 프로젝트의 빌드 코드를 호출해 `RUN` 단계의 외부 빌드 컨테이너를 만듭니다.[^buildah]

빌드가 강제 종료되거나 비정상 종료하면 그 외부 컨테이너가 저장소에 남을 수 있습니다. 이때는 `podman ps --all --external` 로 Buildah 가 남긴 컨테이너까지 함께 확인합니다.[^buildah]



## 관련 문서

> 컨테이너 실행·이미지 빌드와 이어서 볼 시트와 개념 문서입니다.

- [클라우드 명령어 시트](../README.md) — 컨테이너·쿠버네티스 도구 시트 목록
- [docker 참조 시트](./docker.md) — `docker save`·`load`·`export`·`import` 이미지 반입 명령
- [nerdctl 참조 시트](../../../../02_os/docs/cmd/isolate/nerdctl.md) — containerd 환경에서 `docker` 문법과 namespace 를 다루는 시트
- [rootless 빌드의 조건](../../../../07_devops/docs/artifact/container/01-02.rootless%20%EB%B9%8C%EB%93%9C%EC%9D%98%20%EC%A1%B0%EA%B1%B4.md) — user namespace·`/etc/subuid`·비특권 OverlayFS 커널 조건
- [buildah 참조 시트](../../../../07_devops/docs/cmd/image/buildah.md) — 같은 이미지 저장소를 쓰는 빌드 도구 `buildah` 의 명령



## 참고 자료

> 검증 환경과 공식 문서, 각주 정의입니다.

- 검증 환경: OrbStack Ubuntu 26.04.1 LTS VM(aarch64), `podman 5.7.0`(`5.7.0+ds2-3build1`) — 2026-11-23 실측
- [podman(1) v5.7.0 매뉴얼](https://docs.podman.io/en/v5.7.0/markdown/podman.1.html)
- [podman-systemd.unit(5) v5.7.0 매뉴얼](https://docs.podman.io/en/v5.7.0/markdown/podman-systemd.unit.5.html)
- [podman-generate-systemd(1) v5.7.0 매뉴얼](https://docs.podman.io/en/v5.7.0/markdown/podman-generate-systemd.1.html)
- [podman-build(1) v5.7.0 매뉴얼](https://docs.podman.io/en/v5.7.0/markdown/podman-build.1.html)
- [podman-system-service(1) v5.7.0 매뉴얼](https://docs.podman.io/en/v5.7.0/markdown/podman-system-service.1.html)
- [Podman GitHub v6.2.0 릴리스](https://github.com/podman-container-tools/podman/releases/tag/v6.2.0)

[^env]: `podman --version` 실측 `podman version 5.7.0`, `dpkg -l podman` 실측 `5.7.0+ds2-3build1`. GitHub 공식 저장소(`https://github.com/podman-container-tools/podman/releases/tag/v6.2.0`) 기준 가장 새 릴리스는 `v6.2.0`(2026-11-10)입니다.
[^exit]: `podman(1)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman.1.html`) Exit Codes — "125 The error is with podman itself", "126 Executing a container command and the command cannot be invoked", "127 Executing a container command and the command cannot be found".
[^uidmap]: `podman-unshare(1)` `--help` — "Run a command inside of a modified user namespace". `podman` v5.7.0 rootless 튜토리얼(`https://github.com/podman-container-tools/podman/blob/v5.7.0/docs/tutorials/rootless_tutorial.md`) — "If your container runs with the root user, then `root` in the container is actually your user on the host."
[^shortname]: `containers-registries.conf(5)` man 페이지(VM 실측) — `unqualified-search-registries`: "An array of host[:port] registries to try when pulling an unqualified image, in order." 또한 short name 해석은 태그·다이제스트를 뗀 뒤 alias 테이블을 먼저 조회합니다.
[^pod-share]: `podman pod create --help` 실측 — `--share string  A comma delimited list of kernel namespaces the pod will share (default "ipc,net,uts")`.
[^kube]: `podman kube --help` 실측 — `generate` "Generate Kubernetes YAML from containers, pods or volumes.", `play` "Play a pod or volume based on Kubernetes YAML", `down` "Remove pods based on Kubernetes YAML".
[^quadlet]: `podman-generate-systemd(1)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman-generate-systemd.1.html`) — "podman generate systemd is deprecated. We recommend using Quadlet files when running Podman containers or pods under systemd." 및 `podman-systemd.unit(5)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman-systemd.unit.5.html`).
[^unpriv-port]: `podman` v5.7.0 네트워킹 튜토리얼(`https://github.com/podman-container-tools/podman/blob/v5.7.0/docs/tutorials/basic_networking.md`) — "unprivileged users must use ports 1024 through 65535 as lower ports require root privileges. (CAP_NET_BIND_SERVICE) Note: this can be adjusted using the `sysctl net.ipv4.ip_unprivileged_port_start`".
[^socket]: `podman-system-service(1)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman-system-service.1.html`) — "The REST API provided by podman system service is split into two parts: a compatibility layer offering support for the Docker v1.40 API, and a Podman-native Libpod layer."
[^linger]: `podman-generate-systemd(1)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman-generate-systemd.1.html`) — "The systemd user instance is killed after the last session for the user is closed. The systemd user instance can be started at boot and kept running even after the user logs out by enabling lingering using `$ loginctl enable-linger <username>`".
[^buildah]: `podman-build(1)` v5.7.0(`https://docs.podman.io/en/v5.7.0/markdown/podman-build.1.html`) — "podman build uses code sourced from the Buildah project to build container images. This Buildah code creates Buildah containers for the RUN options in container storage. In certain situations, when the podman build crashes or users kill the podman build process, these external containers can be left in container storage. Use the podman ps --all --external command to see these containers."
