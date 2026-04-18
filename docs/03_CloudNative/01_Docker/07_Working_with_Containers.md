# Chapter 7: Working with Containers

## 📌 핵심 요약

> **컨테이너는 이미지의 런타임 인스턴스로, 하나의 이미지에서 여러 컨테이너를 실행할 수 있다.**
> 컨테이너는 단일 프로세스를 실행하도록 설계되었으며, 메인 프로세스(PID 1)가 종료되면 컨테이너도 종료된다.
> 컨테이너는 Stateless하고 Immutable하게 설계되어, 문제 발생 시 수정이 아닌 교체 방식으로 대응한다.

---

## 🎯 학습 목표

이 챕터를 완료하면 다음을 할 수 있습니다:

- [ ] VM과 컨테이너의 차이점 이해
- [ ] 이미지와 컨테이너의 R/W 레이어 관계 파악
- [ ] 컨테이너 시작, 중지, 재시작, 삭제 수행
- [ ] docker exec로 컨테이너 접속 및 명령 실행
- [ ] Entrypoint와 Cmd의 차이점 이해
- [ ] Docker Debug로 Slim 이미지 디버깅
- [ ] Restart Policy로 자가 복구 설정

---

## 📖 본문 정리

### 1. 컨테이너 개요

#### 핵심 특징

```
┌─────────────────────────────────────────────────────────────┐
│                     Container 특징                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ 이미지의 런타임 인스턴스                                  │
│  ✅ 하나의 이미지 → 여러 컨테이너 생성 가능                    │
│  ✅ VM보다 작고, 빠르고, 이식성 높음                          │
│  ✅ Stateless & Ephemeral (상태 없음 & 일시적)               │
│  ✅ Immutable (불변) - 수정 대신 교체                         │
│  ✅ 단일 프로세스 실행 (마이크로서비스)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 이미지와 컨테이너 관계

```
┌─────────────────────────────────────────────────────────────┐
│              Image → Multiple Containers                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌──────────────┐                         │
│                    │   R/W Layer  │ Container 1             │
│                    └──────┬───────┘                         │
│                           │                                 │
│                    ┌──────────────┐                         │
│                    │   R/W Layer  │ Container 2             │
│                    └──────┬───────┘                         │
│                           │                                 │
│                    ┌──────────────┐                         │
│                    │   R/W Layer  │ Container 3             │
│                    └──────┬───────┘                         │
│                           │                                 │
│              ═════════════╪═════════════                    │
│                           ▼                                 │
│              ┌────────────────────────┐                     │
│              │    Shared Image        │  Read-Only          │
│              │    (읽기 전용)          │                     │
│              └────────────────────────┘                     │
│                                                             │
│  • 각 컨테이너는 자신만의 Thin R/W 레이어 보유                │
│  • 이미지는 모든 컨테이너가 공유 (읽기 전용)                   │
│  • 컨테이너 삭제 시 R/W 레이어만 삭제                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. 컨테이너 vs VM

#### 가상화 방식 비교

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VM vs Container 가상화                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│        VM (Hardware Virtualization)      Container (OS Virtualization)  │
│                                                                         │
│   ┌─────┐ ┌─────┐ ┌─────┐              ┌─────┐ ┌─────┐ ┌─────┐         │
│   │ App │ │ App │ │ App │              │ App │ │ App │ │ App │         │
│   ├─────┤ ├─────┤ ├─────┤              ├─────┤ ├─────┤ ├─────┤         │
│   │Guest│ │Guest│ │Guest│              │ Ctr │ │ Ctr │ │ Ctr │         │
│   │ OS  │ │ OS  │ │ OS  │              └──┬──┘ └──┬──┘ └──┬──┘         │
│   └──┬──┘ └──┬──┘ └──┬──┘                 │      │      │             │
│      │      │      │                  ┌───┴──────┴──────┴───┐          │
│   ┌──┴──────┴──────┴──┐               │   Container Runtime │          │
│   │    Hypervisor     │               │      (Docker)       │          │
│   └────────┬──────────┘               └──────────┬──────────┘          │
│            │                                     │                      │
│   ┌────────┴──────────┐               ┌──────────┴──────────┐          │
│   │    Host OS        │               │      Host OS        │          │
│   └────────┬──────────┘               └──────────┬──────────┘          │
│            │                                     │                      │
│   ┌────────┴──────────┐               ┌──────────┴──────────┐          │
│   │    Hardware       │               │      Hardware       │          │
│   └───────────────────┘               └─────────────────────┘          │
│                                                                         │
│   • 하드웨어 리소스를 가상화             • OS 리소스를 가상화              │
│   • 각 VM에 Guest OS 필요               • 호스트 커널 공유                │
│   • GB 단위 크기                        • MB 단위 크기                   │
│   • 부팅 시간: 분 단위                  • 시작 시간: 초 단위              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### VM Tax (VM의 오버헤드)

