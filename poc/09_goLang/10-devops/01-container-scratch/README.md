# 22. Go로 컨테이너 만들기 (Container from Scratch)

컨테이너의 본질을 이해하기 위해 Go로 직접 구현합니다.

## 학습 목표

- [ ] Linux Namespace의 종류와 역할 이해
- [ ] CGroups로 리소스 제한하는 방법
- [ ] chroot와 pivot_root의 차이점
- [ ] 100줄 미만의 Go 코드로 컨테이너 구현

---

## 필수 시청/읽기

| 자료 | 설명 |
|------|------|
| [Containers from Scratch (GOTO 2018)](https://www.youtube.com/watch?v=8fi7uSYlOdc) | Liz Rice의 라이브 코딩 - 컨테이너 원리 설명 |
| [Build a Container in Go (InfoQ)](https://www.infoq.com/articles/build-a-container-golang/) | 100줄 미만 Go 코드로 컨테이너 구현 |

**Liz Rice** (Isovalent/eBPF 전문가)의 핵심 메시지:
> "컨테이너는 마법이 아니다. Linux 커널 기능의 조합일 뿐이다."

---

## 핵심 개념

### 컨테이너의 3가지 핵심 기술

```
┌─────────────────────────────────────────────────────────────┐
│                      컨테이너 = ?                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Namespaces  │  │   CGroups   │  │     Union FS        │  │
│  │ (격리)      │  │ (리소스제한) │  │ (파일시스템 계층화)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

| 기술 | 설명 | Linux 시스템 콜 |
|------|------|----------------|
| **Namespaces** | 프로세스 격리 | `clone()`, `unshare()` |
| **CGroups** | 리소스 제한 | `/sys/fs/cgroup/` |
| **Union FS** | 계층화된 파일시스템 | OverlayFS |

---

### 1. Namespaces (격리)

프로세스가 볼 수 있는 리소스를 제한합니다.

| Namespace | 플래그 | 격리 대상 |
|-----------|--------|----------|
| UTS | `CLONE_NEWUTS` | 호스트명, 도메인명 |
| PID | `CLONE_NEWPID` | 프로세스 ID (컨테이너 내 PID 1) |
| MNT | `CLONE_NEWNS` | 마운트 포인트 |
| NET | `CLONE_NEWNET` | 네트워크 스택 |
| IPC | `CLONE_NEWIPC` | System V IPC |
| USER | `CLONE_NEWUSER` | 사용자/그룹 ID |

```go
// Go에서 Namespace 생성
cmd.SysProcAttr = &syscall.SysProcAttr{
    Cloneflags: syscall.CLONE_NEWUTS |  // 호스트명
                syscall.CLONE_NEWPID |  // PID
                syscall.CLONE_NEWNS,    // 마운트
}
```

---

### 2. CGroups (리소스 제한)

Control Groups - 프로세스 그룹의 리소스 사용량을 제한합니다.

```
/sys/fs/cgroup/
├── memory/
│   └── mycontainer/
│       ├── memory.limit_in_bytes   # 메모리 제한
│       └── cgroup.procs            # 소속 프로세스
└── cpu/
    └── mycontainer/
        └── cpu.cfs_quota_us        # CPU 시간 제한
```

```go
// 메모리 100MB 제한
cgroupPath := "/sys/fs/cgroup/memory/mycontainer"
os.MkdirAll(cgroupPath, 0755)
os.WriteFile(cgroupPath+"/memory.limit_in_bytes", []byte("100000000"), 0700)
os.WriteFile(cgroupPath+"/cgroup.procs", []byte(strconv.Itoa(os.Getpid())), 0700)
```

---

### 3. Chroot vs Pivot_root

| 방식 | 설명 | 보안 |
|------|------|------|
| `chroot` | 루트 디렉토리 변경 (단순) | 탈출 가능 |
| `pivot_root` | 루트 파일시스템 교체 | 더 안전 (Docker 사용) |

```go
// chroot 사용
syscall.Chroot("/path/to/rootfs")
os.Chdir("/")

// pivot_root 사용 (더 안전)
syscall.PivotRoot(newroot, putold)
```

---

## 실행 환경

**주의**: Namespace와 CGroups는 Linux 커널 기능입니다.

| OS | 지원 |
|----|-----|
| Linux (Ubuntu, Alpine) | 네이티브 지원 |
| macOS | Docker Desktop 또는 Lima VM 필요 |
| Windows | WSL2 필요 |

### macOS에서 실행

```bash
# 방법 1: Docker 컨테이너 내에서 실행
docker run -it --privileged -v $(pwd):/app golang:1.21 bash
cd /app
go build -o container main.go
./container run /bin/sh

# 방법 2: Lima VM
limactl start
limactl shell
```

---

## 프로젝트 구조

```
22-container-from-scratch/
├── README.md           # 이 문서
├── EXERCISES.md        # 단계별 실습
├── HINTS.md            # 막힐 때 힌트
├── LEARNED.md          # 학습 회고 템플릿
├── go.mod
└── main.go             # 컨테이너 구현 스켈레톤
```

---

## 참조 자료

### 발표/아티클
- [Containers from Scratch (Liz Rice, GOTO 2018)](https://www.youtube.com/watch?v=8fi7uSYlOdc)
- [Build a Container in Go (InfoQ)](https://www.infoq.com/articles/build-a-container-golang/)
- [Docker Internals](http://docker-saigon.github.io/post/Docker-Internals/)

### 공식 문서
- [Linux Namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
- [CGroups v2](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html)

### 관련 모듈
- **20-docker-k8s**: Docker/K8s 배포 실습
- **21-distributed-systems**: 분산 시스템 (Raft, Leader Election)
