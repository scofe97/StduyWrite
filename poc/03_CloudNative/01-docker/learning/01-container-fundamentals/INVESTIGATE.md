# Ch01. Container Fundamentals & Standards - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. VM과 컨테이너의 성능 차이를 정량적으로 수치화하면?

### 왜 이 질문이 중요한가
"컨테이너가 VM보다 빠르다"는 추상적 설명을 넘어, 실제 벤치마크 데이터를 이해하면 아키텍처 선택 시 근거 있는 결정을 내릴 수 있다.

### 답변

**부팅 시간 비교:**
- VM: 30초~수분 (전체 OS 부팅 필요)
- 컨테이너: 0.1~1초 (프로세스 시작만 필요)
- 실제 측정: nginx 컨테이너는 약 300ms, VM은 평균 45초

**메모리 오버헤드:**
- VM: Guest OS마다 512MB~2GB (최소 메모리)
- 컨테이너: 수 MB~수십 MB (앱 + 최소 라이브러리만)
- 예시: Ubuntu VM (1GB) vs Ubuntu 컨테이너 (70MB)

**밀도(Density) 비교:**
- 8GB RAM 호스트 기준
  - VM: 약 4~8개 (각 1GB OS + 앱)
  - 컨테이너: 수십~수백 개 (공유 커널)
- AWS Lambda 등 서버리스는 컨테이너 기반으로 밀리초 단위 cold start 달성

**I/O 성능:**
- VM: Hypervisor 계층을 거쳐 디스크/네트워크 접근
- 컨테이너: 호스트 커널 직접 접근
- 벤치마크: 컨테이너가 VM 대비 디스크 I/O 5~15% 빠름

**CPU 오버헤드:**
- VM: Hardware-assisted virtualization (VT-x) 사용해도 2~5% 오버헤드
- 컨테이너: 거의 네이티브 수준 (1% 미만)

### 실무 적용
- **마이크로서비스**: 빠른 스케일링이 필요하면 컨테이너 (수초 내 수십 개 인스턴스 생성)
- **레거시 앱**: OS 의존성이 강하거나 다른 커널 필요 시 VM
- **개발 환경**: 로컬에서 프로덕션 환경 모방 시 컨테이너로 빠른 반복 개발
- **비용 최적화**: 클라우드에서 동일 서버에 더 많은 앱 실행 → 컨테이너로 TCO 절감

---

## Q2. OCI 표준의 실질적 의미와 호환성 보장 범위는?

### 왜 이 질문이 중요한가
"OCI 표준을 따른다"는 말이 실무에서 무엇을 보장하는지, 어디까지 이식성이 있는지 이해해야 벤더 락인을 피할 수 있다.

### 답변

**OCI 표준 3가지 스펙:**
1. **image-spec (v1.1.0)**: 이미지 레이어 구조, 매니페스트, 설정 파일 형식
2. **runtime-spec (v1.2.0)**: 컨테이너 생성/실행 방법, config.json 형식
3. **distribution-spec (v1.1.0)**: 레지스트리 API, 이미지 push/pull 프로토콜

**표준이 보장하는 것:**
- Docker 이미지 → containerd, CRI-O, Podman에서 실행 가능
- Docker Hub 이미지 → Quay.io, Harbor, GHCR에서 pull 가능
- Kubernetes는 CRI를 통해 모든 OCI 호환 런타임 사용 가능
- runc 대신 youki, crun, gVisor 같은 다른 저수준 런타임 교체 가능

**표준이 보장하지 않는 것:**
- 상위 레벨 API (Docker API vs Podman API는 다름)
- 네트워킹 구현 (CNI 플러그인은 별도)
- 볼륨/스토리지 드라이버 (CSI는 별도)
- CLI 명령어 호환 (docker run vs podman run은 유사하지만 100% 동일 아님)

