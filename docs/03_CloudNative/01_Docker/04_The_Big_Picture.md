# Chapter 4: The Big Picture

---

## 📌 핵심 요약
> Docker의 전체 그림을 **Ops 관점**과 **Dev 관점**으로 나눠 살펴본다. Ops는 이미지 **다운로드(pull)**, 컨테이너 **시작(run)**, **명령 실행(exec)**, **중지/삭제(stop/rm)** 워크플로우를 다루고, Dev는 소스코드를 **Dockerfile로 이미지화(build)**하고 **컨테이너로 실행(run)**하는 과정을 다룬다. 이것이 바로 **DevOps**의 핵심이다.

---

## 🎯 학습 목표
이 챕터를 읽고 나면:
- [ ] `docker version`으로 설치 상태를 확인할 수 있다
- [ ] `docker pull`로 이미지를 다운로드할 수 있다
- [ ] `docker run`으로 컨테이너를 시작할 수 있다
- [ ] `docker exec`로 컨테이너 내부에서 명령을 실행할 수 있다
- [ ] `docker stop`과 `docker rm`으로 컨테이너를 정리할 수 있다
- [ ] Dockerfile을 이해하고 `docker build`로 이미지를 생성할 수 있다
- [ ] 애플리케이션을 컨테이너화하는 전체 흐름을 설명할 수 있다

---

## 📖 본문 정리

### 1. 두 가지 관점

```
┌─────────────────────────────────────────────────────────┐
│                   Docker 전체 그림                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────┐   ┌─────────────────────┐    │
│   │   🔧 Ops 관점       │   │   💻 Dev 관점       │    │
│   │   (운영 관점)       │   │   (개발 관점)       │    │
│   ├─────────────────────┤   ├─────────────────────┤    │
│   │                     │   │                     │    │
│   │  • 이미지 다운로드   │   │  • 소스 코드 가져오기│    │
│   │  • 컨테이너 시작     │   │  • Dockerfile 작성  │    │
│   │  • 명령 실행        │   │  • 이미지 빌드      │    │
│   │  • 컨테이너 중지/삭제│   │  • 컨테이너 실행    │    │
│   │                     │   │                     │    │
│   └─────────────────────┘   └─────────────────────┘    │
│                      │   │                              │
│                      └───┘                              │
│                        │                                │
│                        ▼                                │
│                   🚀 DevOps                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> 💬 **비유**: Ops는 완성된 요리(이미지)를 받아서 손님에게 서빙(컨테이너 실행)하는 것이고, Dev는 레시피(Dockerfile)를 보고 요리(이미지)를 만드는 것이다.

---

## Part 1: Ops 관점 (운영 관점)

### 2. Docker 설치 확인

```bash
$ docker version

Client:                                     # ← 클라이언트 정보
 Version:           28.1.1
 API version:       1.49
 Go version:        go1.23.8
 OS/Arch:           darwin/arm64
 Context:           desktop-linux

Server: Docker Desktop 4.42.0 (192140)      # ← 서버 정보
 Engine:
  Version:          28.11
  API version:      1.49 (minimum version 1.24)
  Go version:       go1.23.8
  OS/Arch:          linux/arm64
 containerd:
  Version:          1.7.27
 runc:
  Version:          1.2.5
 docker-init:
  Version:          0.19.0
```

**확인 포인트:**
- Client와 Server 둘 다 응답이 오면 정상
- Linux에서 "permission denied" 에러 → `sudo docker version` 사용

---

### 3. 이미지 다운로드 (Pull)

```
┌─────────────────────────────────────────────────────────┐
│                    이미지 Pull 흐름                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────┐                                   │
│   │   Docker Hub    │  (또는 다른 Registry)             │
│   │   ┌─────────┐   │                                   │
│   │   │  nginx  │   │                                   │
│   │   │  :latest│   │                                   │
│   │   └────┬────┘   │                                   │
│   └────────┼────────┘                                   │
│            │ docker pull nginx:latest                   │
│            ▼                                            │
│   ┌─────────────────┐                                   │
│   │   Local Host    │                                   │
│   │   ┌─────────┐   │                                   │
│   │   │  nginx  │   │                                   │
│   │   │  :latest│   │  ← 로컬에 저장됨                   │
│   │   └─────────┘   │                                   │
│   └─────────────────┘                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