```
┌─────────────────────────────────────────────────────────────┐
│                   Container 장점                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 장점                │ 설명                          │   │
│  ├─────────────────────┼──────────────────────────────┤   │
│  │ 더 작음             │ 앱 코드 + 최소 OS 구성요소만   │   │
│  │ 더 많이 실행        │ OS 오버헤드 없음              │   │
│  │ 더 빠른 시작        │ 호스트 OS 이미 부팅됨         │   │
│  │ 관리 부담 감소      │ OS 패치/업데이트 감소         │   │
│  │ 작은 공격 표면      │ 불필요한 구성요소 미포함       │   │
│  └─────────────────────┴──────────────────────────────┘   │
│                                                             │
│  예시: 100개 애플리케이션 배포                               │
│  • VM: 100개 OS 필요 (각각 CPU, 메모리, 스토리지 소비)       │
│  • Container: 추가 OS 불필요 (호스트 OS만 사용)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

💬 **비유**: VM은 각자 주방이 있는 아파트, 컨테이너는 공용 주방을 쓰는 공유 오피스

---

### 3. 컨테이너 시작

#### docker run 명령어

```bash
$ docker run -d --name webserver -p 5005:8080 nigelpoulton/ddd-book:web0.1

# 명령어 분석
# docker run     : 새 컨테이너 실행
# -d             : Detached 모드 (백그라운드 실행)
# --name         : 컨테이너 이름 지정
# -p 5005:8080   : 포트 매핑 (호스트:컨테이너)
# nigelpoulton/ddd-book:web0.1 : 사용할 이미지
```

#### 컨테이너 시작 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                Container 시작 프로세스                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. docker run 명령 실행                                     │
│         │                                                   │
│         ▼                                                   │
│  2. Docker CLI → API 요청 변환 → Docker Daemon              │
│         │                                                   │
│         ▼                                                   │
│  3. 로컬 이미지 검색                                         │
│         │                                                   │
│         ├─ 있음 → 이미지 사용                                │
│         │                                                   │
│         └─ 없음 → Docker Hub에서 Pull                       │
│                    │                                        │
│                    ▼                                        │
│  4. containerd에 컨테이너 생성 요청                          │
│         │                                                   │
│         ▼                                                   │
│  5. runc가 컨테이너 생성 및 앱 시작                          │
│         │                                                   │
│         ▼                                                   │
│  6. 포트 매핑 수행                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 실행 확인

```bash
# 이미지 확인
$ docker images
REPOSITORY              TAG       IMAGE ID       SIZE
nigelpoulton/ddd-book   web0.1    3f5b281b914b   159MB

# 실행 중인 컨테이너 확인
$ docker ps
CONTAINER ID   IMAGE             COMMAND           STATUS      PORTS                  NAMES
b5594b3b8b3f   nigelpoulton...   "node ./app.js"   Up 2 mins   0.0.0.0:5005->8080/tcp webserver
```

---

### 4. 컨테이너의 앱 실행 방법

#### 앱 시작 방법 3가지

```
┌─────────────────────────────────────────────────────────────┐
│                앱 시작 명령 지정 방법                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Entrypoint (이미지 메타데이터)                           │
│     • CLI에서 오버라이드 불가                                 │
│     • CLI 인자는 Entrypoint에 추가됨                         │
│                                                             │
│  2. Cmd (이미지 메타데이터)                                  │
│     • CLI 인자로 오버라이드 가능                              │
│                                                             │
│  3. CLI 인자                                                 │
│     • docker run <image> <command>                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Entrypoint vs Cmd 비교