**실제 호환 시나리오:**
```bash
# Docker로 빌드한 이미지를 Podman으로 실행
docker build -t myapp:v1 .
podman pull docker.io/library/myapp:v1
podman run myapp:v1  # 문제 없이 실행

# Kubernetes는 containerd/CRI-O 사용
kubectl run nginx --image=nginx:latest  # OCI 이미지이므로 동작
```

**버전 업데이트 속도:**
- image-spec: 2017년 v1.0 → 2023년 v1.1 (6년)
- runtime-spec: 2017년 v1.0 → 2023년 v1.2 (6년)
- 이유: 저수준 표준은 안정성 우선, 신중한 변경

### 실무 적용
- **멀티 클라우드 전략**: OCI 이미지 사용 시 AWS ECS, GCP Cloud Run, Azure Container Apps 간 이동 용이
- **런타임 선택**: Docker Desktop 유료화 → Podman/Rancher Desktop으로 전환 시 이미지 재빌드 불필요
- **Kubernetes 마이그레이션**: Docker에서 빌드한 이미지를 K8s에서 그대로 사용
- **보안 강화**: gVisor(샌드박싱), Kata Containers(VM 격리) 같은 대체 런타임으로 교체 가능

---

## Q3. Linux namespace와 cgroup의 실제 동작 메커니즘은?

### 왜 이 질문이 중요한가
컨테이너의 "격리"와 "제한"이 커널 레벨에서 어떻게 구현되는지 이해하면 컨테이너 보안과 리소스 관리를 정확히 파악할 수 있다.

### 답변

**Namespace (격리) - 7가지 종류:**

1. **PID Namespace**: 프로세스 ID 격리
   - 컨테이너 내부에서 `ps`는 자신의 프로세스만 보임
   - 컨테이너의 PID 1 != 호스트의 실제 PID
   ```bash
   # 호스트에서
   ps aux | grep nginx  # PID 12345

   # 컨테이너 내부에서
   ps aux  # PID 1 (nginx)
   ```

2. **Network Namespace**: 네트워크 스택 격리
   - 각 컨테이너는 자신의 네트워크 인터페이스, IP, 라우팅 테이블 보유
   - veth pair로 호스트와 연결 (가상 이더넷)

3. **Mount Namespace**: 파일시스템 마운트 격리
   - 컨테이너는 자신의 루트 파일시스템 (`/`)을 가짐
   - overlay2 드라이버로 레이어 병합

4. **UTS Namespace**: 호스트명/도메인명 격리
   - 컨테이너마다 다른 hostname 설정 가능

5. **IPC Namespace**: 프로세스 간 통신 격리
   - 공유 메모리, 세마포어, 메시지 큐 격리

6. **User Namespace**: 사용자/그룹 ID 매핑
   - 컨테이너 내부 root(UID 0) ≠ 호스트 root
   - 보안 강화용 (rootless 컨테이너)

7. **Cgroup Namespace**: cgroup 트리 격리
   - cgroup v2에서 추가됨

**Cgroups (리소스 제한) - 주요 컨트롤러:**

1. **cpu**: CPU 시간 제한
   ```bash
   docker run --cpus=1.5 nginx  # 최대 1.5 코어 사용
   ```

2. **memory**: 메모리 제한
   ```bash
   docker run --memory=512m nginx  # 최대 512MB
   ```

3. **blkio**: 디스크 I/O 제한
   ```bash
   docker run --device-read-bps /dev/sda:10mb nginx
   ```

4. **pids**: 프로세스 개수 제한
   ```bash
   docker run --pids-limit=100 nginx
   ```

**cgroup v1 vs v2:**
- v1: 각 컨트롤러가 독립적 계층 (복잡)
- v2 (2016~): 통합 계층, 더 나은 리소스 분배
- Ubuntu 22.04+, RHEL 9+는 v2 기본

**실제 생성 과정 (runc):**
```bash
# runc가 실행하는 시스템 콜들
clone(CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS ...)  # namespace 생성
mount("overlay", "/var/lib/docker/overlay2/...")       # 파일시스템 마운트
echo "512000000" > /sys/fs/cgroup/memory/docker/<id>/memory.limit_in_bytes
```

