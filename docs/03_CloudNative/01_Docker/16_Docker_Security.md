# 16장: Docker Security

## 📌 핵심 요약

> Docker 보안은 **다층 방어(Defense in Depth)** 원칙을 따른다. **Linux 보안 기술**(Namespaces, Cgroups, Capabilities, MAC, seccomp)을 기반으로 하고, **Docker 고유 기술**(Swarm TLS, Docker Scout, Content Trust, Secrets)을 추가한다. 대부분 합리적인 기본값이 적용되어 별도 설정 없이도 적절한 보안이 제공된다.

---

## 🎯 학습 목표

- [ ] Docker의 다층 보안 아키텍처 이해
- [ ] Linux 보안 기술(Namespaces, Cgroups, Capabilities, MAC, seccomp) 역할 파악
- [ ] Swarm의 자동 보안 설정(TLS, Join Token, CA) 이해
- [ ] Docker Scout를 통한 이미지 취약점 스캐닝 활용
- [ ] Docker Content Trust(DCT)로 이미지 서명/검증
- [ ] Docker Secrets로 민감 데이터 관리

---

## 📖 본문 정리

### 1. Docker 보안 개요

#### 💬 비유로 이해하기
> Docker 보안은 **양파 껍질**과 같다. 여러 겹의 보안 레이어가 있어 한 겹이 뚫려도 다른 겹들이 보호한다. Namespaces가 격리를, Cgroups가 리소스 제한을, Capabilities가 권한 최소화를, seccomp이 시스템 콜 필터링을 담당한다.

#### 다층 방어 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                 Docker Security - Defense in Depth               │
└─────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────┐
  │                    Docker Technologies                         │
  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
  │  │Docker Scout │  │   Content   │  │   Docker    │           │
  │  │(취약점 스캔)│  │   Trust     │  │   Secrets   │           │
  │  └─────────────┘  └─────────────┘  └─────────────┘           │
  │                                                                │
  │  ┌─────────────────────────────────────────────────────────┐  │
  │  │               Swarm Security (TLS, CA, Tokens)           │  │
  │  └─────────────────────────────────────────────────────────┘  │
  └───────────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                    Linux Technologies                          │
  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
  │  │Namespace│  │ Cgroups │  │Capabilit│  │ seccomp │          │
  │  │ (격리)  │  │ (제한)  │  │(최소권한)│  │(syscall)│          │
  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘          │
  │                                                                │
  │  ┌─────────────────────────────────────────────────────────┐  │
  │  │         MAC (AppArmor / SELinux)                        │  │
  │  └─────────────────────────────────────────────────────────┘  │
  └───────────────────────────────────────────────────────────────┘
                               │
                               ▼
  ┌───────────────────────────────────────────────────────────────┐
  │                      Linux Kernel                              │
  └───────────────────────────────────────────────────────────────┘
```

---

### 2. Linux 보안 기술

#### 2.1 Kernel Namespaces

**Namespace vs Hypervisor 비교**:

| 구분 | Hypervisor (VM) | Namespace (Container) |
|------|-----------------|----------------------|
| **가상화 대상** | 물리 자원 (CPU, 디스크) | OS 구조 (프로세스 트리, 파일시스템) |
| **결과물** | 가상 머신 (물리 머신처럼 보임) | 컨테이너 (OS처럼 보임) |
| **격리 강도** | 강함 | 경량 (추가 보안 기술 필요) |
| **효율성** | 낮음 | 높음 |

**컨테이너별 Namespace**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Namespace 격리 구조                           │
└─────────────────────────────────────────────────────────────────┘

  Docker Host (Root Namespaces)
  ┌───────────────────────────────────────────────────────────────┐
  │  pid: Host processes                                          │
  │  net: Host network stack                                      │
  │  mnt: Host filesystem                                         │
  │  ipc: Host shared memory                                      │
  │  user: Host users                                             │
  │  uts: Host hostname                                           │
  └───────────────────────────────────────────────────────────────┘
           │                              │
           ▼                              ▼
  ┌─────────────────────┐      ┌─────────────────────┐
  │    Container A      │      │    Container B      │
  │  ┌───────────────┐  │      │  ┌───────────────┐  │
  │  │ pid: PID 1... │  │      │  │ pid: PID 1... │  │
  │  │ net: eth0, IP │  │      │  │ net: eth0, IP │  │
  │  │ mnt: / (root) │  │      │  │ mnt: / (root) │  │
  │  │ ipc: 격리됨   │  │      │  │ ipc: 격리됨   │  │
  │  │ user: 격리됨  │  │      │  │ user: 격리됨  │  │
  │  │ uts: hostname │  │      │  │ uts: hostname │  │
  │  └───────────────┘  │      │  └───────────────┘  │
  │                     │      │                     │
  │  서로 볼 수 없음 ✗  │      │  서로 볼 수 없음 ✗  │
  └─────────────────────┘      └─────────────────────┘
```