| 특성 | Entrypoint | Cmd |
|------|------------|-----|
| **위치** | 이미지 메타데이터 | 이미지 메타데이터 |
| **CLI 오버라이드** | ❌ 불가 | ✅ 가능 |
| **CLI 인자 처리** | 인자로 추가 | 대체됨 |
| **용도** | 고정 실행 명령 | 기본 명령 (변경 가능) |

#### Entrypoint 확인

```bash
$ docker inspect nigelpoulton/ddd-book:web0.1 | grep Entrypoint -A 3
"Entrypoint": [
    "node",
    "./app.js"
],

# 실행되는 명령: node ./app.js
```

#### CLI로 명령 지정

```bash
# 이미지에 Entrypoint/Cmd 없으면 CLI로 지정
$ docker run --rm -d alpine sleep 60

# --rm: 종료 후 자동 삭제
# sleep 60: 60초 후 종료
```

---

### 5. 실행 중인 컨테이너 접속

#### docker exec 두 가지 모드

```
┌─────────────────────────────────────────────────────────────┐
│                   docker exec 모드                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Interactive Mode (대화형)                                │
│     $ docker exec -it webserver sh                          │
│     • 터미널을 컨테이너 Shell에 연결                          │
│     • SSH 접속과 유사                                        │
│                                                             │
│  2. Remote Execution (원격 실행)                             │
│     $ docker exec webserver ps                              │
│     • 명령 실행 후 결과만 출력                               │
│     • 대화형 세션 없음                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 대화형 접속 예시

```bash
# 컨테이너에 sh 셸로 접속
$ docker exec -it webserver sh
/src #

# 컨테이너 내부에서 명령 실행
/src # ls -l
total 100
-rw-r--r--    1 root     root           324 Feb 20 12:35 Dockerfile
-rw-r--r--    1 root     root           341 Feb 20 12:35 app.js
drwxr-xr-x  183 root     root          4096 Feb 20 12:41 node_modules
...

# vim 명령 실패 (설치 안됨)
/src # vim app.js
sh: vim: not found
```

---

### 6. 컨테이너 프로세스 검사

#### PID 1 = 메인 프로세스

```
┌─────────────────────────────────────────────────────────────┐
│                  컨테이너 프로세스 구조                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  /src # ps                                                  │
│  PID   USER     TIME  COMMAND                               │
│    1   root      0:00 node ./app.js    ← 메인 프로세스       │
│   13   root      0:00 sh               ← exec 세션          │
│   22   root      0:00 ps               ← ps 명령 (종료됨)    │
│                                                             │
│  ⚠️ 중요:                                                    │
│  • PID 1 = 컨테이너의 메인 앱 프로세스                        │
│  • PID 1이 종료되면 컨테이너도 종료                           │
│  • 컨테이너는 단일 프로세스 실행용으로 설계                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 컨테이너 종료 없이 탈출

```bash
# exit 입력 시: Shell 종료 → 컨테이너도 종료될 수 있음
/src # exit

# Ctrl + P + Q: Shell 프로세스 유지하며 탈출
root@container:/# <Ctrl PQ>
read escape sequence

$ docker ps  # 컨테이너 여전히 실행 중
```

---

### 7. docker inspect 명령어

```bash
$ docker inspect webserver
{
    "State": {
        "Status": "running"
    },
    "Name": "/webserver",
    "PortBindings": {
        "8080/tcp": [
            {
                "HostIp": "",
                "HostPort": "5005"
            }
        ]
    },
    "RestartPolicy": {
        "Name": "no",
        "MaximumRetryCount": 0
    },
    "Image": "nigelpoulton/ddd-book:web0.1",
    "WorkingDir": "/src",
    "Entrypoint": [
        "node",
        "./app.js"
    ]
}
```

