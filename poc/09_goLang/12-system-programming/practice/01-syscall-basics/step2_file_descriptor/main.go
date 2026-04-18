package main

import (
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.O_RDONLY

// Step 2: 파일 디스크립터(fd) 탐구
//
// 목표: fd가 어떻게 할당되는지, 프로세스 fd 테이블이 무엇인지 이해합니다.
//
// 실행: go run main.go
// 검증: ls -la /proc/self/fd/ (Docker 컨테이너에서)

func main() {
	fmt.Println("=== Step 2: 파일 디스크립터(fd) 탐구 ===")

	// ----------------------------------------
	// Part 1: 기본 fd 확인 (0, 1, 2)
	// ----------------------------------------
	fmt.Println("\n--- Part 1: 기본 fd ---")
	fmt.Println("fd 0 = stdin (표준 입력)")
	fmt.Println("fd 1 = stdout (표준 출력)")
	fmt.Println("fd 2 = stderr (표준 에러)")

	// ----------------------------------------
	// TODO 1: 여러 파일을 순서대로 열어서 fd 할당 패턴 확인
	// ----------------------------------------
	fmt.Println("\n--- Part 2: fd 할당 패턴 ---")

	// 힌트:
	// - 파일을 열 때마다 사용 가능한 가장 작은 fd가 할당됩니다
	// - /etc/passwd, /etc/hostname, /etc/hosts 등을 열어보세요

	// TODO: 첫 번째 파일 열기
	// fd1, err := unix.Open("/etc/passwd", unix.O_RDONLY, 0)
	// if err != nil {
	// 	fmt.Printf("열기 실패: %v\n", err)
	// 	return
	// }
	// fmt.Printf("첫 번째 파일 fd: %d\n", fd1)

	// TODO: 두 번째 파일 열기
	// fd2, err := unix.Open("/etc/hostname", unix.O_RDONLY, 0)
	// ...
	// fmt.Printf("두 번째 파일 fd: %d\n", fd2)

	// TODO: 세 번째 파일 열기
	// fd3, err := unix.Open("/etc/hosts", unix.O_RDONLY, 0)
	// ...
	// fmt.Printf("세 번째 파일 fd: %d\n", fd3)

	// ----------------------------------------
	// TODO 2: 중간 fd를 닫고 새 파일 열기
	// ----------------------------------------
	fmt.Println("\n--- Part 3: fd 재사용 ---")

	// 힌트:
	// - 중간 fd를 닫으면, 다음에 열리는 파일이 그 fd를 재사용합니다
	// - 예: fd 3, 4, 5가 열려있을 때 fd 4를 닫으면,
	//       다음에 열리는 파일은 fd 4를 받습니다

	// TODO: fd2를 닫기
	// unix.Close(fd2)
	// fmt.Printf("fd %d 닫음\n", fd2)

	// TODO: 새 파일 열기 - 어떤 fd가 할당될까요?
	// fd4, _ := unix.Open("/etc/resolv.conf", unix.O_RDONLY, 0)
	// fmt.Printf("새 파일 fd: %d (재사용됨!)\n", fd4)

	// ----------------------------------------
	// TODO 3: /proc/self/fd/ 내용 확인
	// ----------------------------------------
	fmt.Println("\n--- Part 4: /proc/self/fd/ 확인 ---")

	// 힌트:
	// - /proc/self/fd/는 현재 프로세스의 fd 목록
	// - 각 항목은 실제 파일/소켓으로의 심볼릭 링크

	entries, err := os.ReadDir("/proc/self/fd")
	if err != nil {
		fmt.Printf("/proc/self/fd 읽기 실패: %v\n", err)
		fmt.Println("(Linux가 아닌 환경에서는 동작하지 않습니다)")
		return
	}

	fmt.Println("현재 열린 fd 목록:")
	for _, entry := range entries {
		// 각 fd가 가리키는 실제 경로 확인
		link, _ := os.Readlink("/proc/self/fd/" + entry.Name())
		fmt.Printf("  fd %s -> %s\n", entry.Name(), link)
	}

	// ----------------------------------------
	// TODO 4: fd 복제 실험 (선택)
	// ----------------------------------------
	fmt.Println("\n--- Part 5: fd 복제 (Dup) ---")

	// 힌트:
	// - unix.Dup(oldfd) - fd를 복제하여 같은 파일을 가리키는 새 fd 생성
	// - 두 fd는 같은 파일 오프셋을 공유합니다

	// TODO: fd 복제해보기
	// dupFd, _ := unix.Dup(fd1)
	// fmt.Printf("원본 fd: %d, 복제된 fd: %d\n", fd1, dupFd)

	// 정리
	// TODO: 열었던 모든 fd 닫기
	// unix.Close(fd1)
	// unix.Close(fd3)
	// unix.Close(fd4)
	// unix.Close(dupFd)

	// ----------------------------------------
	// 생각해볼 점
	// ----------------------------------------
	// 1. 왜 fd는 0부터가 아니라 3부터 시작할까요?
	// 2. fd를 닫지 않으면 어떤 문제가 생길까요? (fd leak)
	// 3. 프로세스당 열 수 있는 fd 개수에 제한이 있을까요?
	//    (힌트: ulimit -n)
}