```bash
# 현재 이미지 목록 확인 (처음엔 비어있음)
$ docker images
REPOSITORY    TAG        IMAGE ID       CREATED       SIZE

# nginx:latest 이미지 다운로드
$ docker pull nginx:latest
latest: Pulling from library/nginx
ad5932596f78: Download complete
e4bc5c1a6721: Download complete
...
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest

# 다시 이미지 목록 확인
$ docker images
REPOSITORY      TAG      IMAGE ID        CREATED         SIZE
nginx           latest   fb197595ebe7    10 days ago     280MB
```

**이미지란?**
- 앱 실행에 필요한 모든 것을 포함 (OS 파일시스템, 앱, 의존성)
- Ops 관점: VM 템플릿과 유사
- Dev 관점: 클래스와 유사

---

### 4. 컨테이너 시작 (Run)

```bash
$ docker run --name test -d -p 8080:80 nginx:latest
e08c3535...30557225
```

**명령어 분석:**

```
┌─────────────────────────────────────────────────────────┐
│            docker run 명령어 해부                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  docker run --name test -d -p 8080:80 nginx:latest     │
│  ─────────  ───────────  ──  ─────────  ────────────   │
│      │           │        │       │          │          │
│      │           │        │       │          └── 이미지 │
│      │           │        │       │                     │
│      │           │        │       └── 포트 매핑         │
│      │           │        │          호스트:컨테이너     │
│      │           │        │                             │
│      │           │        └── Detached 모드             │
│      │           │           (백그라운드 실행)           │
│      │           │                                      │
│      │           └── 컨테이너 이름: "test"              │
│      │                                                  │
│      └── 새 컨테이너 시작                               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

| 플래그 | 의미 | 예시 |
|--------|------|------|
| `--name` | 컨테이너 이름 지정 | `--name test` |
| `-d` | Detached (백그라운드) 실행 | 터미널 점유 안 함 |
| `-p` | 포트 매핑 (호스트:컨테이너) | `-p 8080:80` |

```bash
# 실행 중인 컨테이너 확인
$ docker ps
CONTAINER ID   IMAGE          COMMAND        CREATED      STATUS      PORTS                  NAMES
e08c35352ff3   nginx:latest   "/docker..."   3 mins ago   Up 2 mins   0.0.0.0:8080->80/tcp   test
```

**포트 매핑 시각화:**

```
┌─────────────────────────────────────────────────────────┐
│                   포트 매핑 (-p 8080:80)                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   외부 (브라우저)                                        │
│        │                                                │
│        │ http://localhost:8080                          │
│        ▼                                                │
│   ┌─────────────────────────────────────────────┐      │
│   │              Docker Host                     │      │
│   │                   │                          │      │
│   │              Port 8080                       │      │
│   │                   │ 매핑                     │      │
│   │                   ▼                          │      │
│   │   ┌─────────────────────────────────┐       │      │
│   │   │          Container              │       │      │
│   │   │              │                  │       │      │
│   │   │         Port 80 (nginx)         │       │      │
│   │   └─────────────────────────────────┘       │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 5. 컨테이너 내부 명령 실행 (Exec)

```bash
# 컨테이너에 bash 셸 연결
$ docker exec -it test bash
root@e08c35352ff3:/#
```

**`-it` 플래그:**
- `-i`: Interactive (입력 유지)
- `-t`: TTY (터미널 할당)

```bash
# 컨테이너 내부에서 파일 목록 확인
root@e08c35352ff3:/# ls -l
total 64
lrwxrwxrwx   1 root root    7 Jan  2 00:00 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Oct 31 11:04 boot
drwxr-xr-x   5 root root  340 Jan 12 15:09 dev
drwxr-xr-x   1 root root 4096 Jan  3 02:56 docker-entrypoint.d
...

# ps 명령 시도 (실패!)
root@e08c35352ff3:/# ps -elf
bash: ps: command not found

# 컨테이너에서 나가기
root@e08c35352ff3:/# exit
```