**주요 정보:**
- `State.Status`: 실행 상태
- `PortBindings`: 포트 매핑
- `RestartPolicy`: 재시작 정책
- `Entrypoint`: 시작 명령

---

### 8. 컨테이너 데이터 쓰기

```
┌─────────────────────────────────────────────────────────────┐
│                 컨테이너 R/W 레이어                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────┐                    │
│  │         Container R/W Layer         │  ← 변경 저장       │
│  │  (컨테이너별 독립적인 쓰기 레이어)    │                    │
│  └─────────────────────────────────────┘                    │
│                     │                                       │
│                     ▼                                       │
│  ┌─────────────────────────────────────┐                    │
│  │         Shared Image (R/O)          │  ← 읽기 전용       │
│  └─────────────────────────────────────┘                    │
│                                                             │
│  동작:                                                       │
│  • 파일 읽기: 이미지 레이어에서 읽음                          │
│  • 파일 쓰기: R/W 레이어에 기록                              │
│  • Stop: R/W 레이어 유지                                    │
│  • Restart: R/W 레이어 복원                                 │
│  • Delete: R/W 레이어 삭제 (변경 사항 손실)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

⚠️ **안티패턴 경고**: 실행 중인 컨테이너를 직접 수정하는 것은 권장하지 않음. 변경이 필요하면 새 이미지를 빌드하고 컨테이너를 교체해야 함.

---

### 9. 컨테이너 생명주기 관리

#### Stop, Restart, Delete

```bash
# 실행 상태 확인
$ docker ps
CONTAINER ID   IMAGE             COMMAND           STATUS       NAMES
b5594b3b8b3f   nigelpoulton...   "node ./app.js"   Up 51 mins   webserver

# 컨테이너 중지 (최대 10초 대기 후 종료)
$ docker stop webserver
webserver

# 중지된 컨테이너 확인 (-a 플래그 필요)
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND           STATUS                      NAMES
b5594b3b8b3f   nigelpou...   "node ./app.js"   Exited (137) 1 minute ago   webserver

# 컨테이너 재시작
$ docker restart webserver
webserver

# 강제 삭제 (중지 없이 바로 삭제)
$ docker rm webserver -f
webserver
```

#### 생명주기 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                 Container Lifecycle                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│        docker run              docker stop                  │
│              │                      │                       │
│              ▼                      ▼                       │
│    ┌─────────────────┐    ┌─────────────────┐              │
│    │    Created      │───►│    Running      │──────┐       │
│    └─────────────────┘    └─────────────────┘      │       │
│                                   │                │       │
│                           docker restart           │       │
│                                   │                │       │
│                                   ▼                ▼       │
│                           ┌─────────────────┐              │
│                           │    Stopped      │              │
│                           │   (Exited)      │              │
│                           └────────┬────────┘              │
│                                    │                       │
│                              docker rm                     │
│                                    │                       │
│                                    ▼                       │
│                           ┌─────────────────┐              │
│                           │    Deleted      │              │
│                           └─────────────────┘              │
│                                                             │
│  • Stop: R/W 레이어 유지 (변경 사항 보존)                    │
│  • Restart: 빠른 재시작 (R/W 레이어 복원)                    │
│  • Delete: R/W 레이어 삭제 (복구 불가)                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 10. 메인 프로세스 종료와 컨테이너

```bash
# 대화형 컨테이너 시작 (bash가 PID 1)
$ docker run --name ddd-ctr -it ubuntu:24.04 bash
root@d3c892ad0eb3:/#

# 프로세스 확인
root@d3c892ad0eb3:/# ps
  PID TTY          TIME CMD
    1 pts/0    00:00:00 bash    ← 메인 프로세스
    9 pts/0    00:00:00 ps