### 실무 적용
- **보안 강화**: User Namespace로 컨테이너 내부 root 권한 무력화
- **리소스 할당**: cgroup으로 noisy neighbor 방지 (한 컨테이너가 CPU 독점 방지)
- **디버깅**: namespace 이해하면 컨테이너 네트워크 문제 해결 용이
- **Kubernetes QoS**: Guaranteed/Burstable/BestEffort는 cgroup 설정으로 구현됨

---

## Q4. 컨테이너 기술의 역사적 진화가 현재 아키텍처에 미친 영향은?

### 왜 이 질문이 중요한가
기술의 진화 과정을 이해하면 현재 설계 결정의 배경과 향후 발전 방향을 예측할 수 있다.

### 답변

**타임라인:**

**1979 - chroot**: Unix V7에서 루트 디렉토리 변경 (초기 격리)
- 영향: 현재 컨테이너의 파일시스템 격리 개념 기원

**2000 - FreeBSD Jails**: 완전한 프로세스 격리
- 영향: namespace 개념의 선구자

**2005 - Solaris Zones**: 상용 OS 수준 가상화
- 영향: 엔터프라이즈 컨테이너 개념 확립

**2008 - LXC (Linux Containers)**: cgroup + namespace 결합
- 영향: 최초의 완전한 Linux 컨테이너 구현
- 한계: 복잡한 CLI, 일반 개발자 접근 어려움

**2013 - Docker 출시**: LXC를 추상화
- 혁신: 단순한 API, 이미지 레이어링, 레지스트리
- 영향: 컨테이너 대중화의 결정적 계기

**2015 - rkt (CoreOS)**: Docker 독점 견제
- 영향: OCI 설립의 촉매제

**2015 - OCI 설립**: 표준화 시작
- Docker가 runc와 containerd 기부
- 영향: 생태계 다양성 확보, 벤더 락인 방지

**2016 - Kubernetes 1.0**: 컨테이너 오케스트레이션 표준화
- Docker Swarm 격차 확대
- 영향: 컨테이너 = 클라우드 네이티브의 기본 단위

**2020 - Kubernetes, dockershim 제거 발표**: containerd/CRI-O 직접 사용
- 영향: Docker는 개발 도구로, 프로덕션은 OCI 런타임 직접 사용

**2022 - Docker Desktop 유료화**: 대기업 대상
- 영향: Podman, Rancher Desktop 등 대체제 부상

**현재 아키텍처에 미친 영향:**

1. **모듈화**: 초기 모놀리식 Docker → containerd + runc 분리
   - 이유: Kubernetes 등이 재사용 가능하도록

2. **표준화**: OCI 덕분에 런타임 선택 자유
   - Docker, Podman, containerd 모두 호환

3. **레이어 시스템**: Docker가 도입한 이미지 레이어링
   - 이유: 스토리지 효율 + 빠른 배포

4. **레지스트리 중심**: Docker Hub가 정의한 Build-Share-Run
   - 이유: CI/CD 파이프라인의 핵심

5. **보안 진화**: gVisor, Kata Containers
   - 이유: 공유 커널의 보안 한계 보완

### 실무 적용
- **마이그레이션 전략**: Docker → Podman 전환 시 역사적 맥락 이해하면 호환성 예측 가능
- **아키텍처 선택**: Kubernetes 환경에서는 containerd 직접 사용이 표준
- **보안 요구사항**: 멀티 테넌시 환경에서는 Kata Containers(VM 격리) 고려
- **레거시 시스템**: LXC 기반 시스템을 Docker로 마이그레이션 시 격리 수준 차이 인지

---

## Q5. 컨테이너 보안의 한계와 강화 방법은?

### 왜 이 질문이 중요한가
"컨테이너는 VM만큼 안전하지 않다"는 비판을 이해하고, 실무에서 보안을 강화할 구체적 방법을 알아야 한다.

### 답변

