---
title: "docker 컨테이너 실행과 조회"
tags: ["cloud", "command", "container", "docker", "run", "logs", "exec"]
status: draft
source:
  - "Docker Engine v29.8.2 docker run·ps·exec·logs·stop·start·rm·inspect --help 원문 (OrbStack macOS 실측)"
related:
  - ../README.md
  - ./docker.md
  - ./podman.md
  - ../../../../02_os/docs/cmd/isolate/nerdctl.md
updated: "2026-11-29"
---

# docker 컨테이너 실행과 조회

---

> 컨테이너를 띄우고, 목록과 로그와 상태를 읽고, 안에서 명령을 실행하고, 멈추고 지우는 `docker` 명령을 따라 치면 그대로 나오는 예제로 모았습니다.

## 개요

> `docker run` 은 이미지로 새 컨테이너를 만들어 시작하고, 나머지 명령은 그 컨테이너를 읽고 다루는 데 씁니다.

이미지를 tar 로 묶어 옮기는 `save`·`load`·`export`·`import` 는 [docker 참조 시트](./docker.md)가 맡습니다. 이 시트는 컨테이너 실행과 조회만 다루고, 이미지 빌드와 레지스트리 전송은 DevOps 명령어 시트의 일입니다.

출력은 OrbStack macOS 의 Docker Engine 29.8.2(Client 29.8.2)에서 받았습니다. 컨테이너 안 도구는 busybox 1.36 입니다.[^env]

실습 컨테이너 이름은 모두 `cc-docker-run-` 으로 시작하고 이미지는 `cc-docker-run/busybox:1.36` 입니다. 그래서 이미 쓰는 컨테이너와 섞이지 않고 `--filter name=cc-docker-run` 한 줄로 실습 컨테이너만 골라 볼 수 있습니다.



## 핵심 문법

> 이름 뒤에 오는 첫 인자가 이미지(`run`) 또는 컨테이너(그 밖의 명령)이고, 그 뒤는 컨테이너 안에서 실행할 명령입니다.

```bash
# 호출 형태
# docker run --help 와 하위 명령 --help 의 Usage 줄
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
docker ps [OPTIONS]
docker logs [OPTIONS] CONTAINER
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
docker stop [OPTIONS] CONTAINER [CONTAINER...]
docker start [OPTIONS] CONTAINER [CONTAINER...]
docker rm [OPTIONS] CONTAINER [CONTAINER...]

# 한 번 실행하고 끝나면 지운다 (컨테이너를 한 번 실행하고 지우기)
docker run --rm 이미지 명령

# 백그라운드로 띄운다. 이름·포트·환경변수를 준다 (백그라운드로 띄우고 이름·포트·환경변수 주기)
docker run -d --name 이름 -p 호스트포트:컨테이너포트 -e 키=값 이미지

# 목록을 본다 (컨테이너 목록 조회와 필터)
docker ps
docker ps -a --filter name=이름 --format '{{.Names}}'

# 로그를 읽는다 (컨테이너 로그 읽기)
docker logs --tail 줄수 컨테이너

# 실행 중인 컨테이너 안에서 명령을 돌린다 (컨테이너 안에서 명령 실행)
docker exec 컨테이너 명령

# 상태와 설정을 읽는다 (inspect 로 상태와 설정 읽기)
docker inspect -f '{{.State.Status}}' 컨테이너

# 멈추고, 다시 시작하고, 지운다 (멈추고 다시 시작하고 지우기)
docker stop 컨테이너
docker start 컨테이너
docker rm 컨테이너
```

### 터미널이 필요한 형태

```bash
# -i 와 -t 를 함께 쓰면 사람이 치는 셸이 열린다. 이 시트는 실행하지 않았다
#   -i, --interactive   붙지 않아도 표준 입력을 열어 둔다
#   -t, --tty           가짜 터미널을 할당한다
docker run --rm -it cc-docker-run/busybox:1.36 sh
# 컨테이너 안 sh 프롬프트가 뜬다. exit 를 치면 컨테이너가 끝나고 --rm 때문에 지워진다

docker exec -it 컨테이너 sh
# 이미 도는 컨테이너 안에 새 sh 가 열린다. exit 를 쳐도 컨테이너는 계속 돈다
```