**6가지 Namespace**:

| Namespace | 약어 | 격리 대상 | 효과 |
|-----------|------|-----------|------|
| **Process ID** | pid | 프로세스 트리 | 각 컨테이너 고유 PID 1, 타 컨테이너/호스트 프로세스 숨김 |
| **Network** | net | 네트워크 스택 | 고유 eth0, IP, 포트 범위, 라우팅 테이블 |
| **Mount** | mnt | 파일시스템 | 고유 루트(/), /etc, /var, /dev 등 |
| **IPC** | ipc | 공유 메모리 | 컨테이너 내 공유 메모리 격리 |
| **User** | user | 사용자 | 컨테이너 내 사용자, 호스트 사용자에 매핑 가능 |
| **UTS** | uts | 호스트명 | 고유 hostname |

#### 2.2 Control Groups (Cgroups)

> **Namespaces = 격리**, **Cgroups = 제한**

💬 **비유**: 호텔 방(컨테이너)은 격리되어 있지만, 수도/전기/에어컨/수영장(공유 자원)은 공유한다. Cgroups는 각 방이 자원을 독점하지 못하도록 제한한다.

**Cgroups가 제한하는 공유 자원**:
- CPU
- RAM
- Network I/O
- Disk I/O

**목적**: DoS(Denial of Service) 공격 방지 - 한 컨테이너가 모든 자원을 소비하는 것 방지

#### 2.3 Capabilities

**문제**: root 사용자는 너무 강력하고, 일반 사용자는 너무 무력함

**해결**: root 권한을 세분화된 **capabilities**로 분리

```
┌─────────────────────────────────────────────────────────────────┐
│                 Linux Root = 여러 Capabilities 조합              │
└─────────────────────────────────────────────────────────────────┘

  Root User 권한 분해:
  ┌─────────────────┬────────────────────────────────────────────┐
  │ Capability      │ 기능                                       │
  ├─────────────────┼────────────────────────────────────────────┤
  │ CAP_CHOWN       │ 파일 소유권 변경                            │
  │ CAP_NET_BIND_   │ 낮은 포트(1-1024)에 소켓 바인딩            │
  │ SERVICE         │                                            │
  │ CAP_SETUID      │ 프로세스 권한 상승                          │
  │ CAP_SYS_BOOT    │ 시스템 재부팅                               │
  │ CAP_KILL        │ 프로세스 종료                               │
  │ ... (수십 개)   │                                            │
  └─────────────────┴────────────────────────────────────────────┘
```

**Docker의 Capabilities 활용**:

```
┌─────────────────────────────────────────────────────────────────┐
│              최소 권한 원칙 (Principle of Least Privilege)       │
└─────────────────────────────────────────────────────────────────┘

  시나리오: 컨테이너가 낮은 포트 바인딩만 필요한 경우

  전통적 방식:
  ┌─────────────────────────────────────────────────────────────┐
  │  Root로 실행 → 모든 권한 보유 (위험!)                        │
  └─────────────────────────────────────────────────────────────┘

  Docker + Capabilities:
  ┌─────────────────────────────────────────────────────────────┐
  │  1. Root로 컨테이너 시작                                     │
  │  2. 모든 Capabilities 제거                                   │
  │  3. CAP_NET_BIND_SERVICE만 추가                             │
  │  → 필요한 최소 권한만 보유! ✅                               │
  └─────────────────────────────────────────────────────────────┘
```