**왜 `ps`가 없을까?**
```
┌─────────────────────────────────────────────────────────┐
│              컨테이너 = 최소한의 구성                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   목적:                                                  │
│   ┌─────────────────────────────────────────────┐      │
│   │  ✅ 크기 최소화 (경량)                       │      │
│   │  ✅ 공격 표면 감소 (보안)                    │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   결과:                                                  │
│   ┌─────────────────────────────────────────────┐      │
│   │  ❌ 불필요한 도구 미포함 (ps, vim, curl...)  │      │
│   │  ✅ 필수 앱만 포함 (nginx만!)                │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   💡 해결책: docker debug (Docker Desktop 전용)         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> 💬 **비유**: 컨테이너는 미니멀리스트 아파트와 같다. 살기에 필요한 것만 있고, 불필요한 가구는 없다.

---

### 6. 컨테이너 중지 및 삭제 (Stop & Remove)

```bash
# 컨테이너 중지 (몇 초 소요될 수 있음)
$ docker stop test
test

# 컨테이너 삭제
$ docker rm test
test

# 모든 컨테이너 확인 (중지된 것 포함)
$ docker ps -a
CONTAINER ID    IMAGE    COMMAND    CREATED    STATUS    PORTS    NAMES
```

**명령어 정리:**

| 명령어 | 설명 |
|--------|------|
| `docker stop <name>` | 컨테이너 중지 (graceful) |
| `docker rm <name>` | 컨테이너 삭제 |
| `docker rm -f <name>` | 강제 중지 + 삭제 |
| `docker ps -a` | 모든 컨테이너 조회 (중지 포함) |

---

### 7. Ops 워크플로우 요약

```
┌─────────────────────────────────────────────────────────┐
│                 Ops 워크플로우 요약                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1️⃣ 확인      docker version                           │
│        │                                                │
│        ▼                                                │
│   2️⃣ 다운로드   docker pull nginx:latest                │
│        │                                                │
│        ▼                                                │
│   3️⃣ 실행      docker run --name test -d -p 8080:80    │
│        │       nginx:latest                            │
│        ▼                                                │
│   4️⃣ 접속      docker exec -it test bash               │
│        │                                                │
│        ▼                                                │
│   5️⃣ 종료      docker stop test                        │
│        │                                                │
│        ▼                                                │
│   6️⃣ 삭제      docker rm test                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Part 2: Dev 관점 (개발 관점)

### 8. 애플리케이션 소스 가져오기

```bash
# GitHub에서 애플리케이션 클론
$ git clone https://github.com/nigelpoulton/psweb.git
Cloning into 'psweb'...
remote: Enumerating objects: 63, done.
...

# 디렉토리 이동 및 내용 확인
$ cd psweb

$ ls -l
total 32
-rw-r--r--  1 user  staff  324  Dockerfile      # ← 핵심!
-rw-r--r--  1 user  staff  378  README.md
-rw-r--r--  1 user  staff  341  app.js
-rw-r--r--  1 user  staff  355  package.json
drwxr-xr-x  3 user  staff   96  views
```

---

### 9. Dockerfile 이해

```dockerfile
FROM alpine
LABEL maintainer="nigelpoulton@hotmail.com"
RUN apk add --update nodejs npm curl
COPY . /src
WORKDIR /src
RUN  npm install
EXPOSE 8080
ENTRYPOINT ["node", "./app.js"]
```

**각 명령어 설명:**

```
┌─────────────────────────────────────────────────────────┐
│                  Dockerfile 해부                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  FROM alpine                                            │
│  └── 베이스 이미지 (Alpine Linux)                        │
│                                                         │
│  LABEL maintainer="nigelpoulton@hotmail.com"            │
│  └── 메타데이터 (관리자 정보)                            │
│                                                         │
│  RUN apk add --update nodejs npm curl                   │
│  └── 패키지 설치 (Node.js, npm, curl)                   │
│                                                         │
│  COPY . /src                                            │
│  └── 현재 디렉토리 파일을 /src로 복사                    │
│                                                         │
│  WORKDIR /src                                           │
│  └── 작업 디렉토리 설정                                  │
│                                                         │
│  RUN npm install                                        │
│  └── 의존성 설치                                        │
│                                                         │
│  EXPOSE 8080                                            │
│  └── 8080 포트 노출 (문서화 목적)                        │
│                                                         │
│  ENTRYPOINT ["node", "./app.js"]                        │
│  └── 컨테이너 시작 시 실행할 명령                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

> 💬 **비유**: Dockerfile은 요리 레시피다. 재료(FROM), 준비(RUN), 담기(COPY), 서빙(ENTRYPOINT)까지 모든 단계가 정의되어 있다.

---

### 10. 이미지 빌드 (Build)

```bash
# 이미지 빌드 (psweb 디렉토리에서 실행)
$ docker build -t test:latest .
[+] Building 36.2s (11/11) FINISHED
 => [internal] load .dockerignore                    0.0s
 => [internal] load build definition from Dockerfile 0.0s
 ...
 => => naming to docker.io/library/test:latest       0.0s
 => => unpacking to docker.io/library/test:latest    0.7s