# exit 입력 → bash 종료 → 컨테이너 종료
root@d3c892ad0eb3:/# exit

$ docker ps -a
CONTAINER ID   IMAGE          COMMAND   STATUS                  NAMES
d3c892ad0eb3   ubuntu:24.04   "bash"    Exited (0) 3 secs ago   ddd-ctr
```

#### 종료 vs 탈출

| 동작 | 결과 |
|------|------|
| `exit` | PID 1 종료 → 컨테이너 종료 |
| `Ctrl + P + Q` | 세션만 종료 → 컨테이너 계속 실행 |

---

### 11. Docker Debug (Slim 이미지 디버깅)

#### 개요

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Debug                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  목적: Shell이나 디버깅 도구 없는 Slim 이미지/컨테이너 디버깅   │
│                                                             │
│  요구사항:                                                   │
│  • Docker Desktop (Pro, Team, Business 구독)                │
│  • docker login 필요                                        │
│                                                             │
│  동작 방식:                                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │   Docker Debug Session                                 │ │
│  │  ┌─────────────┐                                      │ │
│  │  │  /nix       │ ← 디버깅 도구 마운트 (세션 종료 시 제거)│ │
│  │  │  toolbox    │                                      │ │
│  │  └─────────────┘                                      │ │
│  │         │                                             │ │
│  │         ▼                                             │ │
│  │  ┌─────────────┐                                      │ │
│  │  │  Container  │                                      │ │
│  │  │  or Image   │                                      │ │
│  │  └─────────────┘                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 사용 예시

```bash
# 컨테이너에서 도구 없음 확인
$ docker attach ddd-ctr
root@container:/# ping nigelpoulton.com
bash: ping: command not found

root@container:/# vim
bash: vim: command not found

# Docker Debug로 디버깅
$ docker debug ddd-ctr

docker > ping nigelpoulton.com
PING nigelpoulton.com (192.124.249.126) 56(84) bytes of data.
64 bytes from cloudproxy10126.sucuri.net: icmp_seq=1 ttl=63 time=211 ms
^C

docker > vim
~                   VIM  - Vi IMproved
:q

# 추가 도구 설치 (search.nixos.org에서)
docker > install bind
docker > nslookup nigelpoulton.com
Server:   192.168.65.7
Name:     nigelpoulton.com
Address:  192.124.249.126
```

#### 실행 중 컨테이너 vs 이미지 디버깅

| 대상 | 변경 사항 |
|------|----------|
| **실행 중 컨테이너** | 즉시 반영, 재시작 후에도 유지 |
| **이미지/중지된 컨테이너** | Sandbox 생성, 세션 종료 시 삭제 |

#### entrypoint 명령

```bash
# 이미지/컨테이너의 시작 명령 확인
docker > entrypoint --print
node ./app.js
```

---

### 12. Restart Policy (자가 복구)

#### 정책 종류

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Restart Policy 비교                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  정책             │ 비정상 종료 │ 정상 종료 │ docker stop │ Daemon 재시작 │
│  ─────────────────┼────────────┼──────────┼────────────┼──────────────│
│  no (기본)        │     ❌     │    ❌    │     ❌     │      ❌      │
│  on-failure       │     ✅     │    ❌    │     ❌     │      ✅      │
│  always           │     ✅     │    ✅    │     ❌     │      ✅      │
│  unless-stopped   │     ✅     │    ✅    │     ❌     │      ❌      │
│                                                                         │
│  • 비정상 종료: exit code ≠ 0                                            │
│  • 정상 종료: exit code = 0                                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### always vs unless-stopped

```
┌─────────────────────────────────────────────────────────────┐
│              always vs unless-stopped 차이                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  시나리오: docker stop → Docker Daemon 재시작               │
│                                                             │
│  always:                                                    │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐      │
│  │Running │───►│Stopped │───►│Daemon  │───►│Running │      │
│  │        │stop│        │restart│      │    │(자동)  │      │
│  └────────┘    └────────┘    └────────┘    └────────┘      │
│                                                             │
│  unless-stopped:                                            │
│  ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐      │
│  │Running │───►│Stopped │───►│Daemon  │───►│Stopped │      │
│  │        │stop│        │restart│      │    │(그대로)│      │
│  └────────┘    └────────┘    └────────┘    └────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 사용 예시

