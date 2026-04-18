# Ch02. Docker Setup & First Run - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Docker Desktop과 Docker Engine의 내부 아키텍처 차이는?

### 왜 이 질문이 중요한가
"Docker Desktop을 사용하면 안 되는 상황"과 "반드시 사용해야 하는 상황"을 구분하려면 둘의 근본적 차이를 이해해야 한다.

### 답변

**Docker Engine (서버용)**:
```
┌─────────────────────────────────────┐
│         Linux Host                  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │     dockerd (daemon)          │  │
│  │     containerd                │  │
│  │     runc                      │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│     ┌────────────────────┐          │
│     │   Containers       │          │
│     │   (Native Linux)   │          │
│     └────────────────────┘          │
└─────────────────────────────────────┘
```
- 패키지: dockerd + CLI만
- 의존성: systemd로 서비스 관리
- 사용자: 서버 환경, 프로덕션

**Docker Desktop (개발자용)**:
```
┌─────────────────────────────────────┐
│       macOS / Windows Host          │
│                                     │
│  ┌───────────────────────────────┐  │
│  │   Docker Desktop GUI          │  │ ← UI
│  ├───────────────────────────────┤  │
│  │   Docker CLI (Client)         │  │ ← CLI
│  ├───────────────────────────────┤  │
│  │   Extensions (Plugins)        │  │ ← 확장
│  ├───────────────────────────────┤  │
│  │   Kubernetes (Optional)       │  │ ← K8s
│  ├───────────────────────────────┤  │
│  │   Docker Compose              │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │   Linux VM (내장)             │  │ ← 핵심 차이
│  │   ┌─────────────────────────┐ │  │
│  │   │  dockerd              │ │  │
│  │   │  containerd           │ │  │
│  │   │  runc                 │ │  │
│  │   │  Containers           │ │  │
│  │   └─────────────────────────┘ │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```
- 패키지: VM + dockerd + GUI + Extensions + K8s
- 의존성: Hypervisor (macOS: Hypervisor.framework, Windows: Hyper-V/WSL 2)
- 사용자: 개발 환경

**Docker Desktop만의 기능**:

1. **docker scout**: 이미지 취약점 스캔
   ```bash
   docker scout quickview myapp:latest
   docker scout cves myapp:latest
   ```

2. **docker debug**: Slim 이미지 디버깅
   ```bash
   docker debug mycontainer
   # → vim, ping, nslookup 등 도구 일시 마운트
   ```

3. **docker init**: 프로젝트 자동 Dockerize
   ```bash
   docker init
   # → 언어 감지 → Dockerfile/compose.yaml 자동 생성
   ```

4. **Extensions Marketplace**:
   - Disk Usage: 스토리지 사용량 시각화
   - Logs Explorer: 로그 검색 UI
   - Resource Usage: 리소스 모니터링
   - Tailscale: VPN 통합

5. **통합 Kubernetes 클러스터**:
   - Settings → Kubernetes → Enable
   - 로컬 K8s 클러스터 즉시 사용 (minikube 불필요)

6. **파일 공유 최적화**:
   - macOS: VirtioFS (빠른 볼륨 마운트)
   - Windows: WSL 2 통합

**라이선스 차이**:
- Engine: 완전 무료 (오픈소스)
- Desktop: 대기업 유료 (직원 250명+ 또는 매출 $10M+)

**실제 사용 시나리오**:

**Docker Desktop 적합**:
- 로컬 개발 (Mac/Windows)
- 보안 스캔 필요 (scout)
- GUI 선호
- K8s 로컬 테스트

**Docker Engine 적합**:
- Linux 서버
- CI/CD 파이프라인
- 프로덕션 배포
- 라이선스 비용 절감

**성능 차이**:
- Linux 네이티브 Engine: 100% 성능
- Docker Desktop (Mac/Windows): VM 오버헤드 5~10%

### 실무 적용
- **개발 환경 구축**: 팀 전체에 Docker Desktop 설치 → 일관된 환경
- **CI/CD**: Jenkins/GitLab Runner에는 Docker Engine 사용 (경량)
- **라이선스 절약**: 대기업은 개발자 PC만 Desktop, 서버는 Engine
- **보안 스캔**: scout이 필요하면 Desktop, 불필요하면 Trivy 같은 대체 도구