# 생성된 이미지 확인
$ docker images
REPO     TAG      IMAGE ID        CREATED          SIZE
test     latest   0435f2738cf6    21 seconds ago   160MB
```

**`docker build` 명령어:**

| 요소 | 설명 |
|------|------|
| `-t test:latest` | 이미지 이름과 태그 |
| `.` | 빌드 컨텍스트 (현재 디렉토리) |

```
┌─────────────────────────────────────────────────────────┐
│                  이미지 빌드 과정                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────┐                                   │
│   │   Source Code   │  app.js, package.json, views/     │
│   └────────┬────────┘                                   │
│            │                                            │
│            │ + Dockerfile                               │
│            ▼                                            │
│   ┌─────────────────┐                                   │
│   │  docker build   │                                   │
│   │   -t test:latest│                                   │
│   │        .        │                                   │
│   └────────┬────────┘                                   │
│            │                                            │
│            │ 각 명령어 순차 실행                         │
│            │ (FROM → RUN → COPY → ...)                  │
│            ▼                                            │
│   ┌─────────────────┐                                   │
│   │  Docker Image   │  test:latest (160MB)              │
│   │   ┌─────────┐   │                                   │
│   │   │ Alpine  │   │  ← 베이스 이미지                   │
│   │   │ Node.js │   │  ← 런타임                         │
│   │   │  app.js │   │  ← 애플리케이션                   │
│   │   │  deps   │   │  ← 의존성                         │
│   │   └─────────┘   │                                   │
│   └─────────────────┘                                   │
│                                                         │
│   🎉 "Containerizing an app" = 앱을 이미지로 빌드!       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 11. 컨테이너로 실행

```bash
# 컨테이너 실행
$ docker run -d \
  --name web1 \
  --publish 8080:8080 \
  test:latest

# 브라우저에서 확인
# Docker Desktop: localhost:8080 또는 127.0.0.1:8080
# Multipass: 192.168.x.x:8080
```

**결과:**

```
┌─────────────────────────────────────────────────────────┐
│                   브라우저 결과                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────────────────────────────────────┐      │
│   │  🌐 http://localhost:8080                   │      │
│   ├─────────────────────────────────────────────┤      │
│   │                                             │      │
│   │           ┌─────────────────┐              │      │
│   │           │                 │              │      │
│   │           │   Hello from    │              │      │
│   │           │   Docker!       │              │      │
│   │           │                 │              │      │
│   │           └─────────────────┘              │      │
│   │                                             │      │
│   └─────────────────────────────────────────────┘      │
│                                                         │
│   🎉 앱이 컨테이너에서 성공적으로 실행됨!                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 12. 정리 (Clean Up)

```bash
# 컨테이너 강제 삭제
$ docker rm web1 -f
web1

# 이미지 삭제
$ docker rmi test:latest
Untagged: test:latest
Deleted: sha256:0435f27...cac8e2b
```

---

### 13. Dev 워크플로우 요약

```
┌─────────────────────────────────────────────────────────┐
│                 Dev 워크플로우 요약                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   1️⃣ 코드 가져오기   git clone <repo>                   │
│        │                                                │
│        ▼                                                │
│   2️⃣ Dockerfile 작성/확인                               │
│        │                                                │
│        ▼                                                │
│   3️⃣ 이미지 빌드    docker build -t myapp:latest .     │
│        │           ("Containerizing")                   │
│        ▼                                                │
│   4️⃣ 컨테이너 실행   docker run -d --name app          │
│        │            -p 8080:8080 myapp:latest          │
│        ▼                                                │
│   5️⃣ 테스트         브라우저에서 확인                   │
│        │                                                │
│        ▼                                                │
│   6️⃣ 정리          docker rm -f app                    │
│                     docker rmi myapp:latest            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 심화 학습