```bash
# always 정책으로 컨테이너 시작
$ docker run --name neversaydie -it --restart always alpine sh
/#

# exit로 강제 종료
/# exit

# 자동 재시작 확인
$ docker ps
CONTAINER ID   IMAGE    COMMAND   CREATED          STATUS          NAMES
1933623830bb   alpine   "sh"      35 seconds ago   Up 2 seconds    neversaydie

# RestartCount 확인
$ docker inspect neversaydie | grep RestartCount
        "RestartCount": 1,
```

#### Docker Compose에서 Restart Policy

```yaml
services:
  myservice:
    image: nginx
    restart_policy:
      condition: always | unless-stopped | on-failure
```

---

### 13. 정리 (Cleanup)

```bash
# 실행 중인 컨테이너 확인
$ docker ps
CONTAINER ID   IMAGE          COMMAND   CREATED       STATUS        NAMES
ac165419214f   alpine         "sh"      33 secs ago   Up 24 secs    neversaydie
5bd3741185fa   ubuntu:24.04   "bash"    3 mins ago    Up 1 min      ddd-ctr

# 개별 삭제
$ docker rm <container> -f

# 모든 컨테이너 삭제
$ docker rm $(docker ps -aq) -f

# 모든 이미지 삭제
$ docker rmi $(docker images -q)
```

---

### 14. 주요 명령어 정리

| 명령어 | 설명 |
|--------|------|
| `docker run` | 새 컨테이너 시작 |
| `docker run -it` | 대화형 컨테이너 시작 |
| `docker run -d` | 백그라운드 실행 |
| `docker run --restart` | 재시작 정책 설정 |
| `docker ps` | 실행 중인 컨테이너 목록 |
| `docker ps -a` | 모든 컨테이너 목록 |
| `docker exec -it` | 대화형 명령 실행 |
| `docker exec` | 원격 명령 실행 |
| `docker attach` | 메인 프로세스에 연결 |
| `docker stop` | 컨테이너 중지 (SIGTERM → SIGKILL) |
| `docker restart` | 컨테이너 재시작 |
| `docker rm` | 컨테이너 삭제 |
| `docker rm -f` | 강제 삭제 |
| `docker inspect` | 상세 정보 조회 |
| `docker debug` | Slim 컨테이너 디버깅 |
| `Ctrl + P + Q` | 종료 없이 탈출 |

---

## 🔍 심화 학습

### 핵심 개념 비교

| 개념 | 설명 |
|------|------|
| **Image** | 읽기 전용 템플릿 (Build Time) |
| **Container** | 이미지의 실행 인스턴스 (Run Time) |
| **R/W Layer** | 컨테이너별 독립적 쓰기 레이어 |
| **PID 1** | 컨테이너의 메인 프로세스 |
| **Entrypoint** | 고정 시작 명령 (오버라이드 불가) |
| **Cmd** | 기본 시작 명령 (오버라이드 가능) |

### 추가 학습 자료