> Docker는 합리적인 기본 capabilities를 제공하지만, 프로덕션에서는 커스텀 설정 권장

#### 2.4 Mandatory Access Control (MAC)

**지원 기술**:
- **AppArmor**: Debian/Ubuntu 계열
- **SELinux**: RHEL/CentOS 계열

Docker는 Linux 배포판에 따라 **기본 AppArmor/SELinux 프로파일**을 자동 적용

| 설정 | 설명 |
|------|------|
| **기본 프로파일** | 중간 수준 보호 + 높은 앱 호환성 |
| **커스텀 프로파일** | 강력하지만 복잡, 광범위한 테스트 필요 |
| **비활성화** | 가능하지만 비권장 |

#### 2.5 seccomp

**역할**: 컨테이너가 호스트 커널에 요청할 수 있는 **syscall 제한**

```
┌─────────────────────────────────────────────────────────────────┐
│                    seccomp 필터링                                │
└─────────────────────────────────────────────────────────────────┘

  Container                           Host Kernel
  ┌─────────────────┐                ┌─────────────────┐
  │  Application    │                │  300+ syscalls  │
  │       │         │                │                 │
  │       ▼         │                │  ┌───────────┐  │
  │  syscall 요청   │───────────────►│  │  허용     │  │
  │                 │                │  │  syscalls │  │
  │                 │      ┌─────┐   │  └───────────┘  │
  │                 │──────│Block│   │                 │
  │                 │      └─────┘   │  ┌───────────┐  │
  │                 │                │  │  차단     │  │
  │                 │       ✗        │  │  ~40-50개 │  │
  └─────────────────┘                │  └───────────┘  │
                                     └─────────────────┘

  Docker 기본 프로파일:
  • Linux 300+ syscalls 중 ~40-50개 차단
  • 보안과 앱 호환성 균형
```

---

### 3. Docker 보안 기술

#### 3.1 Swarm 보안

**자동 설정 보안 기능**:

| 기능 | 설명 |
|------|------|
| **Cryptographic Node ID** | 각 노드 고유 암호화 ID |
| **Mutual TLS** | 노드 간 상호 인증 |
| **Secure Join Tokens** | Manager/Worker 토큰 분리 |
| **CA 자동 구성** | 90일 인증서 자동 로테이션 |
| **Encrypted Cluster Store** | etcd 기반 암호화 저장소 |
| **Encrypted Networks** | 네트워크 트래픽 암호화 |

#### Swarm 클러스터 보안 구성

```bash
# 1단계: Swarm 초기화 (보안 자동 구성)
$ docker swarm init
Swarm initialized: current node (7xam...662z) is now a manager.

# 자동 설정 항목:
# • 암호화된 클러스터 ID
# • 암호화된 클러스터 스토어
# • CA + 90일 인증서 로테이션
# • Manager/Worker용 보안 Join Token
# • 상호 TLS용 클라이언트 인증서

# 2단계: Manager 토큰 확인
$ docker swarm join-token manager

# 3단계: Worker 토큰 확인
$ docker swarm join-token worker
```

**Join Token 구조**:

```
SWMTKN-1-<cluster-certificate-hash>-<manager-or-worker-token>
   │    │           │                         │
   │    │           │                         └─ 역할별 고유 토큰
   │    │           └─ Swarm 인증서 해시
   │    └─ 버전
   └─ 접두사 (유출 방지용 패턴 매칭)
```

| 역할 | Prefix | Version | Swarm ID | Token |
|------|--------|---------|----------|-------|
| Manager | SWMTKN | 1 | 1dmtwusdc...r17stb | 2axi53zj...7glz |
| Worker | SWMTKN | 1 | 1dmtwusdc...r17stb | ehp8gltj...738q |

**토큰 로테이션** (유출 시):

```bash
# Manager 토큰 무효화 및 새 토큰 발급
$ docker swarm join-token --rotate manager
Successfully rotated manager join token.

# 기존 Manager는 영향 없음, 새 Manager는 새 토큰 필요
```

