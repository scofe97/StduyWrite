# 22. Go로 컨테이너 만들기 실습 과제

## 필수 시청

시작 전 반드시 시청하세요:
- [Containers from Scratch (GOTO 2018)](https://www.youtube.com/watch?v=8fi7uSYlOdc) - Liz Rice

---

## 준비 작업

### Linux 환경 준비 (macOS/Windows)

```bash
# Docker 컨테이너 내에서 실습
docker run -it --privileged -v $(pwd):/app golang:1.21 bash
cd /app
```

### rootfs 준비

```bash
# Alpine Linux rootfs 다운로드
mkdir -p rootfs
docker export $(docker create alpine) | tar -C rootfs -xvf -
```

---

## 1단계: 기본 프로세스 실행

### 과제 1-1: exec.Command로 명령 실행
- [ ] `os/exec` 패키지로 `/bin/sh` 실행
- [ ] Stdin, Stdout, Stderr 연결
- [ ] 호스트에서 정상 동작 확인

```go
// 힌트
cmd := exec.Command("/bin/sh")
cmd.Stdin = os.Stdin
cmd.Stdout = os.Stdout
cmd.Stderr = os.Stderr
cmd.Run()
```

### 과제 1-2: run/child 패턴
- [ ] `os.Args[1]`로 "run"/"child" 분기
- [ ] `/proc/self/exe`로 자기 자신 재실행
- [ ] 왜 이 패턴이 필요한지 이해하기

---

## 2단계: Namespace 격리

### 과제 2-1: UTS Namespace (호스트명)
- [ ] `CLONE_NEWUTS` 플래그 추가
- [ ] `syscall.Sethostname()` 호출
- [ ] `hostname` 명령으로 격리 확인

```bash
# 컨테이너 내에서
hostname  # "container" 출력 예상
```

### 과제 2-2: PID Namespace
- [ ] `CLONE_NEWPID` 플래그 추가
- [ ] `ps aux` 실행하여 PID 1 확인
- [ ] 호스트 프로세스가 안 보이는지 확인

```bash
# 컨테이너 내에서
ps aux  # PID 1이 우리 프로세스
```

### 과제 2-3: Mount Namespace
- [ ] `CLONE_NEWNS` 플래그 추가
- [ ] `/proc` 마운트
- [ ] 호스트 마운트와 격리 확인

---

## 3단계: 파일시스템 격리

### 과제 3-1: chroot
- [ ] `syscall.Chroot()` 호출
- [ ] `os.Chdir("/")` 호출
- [ ] rootfs 내부만 보이는지 확인

```bash
# 컨테이너 내에서
ls /  # rootfs 내용만 보여야 함
cat /etc/os-release  # Alpine 정보
```

### 과제 3-2: /proc 마운트
- [ ] chroot 후 `/proc` 마운트
- [ ] `ps` 명령 동작 확인
- [ ] PID 1이 우리 프로세스인지 확인

```go
// 힌트
syscall.Mount("proc", "proc", "proc", 0, "")
```

---

## 4단계: CGroups 리소스 제한

### 과제 4-1: 메모리 제한
- [ ] CGroup 디렉토리 생성
- [ ] `memory.limit_in_bytes` 설정 (100MB)
- [ ] 현재 프로세스 등록

```go
// 힌트
cgroupPath := "/sys/fs/cgroup/memory/mycontainer"
os.MkdirAll(cgroupPath, 0755)
os.WriteFile(cgroupPath+"/memory.limit_in_bytes", []byte("100000000"), 0700)
```

### 과제 4-2: 메모리 제한 테스트
- [ ] 메모리 100MB 이상 사용하는 코드 작성
- [ ] OOM Killer 동작 확인
- [ ] `dmesg`에서 OOM 로그 확인

```bash
# 컨테이너 내에서 메모리 소비
dd if=/dev/zero of=/dev/null bs=1M count=200
```

### 과제 4-3: CPU 제한 (도전)
- [ ] `cpu.cfs_quota_us` 설정
- [ ] CPU 집약적 작업 실행
- [ ] `top`으로 CPU 사용률 확인

---

## 5단계: 통합 및 개선 (도전)

### 과제 5-1: CLI 인터페이스
- [ ] `container run <image> <cmd>` 형식
- [ ] 이미지 경로 지정 가능
- [ ] 인자 전달 가능

### 과제 5-2: 네트워크 격리
- [ ] `CLONE_NEWNET` 플래그 추가
- [ ] veth 페어 생성
- [ ] 브릿지 연결

### 과제 5-3: pivot_root 구현
- [ ] chroot 대신 pivot_root 사용
- [ ] 이전 root 언마운트
- [ ] 보안 향상 확인

---

## 검증 체크리스트

### 빌드 및 실행
```bash
# 빌드
go build -o container main.go

# 실행 (root 권한 필요)
sudo ./container run /bin/sh
```

### 격리 확인
```bash
# 컨테이너 내에서
hostname           # "container" 출력
ps aux             # PID 1이 우리 프로세스
cat /etc/os-release # Alpine 정보
```

### 리소스 제한 확인
```bash
# 호스트에서
cat /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes
# 100000000 출력
```

---

## 학습 완료 후

`LEARNED.md`에 다음을 기록하세요:
- 컨테이너가 VM과 다른 점
- Namespace가 격리하는 것들
- CGroups가 제한하는 것들
- Docker가 추가로 하는 일들
- "컨테이너가 가벼운 이유"