- [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
- [Docker Debug Documentation](https://docs.docker.com/desktop/debug/)
- [Restart Policies](https://docs.docker.com/config/containers/start-containers-automatically/)

---

## 💡 실무 적용 포인트

### 면접 대비 질문

1. **Q: 컨테이너와 VM의 주요 차이점은?**
   > A: VM은 하드웨어를 가상화하여 각 VM에 Guest OS가 필요하지만, 컨테이너는 OS를 가상화하여 호스트 커널을 공유합니다. 이로 인해 컨테이너는 더 작고(MB 단위), 빠르게 시작하며(초 단위), 더 많이 실행할 수 있습니다. VM은 각자 독립적인 커널로 보안 격리가 강하지만, 컨테이너는 SELinux, AppArmor, seccomp 등으로 보안을 강화합니다.

2. **Q: 컨테이너의 PID 1이 중요한 이유는?**
   > A: PID 1은 컨테이너의 메인 프로세스로, 이 프로세스가 종료되면 컨테이너도 함께 종료됩니다. 컨테이너는 단일 프로세스 실행을 위해 설계되었으며, docker stop은 PID 1에 SIGTERM을 보내고 10초 후 SIGKILL을 보냅니다. 따라서 앱은 SIGTERM을 적절히 처리해야 graceful shutdown이 가능합니다.

3. **Q: Entrypoint와 Cmd의 차이점은?**
   > A: 둘 다 컨테이너 시작 시 실행할 명령을 지정하지만, Entrypoint는 CLI에서 오버라이드할 수 없고 CLI 인자가 추가됩니다. Cmd는 CLI 인자로 완전히 대체됩니다. 일반적으로 Entrypoint는 고정된 실행 파일을, Cmd는 기본 인자를 지정할 때 사용합니다.

4. **Q: 컨테이너 Restart Policy의 종류와 차이점은?**
   > A: no(기본), on-failure, always, unless-stopped 4가지가 있습니다. on-failure는 비정상 종료 시만 재시작하고, always는 모든 종료 시 재시작합니다. always와 unless-stopped의 차이는 docker stop 후 Daemon 재시작 시 동작입니다. always는 자동 시작하고, unless-stopped는 중지 상태를 유지합니다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] 컨테이너 = 이미지의 런타임 인스턴스
- [ ] Stateless & Immutable 설계 철학
- [ ] 단일 프로세스 실행 (마이크로서비스)
- [ ] PID 1 = 메인 프로세스 (종료 시 컨테이너도 종료)

### VM vs Container
- [ ] VM: 하드웨어 가상화, Guest OS 필요
- [ ] Container: OS 가상화, 호스트 커널 공유
- [ ] Container 장점: 작음, 빠름, 많이 실행 가능

### R/W 레이어
- [ ] 이미지: 읽기 전용, 공유됨
- [ ] 컨테이너: 각자 R/W 레이어 보유
- [ ] Stop: R/W 레이어 유지
- [ ] Delete: R/W 레이어 삭제

### 앱 시작 방법
- [ ] Entrypoint: 고정 명령 (오버라이드 불가)
- [ ] Cmd: 기본 명령 (CLI로 대체 가능)
- [ ] CLI 인자: docker run <image> <command>

### 컨테이너 접속
- [ ] docker exec -it: 대화형 세션
- [ ] docker exec: 원격 명령 실행
- [ ] docker attach: 메인 프로세스 연결
- [ ] Ctrl + P + Q: 종료 없이 탈출

### Restart Policy
- [ ] no: 재시작 안함 (기본)
- [ ] on-failure: 비정상 종료 시만
- [ ] always: 항상 재시작
- [ ] unless-stopped: docker stop 제외

### Docker Debug
- [ ] Slim 이미지/컨테이너 디버깅 도구
- [ ] /nix 디렉토리에 도구 마운트
- [ ] 실행 중 컨테이너: 변경 유지
- [ ] 이미지/중지 컨테이너: 세션 종료 시 삭제

### 명령어
- [ ] docker run, ps, exec, attach
- [ ] docker stop, restart, rm
- [ ] docker inspect, debug

---

## 🔗 참고 자료

- **공식 문서**
  - [Docker Run Reference](https://docs.docker.com/engine/reference/run/)
  - [Docker Debug](https://docs.docker.com/desktop/debug/)
  - [Restart Policies](https://docs.docker.com/config/containers/start-containers-automatically/)

- **관련 명령어**
  - `docker run`, `docker ps`, `docker exec`
  - `docker stop`, `docker restart`, `docker rm`
  - `docker inspect`, `docker debug`
  - `docker attach`, `Ctrl + P + Q`

---

## 다음 챕터 예고

> **Chapter 8**: Containerizing an Application - Dockerfile로 이미지 빌드하기
