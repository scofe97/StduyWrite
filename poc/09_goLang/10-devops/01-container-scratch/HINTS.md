# 22. Go로 컨테이너 만들기 힌트

막힐 때만 참고하세요.

---

## 기본 구조: run/child 패턴

```go
package main

import (
    "os"
    "os/exec"
    "syscall"
)

func main() {
    switch os.Args[1] {
    case "run":
        run()
    case "child":
        child()
    default:
        panic("unknown command")
    }
}

func run() {
    // 새 네임스페이스에서 자기 자신 재실행
    cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS |
                    syscall.CLONE_NEWPID |
                    syscall.CLONE_NEWNS,
    }

    must(cmd.Run())
}

func child() {
    // 새 네임스페이스 안에서 실행됨
    // 여기서 호스트명 변경, chroot 등 수행
}

func must(err error) {
    if err != nil {
        panic(err)
    }
}
```

### 왜 run/child 패턴이 필요한가?

`CLONE_NEWPID`를 사용하면 **자식 프로세스**가 새 PID namespace의 PID 1이 됩니다.
현재 프로세스는 여전히 기존 namespace에 있습니다.

```
[run]  ─── clone(CLONE_NEWPID) ──→ [child] (PID 1 in new namespace)
 │                                    │
 │ (기존 PID namespace)               │ (새 PID namespace)
```

---

## Namespace 플래그

```go
cmd.SysProcAttr = &syscall.SysProcAttr{
    Cloneflags: syscall.CLONE_NEWUTS |    // 호스트명 격리
                syscall.CLONE_NEWPID |    // PID 격리
                syscall.CLONE_NEWNS |     // 마운트 격리
                syscall.CLONE_NEWNET |    // 네트워크 격리 (도전)
                syscall.CLONE_NEWIPC |    // IPC 격리 (도전)
                syscall.CLONE_NEWUSER,    // 사용자 격리 (도전)
}
```

---

## 호스트명 변경

```go
func child() {
    // UTS namespace에서만 작동
    must(syscall.Sethostname([]byte("container")))

    // ... 나머지 코드
}
```

---

## 파일시스템 격리 (chroot)

```go
func child() {
    // 1. 호스트명 변경
    must(syscall.Sethostname([]byte("container")))

    // 2. 루트 변경
    must(syscall.Chroot("/path/to/rootfs"))
    must(os.Chdir("/"))

    // 3. /proc 마운트 (ps 명령을 위해)
    must(syscall.Mount("proc", "proc", "proc", 0, ""))

    // 4. 실제 명령 실행
    cmd := exec.Command(os.Args[2], os.Args[3:]...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    must(cmd.Run())

    // 5. 정리 (선택)
    must(syscall.Unmount("proc", 0))
}
```

### rootfs 경로

```go
const rootfsPath = "/home/user/rootfs"  // 실제 경로로 변경

func child() {
    must(syscall.Chroot(rootfsPath))
    // ...
}
```

---

## CGroups 설정

```go
func cg() {
    // CGroup v1 (Ubuntu 20.04 이하)
    cgroupPath := "/sys/fs/cgroup/memory/mycontainer"

    // 디렉토리 생성
    must(os.MkdirAll(cgroupPath, 0755))

    // 메모리 100MB 제한
    must(os.WriteFile(
        cgroupPath+"/memory.limit_in_bytes",
        []byte("100000000"),
        0700,
    ))

    // 현재 프로세스 등록
    must(os.WriteFile(
        cgroupPath+"/cgroup.procs",
        []byte(strconv.Itoa(os.Getpid())),
        0700,
    ))
}
```

### CGroup v2 (Ubuntu 22.04+)

```go
func cgV2() {
    cgroupPath := "/sys/fs/cgroup/mycontainer"

    must(os.MkdirAll(cgroupPath, 0755))

    // 메모리 100MB 제한 (v2 방식)
    must(os.WriteFile(
        cgroupPath+"/memory.max",
        []byte("100000000"),
        0700,
    ))

    // 현재 프로세스 등록
    must(os.WriteFile(
        cgroupPath+"/cgroup.procs",
        []byte(strconv.Itoa(os.Getpid())),
        0700,
    ))
}
```

---

## 전체 예시 (간단 버전)

```go
package main

import (
    "fmt"
    "os"
    "os/exec"
    "syscall"
)

func main() {
    switch os.Args[1] {
    case "run":
        run()
    case "child":
        child()
    default:
        panic("bad command")
    }
}

func run() {
    fmt.Println("Running:", os.Args[2:])

    cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr
    cmd.SysProcAttr = &syscall.SysProcAttr{
        Cloneflags: syscall.CLONE_NEWUTS |
                    syscall.CLONE_NEWPID |
                    syscall.CLONE_NEWNS,
    }

    must(cmd.Run())
}

func child() {
    fmt.Println("Child running:", os.Args[2:])

    // 호스트명 변경
    must(syscall.Sethostname([]byte("container")))

    // chroot
    must(syscall.Chroot("/home/user/rootfs"))  // 경로 수정 필요
    must(os.Chdir("/"))

    // /proc 마운트
    must(syscall.Mount("proc", "proc", "proc", 0, ""))

    // 명령 실행
    cmd := exec.Command(os.Args[2], os.Args[3:]...)
    cmd.Stdin = os.Stdin
    cmd.Stdout = os.Stdout
    cmd.Stderr = os.Stderr

    must(cmd.Run())

    // 정리
    must(syscall.Unmount("proc", 0))
}

func must(err error) {
    if err != nil {
        panic(err)
    }
}
```

---

## 디버깅 팁

### 1. Namespace 확인

```bash
# 호스트에서
ls -la /proc/$$/ns/

# 각 namespace 파일이 다른 inode를 가리키면 격리됨
```

### 2. CGroup 확인

```bash
# 메모리 제한 확인
cat /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes

# 현재 사용량
cat /sys/fs/cgroup/memory/mycontainer/memory.usage_in_bytes
```

### 3. 권한 문제

```bash
# root로 실행 필요
sudo ./container run /bin/sh

# 또는 capabilities 추가
sudo setcap cap_sys_admin+ep ./container
```

---

## pivot_root (chroot보다 안전)

```go
func pivotRoot(newroot string) error {
    putold := filepath.Join(newroot, "/.pivot_root")

    // put_old 디렉토리 생성
    if err := os.MkdirAll(putold, 0700); err != nil {
        return err
    }

    // pivot_root 호출
    if err := syscall.PivotRoot(newroot, putold); err != nil {
        return err
    }

    // 루트로 이동
    if err := os.Chdir("/"); err != nil {
        return err
    }

    // 이전 루트 언마운트
    putold = "/.pivot_root"
    if err := syscall.Unmount(putold, syscall.MNT_DETACH); err != nil {
        return err
    }

    // 이전 루트 삭제
    return os.RemoveAll(putold)
}
```
