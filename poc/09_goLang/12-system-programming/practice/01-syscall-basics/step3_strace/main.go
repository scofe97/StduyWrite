package main

import (
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.O_RDONLY

// Step 3: Go 표준 라이브러리 vs unix 패키지 비교
//
// 목표: os.Open()과 unix.Open()이 내부적으로 같은 시스템 콜을 호출함을 확인합니다.
//
// 실행:
//   go run main.go
//
// 검증:
//   strace -e openat,read,close go run main.go 2>&1 | grep -E "(openat|read|close)"

func main() {
	fmt.Println("=== Step 3: Go 표준 라이브러리 추적 ===")
	fmt.Println()

	// ----------------------------------------
	// Part 1: unix 패키지로 직접 시스템 콜
	// ----------------------------------------
	fmt.Println("--- Part 1: unix 패키지 (저수준) ---")

	// TODO 1: unix.Open()으로 파일 열기
	// 힌트: 이전 step에서 배운 대로 구현

	// fd, err := unix.Open("/etc/hostname", unix.O_RDONLY, 0)
	// if err != nil {
	// 	fmt.Printf("unix.Open 실패: %v\n", err)
	// 	return
	// }

	// buf := make([]byte, 256)
	// n, _ := unix.Read(fd, buf)
	// fmt.Printf("unix.Read 결과: %s", string(buf[:n]))
	// unix.Close(fd)

	fmt.Println("(TODO: unix 패키지로 파일 읽기 구현)")

	// ----------------------------------------
	// Part 2: os 패키지로 같은 작업
	// ----------------------------------------
	fmt.Println("\n--- Part 2: os 패키지 (고수준) ---")

	// TODO 2: os.Open()으로 같은 파일 열기
	// 힌트: os.Open()은 *os.File을 반환합니다

	file, err := os.Open("/etc/hostname")
	if err != nil {
		fmt.Printf("os.Open 실패: %v\n", err)
		return
	}
	defer file.Close()

	buf2 := make([]byte, 256)
	n2, _ := file.Read(buf2)
	fmt.Printf("os.Read 결과: %s", string(buf2[:n2]))

	// *os.File에서 fd 추출
	fmt.Printf("os.File 내부 fd: %d\n", file.Fd())

	// ----------------------------------------
	// Part 3: strace 결과 비교
	// ----------------------------------------
	fmt.Println("\n--- Part 3: strace로 비교해보세요 ---")
	fmt.Println(`
실행 명령어:
  strace -e openat,read,close go run main.go 2>&1 | grep hostname

예상 결과 (두 방식 모두 동일한 시스템 콜):
  openat(AT_FDCWD, "/etc/hostname", O_RDONLY|O_CLOEXEC) = 3
  read(3, "container-id\n", 256) = 13
  close(3) = 0
`)

	// ----------------------------------------
	// Part 4: 시스템 콜 횟수 비교
	// ----------------------------------------
	fmt.Println("--- Part 4: 시스템 콜 통계 ---")
	fmt.Println(`
실행 명령어:
  strace -c go run main.go 2>&1 | tail -30

확인할 점:
  - openat, read, close 호출 횟수
  - os 패키지가 추가로 호출하는 시스템 콜이 있는가?
`)

	// ----------------------------------------
	// TODO 3: 추상화의 장단점 정리
	// ----------------------------------------
	fmt.Println("\n--- 추상화의 장단점 ---")
	fmt.Println(`
os 패키지 (고수준):
  장점:
    - 사용하기 쉬움
    - 에러 처리가 Go 스타일
    - 크로스 플랫폼 호환
  단점:
    - (생각해보세요)

unix 패키지 (저수준):
  장점:
    - 시스템 콜 직접 제어
    - 세밀한 옵션 설정 가능
  단점:
    - (생각해보세요)
`)

	// ----------------------------------------
	// 생각해볼 점
	// ----------------------------------------
	// 1. os.Open()의 O_CLOEXEC 플래그는 무엇인가요?
	// 2. 언제 unix 패키지를 직접 사용해야 할까요?
	// 3. Go 런타임은 파일 I/O 외에 어떤 시스템 콜을 호출할까요?
	//    (strace -c로 확인해보세요)
}