---

## Q2. Build-Ship-Run 파이프라인의 각 단계에서 일어나는 일은?

### 왜 이 질문이 중요한가
"이미지를 어떻게 배포하나요?"라는 질문에 단순히 "docker push"라고 답하는 것을 넘어, 전체 워크플로우와 각 단계의 내부 동작을 이해해야 한다.

### 답변

**전체 파이프라인**:
```
┌─────────┐      ┌─────────┐      ┌─────────┐
│  Build  │ ───► │  Ship   │ ───► │   Run   │
│  (Dev)  │      │(Registry│      │  (Ops)  │
└─────────┘      └─────────┘      └─────────┘
```

**Build 단계 (docker build)**:

```bash
docker build -t myapp:v1 .
```

**내부 동작**:
1. **Build Context 생성**:
   - 현재 디렉토리(`.`)의 모든 파일을 tar로 압축
   - dockerd에 전송
   - `.dockerignore`로 제외 파일 지정 가능

2. **Dockerfile 파싱**:
   - 각 명령어 순차 실행
   - 각 명령어 = 하나의 레이어

3. **레이어 캐싱**:
   ```dockerfile
   FROM node:18          # Layer 1 (캐시 가능)
   COPY package.json .   # Layer 2 (package.json 변경 시만 재빌드)
   RUN npm install       # Layer 3 (Layer 2 변경 시만 재빌드)
   COPY . .              # Layer 4 (소스 변경 시마다 재빌드)
   ```
   - 레이어 재사용 → 빌드 속도 향상

4. **이미지 생성**:
   - 최종 레이어 스택을 이미지로 저장
   - 이미지 ID (SHA256 해시) 생성
   - 태그(myapp:v1) 부여

**BuildKit 최적화 (Docker 18.09+)**:
```bash
DOCKER_BUILDKIT=1 docker build .
```
- 병렬 빌드 (독립적 단계 동시 실행)
- 증분 전송 (변경된 파일만)
- 더 나은 캐싱

**Ship 단계 (docker push)**:

```bash
docker push myregistry.com/myapp:v1
```

**내부 동작**:
1. **레이어 분석**:
   - 이미지를 구성하는 레이어 목록 추출
   - 각 레이어의 SHA256 해시 계산

2. **레지스트리 체크**:
   - 레지스트리에 이미 존재하는 레이어 확인
   - 존재하는 레이어는 스킵 (중복 전송 방지)

3. **레이어 압축 및 전송**:
   ```
   Layer 1 (base image)     → [이미 존재] 스킵
   Layer 2 (dependencies)   → [이미 존재] 스킵
   Layer 3 (app code)       → [새 레이어] gzip 압축 → 전송
   ```

4. **Manifest 생성**:
   - 레이어 목록 + 설정 정보
   - Manifest를 레지스트리에 업로드
   - 태그와 Manifest 연결

**Distribution Hash vs Content Hash**:
- Distribution Hash: gzip 압축된 레이어 해시 (전송 중 검증)
- Content Hash: 비압축 레이어 해시 (로컬 저장 검증)
- 같은 레이어여도 다르게 보일 수 있음

**Run 단계 (docker pull + run)**:

```bash
docker pull myregistry.com/myapp:v1
docker run -d myapp:v1
```

**Pull 내부 동작**:
1. **Manifest 다운로드**:
   - 태그로 Manifest 요청
   - Manifest List인 경우 호스트 아키텍처에 맞는 Manifest 선택

2. **레이어 다운로드**:
   ```
   952132ac251a: Downloading [>          ] 100KB/50MB
   82659f8f1b76: Already exists  ← 로컬에 이미 있음
   c19118ca682d: Download complete
   ```
   - 병렬 다운로드 (동시에 여러 레이어)
   - 로컬에 없는 레이어만

3. **레이어 추출 및 검증**:
   - gzip 압축 해제
   - Content Hash 검증
   - `/var/lib/docker/overlay2/`에 저장

**Run 내부 동작**:
1. **이미지 → 컨테이너 변환**:
   - 읽기 전용 이미지 레이어 위에 R/W 레이어 생성
   - overlay2 드라이버로 단일 파일시스템 뷰 제공