### 핵심 명령어 치트시트

| 명령어 | 설명 |
|--------|------|
| `docker version` | 버전 확인 |
| `docker images` | 이미지 목록 |
| `docker pull <image>` | 이미지 다운로드 |
| `docker build -t <name> .` | 이미지 빌드 |
| `docker run -d --name <name> -p <host>:<container> <image>` | 컨테이너 실행 |
| `docker ps` | 실행 중 컨테이너 |
| `docker ps -a` | 모든 컨테이너 |
| `docker exec -it <name> bash` | 컨테이너 접속 |
| `docker stop <name>` | 컨테이너 중지 |
| `docker rm <name>` | 컨테이너 삭제 |
| `docker rmi <image>` | 이미지 삭제 |

---

## 💡 실무 적용 포인트

### 면접 질문

**Q1: `docker run`과 `docker exec`의 차이는 무엇인가요?**
```
A: docker run: 새로운 컨테이너를 생성하고 시작합니다.
   docker exec: 이미 실행 중인 컨테이너 내부에서 명령을 실행합니다.

   예시:
   - docker run nginx → 새 nginx 컨테이너 생성 및 시작
   - docker exec -it mycontainer bash → 실행 중인 컨테이너에 셸 접속
```

**Q2: `-d` 플래그 없이 `docker run`을 실행하면 어떻게 되나요?**
```
A: 컨테이너가 포그라운드(attached) 모드로 실행됩니다.

   결과:
   - 터미널이 컨테이너 출력을 표시
   - Ctrl+C로 컨테이너가 중지됨
   - 터미널을 사용할 수 없음

   -d (detached)는 백그라운드 실행으로 터미널을 반환합니다.
```

**Q3: Dockerfile의 `ENTRYPOINT`와 `CMD`의 차이는?**
```
A: 둘 다 컨테이너 시작 시 실행할 명령을 지정하지만:

   ENTRYPOINT: 항상 실행되는 기본 명령 (변경 어려움)
   CMD: 기본 인자, docker run 시 덮어쓰기 가능

   예시:
   ENTRYPOINT ["node"]
   CMD ["app.js"]

   → docker run myapp → node app.js 실행
   → docker run myapp test.js → node test.js 실행 (CMD만 덮어씀)
```

**Q4: 컨테이너에서 `ps` 같은 기본 명령어가 없는 이유는?**
```
A: 두 가지 이유:

   1. 크기 최소화: 불필요한 도구를 제외하여 이미지를 작게 유지
   2. 보안 강화: 공격 표면(attack surface)을 줄임

   해결책:
   - docker debug (Docker Desktop)
   - 멀티스테이지 빌드로 디버깅 도구 포함 이미지 별도 생성
   - docker exec로 필요한 패키지 설치 후 실행
```

---

## ✅ 체크리스트

### Ops 관점
- [ ] `docker version`으로 Client/Server 상태를 확인할 수 있다
- [ ] `docker pull`로 이미지를 다운로드할 수 있다
- [ ] `docker run`의 `-d`, `-p`, `--name` 플래그를 이해한다
- [ ] `docker exec -it <container> bash`로 컨테이너에 접속할 수 있다
- [ ] `docker stop`과 `docker rm`으로 컨테이너를 정리할 수 있다
- [ ] `docker ps -a`로 모든 컨테이너(중지 포함)를 볼 수 있다

### Dev 관점
- [ ] Dockerfile의 각 명령어(FROM, RUN, COPY, WORKDIR, EXPOSE, ENTRYPOINT)를 이해한다
- [ ] `docker build -t <name> .`로 이미지를 빌드할 수 있다
- [ ] "Containerizing"이 무엇을 의미하는지 설명할 수 있다
- [ ] 소스코드 → Dockerfile → 이미지 → 컨테이너 흐름을 설명할 수 있다

### 종합
- [ ] Ops와 Dev 워크플로우를 각각 설명할 수 있다
- [ ] DevOps 관점에서 두 워크플로우가 어떻게 연결되는지 이해한다

---

## 🔗 참고 자료

- 📘 [Docker CLI Reference](https://docs.docker.com/reference/cli/docker/)
- 📘 [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- 📘 [Docker Hub](https://hub.docker.com/)
- 📘 [샘플 앱 저장소](https://github.com/nigelpoulton/psweb)
