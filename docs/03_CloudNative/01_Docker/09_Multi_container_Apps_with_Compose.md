# Chapter 9: Multi-container Apps with Compose

## 📌 핵심 요약

> **Docker Compose**는 멀티 컨테이너 마이크로서비스 애플리케이션을 **YAML 파일 하나로 정의**하고, **단일 명령어로 배포/관리**할 수 있게 해주는 도구이다. 복잡한 스크립트나 긴 docker 명령어 대신, 선언적 구성 파일로 전체 애플리케이션 라이프사이클을 관리한다.

---

## 🎯 학습 목표

- [ ] Docker Compose의 개념과 탄생 배경 이해
- [ ] Compose 파일(compose.yaml) 구조 파악
- [ ] services, networks, volumes 블록 작성법 습득
- [ ] docker compose 명령어로 앱 배포/관리 실습
- [ ] 프로젝트 네이밍 규칙과 리소스 관리 이해

---

## 📖 본문 정리

### 1. Docker Compose란?

#### 💬 비유로 이해하기
> Compose 파일은 **오케스트라 악보**와 같다. 지휘자(docker compose)가 악보(compose.yaml)를 읽고, 각 악기(컨테이너)들이 언제, 어떻게 연주할지 조율한다. 복잡한 교향곡(마이크로서비스 앱)도 하나의 악보로 완벽하게 연주할 수 있다.

#### 마이크로서비스 애플리케이션 구성 예시
```
┌─────────────────────────────────────────────────────────┐
│                   마이크로서비스 앱                        │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │ Web     │  │ Ordering│  │ Catalog │  │ Auth    │    │
│  │ Frontend│  │ Service │  │ Service │  │ Service │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       │            │            │            │          │
│       └────────────┴─────┬──────┴────────────┘          │
│                          │                              │
│              ┌───────────┴───────────┐                  │
│              │   Backend Datastore   │                  │
│              │   (Redis, MySQL 등)   │                  │
│              └───────────────────────┘                  │
└─────────────────────────────────────────────────────────┘

        ↓ Compose 파일 하나로 전체 정의 및 배포 ↓

┌─────────────────────────────────────────────────────────┐
│  compose.yaml                                           │
│  ─────────────                                          │
│  services:                                              │
│    web-fe: ...                                          │
│    ordering: ...                                        │
│    catalog: ...                                         │
│    auth: ...                                            │
│    datastore: ...                                       │
│  networks: ...                                          │
│  volumes: ...                                           │
└─────────────────────────────────────────────────────────┘
```

### 2. Compose 탄생 배경

```
┌─────────────────────────────────────────────────────────┐
│                    Compose 역사                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Orchard Labs        Docker, Inc.         현재          │
│       │                  인수                │           │
│       ▼                   │                 ▼           │
│  ┌─────────┐         ┌────┴────┐      ┌──────────┐     │
│  │   Fig   │   →     │ Docker  │  →   │  docker  │     │
│  │ (Python)│         │ Compose │      │ compose  │     │
│  └─────────┘         └─────────┘      │ (서브커맨드) │  │
│       │                   │           └──────────┘     │
│    fig CLI          docker-compose      docker CLI      │
│                          CLI           통합 완료        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Compose Specification**
- 커뮤니티 주도의 오픈 스탠다드
- Docker 구현체와 별도로 관리 (거버넌스 분리)
- Docker Compose는 레퍼런스 구현체

### 3. Compose 파일 구조

#### 기본 구조 (Top-level Keys)

```yaml
services:      # 필수 - 마이크로서비스 정의
  web-fe:
    ...
  redis:
    ...

networks:      # 선택 - 네트워크 정의
  counter-net:

volumes:       # 선택 - 볼륨 정의
  counter-vol:
```

#### 샘플 애플리케이션 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│                    Sample App                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   Host Port 5001                                        │
│        │                                                │
│        ▼                                                │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   web-fe     │         │    redis     │             │
│  │ ──────────── │         │ ──────────── │             │
│  │ Python Flask │◄───────►│ Redis:alpine │             │
│  │  Port 8080   │  counter│   Port 6379  │             │
│  │              │   -net  │              │             │
│  └──────────────┘         └──────┬───────┘             │
│                                  │                      │
│                                  ▼                      │
│                           ┌──────────────┐             │
│                           │ counter-vol  │             │
│                           │   /data      │             │
│                           └──────────────┘             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### 완전한 Compose 파일 예시

```yaml
services:
  web-fe:                          # 서비스 이름
    deploy:
      replicas: 1                  # 컨테이너 복제본 수
    build: .                       # Dockerfile 위치 (현재 디렉토리)
    command: python app/app.py    # 컨테이너 실행 명령
    ports:
      - target: 8080               # 컨테이너 내부 포트
        published: 5001            # 호스트 노출 포트
    networks:
      - counter-net                # 연결할 네트워크

  redis:
    image: "redis:alpine"          # 사용할 이미지 (Docker Hub)
    deploy:
      replicas: 1
    networks:
      - counter-net
    volumes:
      - type: volume
        source: counter-vol        # 볼륨 이름
        target: /data              # 컨테이너 내 마운트 경로

networks:
  counter-net:                     # 네트워크 정의

volumes:
  counter-vol:                     # 볼륨 정의
```

#### 서비스 정의 상세 분석

| 속성 | 설명 | 예시 |
|------|------|------|
| `build` | Dockerfile 위치 | `.` (현재 디렉토리) |
| `image` | 사용할 이미지 | `redis:alpine` |
| `deploy.replicas` | 컨테이너 복제본 수 | `1` |
| `command` | 컨테이너 실행 명령 | `python app.py` |
| `ports.target` | 컨테이너 내부 포트 | `8080` |
| `ports.published` | 호스트 노출 포트 | `5001` |
| `networks` | 연결할 네트워크 | `- counter-net` |
| `volumes.source` | 볼륨 이름 | `counter-vol` |
| `volumes.target` | 마운트 경로 | `/data` |

### 4. 프로젝트 네이밍 규칙

Docker Compose는 **빌드 컨텍스트 디렉토리명**을 프로젝트 이름으로 사용한다.

```
빌드 컨텍스트: /path/to/multi-container/
                            ↓
                    프로젝트명: multi-container
```

#### 리소스 네이밍 패턴

| 리소스 타입 | 정의된 이름 | 실제 생성 이름 |
|-------------|-------------|----------------|
| 서비스 (web-fe) | web-fe | `multi-container-web-fe-1` |
| 서비스 (redis) | redis | `multi-container-redis-1` |
| 네트워크 | counter-net | `multi-container_counter-net` |
| 볼륨 | counter-vol | `multi-container_counter-vol` |
| 이미지 | (빌드된 경우) | `multi-container-web-fe:latest` |

```
네이밍 패턴:
┌─────────────────────────────────────────────────────┐
│ 컨테이너: {프로젝트명}-{서비스명}-{복제본번호}       │
│           multi-container-web-fe-1                  │
│                                                     │
│ 네트워크/볼륨: {프로젝트명}_{리소스명}              │
│               multi-container_counter-net           │
└─────────────────────────────────────────────────────┘
```

### 5. 앱 배포 (docker compose up)

#### 배포 명령어

```bash
# 기본 배포 (백그라운드 실행)
$ docker compose up --detach

# 특정 Compose 파일 지정
$ docker compose -f apps/sample-app.yml up --detach
```

#### 배포 과정

```
docker compose up --detach
        │
        ▼