**근본적 한계:**

1. **공유 커널 공격 표면**:
   - 모든 컨테이너가 같은 호스트 커널 사용
   - 커널 취약점 발견 시 모든 컨테이너 위험
   - 예: Dirty COW (CVE-2016-5195) → 컨테이너 탈출 가능

2. **Namespace 탈출 가능성**:
   - 특권 컨테이너(--privileged) 사용 시 호스트 접근 가능
   - 잘못된 capability 설정 시 namespace 탈출

3. **리소스 격리 불완전**:
   - `/proc`, `/sys` 일부는 호스트와 공유
   - cgroup 버그로 인한 DoS 가능성

**강화 방법 - 5단계 방어:**

**레벨 1: 최소 권한 원칙**
```bash
# 나쁜 예
docker run --privileged myapp

# 좋은 예
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE myapp
```
- 필요한 capability만 부여
- root 사용자 회피 (Dockerfile에서 USER 지정)

**레벨 2: Seccomp/AppArmor/SELinux**
```bash
# Seccomp 프로파일로 시스템 콜 제한
docker run --security-opt seccomp=custom.json myapp

# AppArmor 프로파일
docker run --security-opt apparmor=docker-default myapp
```
- 256개 이상의 시스템 콜 중 필요한 것만 허용

**레벨 3: User Namespace (Rootless)**
```bash
# 컨테이너 내부 UID 0 → 호스트 UID 100000으로 매핑
dockerd-rootless-setuptool.sh install
docker run --userns-remap=default myapp
```
- 컨테이너 탈출해도 호스트에서 권한 없음

**레벨 4: 이미지 보안**
```bash
# Docker Scout로 취약점 스캔
docker scout cves myapp:latest

# Distroless 이미지 사용 (공격 표면 최소화)
FROM gcr.io/distroless/python3
```
- 정기 스캔 + 자동 패치 적용

**레벨 5: 런타임 보안 (샌드박싱)**

**gVisor**: 샌드박스 커널
```bash
docker run --runtime=runsc myapp
```
- 장점: 시스템 콜 인터셉트, 커널 취약점 격리
- 단점: 10~20% 성능 오버헤드

**Kata Containers**: 경량 VM
```bash
docker run --runtime=kata-runtime myapp
```
- 장점: 하드웨어 수준 격리
- 단점: 부팅 시간 증가 (수백 ms)

**Firecracker**: AWS Lambda 기반 microVM
- 장점: VM 수준 격리 + 컨테이너급 시작 속도
- 단점: AWS 환경에 최적화

**실제 보안 사고 사례:**

1. **Tesla Kubernetes Hack (2018)**:
   - 공개된 Kubernetes 대시보드 → 크립토마이닝
   - 교훈: RBAC 설정 + 네트워크 정책 필수

2. **Docker Hub 침해 (2019)**:
   - 19만 계정 정보 유출
   - 교훈: 프라이빗 레지스트리 사용, 이미지 서명 (Notary)

3. **runC CVE-2019-5736**:
   - 컨테이너에서 호스트 runc 바이너리 덮어쓰기
   - 교훈: 런타임 정기 업데이트 필수

### 실무 적용
- **멀티 테넌시**: 서로 다른 고객 워크로드 → Kata Containers로 VM 수준 격리
- **규제 준수**: 금융/의료 → gVisor + 정기 감사
- **CI/CD 파이프라인**: 이미지 빌드 시 자동 보안 스캔 추가
- **제로 트러스트**: 컨테이너 간 통신도 mTLS 적용 (Service Mesh)

---

## Q6. Windows 컨테이너와 Linux 컨테이너의 근본적 차이는?

### 왜 이 질문이 중요한가
"컨테이너는 호스트 커널을 공유한다"는 원칙이 Windows에서 어떻게 다르게 구현되는지 이해하면 멀티 플랫폼 전략을 수립할 수 있다.

### 답변

**커널 아키텍처 차이:**