#### TLS 인증서 확인

```bash
# 노드 인증서 확인
$ sudo openssl x509 \
  -in /var/lib/docker/swarm/certificates/swarm-node.crt \
  -text

# 출력 예시:
Subject: O = tcz3w1t7yu0s4wacovn1rtgp4,    # Swarm ID
         OU = swarm-manager,                 # 노드 역할
         CN = 2gxz2h1f0rnmc3atm35qcd1zw     # 노드 ID

Validity:
  Not Before: May 23 08:23:00 2024 GMT
  Not After : Aug 21 09:23:00 2024 GMT     # 90일 후 만료
```

**CA 설정 변경**:

```bash
# 인증서 로테이션 주기 변경 (30일로)
$ docker swarm update --cert-expiry 720h

# CA 관련 설정 확인
$ docker swarm ca --help
```

#### 3.2 Docker Scout (취약점 스캐닝)

**동작 방식**:
1. 이미지의 모든 소프트웨어 패키지 분석
2. **SBOM (Software Bill of Materials)** 생성
3. 알려진 취약점 DB와 비교
4. 취약점 보고서 + 해결 방안 제공

```bash
# 빠른 취약점 개요
$ docker scout quickview nigelpoulton/tu-demo:latest

    ✓ Indexed 66 packages

  Target             │  nigelpoulton/tu-demo:latest
    digest           │  b4210d0aa52f
  Base image         │  python:3-alpine        │  0C  2H  1M  0L
  Updated base image │  python:3.11-alpine     │  0C  1H  1M  0L
```

**취약점 등급**:

| 등급 | 약자 | 의미 |
|------|------|------|
| Critical | C | 즉시 조치 필요 |
| High | H | 높은 위험 |
| Medium | M | 중간 위험 |
| Low | L | 낮은 위험 |

```bash
# 상세 취약점 정보
$ docker scout cves nigelpoulton/tu-demo:latest

## Packages and Vulnerabilities
   0C     1H     1M     0L  expat 2.5.0-r2

    ✗ HIGH CVE-2023-52425
      https://scout.docker.com/v/CVE-2023-52425
      Affected range : <2.6.0-r0
      Fixed version  : 2.6.0-r0        ← 해결 버전 제안!

   ✗ MEDIUM CVE-2023-52426
      Affected range : <2.6.0-r0
      Fixed version  : 2.6.0-r0
```

> ⚠️ **한계**: 이미지만 스캔, 네트워크/노드/오케스트레이터 보안 문제는 감지 못함

#### 3.3 Docker Content Trust (DCT)

**목적**: 이미지 **무결성**과 **게시자** 검증

```
┌─────────────────────────────────────────────────────────────────┐
│                Docker Content Trust 워크플로우                    │
└─────────────────────────────────────────────────────────────────┘

  Publisher                                    Consumer
  ┌─────────────────┐                         ┌─────────────────┐
  │  1. 이미지 빌드  │                         │  4. 이미지 Pull │
  │  2. 개인키로 서명│                         │  5. 서명 검증   │
  │  3. Registry Push│                         │  6. 검증 성공   │
  └────────┬────────┘                         └────────┬────────┘
           │                                           │
           │  ┌─────────────────────────────┐          │
           └─►│       Docker Registry       │◄─────────┘
              │  (서명된 이미지 + 메타데이터) │
              └─────────────────────────────┘
```

**DCT 설정 및 사용**:

```bash
# 1단계: 키 페어 생성
$ docker trust key generate nigel
Enter passphrase for new nigel key with ID 1f78609:
Successfully generated and loaded private key...

# 2단계: 키를 레포지토리에 연결
$ docker trust signer add --key nigel.pub nigel nigelpoulton/ddd-trust
Adding signer "nigel" to nigelpoulton/ddd-trust...
Successfully added signer: nigel to nigelpoulton/ddd-trust

# 3단계: 이미지 서명 및 푸시
$ docker trust sign nigelpoulton/ddd-trust:signed
Signing and pushing trust data...
Successfully signed docker.io/nigelpoulton/ddd-trust:signed

# 4단계: 서명 정보 확인
$ docker trust inspect nigelpoulton/ddd-trust:signed --pretty
Signatures for nigelpoulton/ddd-trust:signed
  SIGNED TAG   DIGEST                    SIGNERS
  signed       30e6d35703c578ee...       nigel
```