┌───────────────────────────────────────────────────┐
│ 1. Compose 파일 파싱 (compose.yaml)               │
├───────────────────────────────────────────────────┤
│ 2. 이미지 준비                                    │
│    - build: . → Dockerfile로 이미지 빌드          │
│    - image: redis:alpine → Docker Hub에서 Pull    │
├───────────────────────────────────────────────────┤
│ 3. 네트워크 생성                                  │
│    - multi-container_counter-net Created          │
├───────────────────────────────────────────────────┤
│ 4. 볼륨 생성                                      │
│    - multi-container_counter-vol Created          │
├───────────────────────────────────────────────────┤
│ 5. 컨테이너 시작                                  │
│    - multi-container-redis-1 Started              │
│    - multi-container-web-fe-1 Started             │
└───────────────────────────────────────────────────┘
```

### 6. 앱 관리 명령어

#### 명령어 비교표

| 명령어 | 동작 | 컨테이너 | 네트워크 | 볼륨 | 이미지 |
|--------|------|----------|----------|------|--------|
| `docker compose stop` | 정지 | 유지 | 유지 | 유지 | 유지 |
| `docker compose down` | 삭제 | **삭제** | **삭제** | 유지 | 유지 |
| `docker compose down --volumes` | 삭제+볼륨 | **삭제** | **삭제** | **삭제** | 유지 |
| `docker compose down --volumes --rmi all` | 완전 삭제 | **삭제** | **삭제** | **삭제** | **삭제** |

#### 앱 라이프사이클 관리

```
┌─────────────────────────────────────────────────────────┐
│                  Compose 앱 라이프사이클                  │
└─────────────────────────────────────────────────────────┘

                    docker compose up
                          │
                          ▼
                   ┌──────────────┐
                   │   Running    │◄──────────────────┐
                   └──────┬───────┘                   │
                          │                           │
          docker compose  │  docker compose           │ docker compose
               stop       │      down                 │    restart
                          ▼                           │
                   ┌──────────────┐                   │
                   │   Stopped    │───────────────────┘
                   └──────┬───────┘
                          │
          docker compose  │
          down --volumes  │
          --rmi all       │
                          ▼
                   ┌──────────────┐
                   │   Removed    │ (볼륨, 이미지까지 삭제)
                   └──────────────┘
```

#### 주요 관리 명령어

```bash
# 앱 상태 확인
$ docker compose ps
NAME                       SERVICE    STATUS        PORTS
multi-container-redis-1    redis      Up 33 sec     6379/tcp
multi-container-web-fe-1   web-fe     Up 33 sec     0.0.0.0:5001->8080

# 컨테이너 내부 프로세스 확인
$ docker compose top
multi-container-redis-1
UID   PID     CMD
lxd   12023   redis-server *:6379

multi-container-web-fe-1
UID    PID     CMD
root   12024   python app/app.py

# 전체 Compose 앱 목록 확인
$ docker compose ls
NAME               STATUS       CONFIG FILES
multi-container    running(2)   /path/to/compose.yaml

# 앱 정지 (컨테이너 유지)
$ docker compose stop

# 앱 재시작
$ docker compose restart

# 앱 삭제 (볼륨, 이미지는 유지)
$ docker compose down

# 완전 정리 (볼륨, 이미지까지 삭제)
$ docker compose down --volumes --rmi all
```

### 7. 데이터 영속성

#### 볼륨을 통한 데이터 보존

```
┌─────────────────────────────────────────────────────────┐
│                데이터 영속성 흐름                        │
└─────────────────────────────────────────────────────────┘

  1. 앱 실행 → 웹페이지 방문 → 카운터 증가 (예: 42회)
                                    │
                                    ▼
                           Redis 컨테이너
                           ┌──────────────┐
                           │   /data      │
                           │  count: 42   │
                           └──────┬───────┘
                                  │ 마운트
                                  ▼
                           ┌──────────────┐
                           │ counter-vol  │ ← 볼륨에 저장
                           │  count: 42   │
                           └──────────────┘

  2. docker compose down (볼륨은 유지됨)
                           ┌──────────────┐
                           │ counter-vol  │ ← 여전히 존재
                           │  count: 42   │
                           └──────────────┘

  3. docker compose up (재배포)
                           Redis 컨테이너 (새로 생성)
                           ┌──────────────┐
                           │   /data      │
                           │  count: 42   │ ← 기존 데이터 복원!
                           └──────┬───────┘
                                  │ 마운트
                                  ▼
                           ┌──────────────┐
                           │ counter-vol  │
                           │  count: 42   │
                           └──────────────┘
```

### 8. 서비스 간 통신

```yaml
# app.py 코드
cache = redis.Redis(host='redis', port=6379)
#                        ↑
#                   서비스 이름으로 통신
```

```
┌─────────────────────────────────────────────────────────┐
│                  서비스 간 DNS 기반 통신                  │
└─────────────────────────────────────────────────────────┘

  ┌────────────────┐                ┌────────────────┐
  │    web-fe      │                │     redis      │
  │ ────────────── │                │ ────────────── │
  │                │    "redis"     │                │
  │  redis.Redis(  │ ─────────────► │   Port 6379    │
  │   host='redis' │   DNS 해석     │                │
  │  )             │                │                │
  └────────────────┘                └────────────────┘
          │                                  │
          └──────────────┬───────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │   counter-net      │
              │ (Docker Network)   │
              │                    │
              │ 내부 DNS 서버가     │
              │ 서비스명 → IP 해석  │
              └────────────────────┘