2. **containerd/runc 호출**:
   - namespace 생성 (PID, Network, Mount, ...)
   - cgroup 설정 (CPU, Memory 제한)
   - 네트워크 설정 (포트 매핑)

3. **프로세스 시작**:
   - Entrypoint/Cmd 실행
   - PID 1로 앱 프로세스 시작

**전체 흐름 예시**:
```bash
# Dev 환경
cd myapp
docker build -t ghcr.io/mycompany/myapp:v1.2.3 .
docker push ghcr.io/mycompany/myapp:v1.2.3

# CI/CD 파이프라인에서 자동화
# (GitHub Actions / GitLab CI)

# Prod 환경
ssh prod-server
docker pull ghcr.io/mycompany/myapp:v1.2.3
docker run -d --name myapp \
  -p 443:8080 \
  --restart unless-stopped \
  ghcr.io/mycompany/myapp:v1.2.3
```

### 실무 적용
- **CI/CD 최적화**: 레이어 캐싱 활용 → 빌드 시간 10분 → 30초
- **네트워크 절약**: 베이스 이미지 공유 → 전송량 80% 절감
- **배포 속도**: 로컬 캐시된 레이어 재사용 → pull 시간 단축
- **롤백 전략**: 이전 태그로 즉시 롤백 가능

---

## Q3. 이미지 Pull 프로세스의 실제 네트워크 흐름은?

### 왜 이 질문이 중요한가
"이미지를 못 받아요"라는 문제를 디버깅하려면 Pull 과정에서 발생하는 HTTP 요청과 레지스트리 API를 이해해야 한다.

### 답변

**Pull 명령어**:
```bash
docker pull nginx:1.25
```

**실제 네트워크 흐름 (7단계)**:

**1단계: 레지스트리 확인**
```
Client → Registry API
GET https://registry-1.docker.io/v2/
```
- 응답: 401 Unauthorized + WWW-Authenticate 헤더
- 인증 서버 주소 포함

**2단계: 인증 토큰 획득**
```
Client → Auth Server
GET https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/nginx:pull
```
- 응답: Bearer 토큰
- 공개 이미지는 익명 토큰, 프라이빗은 로그인 필요

**3단계: Manifest 요청**
```
Client → Registry API
GET https://registry-1.docker.io/v2/library/nginx/manifests/1.25
Authorization: Bearer <token>
Accept: application/vnd.docker.distribution.manifest.v2+json
        application/vnd.docker.distribution.manifest.list.v2+json
```
- Manifest List 또는 Image Manifest 반환

**4단계: 아키텍처 선택 (Manifest List인 경우)**
```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.list.v2+json",
  "manifests": [
    {
      "platform": {"architecture": "amd64", "os": "linux"},
      "digest": "sha256:abc123..."
    },
    {
      "platform": {"architecture": "arm64", "os": "linux"},
      "digest": "sha256:def456..."
    }
  ]
}
```
- 호스트 아키텍처(linux/arm64) 확인
- 해당 Manifest 다시 요청

**5단계: Image Manifest 파싱**
```json
{
  "schemaVersion": 2,
  "config": {
    "digest": "sha256:config123...",
    "size": 7234
  },
  "layers": [
    {"digest": "sha256:layer1...", "size": 27145613},
    {"digest": "sha256:layer2...", "size": 3232112},
    {"digest": "sha256:layer3...", "size": 1234567}
  ]
}
```

**6단계: 레이어 다운로드 (병렬)**
```bash
# 각 레이어마다 별도 요청
GET /v2/library/nginx/blobs/sha256:layer1...
GET /v2/library/nginx/blobs/sha256:layer2...
GET /v2/library/nginx/blobs/sha256:layer3...

# 응답: gzip 압축된 tar 파일
# 다운로드 중 출력:
# layer1: Downloading [========>          ] 15MB/27MB
# layer2: Download complete
# layer3: Already exists  ← 로컬 캐시
```

**7단계: 레이어 추출 및 저장**
```bash
# gzip 압축 해제
# tar 추출
# Content Hash 검증
# overlay2 레이어로 저장: /var/lib/docker/overlay2/<hash>/
```

**Registry API v2 주요 엔드포인트**:

| 엔드포인트 | 용도 |
|-----------|------|
| `GET /v2/` | API 버전 확인 |
| `GET /v2/<name>/manifests/<tag>` | Manifest 가져오기 |
| `GET /v2/<name>/blobs/<digest>` | 레이어 다운로드 |
| `HEAD /v2/<name>/blobs/<digest>` | 레이어 존재 여부 확인 |
| `POST /v2/<name>/blobs/uploads/` | 레이어 업로드 시작 |
| `PUT /v2/<name>/manifests/<tag>` | Manifest 업로드 |

**실제 디버깅 예시**:

**문제: "Unable to pull image"**
```bash
# 1. DNS 확인
nslookup registry-1.docker.io

# 2. 레지스트리 연결 확인
curl https://registry-1.docker.io/v2/

# 3. 인증 확인
docker login

# 4. 프록시 설정 (회사 방화벽)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# 5. 레지스트리 미러 설정 (중국 등)
# /etc/docker/daemon.json
{
  "registry-mirrors": ["https://mirror.gcr.io"]
}
```

**Rate Limiting (Docker Hub)**:
- 익명 사용자: 6시간에 100회 pull
- 로그인 사용자: 6시간에 200회 pull
- 초과 시: `429 Too Many Requests`
- 해결: docker login 또는 프라이빗 레지스트리 사용

**Content-Addressable Storage**:
- 레이어는 내용(content)의 해시로 저장
- 같은 내용 = 같은 해시 → 자동 중복 제거
- `docker pull ubuntu` + `docker pull nginx` → 공통 레이어 재사용

### 실무 적용
- **프록시 환경**: 회사 방화벽 뒤에서 daemon.json에 프록시 설정
- **중국 등 제한 지역**: registry-mirrors로 속도 향상
- **프라이빗 레지스트리**: Harbor, Artifactory로 내부 레지스트리 구축
- **CI/CD**: Rate limiting 회피 위해 로컬 캐시 또는 프라이빗 레지스트리

---

## Q4. Linux 커널 의존성과 호환성 문제는?

### 왜 이 질문이 중요한가
"컨테이너는 호스트 커널을 공유한다"는 원칙이 실무에서 어떤 호환성 제약을 만드는지 이해해야 한다.

### 답변

**기본 원칙**:
- 컨테이너 = 호스트 커널 의존
- 컨테이너 내부 `/lib`, `/usr` 등은 독립적
- 하지만 시스템 콜은 호스트 커널로 전달

**커널 버전 호환성**:

**시나리오 1: 새로운 시스템 콜**
- 컨테이너 앱이 Linux 5.10+ 전용 시스템 콜 사용
- 호스트 커널: Linux 4.19
- 결과: `ENOSYS (Function not implemented)` 에러

**시나리오 2: 오래된 libc**
- 컨테이너: Ubuntu 14.04 (glibc 2.19)
- 호스트: Ubuntu 22.04 (Linux 5.15)
- 결과: 정상 동작 (하위 호환)

**실제 사례**:

**1. 파일시스템 타입**:
```bash
# 컨테이너에서 btrfs 마운트 시도
mount -t btrfs /dev/sda1 /mnt

# 호스트 커널에 btrfs 모듈 없으면
# mount: unknown filesystem type 'btrfs'
```

**2. 네트워크 기능**:
```bash
# eBPF 사용하는 최신 CNI 플러그인
# 호스트 커널 4.18+ 필요
# 호스트 커널 3.10 → 실패
```

**3. cgroup v2**:
- Systemd 기반 최신 배포판은 cgroup v2 사용
- 호스트가 cgroup v1만 지원 → 일부 기능 제한

**Alpine Linux의 특수성**:
```dockerfile
FROM alpine:3.19
RUN apk add python3
```
- Alpine은 glibc 대신 musl libc 사용
- 바이너리 호환성 문제 발생 가능
- 예: 상용 소프트웨어 (Oracle, IBM) → glibc 의존

**해결책**:
```dockerfile
# glibc 호환 레이어 추가
RUN apk add --no-cache libc6-compat
```

**컨테이너 내부 커널 버전 확인**:
```bash
# 컨테이너 내부
$ uname -r
5.15.0-91-generic  # ← 호스트 커널 버전!

# 컨테이너 OS 버전
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.6 LTS"

# 불일치 가능: Ubuntu 20.04 컨테이너 + Ubuntu 22.04 호스트
# → 호스트 커널(5.15) 사용, 컨테이너 userspace(20.04)
```