**Linux 컨테이너**:
- 단일 커널 (모든 컨테이너가 동일 커널 공유)
- namespace + cgroup으로 격리
- 경량 (MB 단위)

**Windows 컨테이너** (2가지 모드):

1. **Windows Server Containers** (Process Isolation):
   - Linux와 유사, 호스트 커널 공유
   - 요구사항: 컨테이너와 호스트의 Windows 버전 일치 필요
   - 예: Windows Server 2022 컨테이너 → Windows Server 2022 호스트만 가능

2. **Hyper-V Containers** (Hyper-V Isolation):
   - 각 컨테이너가 경량 VM 내부에서 실행
   - 호스트와 다른 Windows 버전 사용 가능
   - 더 강한 격리, 하지만 무겁고 느림

**버전 호환성 문제:**
```bash
# Linux
docker pull ubuntu:20.04  # 어떤 Linux 호스트에서든 실행 가능

# Windows
docker pull mcr.microsoft.com/windows/servercore:ltsc2022
# → Windows Server 2022 또는 Windows 11 호스트 필요
# → Windows Server 2019에서 실행 불가 (Process Isolation 모드)
```

**이미지 크기 비교:**
- Linux alpine: ~5MB
- Windows Nano Server: ~100MB
- Windows Server Core: ~2GB

**실제 사용 예시:**

**ASP.NET Framework (레거시)**:
```dockerfile
FROM mcr.microsoft.com/dotnet/framework/aspnet:4.8-windowsservercore-ltsc2022
WORKDIR /inetpub/wwwroot
COPY . .
```
- 반드시 Windows 컨테이너 필요
- 이유: .NET Framework는 Windows API 의존

**ASP.NET Core (크로스 플랫폼)**:
```dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY . .
```
- Linux 또는 Windows 컨테이너 모두 가능
- 권장: Linux 컨테이너 (작고 빠름)

**Windows 전용 기능:**
- Active Directory 인증
- Windows 인증 (NTLM, Kerberos)
- IIS (Internet Information Services)
- Windows 서비스 실행

**Docker Desktop on Windows 동작:**
```
┌─────────────────────────────────────┐
│       Windows 10/11 (Host)          │
│                                     │
│  ┌───────────────────────────────┐  │
│  │      WSL 2 (Linux VM)         │  │  ← Linux 컨테이너 실행
│  │  ┌─────────────────────────┐  │  │
│  │  │  Linux Containers       │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Windows Containers           │  │  ← Windows 컨테이너 실행
│  │  (Process/Hyper-V Isolation)  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

- 우클릭 → "Switch to Windows containers" 필요
- 두 모드를 동시에 실행 불가

### 실무 적용
- **.NET 마이그레이션**: .NET Framework → .NET Core로 전환 → Linux 컨테이너로 이동 (비용 절감)
- **하이브리드 환경**: Linux 컨테이너(신규) + Windows 컨테이너(레거시) 병행 운영
- **Kubernetes on Windows**: Windows 노드 + Linux 노드 혼합 클러스터 구성
- **라이선스 비용**: Windows Server Core 이미지는 Windows 라이선스 필요 → Nano Server로 최소화

---

## Q7. Rootless 컨테이너의 동작 원리와 트레이드오프는?

### 왜 이 질문이 중요한가
보안 강화를 위해 rootless 모드가 필수가 되어가는 추세에서, 구현 원리와 제약사항을 이해해야 적절히 활용할 수 있다.

### 답변

**기본 개념:**

**일반 컨테이너 (Rootful)**:
- dockerd가 root 권한으로 실행
- 컨테이너 내부 UID 0 = 호스트 UID 0
- 위험: 컨테이너 탈출 시 호스트 root 권한 획득

**Rootless 컨테이너**:
- dockerd를 일반 사용자 권한으로 실행
- User Namespace로 UID 매핑
- 컨테이너 내부 UID 0 → 호스트 UID 100000 (예시)

**UID 매핑 메커니즘:**
```bash
# /etc/subuid 설정
alice:100000:65536