**DCT 강제 활성화**:

```bash
# 환경변수로 DCT 강제 적용
$ export DOCKER_CONTENT_TRUST=1

# 서명 없는 이미지 Pull 시도 → 실패!
$ docker pull nigelpoulton/ddd-book:web0.2
Error: remote trust data does not exist...

# 서명된 이미지 Pull → 성공!
$ docker pull nigelpoulton/ddd-trust:signed
Pull (1 of 1): nigelpoulton/ddd-trust:signed@sha256:30e6...
```

#### 3.4 Docker Secrets

**요구사항**: Swarm 모드 필수 (클러스터 스토어 활용)

**보안 특성**:
- 클러스터 스토어에 **암호화 저장** (at rest)
- 네트워크 전송 시 **암호화** (in flight)
- **인메모리 파일시스템**에 마운트 (디스크에 저장 안 됨)
- **최소 권한** 모델 (명시적으로 허가된 서비스만 접근)

```
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Secrets 워크플로우                      │
└─────────────────────────────────────────────────────────────────┘

  1. Secret 생성
  ┌─────────────┐
  │   Secret    │ ─────► docker secret create
  │  (password) │
  └─────────────┘
         │
         ▼
  2. 암호화된 클러스터 스토어에 저장
  ┌─────────────────────────────────────────────────────────────┐
  │              Encrypted Cluster Store (etcd)                  │
  │  ┌─────────┐                                                │
  │  │ 🔐 Secret │ (암호화됨)                                    │
  │  └─────────┘                                                │
  └─────────────────────────────────────────────────────────────┘
         │
         │ 3. 서비스에 Secret 연결
         ▼
  ┌─────────────────────────────────────────────────────────────┐
  │                     서비스 레플리카                           │
  │  ┌───────────┐     ┌───────────┐     ┌───────────┐         │
  │  │ Container │     │ Container │     │ Container │         │
  │  │ (허가됨)  │     │ (허가됨)  │     │ (비허가)  │         │
  │  │    🔑     │     │    🔑     │     │    ✗     │         │
  │  │ /run/     │     │ /run/     │     │           │         │
  │  │ secrets/  │     │ secrets/  │     │           │         │
  │  └───────────┘     └───────────┘     └───────────┘         │
  │                                                             │
  │  • 인메모리 파일시스템에 복호화된 상태로 마운트              │
  │  • 컨테이너 종료 시 즉시 삭제                                │
  └─────────────────────────────────────────────────────────────┘
```

**Secret 관리 명령어**:

```bash
# Secret 생성
$ echo "mypassword" | docker secret create db_password -

# Secret을 서비스에 연결
$ docker service create --name myapp \
    --secret db_password \
    myimage

# 컨테이너 내부에서 Secret 접근
# cat /run/secrets/db_password
mypassword
```

---

## 🔍 심화 학습

### Linux vs Docker 보안 기술 비교

| 기술 | 유형 | 역할 | 커스텀 난이도 |
|------|------|------|---------------|
| Namespaces | Linux | 격리 | 중간 |
| Cgroups | Linux | 리소스 제한 | 낮음 |
| Capabilities | Linux | 권한 최소화 | 높음 |
| MAC (AppArmor/SELinux) | Linux | 접근 제어 | 높음 |
| seccomp | Linux | Syscall 필터 | 높음 |
| Swarm TLS/CA | Docker | 노드 인증 | 낮음 (자동) |
| Docker Scout | Docker | 취약점 스캔 | 낮음 |
| Content Trust | Docker | 이미지 서명 | 중간 |
| Secrets | Docker | 민감 데이터 | 낮음 |

### 추가 학습 주제
- User Namespace Remapping
- rootless Docker
- gVisor / Kata Containers (강화된 격리)
- Pod Security Policies (Kubernetes)

---

## 💡 실무 적용 포인트