**Kernel Feature 확인**:
```bash
# seccomp 지원 확인
grep CONFIG_SECCOMP /boot/config-$(uname -r)

# cgroup v2 확인
mount | grep cgroup2

# namespace 확인
ls /proc/$$/ns/
```

**호환성 매트릭스**:

| 컨테이너 | 호스트 커널 | 결과 |
|---------|-----------|------|
| Ubuntu 20.04 | Ubuntu 22.04 (5.15) | ✅ 정상 |
| Ubuntu 22.04 | Ubuntu 18.04 (4.15) | ⚠️ 일부 기능 제한 |
| Alpine 3.19 | RHEL 8 (4.18) | ✅ 정상 (musl은 독립적) |
| CentOS 7 | Ubuntu 22.04 | ✅ 정상 |

**실무 문제 사례**:

**1. 오래된 호스트 커널**:
- RHEL 7 (커널 3.10) 호스트
- 최신 Docker 이미지 (overlay2 필요, 4.0+)
- 해결: 커널 업그레이드 또는 devicemapper 사용

**2. 최신 앱 요구사항**:
- Cilium CNI → eBPF → 커널 4.19+
- GKE, EKS는 자동 커널 업그레이드
- 온프레미스는 수동 관리 필요

**3. GPU/특수 하드웨어**:
- NVIDIA GPU → 호스트에 NVIDIA 드라이버 설치 필수
- 컨테이너는 `/dev/nvidia*` 장치 마운트
- 커널 모듈은 호스트 의존

### 실무 적용
- **베이스 이미지 선택**: Alpine은 가볍지만 호환성 문제 → Debian/Ubuntu가 안전
- **호스트 커널 관리**: 정기 업그레이드로 최신 기능 지원
- **Kubernetes**: 노드 OS 업그레이드 전략 수립 (rolling update)
- **테스트**: 프로덕션과 동일한 커널 버전에서 테스트

---

## Q5. Docker 설치 트러블슈팅 시나리오와 해결 방법은?

### 왜 이 질문이 중요한가
설치 단계에서 발생하는 문제를 빠르게 해결하려면 일반적인 오류 패턴과 진단 방법을 알아야 한다.

### 답변

**시나리오 1: Permission Denied (Linux)**

**증상**:
```bash
$ docker ps
Got permission denied while trying to connect to the Docker daemon socket
```

**원인**: 현재 사용자가 docker 그룹에 없음

**해결**:
```bash
# docker 그룹에 사용자 추가
sudo usermod -aG docker $USER

# 로그아웃 후 재로그인 (또는)
newgrp docker

# 확인
docker ps
```

**시나리오 2: WSL 2 미설치 (Windows)**

**증상**:
```
Docker Desktop requires Windows Subsystem for Linux 2
```

**해결**:
```powershell
# PowerShell (관리자 권한)
wsl --install

# 기본 배포판 설치
wsl --set-default-version 2

# Docker Desktop 재설치
```

**시나리오 3: Virtualization 비활성화**

**증상** (Windows):
```
Hardware assisted virtualization and data execution protection must be enabled in the BIOS
```

**증상** (Mac):
```
Hypervisor.framework is not available
```

**해결**:
- BIOS/UEFI 진입 (재부팅 시 F2/F10/Del)
- Intel VT-x / AMD-V 활성화
- Hyper-V 활성화 (Windows)

**⚠️ 주의**: BIOS 설정 변경은 신중히

**시나리오 4: 포트 충돌**

**증상**:
```bash
docker run -p 80:80 nginx
Error: bind: address already in use
```

**진단**:
```bash
# Linux
sudo lsof -i :80
sudo netstat -tulpn | grep :80

# macOS
sudo lsof -i :80

# Windows
netstat -ano | findstr :80
```

**해결**:
```bash
# 다른 포트 사용
docker run -p 8080:80 nginx

# 또는 기존 프로세스 종료
sudo kill <PID>
```

**시나리오 5: Docker Daemon 미실행 (Linux)**

**증상**:
```bash
$ docker ps
Cannot connect to the Docker daemon
```