# 의미
# 사용자 alice가
# 100000~165535 범위의 UID를 컨테이너에서 사용 가능
# 컨테이너 내부 UID 0 → 호스트 UID 100000
# 컨테이너 내부 UID 1 → 호스트 UID 100001
```

**실제 설정:**
```bash
# Rootless Docker 설치
dockerd-rootless-setuptool.sh install

# 컨테이너 실행
docker run -d nginx

# 호스트에서 프로세스 확인
ps aux | grep nginx
# alice  100000  ... nginx: master process
# alice  100001  ... nginx: worker process
```

**동작 원리 (slirp4netns):**

일반 Docker는 호스트 네트워크 스택을 직접 사용하지만, rootless는 권한 부족으로 불가능.
→ slirp4netns: 사용자 공간 네트워크 스택

```
┌─────────────────────────────────────┐
│         Host (as alice)             │
│                                     │
│  ┌───────────────────────────────┐  │
│  │   Container                   │  │
│  │   (UID 0 → Host UID 100000)   │  │
│  │                               │  │
│  │   App (Port 80)               │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│      slirp4netns (포트 포워딩)       │
│              │                       │
│              ▼                       │
│      Host Port 8080 (alice 소유)    │
└─────────────────────────────────────┘
```

**제약사항 (Trade-offs):**

1. **포트 바인딩 제한**:
   - 1024 미만 포트 바인딩 불가
   ```bash
   # rootful
   docker run -p 80:80 nginx  # OK

   # rootless
   docker run -p 80:80 nginx  # 실패
   docker run -p 8080:80 nginx  # OK
   ```

2. **네트워크 성능 저하**:
   - slirp4netns 오버헤드 → 10~20% 느림
   - 대안: 최신 커널(5.6+)에서 VPNKit 사용

3. **스토리지 드라이버 제한**:
   - overlay2 사용 불가 (권한 부족)
   - 대신 fuse-overlayfs 사용 (약간 느림)

4. **cgroup 제한**:
   - cgroup v1에서 리소스 제한 불가
   - cgroup v2 필요 (Ubuntu 22.04+)

5. **호스트 볼륨 마운트**:
   - 호스트 파일 소유자가 alice가 아니면 쓰기 불가
   - 해결: `--userns-remap` 또는 subuid/subgid 조정

**보안 이점:**

1. **컨테이너 탈출 무력화**:
   - 탈출해도 호스트에서 UID 100000 (일반 사용자)
   - root 권한 획득 불가

2. **CVE 영향 최소화**:
   - runC CVE-2019-5736 같은 취약점도 일반 사용자 권한만 획득

3. **멀티 테넌시**:
   - 각 사용자가 독립된 dockerd 실행 가능
   - 서로의 컨테이너 간섭 불가

**성능 벤치마크:**
- CPU: rootful과 동일 (99%)
- 메모리: rootful과 동일
- 네트워크: 10~20% 느림 (slirp4netns)
- 디스크 I/O: 5% 느림 (fuse-overlayfs)

**실무 도입 시나리오:**

**적합:**
- 개발 환경 (각 개발자가 rootless Docker 사용)
- CI/CD 러너 (GitLab Runner rootless 모드)
- 공유 서버 (여러 사용자가 독립적 컨테이너 실행)

**부적합:**
- 고성능 네트워킹 요구 (slirp4netns 오버헤드)
- 레거시 시스템 (cgroup v1만 지원)
- 특권 컨테이너 필요 (하드웨어 접근)

### 실무 적용
- **개발 환경 표준화**: 전사 개발자 PC에 rootless Docker 배포 → sudo 권한 불필요
- **보안 규정 준수**: 금융권에서 root 권한 사용 금지 정책 → rootless 컨테이너로 해결
- **Kubernetes**: User Namespace 기능 활성화 (1.25+)
- **성능 vs 보안**: 프로덕션 고부하 → rootful + gVisor, 개발/스테이징 → rootless
