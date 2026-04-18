# 01-docker: Docker 핵심 개념과 실전 활용

> **프로젝트 개요**
> 이 프로젝트는 `docs/03_CloudNative/01_Docker/`의 이론을 실습 중심으로 재구성한 학습 자료입니다. VM에서 컨테이너로의 진화, Docker 플랫폼의 작동 원리, 이미지 빌드부터 운영까지 전 과정을 실전 예제와 함께 다룹니다. 13개 챕터를 통해 기초부터 고급 주제(보안, Swarm, AI, WebAssembly)까지 단계적으로 학습합니다.

---

## 📚 챕터 목록

| Ch | 제목 | 시간 | 핵심 주제 |
|----|------|------|----------|
| 01 | Container Fundamentals & Standards | 30m | VM vs Container, OCI/CNCF/Moby, 컨테이너 진화사 |
| 02 | Docker Setup & First Run | 30m | Docker Desktop/Multipass 설치, build-ship-run |
| 03 | Docker Engine Internals | 45m | containerd/runc, 네임스페이스, cgroups |
| 04 | Working with Images | 45m | 이미지 레이어, 레지스트리, 멀티아키텍처 |
| 05 | Container Lifecycle | 45m | 시작/중지/재시작, 로그, 리소스 제한 |
| 06 | Containerizing Applications | 60m | Dockerfile 작성, 멀티스테이지 빌드, 최적화 |
| 07 | Multi-container Apps with Compose | 60m | Docker Compose, 서비스 정의, 네트워크/볼륨 |
| 08 | Docker Networking | 60m | Bridge/Host/Overlay, 서비스 디스커버리 |
| 09 | Volumes & Persistent Data | 45m | 볼륨 타입, 바인드 마운트, 데이터 백업 |
| 10 | Docker Security | 45m | 이미지 스캔, 시크릿 관리, 네트워크 격리 |
| 11 | Docker Swarm vs Kubernetes | 30m | 오케스트레이션 비교, 선택 기준 |
| 12 | Docker & AI | 30m | GPU 컨테이너, Model Runner, LLM 배포 |
| 13 | Docker & WebAssembly | 30m | Wasm 런타임, 경량화, 미래 전망 |

**총 학습 시간**: 약 8시간 30분

---

## 📂 디렉토리 구조