**진단 및 해결**:
```bash
# 상태 확인
sudo systemctl status docker

# 시작
sudo systemctl start docker

# 부팅 시 자동 시작
sudo systemctl enable docker

# 로그 확인
sudo journalctl -u docker -f
```

**시나리오 6: 스토리지 부족**

**증상**:
```
no space left on device
```

**진단**:
```bash
# 디스크 사용량 확인
df -h

# Docker 스토리지 확인
docker system df

# 상세 정보
docker system df -v
```

**해결**:
```bash
# 정리
docker system prune -a --volumes

# 또는 선택적 삭제
docker image prune  # 사용 안 하는 이미지
docker container prune  # 중지된 컨테이너
docker volume prune  # 사용 안 하는 볼륨
```

**시나리오 7: DNS 문제**

**증상**:
```bash
docker run alpine ping google.com
ping: bad address 'google.com'
```

**원인**: 컨테이너가 DNS 서버 접근 불가

**해결**:
```bash
# /etc/docker/daemon.json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}

# Docker 재시작
sudo systemctl restart docker
```

**시나리오 8: 프록시 환경**

**증상**: 이미지 pull 실패

**해결**:
```bash
# /etc/systemd/system/docker.service.d/http-proxy.conf
[Service]
Environment="HTTP_PROXY=http://proxy.company.com:8080"
Environment="HTTPS_PROXY=http://proxy.company.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1"

# Reload
sudo systemctl daemon-reload
sudo systemctl restart docker
```

**시나리오 9: macOS에서 느린 파일 공유**

**증상**: 볼륨 마운트 시 성능 저하

**해결**:
```bash
# Docker Desktop → Settings → Resources → File Sharing
# VirtioFS 활성화

# 또는 명시적 마운트 옵션
docker run -v $(pwd):/app:cached myapp
# cached = 호스트 → 컨테이너 전파 지연 허용
```

**시나리오 10: Docker Desktop 시작 실패 (Mac)**

**증상**: "Docker Desktop is starting..." 무한 대기

**해결**:
```bash
# 완전 초기화
rm -rf ~/Library/Group\ Containers/group.com.docker
rm -rf ~/Library/Containers/com.docker.docker

# Docker Desktop 재설치
```

### 실무 적용
- **자동화된 설치 스크립트**: Ansible/Chef로 일관된 환경 구축
- **모니터링**: 디스크 사용량 알림 설정 → 자동 정리
- **문서화**: 사내 트러블슈팅 가이드 작성
- **컨테이너 헬스체크**: 정기적 `docker system df` 실행

---

## Q6. 프록시 환경에서 Docker 설정은?

### 왜 이 질문이 중요한가
기업 환경에서는 인터넷 접근이 프록시를 통해 제한되는 경우가 많아, 프록시 설정 없이는 이미지 pull조차 불가능하다.

### 답변

**3가지 프록시 설정이 필요한 이유**:

1. **dockerd (daemon)**: 이미지 pull/push 시
2. **컨테이너 런타임**: 컨테이너 내부 네트워크
3. **Docker CLI**: 레지스트리 인증 시

**1. Docker Daemon 프록시 설정**:

**systemd 기반 (Ubuntu, RHEL)**:
```bash
# 디렉토리 생성
sudo mkdir -p /etc/systemd/system/docker.service.d

# 프록시 설정 파일
sudo vi /etc/systemd/system/docker.service.d/http-proxy.conf
```

```ini
[Service]
Environment="HTTP_PROXY=http://proxy.company.com:8080"
Environment="HTTPS_PROXY=http://proxy.company.com:8080"
Environment="NO_PROXY=localhost,127.0.0.1,.company.com,10.0.0.0/8"
```

```bash
# Reload 및 재시작
sudo systemctl daemon-reload
sudo systemctl restart docker

# 확인
sudo systemctl show --property=Environment docker
```

**2. 컨테이너 런타임 프록시**:

**방법 A: daemon.json (모든 컨테이너 기본값)**:
```bash
# /etc/docker/daemon.json
{
  "proxies": {
    "http-proxy": "http://proxy.company.com:8080",
    "https-proxy": "http://proxy.company.com:8080",
    "no-proxy": "localhost,127.0.0.1,.company.com"
  }
}
```