## 종료 코드

> 성공하면 0 이고, `docker run` 자체가 실패하면 125, 명령을 실행할 수 없으면 126, 명령이 없으면 127 이며, 그 밖에는 컨테이너 안 명령의 종료 코드를 그대로 돌려줍니다.[^exit]

실습 이미지 `cc-docker-run/busybox:1.36` 이 없으면 아래 예가 모두 125 로 끝나므로 [실습 준비](#실습-준비)를 먼저 돌립니다.

```bash
# 0  컨테이너 안 명령이 성공했다
docker run --rm cc-docker-run/busybox:1.36 true; echo $?
```

```bash
# 결과
0
```

```bash
# 125  docker 에 넘긴 플래그가 틀려 컨테이너를 만들지 못했다
docker run --nosuchflag cc-docker-run/busybox:1.36 2>&1; echo $?
```

```bash
# 결과
unknown flag: --nosuchflag

Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

Run 'docker run --help' for more information
125
```

```bash
# 125  이미지를 찾지 못했다
docker run --rm cc-docker-run/nosuchimage:1 2>&1; echo $?
```

```bash
# 결과
Unable to find image 'cc-docker-run/nosuchimage:1' locally
docker: Error response from daemon: pull access denied for cc-docker-run/nosuchimage, repository does not exist or may require 'docker login'

Run 'docker run --help' for more information
125
```

```bash
# 126  컨테이너 안에서 명령으로 지정한 것을 실행할 수 없다 (디렉터리)
docker run --rm cc-docker-run/busybox:1.36 /etc 2>&1; echo $?
```

```bash
# 결과
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "/etc": is a directory: permission denied

Run 'docker run --help' for more information
126
```

```bash
# 127  컨테이너 안에서 명령을 찾지 못했다
docker run --rm cc-docker-run/busybox:1.36 nosuchcmd 2>&1; echo $?
```

```bash
# 결과
docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: exec: "nosuchcmd": executable file not found in $PATH

Run 'docker run --help' for more information
127
```

```bash
# 그 외  컨테이너 안 명령의 종료 코드를 그대로 돌려준다
docker run --rm cc-docker-run/busybox:1.36 sh -c 'exit 3'; echo $?

# 137  SIGKILL(9)로 죽은 프로세스의 코드이다. 128 + 9 이다
#   여기서는 셸이 SIGKILL 로 죽인 자식을 wait 하고, 그 137 로 셸이 끝난다
docker run --rm cc-docker-run/busybox:1.36 sh -c 'sleep 60 & kill -9 $!; wait $!'; echo $?
```

```bash
# 결과
3
Killed
137
```

```bash
# 1  없는 컨테이너를 inspect 했다
docker inspect cc-docker-run-nosuch 2>&1; echo $?
```

```bash
# 결과
[]
error: no such object: cc-docker-run-nosuch
1
```



## 유스케이스

> 예는 앞 예가 만든 컨테이너를 이어 쓰므로 위에서 아래로 차례로 돌립니다.

### 실습 준비

> 시험 이미지를 받고 `cc-docker-run/` 접두 태그를 붙입니다.

```bash
# busybox 이미지를 받고 실습용 태그를 붙인다
#   pull -q   진행 상황을 숨기고 받은 이미지의 전체 이름만 찍는다
docker pull -q busybox:1.36
docker tag busybox:1.36 cc-docker-run/busybox:1.36
docker image ls cc-docker-run/busybox --format '{{.Repository}}:{{.Tag}}'
```

```bash
# 결과
docker.io/library/busybox:1.36
cc-docker-run/busybox:1.36
```

### 컨테이너를 한 번 실행하고 지우기

> `docker run` 은 이미지에서 새 컨테이너를 만들어 명령을 실행하고, `--rm` 을 주면 끝난 컨테이너를 바로 지웁니다.

```bash
# 명령 하나를 실행하고 결과를 받는다
#   run --rm   컨테이너가 끝나면 컨테이너를 지운다
docker run --rm cc-docker-run/busybox:1.36 echo hello
```

```bash
# 결과
hello
```

```bash
# 컨테이너 안의 사용자와 호스트 이름을 본다
docker run --rm cc-docker-run/busybox:1.36 sh -c 'id -u; hostname; uname -s'
```

```bash
# 결과
0
d64793230bb9
Linux
```

```bash
# --rm 으로 돌린 컨테이너는 끝난 뒤 목록에 남지 않는다
#   ps -a      멈춘 컨테이너도 보인다
#   --filter   조건에 맞는 컨테이너만 고른다
docker ps -a --filter name=cc-docker-run --format '{{.Names}}' | wc -l | tr -d ' '
```

```bash
# 결과
0
```

### 백그라운드로 띄우고 이름·포트·환경변수 주기

> `-d` 로 띄우면 컨테이너 ID 를 찍고 바로 돌아오고, `--name`·`-p`·`-e` 로 이름과 포트 연결과 환경변수를 정합니다.

```bash
# 웹 서버를 백그라운드로 띄운다
#   -d       백그라운드로 돌리고 컨테이너 ID 를 찍는다
#   --name   컨테이너 이름을 정한다
#   -p       호스트 포트와 컨테이너 포트를 잇는다 (호스트:컨테이너)
#   -e       환경변수를 준다
docker run -d --name cc-docker-run-web -p 8081:80 -e MSG=hello-from-env \
  cc-docker-run/busybox:1.36 \
  sh -c 'mkdir -p /www && echo "$MSG" > /www/index.html && exec httpd -f -vv -p 80 -h /www'
```

```bash
# 결과
08049215e6f511ca12d80b7cc6e9561acb19ad7fa9fbd6360a80c876a5f6ad01
```

```bash
# 호스트 포트로 요청을 보낸다
sleep 1; /usr/bin/curl -s localhost:8081
```

```bash
# 결과
hello-from-env
```

```bash
# 끝나는 컨테이너를 하나 더 만든다. 이름을 주면 끝난 뒤에도 남는다
docker run --name cc-docker-run-job cc-docker-run/busybox:1.36 sh -c 'echo job done; exit 3'; echo $?
```

```bash
# 결과
job done
3
```

### 컨테이너 목록 조회와 필터

> 기본은 실행 중인 컨테이너만 보이고 `-a` 를 주면 멈춘 컨테이너도 보입니다. `--filter` 와 `--format` 으로 줄과 열을 고릅니다.

```bash
# 실행 중인 컨테이너를 본다
docker ps --filter name=cc-docker-run
```

```bash
# 결과
CONTAINER ID   IMAGE                        COMMAND                  CREATED        STATUS        PORTS                                     NAMES
08049215e6f5   cc-docker-run/busybox:1.36   "sh -c 'mkdir -p /ww…"   1 second ago   Up 1 second   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   cc-docker-run-web
```

```bash
# 멈춘 컨테이너까지 본다. STATUS 의 괄호가 종료 코드이다
docker ps -a --filter name=cc-docker-run
```

```bash
# 결과
CONTAINER ID   IMAGE                        COMMAND                  CREATED                  STATUS                              PORTS                                     NAMES
1fd2cf35a057   cc-docker-run/busybox:1.36   "sh -c 'echo job don…"   Less than a second ago   Exited (3) Less than a second ago                                             cc-docker-run-job
08049215e6f5   cc-docker-run/busybox:1.36   "sh -c 'mkdir -p /ww…"   1 second ago             Up 1 second                         0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   cc-docker-run-web
```

```bash
# 멈춘 컨테이너만 고른다
docker ps -a --filter name=cc-docker-run --filter status=exited --format '{{.Names}}  {{.Status}}'

# 실행 중인 컨테이너의 이름과 포트만 뽑는다
docker ps --filter name=cc-docker-run --format '{{.Names}}  {{.Ports}}'
```

```bash
# 결과
cc-docker-run-job  Exited (3) Less than a second ago
cc-docker-run-web  0.0.0.0:8081->80/tcp, [::]:8081->80/tcp
```

```bash
# ID 만 찍는다. 다른 명령의 인자로 넘길 때 쓴다
#   ps -q   ID 만 찍는다
docker ps -q --filter name=cc-docker-run-web | wc -l | tr -d ' '

# 가장 마지막에 만든 컨테이너 하나를 본다
#   ps -n   멈춘 컨테이너를 포함해 마지막에 만든 n 개를 보인다
docker ps -n 1 --format '{{.Names}}'
```

```bash
# 결과
1
cc-docker-run-job
```

### 컨테이너 로그 읽기

> `docker logs` 는 컨테이너의 표준 출력과 표준 에러를 읽습니다. 끝 줄 수와 시각은 옵션으로 정합니다.

```bash
# 끝난 컨테이너의 로그를 읽는다
docker logs cc-docker-run-job
```

```bash
# 결과
job done
```

```bash
# 줄마다 기록 시각을 붙인다
#   logs -t   각 줄 앞에 시각을 붙인다
docker logs -t cc-docker-run-job | sed -E 's/^[0-9T:.-]+Z/<시각>/'
```

```bash
# 결과
<시각> job done
```

```bash
# 웹 서버가 받은 요청은 표준 에러로 나온다. 끝 2줄만 읽는다
#   logs -n   로그 끝에서 이 줄 수만 보인다 (--tail)
docker logs -n 2 cc-docker-run-web 2>&1 | sed -E 's/\[[0-9a-f:.]+\]:[0-9]+/<클라이언트>/'
```

```bash
# 결과
<클라이언트>: url:/
<클라이언트>: response:200
```

```bash
# 표준 출력만 받으면 표준 에러로 나온 요청 로그는 비어 있다
docker logs cc-docker-run-web 2>/dev/null | wc -l | tr -d ' '
```

```bash
# 결과
0
```

### 컨테이너 안에서 명령 실행

> `docker exec` 는 이미 도는 컨테이너 안에 프로세스 하나를 더 띄웁니다. 컨테이너의 메인 프로세스(PID 1)는 그대로입니다.

```bash
# 컨테이너 안 파일을 읽는다
docker exec cc-docker-run-web cat /www/index.html
```

```bash
# 결과
hello-from-env
```

```bash
# 환경변수와 작업 디렉터리를 정해 실행한다
#   exec -e   이 명령에만 쓸 환경변수를 준다
#   exec -w   명령을 실행할 디렉터리를 정한다
docker exec -e EXTRA=1 -w /www cc-docker-run-web sh -c 'pwd; echo $EXTRA $MSG; ls'
```

```bash
# 결과
/www
1 hello-from-env
index.html
```

```bash
# 컨테이너 안 프로세스를 본다. httpd 가 PID 1 이고 exec 로 띄운 ps 는 새 프로세스이다
docker exec cc-docker-run-web ps -o pid,args
```

```bash
# 결과
PID   COMMAND
    1 httpd -f -vv -p 80 -h /www
   18 ps -o pid,args
```

```bash
# 사용자를 바꿔 실행한다
#   exec -u   명령을 실행할 사용자나 UID 를 정한다
docker exec -u 1000 cc-docker-run-web id
```

```bash
# 결과
uid=1000 gid=0(root) groups=0(root)
```

```bash
# exec 한 명령의 종료 코드가 docker exec 의 종료 코드가 된다
docker exec cc-docker-run-web sh -c 'exit 7'; echo $?
```

```bash
# 결과
7
```

### inspect 로 상태와 설정 읽기

> `docker inspect` 는 컨테이너의 전체 설정을 JSON 으로 주고, `-f` 의 Go 템플릿으로 필요한 값만 뽑습니다.

```bash
# 상태와 종료 코드를 뽑는다
#   inspect -f   Go 템플릿으로 출력 모양을 정한다 (--format)
docker inspect -f '{{.Name}}  {{.State.Status}}  exit={{.State.ExitCode}}' \
  cc-docker-run-web cc-docker-run-job
```

```bash
# 결과
/cc-docker-run-web  running  exit=0
/cc-docker-run-job  exited  exit=3
```

```bash
# 이미지와 실행 명령, 환경변수를 뽑는다
docker inspect -f '{{.Config.Image}}' cc-docker-run-web
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' cc-docker-run-web | grep MSG
```

```bash
# 결과
cc-docker-run/busybox:1.36
MSG=hello-from-env
```

```bash
# 포트 연결을 JSON 으로 뽑는다
docker inspect -f '{{json .NetworkSettings.Ports}}' cc-docker-run-web
docker inspect -f '{{json .HostConfig.PortBindings}}' cc-docker-run-web
```

```bash
# 결과
{"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"8081"},{"HostIp":"::","HostPort":"8081"}]}
{"80/tcp":[{"HostIp":"","HostPort":"8081"}]}
```

```bash
# 컨테이너 IP 와 실행 여부를 뽑는다. 끝난 컨테이너의 PID 는 0 이다
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' cc-docker-run-web
docker inspect -f '{{.Name}}  running={{.State.Running}}  pid0={{eq .State.Pid 0}}' cc-docker-run-web cc-docker-run-job
```

```bash
# 결과
192.168.215.2
/cc-docker-run-web  running=true  pid0=false
/cc-docker-run-job  running=false  pid0=true
```

### 멈추고 다시 시작하고 지우기

> `stop` 은 컨테이너를 멈추되 지우지 않고, `start` 는 멈춘 컨테이너를 같은 컨테이너로 다시 시작하며, `rm` 은 멈춘 컨테이너를 지웁니다.

```bash
# 컨테이너를 멈춘다. 종료 코드 137 은 SIGKILL 로 끝났다는 뜻이다
#   stop -t   SIGTERM 을 보낸 뒤 강제로 죽이기까지 기다릴 초를 정한다
docker stop -t 2 cc-docker-run-web
docker ps -a --filter name=cc-docker-run-web --format '{{.Names}}  {{.Status}}'
```

```bash
# 결과
cc-docker-run-web
cc-docker-run-web  Exited (137) Less than a second ago
```

```bash
# 멈춘 컨테이너 안에서는 exec 가 실패한다
docker exec cc-docker-run-web cat /www/index.html 2>&1; echo $?
```

```bash
# 결과
Error response from daemon: container 08049215e6f511ca12d80b7cc6e9561acb19ad7fa9fbd6360a80c876a5f6ad01 is not running
1
```

```bash
# 멈춘 컨테이너를 다시 시작한다. 컨테이너 ID 와 -e 로 준 값은 그대로이다
docker start cc-docker-run-web
sleep 1; /usr/bin/curl -s localhost:8081
docker ps --filter name=cc-docker-run-web --format '{{.Names}}  {{.Status}}'
```

```bash
# 결과
cc-docker-run-web
hello-from-env
cc-docker-run-web  Up 1 second
```

```bash
# 실행 중인 컨테이너는 rm 이 거절한다
docker rm cc-docker-run-web 2>&1; echo $?
```

```bash
# 결과
Error response from daemon: cannot remove container "cc-docker-run-web": container is running: stop the container before removing or force remove
1
```

```bash
# 멈춘 컨테이너와 실행 중인 컨테이너를 함께 지운다
#   rm -f   실행 중이어도 SIGKILL 로 죽이고 지운다
#   rm -v   컨테이너에 딸린 익명 볼륨을 함께 지운다
docker rm -fv cc-docker-run-web cc-docker-run-job
docker ps -a --filter name=cc-docker-run --format '{{.Names}}' | wc -l | tr -d ' '
```

```bash
# 결과
cc-docker-run-web
cc-docker-run-job
0
```

### 실습 정리

> 남은 실습 컨테이너와 실습 태그를 지웁니다.

```bash
# 남은 실습 컨테이너가 있으면 지우고, 실습 태그를 뗀다
#   rmi   이미지 태그를 뗀다. 다른 태그가 남은 이미지 내용은 지워지지 않는다
docker ps -aq --filter name=cc-docker-run | xargs -r docker rm -fv
docker rmi cc-docker-run/busybox:1.36
docker ps -aq --filter name=cc-docker-run | wc -l | tr -d ' '
```

```bash
# 결과
Untagged: cc-docker-run/busybox:1.36
0
```



## 주의사항과 동작 원리

> 같은 이름처럼 보이는 명령이 다른 일을 하고, 시간과 상태에 따라 결과가 달라지는 곳을 모았습니다.

> 아래 예는 앞의 실습 정리에서 뗀 실습 태그를 다시 붙여 쓰고, 마지막 예에서 다시 뗍니다.

```bash
# 실습 태그를 다시 붙인다
docker tag busybox:1.36 cc-docker-run/busybox:1.36
docker image ls cc-docker-run/busybox --format '{{.Repository}}:{{.Tag}}'
```

```bash
# 결과
cc-docker-run/busybox:1.36
```

### run 과 start 의 차이

> `run` 은 매번 새 컨테이너를 만들고, `start` 는 이미 있는 컨테이너를 같은 쓰기 층 그대로 다시 시작합니다.

```bash
# run 으로 파일에 한 줄을 쓰는 컨테이너를 만든다
docker run --name cc-docker-run-rs cc-docker-run/busybox:1.36 sh -c 'echo line >> /log.txt; cat /log.txt'
```

```bash
# 결과
line
```

```bash
# start 는 같은 컨테이너를 다시 돌려서 파일이 쌓인다. 새 컨테이너가 아니다
#   start -a   표준 출력과 표준 에러를 붙여서 본다 (--attach)
docker start -a cc-docker-run-rs
```

```bash
# 결과
line
line
```

```bash
# 같은 이름으로 run 을 다시 하면 새 컨테이너를 만들려다 이름이 겹쳐 실패한다
docker run --name cc-docker-run-rs cc-docker-run/busybox:1.36 true 2>&1 | sed -E 's/"[0-9a-f]{64}"/"<ID>"/; s/container [0-9a-f]{64}/container <ID>/'; echo ${PIPESTATUS[0]}
```

```bash
# 결과
docker: Error response from daemon: Conflict. The container name "/cc-docker-run-rs" is already in use by container "<ID>". You have to remove (or rename) that container to be able to reuse that name.

Run 'docker run --help' for more information
125
```

```bash
# 이름을 바꿔 run 하면 파일이 없는 새 컨테이너가 돈다
docker run --name cc-docker-run-rs2 cc-docker-run/busybox:1.36 sh -c 'echo line >> /log.txt; cat /log.txt'
docker ps -a --filter name=cc-docker-run-rs --format '{{.Names}}' | sort
docker rm -fv cc-docker-run-rs cc-docker-run-rs2
```

```bash
# 결과
line
cc-docker-run-rs
cc-docker-run-rs2
cc-docker-run-rs
cc-docker-run-rs2
```

`start` 는 컨테이너를 만들 때 정한 명령과 옵션을 그대로 다시 씁니다. 명령이나 포트를 바꾸려면 컨테이너를 지우고 `run` 을 다시 해야 합니다.

### stop 의 SIGTERM 과 SIGKILL 유예

> `docker stop` 은 먼저 SIGTERM 을 보내고, 정해진 시간(기본 10초) 안에 끝나지 않으면 SIGKILL 로 죽입니다.[^stop]

```bash
# SIGTERM 을 받으면 로그를 남기고 끝나는 컨테이너는 바로 멈추고 종료 코드가 0 이다
docker run -d --name cc-docker-run-trap cc-docker-run/busybox:1.36 \
  sh -c 'trap "echo got-TERM; exit 0" TERM; while :; do sleep 1; done'
sleep 1
SECONDS=0; docker stop cc-docker-run-trap; echo "걸린 시간 ${SECONDS}초"
docker logs cc-docker-run-trap
docker inspect -f 'exit={{.State.ExitCode}}' cc-docker-run-trap
```

```bash
# 결과
ab1dcd1aa7d4851268eed0d555b0b69e4da3bca730b0398aebf9d09f20301bbe
cc-docker-run-trap
걸린 시간 0초
got-TERM
exit=0
```

```bash
# PID 1 이 SIGTERM 을 무시하면 기본 10초를 기다린 뒤 SIGKILL 로 끝난다
docker run -d --name cc-docker-run-ign cc-docker-run/busybox:1.36 sleep 300
SECONDS=0; docker stop cc-docker-run-ign; echo "걸린 시간 ${SECONDS}초"
docker inspect -f 'exit={{.State.ExitCode}}' cc-docker-run-ign
```

```bash
# 결과
c4d421fafdfe29bd051f3781cdafbe28eb9210614fb62db32c46dbc64c0b4075
cc-docker-run-ign
걸린 시간 10초
exit=137
```

```bash
# 이 예가 만든 컨테이너를 지운다
docker rm -fv cc-docker-run-trap cc-docker-run-ign
```

```bash
# 결과
cc-docker-run-trap
cc-docker-run-ign
```

PID 1 은 리눅스에서 핸들러를 등록하지 않은 신호를 무시합니다. 그래서 `sleep` 처럼 SIGTERM 핸들러가 없는 프로그램이 PID 1 이면 `stop` 은 항상 유예 시간을 다 기다립니다. 기다릴 시간은 `-t` 로 줄입니다.

### 포트 충돌이 남기는 Created 컨테이너

> 호스트 포트가 이미 쓰이고 있으면 컨테이너는 만들어진 뒤 시작에서 실패해서, 이름이 그대로 남습니다.

```bash
# 8082 포트를 쓰는 컨테이너 둘을 연달아 띄운다
docker run -d --name cc-docker-run-p1 -p 8082:80 cc-docker-run/busybox:1.36 sleep 300 > /dev/null
docker run -d --name cc-docker-run-p2 -p 8082:80 cc-docker-run/busybox:1.36 sleep 300 2>&1 | sed -E 's/\(([0-9a-f]{64})\)/(<ID>)/; s/endpoint (cc-docker-run-p2)/endpoint \1/'; echo ${PIPESTATUS[0]}
```

```bash
# 결과
3a4abc51acde9405fea792a3dbf6946fc1ae21601b8512e143dffcedbbf0d695
docker: Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint cc-docker-run-p2 (<ID>): Bind for 0.0.0.0:8082 failed: port is already allocated

Run 'docker run --help' for more information
125
```

```bash
# 실패한 p2 는 Created 상태로 남아 있다
docker ps -a --filter name=cc-docker-run-p --format '{{.Names}}  {{.Status}}'
docker rm -fv cc-docker-run-p1 cc-docker-run-p2
docker rmi cc-docker-run/busybox:1.36
```

```bash
# 결과
cc-docker-run-p2  Created
cc-docker-run-p1  Up Less than a second
cc-docker-run-p1
cc-docker-run-p2
Untagged: cc-docker-run/busybox:1.36
```



## 관련 문서

> 이 시트와 이어지는 문서입니다.

- [클라우드 명령어 시트](../README.md) — 컨테이너와 쿠버네티스 도구의 시트 모음
- [docker 참조 시트](./docker.md) — 이미지를 tar 로 내보내고 들이는 `save`·`load`·`export`·`import`
- [podman 참조 시트](./podman.md) — 같은 명령 꼴을 데몬 없이 일반 사용자 권한으로 쓰는 도구
- [nerdctl 참조 시트](../../../../02_os/docs/cmd/isolate/nerdctl.md) — containerd 위에서 같은 문법으로 컨테이너를 다루는 시트



## 참고 자료

> 검증 환경과 각주 정의입니다.

- 검증 환경: OrbStack macOS Docker Engine 29.8.2 (Client 29.8.2, arm64)
- 컨테이너 안 도구: busybox 1.36

[^env]: `docker version --format '{{.Client.Version}} / {{.Server.Version}}'` 의 출력이 `29.8.2 / 29.8.2` 였습니다. 다른 엔진 버전과 overlay2 저장소는 실측하지 않았습니다.
[^exit]: 이 시트의 실측에서 본 값입니다. 125·126·127 은 `docker run` 의 실패 유형을 가르는 값이고, 0·3·137 은 컨테이너 안 명령이 낸 값이 그대로 전달된 것입니다(`stop` 으로 멈춘 컨테이너의 137 은 아래 유스케이스에 있습니다). 이 밖의 실패 유형은 확인하지 않았습니다.
[^stop]: `docker stop --help` 의 `-t, --timeout int  Seconds to wait before killing the container` 와 `docker rm --help` 의 `-f, --force  Force the removal of a running container (uses SIGKILL)` 를 근거로 했고, 기다림은 아래 실측의 걸린 시간과 종료 코드 137 에서 확인했습니다. 기본 유예 시간 10초는 이 실측의 걸린 시간에서 읽은 값입니다.