```
01-docker/
├── README.md                          # 이 파일
├── learning/                          # 학습 자료 (13개 챕터)
│   ├── 01-container-fundamentals/
│   │   ├── LEARN.md                   # 컨테이너 기초와 표준
│   │   └── INVESTIGATE.md             # OCI 스펙 상세 분석
│   ├── 02-setup-first-run/
│   │   ├── LEARN.md                   # Docker 설치와 첫 실행
│   │   └── INVESTIGATE.md             # Docker Desktop 아키텍처
│   ├── 03-engine-internals/
│   │   ├── LEARN.md                   # Docker Engine 내부 구조
│   │   └── INVESTIGATE.md             # containerd/runc 심화
│   ├── 04-images/
│   │   ├── LEARN.md                   # 이미지 관리
│   │   └── INVESTIGATE.md             # 레이어 최적화 기법
│   ├── 05-container-lifecycle/
│   │   ├── LEARN.md                   # 컨테이너 생명주기
│   │   └── INVESTIGATE.md             # 상태 관리 패턴
│   ├── 06-containerizing-apps/
│   │   ├── LEARN.md                   # 앱 컨테이너화
│   │   └── INVESTIGATE.md             # 멀티스테이지 빌드 패턴
│   ├── 07-compose/
│   │   ├── LEARN.md                   # Docker Compose
│   │   └── INVESTIGATE.md             # 복잡한 스택 구성
│   ├── 08-networking/
│   │   ├── LEARN.md                   # Docker 네트워킹
│   │   └── INVESTIGATE.md             # Overlay 네트워크 상세
│   ├── 09-volumes/
│   │   ├── LEARN.md                   # 볼륨과 데이터 관리
│   │   └── INVESTIGATE.md             # 스토리지 드라이버
│   ├── 10-security/
│   │   ├── LEARN.md                   # Docker 보안
│   │   └── INVESTIGATE.md             # Content Trust, Secrets
│   ├── 11-orchestration/
│   │   ├── LEARN.md                   # Swarm vs K8s
│   │   └── INVESTIGATE.md             # 오케스트레이션 패턴
│   ├── 12-ai/
│   │   ├── LEARN.md                   # Docker & AI
│   │   └── INVESTIGATE.md             # GPU 컨테이너 최적화
│   └── 13-wasm/
│       ├── LEARN.md                   # Docker & WebAssembly
│       └── INVESTIGATE.md             # Wasm 런타임 비교
└── practice/                          # 실습 프로젝트
    ├── simple-app/                    # Ch06: 기본 앱 컨테이너화
    │   ├── Dockerfile
    │   ├── app.js
    │   └── package.json
    ├── multi-stage/                   # Ch06: 멀티스테이지 빌드
    │   ├── Dockerfile
    │   └── go-app/
    ├── compose-stack/                 # Ch07: Compose 스택
    │   ├── docker-compose.yml
    │   ├── web/
    │   ├── api/
    │   └── db/
    ├── networking/                    # Ch08: 네트워크 실습
    │   └── network-demo.sh
    ├── volumes/                       # Ch09: 볼륨 실습
    │   └── volume-demo.sh
    ├── security/                      # Ch10: 보안 실습
    │   ├── scan-demo.sh
    │   └── secrets-demo/
    ├── swarm/                         # Ch11: Swarm 실습
    │   └── swarm-init.sh
    ├── ai-runner/                     # Ch12: AI 모델 실습
    │   └── llm-container/
    └── wasm/                          # Ch13: Wasm 실습
        └── wasm-demo/
```

---

## 🎯 학습 순서 가이드

### 1단계: 기초 (Ch01-02) - 1시간
**목표**: Docker가 무엇이고 왜 필요한지 이해
- Ch01: 컨테이너 기초 개념과 VM 대비 장점
- Ch02: Docker 설치 및 첫 컨테이너 실행

**체크포인트**:
- [ ] VM과 컨테이너의 차이를 설명할 수 있다
- [ ] `docker run nginx`를 실행하고 브라우저로 확인할 수 있다

---

### 2단계: 중급 (Ch03-07) - 4.5시간
**목표**: 이미지 빌드부터 멀티 컨테이너 앱까지 실전 활용
- Ch03: Docker Engine 내부 구조 (containerd, runc)
- Ch04: 이미지 관리 (레이어, 레지스트리)
- Ch05: 컨테이너 생명주기 관리
- Ch06: Dockerfile 작성과 앱 컨테이너화
- Ch07: Docker Compose로 멀티 컨테이너 구성

**체크포인트**:
- [ ] Dockerfile을 작성하여 자신의 앱을 이미지로 빌드할 수 있다
- [ ] Docker Compose로 웹+DB 스택을 실행할 수 있다
- [ ] 이미지 레이어 최적화 기법 3가지를 설명할 수 있다

---

### 3단계: 고급 (Ch08-10) - 2.5시간
**목표**: 운영 환경을 위한 네트워크, 스토리지, 보안
- Ch08: Docker 네트워킹 (Bridge, Overlay)
- Ch09: 볼륨과 퍼시스턴트 데이터
- Ch10: Docker 보안 (스캔, 시크릿, 격리)

**체크포인트**:
- [ ] 커스텀 네트워크를 생성하고 컨테이너 간 통신을 설정할 수 있다
- [ ] 볼륨을 사용하여 데이터를 영구 보존할 수 있다
- [ ] `docker scout`로 이미지 취약점을 스캔할 수 있다

---