**방법 B: docker run 시 환경변수**:
```bash
docker run -e HTTP_PROXY=http://proxy.company.com:8080 \
           -e HTTPS_PROXY=http://proxy.company.com:8080 \
           -e NO_PROXY=localhost,127.0.0.1 \
           alpine sh
```

**방법 C: Dockerfile에서**:
```dockerfile
FROM alpine

# Build time
ARG HTTP_PROXY=http://proxy.company.com:8080
ARG HTTPS_PROXY=http://proxy.company.com:8080

# Runtime
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}

RUN apk add --no-cache curl
```

**빌드 시 프록시 전달**:
```bash
docker build --build-arg HTTP_PROXY=$HTTP_PROXY \
             --build-arg HTTPS_PROXY=$HTTPS_PROXY \
             -t myapp .
```

**3. Docker Desktop 프록시 (Mac/Windows)**:

**GUI 설정**:
- Docker Desktop → Settings → Resources → Proxies
- Manual proxy configuration
  - HTTP Proxy: `http://proxy.company.com:8080`
  - HTTPS Proxy: `http://proxy.company.com:8080`
  - No Proxy: `localhost,127.0.0.1,.company.com`

**CLI 설정** (Mac):
```bash
# ~/.docker/config.json
{
  "proxies": {
    "default": {
      "httpProxy": "http://proxy.company.com:8080",
      "httpsProxy": "http://proxy.company.com:8080",
      "noProxy": "localhost,127.0.0.1,.company.com"
    }
  }
}
```

**NO_PROXY 패턴**:
```bash
NO_PROXY=localhost,127.0.0.1,.company.com,10.0.0.0/8,*.local
```
- `localhost`, `127.0.0.1`: 로컬호스트
- `.company.com`: 도메인 와일드카드
- `10.0.0.0/8`: CIDR 블록
- `*.local`: 도메인 패턴

**인증이 필요한 프록시**:
```bash
HTTP_PROXY=http://username:password@proxy.company.com:8080
```

**⚠️ 주의**: 비밀번호에 특수문자 있으면 URL 인코딩
- `@` → `%40`
- `:` → `%3A`

**프록시 우회 (내부 레지스트리)**:
```bash
# 내부 Harbor 레지스트리
NO_PROXY=harbor.company.com,10.0.0.0/8
```

**디버깅**:
```bash
# 프록시 테스트
docker run --rm alpine sh -c "apk add curl && curl -I https://google.com"

# 프록시 환경변수 확인
docker run --rm alpine env | grep -i proxy

# dockerd 환경변수 확인
sudo systemctl show docker | grep -i proxy
```

**Docker Compose 프록시**:
```yaml
services:
  web:
    image: nginx
    environment:
      - HTTP_PROXY=http://proxy.company.com:8080
      - HTTPS_PROXY=http://proxy.company.com:8080
      - NO_PROXY=localhost,127.0.0.1
```

### 실무 적용
- **자동화**: Ansible 플레이북으로 프록시 설정 자동 배포
- **보안**: 비밀번호는 환경변수나 Secret으로 관리
- **CI/CD**: GitLab Runner, Jenkins에도 동일한 프록시 설정
- **내부 레지스트리**: NO_PROXY로 내부 트래픽 최적화

---

## Q7. Docker Desktop 라이선스 정책과 대체 솔루션은?

### 왜 이 질문이 중요한가
2021년 Docker Desktop 유료화 이후, 기업 환경에서 라이선스 비용과 대체 솔루션을 고려해야 한다.

### 답변

**라이선스 정책 (2024년 기준)**:

**무료 사용 가능**:
- 개인 사용 (Personal Use)
- 교육 목적 (Education)
- 비영리 단체 (Non-profit)
- 소규모 기업:
  - 직원 250명 미만 AND
  - 연 매출 $10M 미만

**유료 구독 필요**:
- 직원 250명 이상 OR
- 연 매출 $10M 이상
- 업무용 사용

**가격**:
- Personal: $0
- Pro: $7/월 (개인)
- Team: $11/월/인 (최소 5명)
- Business: $24/월/인 (최소 50명)

**유료 구독 이점**:
- Docker Scout (보안 스캔)
- Docker Build Cloud
- 우선 지원
- SSO 통합 (Business)