### 면접 대비 Q&A

**Q1: Docker 컨테이너가 VM보다 보안이 약하다고 하는 이유는?**

> A: 컨테이너는 **Namespace**로 격리되지만, 호스트 커널을 공유합니다. VM은 하이퍼바이저가 하드웨어를 가상화하여 더 강한 격리를 제공합니다. 그러나 Docker는 **Cgroups, Capabilities, MAC, seccomp** 등 추가 보안 레이어를 적용하여 이 차이를 보완합니다.

**Q2: Docker Swarm이 기본 제공하는 보안 기능은?**

> A: `docker swarm init` 한 번으로 다음이 자동 구성됩니다: **암호화된 노드 ID**, **상호 TLS 인증**, **보안 Join Token** (Manager/Worker 분리), **CA 및 90일 인증서 자동 로테이션**, **암호화된 클러스터 스토어**, **암호화된 네트워크**. 대부분 합리적인 기본값이 적용됩니다.

**Q3: Capabilities가 보안에 어떻게 기여하는가?**

> A: Linux root 권한을 세분화된 **capabilities**로 분리합니다. Docker는 컨테이너를 root로 시작하되 불필요한 capabilities를 제거하고 필요한 것만 추가합니다. 예: 낮은 포트 바인딩만 필요하면 `CAP_NET_BIND_SERVICE`만 부여. 이는 **최소 권한 원칙**을 구현합니다.

**Q4: Docker Content Trust(DCT)와 Docker Scout의 차이점은?**

> A: **Docker Scout**는 이미지 내 소프트웨어 패키지의 **알려진 취약점**을 스캔하고 보고합니다. **DCT**는 이미지의 **무결성**과 **게시자**를 암호화 서명으로 검증합니다. Scout는 "이미지에 취약점이 있는가?", DCT는 "이미지가 변조되지 않았고 신뢰할 수 있는 출처인가?"에 답합니다.

---

## ✅ 체크리스트

### Linux 보안 기술
- [ ] 6가지 Namespace (pid, net, mnt, ipc, user, uts) 역할 이해
- [ ] Cgroups의 리소스 제한 목적 (DoS 방지)
- [ ] Capabilities와 최소 권한 원칙
- [ ] MAC (AppArmor/SELinux) 기본 프로파일 동작
- [ ] seccomp의 syscall 필터링 (~40-50개 차단)

### Swarm 보안
- [ ] `docker swarm init`의 자동 보안 설정 항목
- [ ] Join Token 구조 및 Manager/Worker 분리
- [ ] `docker swarm join-token --rotate`: 토큰 무효화
- [ ] TLS 인증서 확인 및 CA 설정 변경
- [ ] 클러스터 스토어 암호화

### Docker Scout
- [ ] `docker scout quickview`: 빠른 취약점 개요
- [ ] `docker scout cves`: 상세 CVE 정보 및 해결책
- [ ] SBOM (Software Bill of Materials) 개념
- [ ] 취약점 등급 (Critical/High/Medium/Low)

### Docker Content Trust
- [ ] `docker trust key generate`: 키 페어 생성
- [ ] `docker trust signer add`: 키를 레포지토리에 연결
- [ ] `docker trust sign`: 이미지 서명 및 푸시
- [ ] `DOCKER_CONTENT_TRUST=1`: 강제 검증 활성화
- [ ] 서명 없는 이미지 Pull 차단 동작

### Docker Secrets
- [ ] Swarm 모드 필수 요구사항
- [ ] 암호화 저장(at rest) + 전송 중 암호화(in flight)
- [ ] 인메모리 파일시스템 마운트
- [ ] `docker secret create`, `--secret` 플래그 사용

---

## 🔗 참고 자료

- [Docker Security 공식 문서](https://docs.docker.com/engine/security/)
- [Docker Scout](https://docs.docker.com/scout/)
- [Docker Content Trust](https://docs.docker.com/engine/security/trust/)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Linux Capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html)
- [seccomp 보안 프로파일](https://docs.docker.com/engine/security/seccomp/)
- 도서: *Docker Deep Dive* - Nigel Poulton, Chapter 16