```

---

## 🔍 심화 학습

### Compose Specification
- **공식 문서**: https://compose-spec.io/
- Docker 구현체와 별개로 커뮤니티에서 관리하는 오픈 스탠다드

### 추가 학습 주제
- **docker compose watch**: 개발 중 파일 변경 감지 및 자동 재시작
- **Profiles**: 환경별(dev/prod) 서비스 그룹 관리
- **Extends**: Compose 파일 상속 및 확장
- **Secrets/Configs**: 민감 정보 및 설정 파일 관리

---

## 💡 실무 적용 포인트

### 면접 대비 질문

**Q1: docker compose stop과 docker compose down의 차이점은?**
> **A**: `stop`은 컨테이너를 정지만 하고 유지하여 `restart`로 빠르게 재시작 가능하다. `down`은 컨테이너와 네트워크를 삭제하지만, 볼륨과 이미지는 기본적으로 유지한다. 완전 정리하려면 `--volumes`와 `--rmi all` 플래그를 사용한다.

**Q2: Compose 파일에서 build와 image의 차이는?**
> **A**: `build`는 Dockerfile을 기반으로 이미지를 직접 빌드하며, `image`는 이미 존재하는 이미지(Docker Hub 등)를 pull해서 사용한다. 커스텀 앱은 `build`, 공식 이미지(DB, 캐시 등)는 `image`를 사용하는 것이 일반적이다.

**Q3: Compose에서 서비스 간 통신은 어떻게 이루어지는가?**
> **A**: 같은 네트워크에 연결된 서비스들은 **서비스 이름**으로 서로를 참조할 수 있다. Docker의 내장 DNS 서버가 서비스명을 해당 컨테이너의 IP로 해석해준다. 예: `redis.Redis(host='redis')`

**Q4: docker compose down 후에도 데이터가 보존되는 이유는?**
> **A**: `down` 명령은 기본적으로 볼륨을 삭제하지 않는다. 볼륨에 저장된 데이터(DB, 캐시 등)는 앱 재배포 시에도 유지되어 데이터 영속성을 보장한다. 볼륨까지 삭제하려면 `--volumes` 플래그를 명시해야 한다.

---

## ✅ 체크리스트

### 개념 이해
- [ ] Docker Compose의 목적과 장점 설명 가능
- [ ] Compose의 역사 (Fig → Docker Compose → docker compose 서브커맨드)
- [ ] Compose Specification과 Docker 구현체의 관계 이해

### Compose 파일 작성
- [ ] services, networks, volumes 블록 구조 이해
- [ ] 서비스 정의 속성 (build, image, ports, networks, volumes, command)
- [ ] 포트 매핑 (target vs published)
- [ ] 볼륨 마운트 (source vs target)

### 프로젝트 관리
- [ ] 프로젝트 네이밍 규칙 (빌드 컨텍스트 디렉토리명 기반)
- [ ] 리소스 네이밍 패턴 ({프로젝트명}-{서비스명}-{번호})
- [ ] 복제본(replicas) 개념 이해

### 명령어 활용
- [ ] `docker compose up --detach`: 앱 배포
- [ ] `docker compose ps`: 상태 확인
- [ ] `docker compose top`: 프로세스 확인
- [ ] `docker compose ls`: 앱 목록 확인
- [ ] `docker compose stop`: 앱 정지 (컨테이너 유지)
- [ ] `docker compose restart`: 앱 재시작
- [ ] `docker compose down`: 앱 삭제 (볼륨/이미지 유지)
- [ ] `docker compose down --volumes --rmi all`: 완전 정리

### 데이터 관리
- [ ] 볼륨을 통한 데이터 영속성 이해
- [ ] stop/down/restart에 따른 데이터 보존 여부 파악
- [ ] 서비스 간 DNS 기반 통신 원리

### 실무 적용
- [ ] Compose 파일을 버전 관리 시스템(Git)에 포함
- [ ] 개발 환경에서 멀티 컨테이너 앱 관리
- [ ] 마이크로서비스 아키텍처 문서화 도구로 활용

---

## 🔗 참고 자료

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [Compose Specification](https://compose-spec.io/)
- [Compose 파일 레퍼런스](https://docs.docker.com/compose/compose-file/)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 9