### 4단계: 전문 (Ch11-13) - 1.5시간
**목표**: 오케스트레이션, AI, 미래 기술 탐색
- Ch11: Docker Swarm vs Kubernetes
- Ch12: Docker & AI (GPU, Model Runner)
- Ch13: Docker & WebAssembly

**체크포인트**:
- [ ] Swarm과 Kubernetes의 선택 기준을 설명할 수 있다
- [ ] Docker로 로컬 LLM을 실행할 수 있다
- [ ] Wasm과 컨테이너의 차이와 미래 전망을 설명할 수 있다

---

## 🔧 실습 환경 설정

### 권장 설치 방법
```bash
# macOS/Windows: Docker Desktop (권장)
# https://www.docker.com/products/docker-desktop

# 설치 확인
docker version
docker-compose version

# 테스트 실행
docker run hello-world
```

### Multipass 대안 (Docker Desktop 사용 불가 시)
```bash
# Multipass 설치
# https://multipass.run/install

# Docker VM 생성
multipass launch docker --name docker-node
multipass shell docker-node
```

---

## 📖 학습 팁

### 각 챕터 학습 패턴
1. **LEARN.md 읽기**: 개념과 워크플로우 이해
2. **실습 프로젝트 실행**: practice/ 디렉토리의 예제 직접 실행
3. **INVESTIGATE.md 심화**: 궁금한 부분 깊이 탐구
4. **체크리스트 완료**: 핵심 개념 확인

### 효과적인 학습 방법
- **실습 우선**: 이론보다 먼저 `docker run`을 직접 실행해보세요
- **에러는 학습 기회**: 에러 메시지를 읽고 이해하는 연습
- **작은 단위로**: 챕터당 하루에 1-2개씩 소화
- **노트 작성**: 실수한 부분, 헷갈린 개념을 기록

---

## 🔗 다음 단계

### 02-kubernetes
Docker를 마스터한 후에는 Kubernetes로 넘어가세요.

**연결 포인트**:
- Docker 이미지 → K8s Pod
- Docker Compose → K8s Deployment
- Docker Swarm → K8s Cluster

**추천 순서**:
```
01-docker (이 프로젝트)
    ↓
02-kubernetes
    ↓
03-helm (K8s 패키지 관리)
    ↓
04-service-mesh (Istio/Linkerd)
```

---

## 📚 참고 자료

### 공식 문서
- [Docker Docs](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [OCI Specs](https://opencontainers.org/)
- [CNCF Projects](https://www.cncf.io/projects/)

### 추천 도서
- **Docker Deep Dive** by Nigel Poulton (이 학습 자료의 원천)
- **The Kubernetes Book** by Nigel Poulton

### 커뮤니티
- [Docker Community Forums](https://forums.docker.com/)
- [r/docker](https://www.reddit.com/r/docker/)
- [Docker Discord](https://discord.gg/docker)

---

## ✅ 학습 완료 체크리스트

### 기초 마스터
- [ ] VM과 컨테이너의 차이를 비유로 설명할 수 있다
- [ ] OCI 3대 표준을 나열할 수 있다
- [ ] Docker Desktop을 설치하고 버전을 확인할 수 있다

### 실전 활용
- [ ] Dockerfile을 작성하여 이미지를 빌드할 수 있다
- [ ] Docker Compose로 3-tier 앱을 구성할 수 있다
- [ ] 이미지 레이어를 최적화할 수 있다

### 운영 능력
- [ ] 커스텀 네트워크를 생성할 수 있다
- [ ] 볼륨으로 데이터를 영구 보존할 수 있다
- [ ] `docker scout`로 보안 스캔을 실행할 수 있다

### 고급 주제
- [ ] Swarm과 Kubernetes의 차이를 설명할 수 있다
- [ ] Docker로 GPU 기반 AI 모델을 실행할 수 있다
- [ ] Wasm과 컨테이너의 미래를 전망할 수 있다

---

**Happy Dockering!** 🐳
