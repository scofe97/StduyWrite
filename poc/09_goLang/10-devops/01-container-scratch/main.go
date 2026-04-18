// 22-container-from-scratch: Go로 컨테이너 만들기
//
// 학습 목표:
// 1. Linux Namespace 이해 (UTS, PID, MNT)
// 2. CGroups로 리소스 제한
// 3. chroot/pivot_root로 파일시스템 격리
// 4. 100줄 미만의 Go 코드로 컨테이너 구현
//
// 참조:
// - https://www.youtube.com/watch?v=8fi7uSYlOdc (Liz Rice, GOTO 2018)
// - https://www.infoq.com/articles/build-a-container-golang/
//
// 실행 (Linux 필요, root 권한 필요):
// go build -o container main.go
// sudo ./container run /bin/sh

package main

import (
	"fmt"
	"os"
	"os/exec"
	"syscall"
)

// rootfs 경로 (Alpine Linux 추출 경로)
// docker export $(docker create alpine) | tar -C rootfs -xvf -
const rootfsPath = "./rootfs"

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: container <command> [args...]")
		fmt.Println("  run  <cmd>  - 컨테이너에서 명령 실행")
		fmt.Println("  child <cmd> - (내부용)")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "run":
		run()
	case "child":
		child()
	default:
		fmt.Printf("알 수 없는 명령: %s\n", os.Args[1])
		os.Exit(1)
	}
}

// run: 새 네임스페이스에서 자기 자신 재실행
func run() {
	fmt.Printf("=== 22. Go로 컨테이너 만들기 ===\n\n")
	fmt.Printf("Running: %v\n", os.Args[2:])

	// TODO: 자기 자신을 child 모드로 재실행
	// 힌트:
	// cmd := exec.Command("/proc/self/exe", append([]string{"child"}, os.Args[2:]...)...)
	// cmd.Stdin = os.Stdin
	// cmd.Stdout = os.Stdout
	// cmd.Stderr = os.Stderr

	_ = exec.Command // 사용할 함수

	// TODO: 새 네임스페이스 설정
	// 힌트:
	// cmd.SysProcAttr = &syscall.SysProcAttr{
	//     Cloneflags: syscall.CLONE_NEWUTS |  // 호스트명 격리
	//                 syscall.CLONE_NEWPID |  // PID 격리
	//                 syscall.CLONE_NEWNS,    // 마운트 격리
	// }

	_ = syscall.CLONE_NEWUTS // 사용할 상수
	_ = syscall.CLONE_NEWPID
	_ = syscall.CLONE_NEWNS

	// TODO: cmd.Run() 호출

	fmt.Println("📌 TODO 주석을 채워서 컨테이너를 완성하세요!")
	fmt.Println("📺 참조: https://www.youtube.com/watch?v=8fi7uSYlOdc")
}

// child: 새 네임스페이스 안에서 실행됨
func child() {
	fmt.Printf("Child running: %v (PID=%d)\n", os.Args[2:], os.Getpid())

	// TODO: 호스트명 변경 (UTS namespace)
	// 힌트:
	// must(syscall.Sethostname([]byte("container")))

	_ = syscall.Sethostname // 사용할 함수

	// TODO: 루트 파일시스템 변경 (chroot)
	// 힌트:
	// must(syscall.Chroot(rootfsPath))
	// must(os.Chdir("/"))

	_ = syscall.Chroot // 사용할 함수
	_ = rootfsPath

	// TODO: /proc 마운트 (ps 명령을 위해)
	// 힌트:
	// must(syscall.Mount("proc", "proc", "proc", 0, ""))

	_ = syscall.Mount // 사용할 함수

	// TODO: CGroups 설정 (선택)
	// cg()

	// TODO: 실제 명령 실행
	// 힌트:
	// cmd := exec.Command(os.Args[2], os.Args[3:]...)
	// cmd.Stdin = os.Stdin
	// cmd.Stdout = os.Stdout
	// cmd.Stderr = os.Stderr
	// must(cmd.Run())

	// TODO: /proc 언마운트 (정리)
	// must(syscall.Unmount("proc", 0))

	fmt.Println("📌 child() 함수의 TODO를 채우세요!")
}

// cg: CGroups 설정 (메모리 제한)
func cg() {
	// TODO: CGroups로 메모리 100MB 제한
	// 힌트:
	// cgroupPath := "/sys/fs/cgroup/memory/mycontainer"
	// os.MkdirAll(cgroupPath, 0755)
	// os.WriteFile(cgroupPath+"/memory.limit_in_bytes", []byte("100000000"), 0700)
	// os.WriteFile(cgroupPath+"/cgroup.procs", []byte(strconv.Itoa(os.Getpid())), 0700)

	fmt.Println("📌 cg() 함수의 TODO를 채우세요!")
}

// must: 에러 발생 시 panic
func must(err error) {
	if err != nil {
		panic(err)
	}
}