**대체 솔루션 비교**:

**1. Podman Desktop**:
```bash
# 설치 (Mac)
brew install podman
podman machine init
podman machine start

# 사용법 (docker 명령과 동일)
podman run -d -p 8080:80 nginx
podman ps
podman build -t myapp .
```

**장점**:
- 완전 무료 (오픈소스)
- Daemonless (rootless 기본)
- Docker 호환 API

**단점**:
- scout, debug 같은 Docker Desktop 전용 기능 없음
- GUI 미성숙 (Podman Desktop은 개발 중)
- macOS에서 VM 필요 (docker와 동일)

**2. Rancher Desktop**:
```bash
# 설치 (Mac)
brew install --cask rancher

# 특징
# - containerd 또는 dockerd 선택 가능
# - Kubernetes 통합
# - nerdctl (containerd CLI)
```

**장점**:
- 무료 (오픈소스)
- K8s 포함
- GUI 있음

**단점**:
- Docker CLI 대신 nerdctl 사용 (일부 명령 차이)
- Extensions 없음

**3. Colima (macOS)**:
```bash
# 설치
brew install colima docker

# 시작
colima start

# Docker CLI 사용
docker run hello-world
```

**장점**:
- 경량 (Docker Desktop 대비 1/10 메모리)
- Docker CLI 완전 호환
- 무료

**단점**:
- macOS 전용
- GUI 없음 (CLI만)

**4. Lima + nerdctl (macOS/Linux)**:
```bash
# 설치
brew install lima

# VM 시작
limactl start

# nerdctl 사용
lima nerdctl run -d nginx
```

**장점**:
- 경량
- containerd 기반
- 무료

**단점**:
- 학습 곡선 (nerdctl 문법 차이)

**5. Linux 네이티브 Docker Engine**:
```bash
# Ubuntu
sudo apt install docker.io

# RHEL/CentOS
sudo yum install docker-ce
```

**장점**:
- 완전 무료
- 프로덕션 환경과 동일
- 최고 성능 (VM 없음)

**단점**:
- Linux 전용
- GUI 없음

**마이그레이션 전략**:

**시나리오 1: 개발자 PC (Mac/Windows)**
```
Before: Docker Desktop (유료 라이선스 필요)
         ↓
After:   Rancher Desktop (무료)
         또는 Podman Desktop (무료)
```

**시나리오 2: CI/CD 서버**
```
Before: Docker Desktop on Windows Server
         ↓
After:   Linux VM + Docker Engine (무료)
```

**시나리오 3: 소규모 스타트업**
```
- 직원 50명, 매출 $5M
- → Docker Desktop 무료 사용 가능
```

**시나리오 4: 대기업**
```
옵션 A: Docker Desktop 구독 ($24/월 × 500명 = $144K/년)
옵션 B: Rancher Desktop 전환 (무료, 마이그레이션 비용 1회)
옵션 C: Linux 개발 환경 전환 (무료, 학습 곡선)
```

**실제 전환 사례**:

**1. 게임 회사 A**:
- 개발자 300명 → Rancher Desktop 전환
- 비용 절감: $86K/년
- 마이그레이션 시간: 1주일

**2. 핀테크 B**:
- Docker Scout 필요 → Docker Desktop Business 유지
- 대신 CI/CD 서버는 Linux Engine 사용

**3. 스타트업 C**:
- 직원 100명 → 무료 사용 가능
- 성장 후 재평가 계획

**호환성 체크리스트**:
```bash
# Docker Compose 호환
docker compose up  # Desktop
podman compose up  # Podman (플러그인 필요)
rancher compose up # Rancher (docker CLI)

# BuildKit
DOCKER_BUILDKIT=1 docker build  # Desktop
podman build --squash  # Podman (일부 차이)

# Extensions
# → Desktop 전용, 대체 불가
```

### 실무 적용
- **비용 분석**: 직원 수 × $24 × 12 vs 마이그레이션 비용
- **기능 요구사항**: scout/debug 필요 시 Desktop, 불필요 시 대체
- **점진적 전환**: 일부 팀만 먼저 대체 도구 테스트
- **정책 수립**: 회사 규모에 맞는 Docker 사용 정책 문서화
