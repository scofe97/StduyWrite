package main

import (
	"fmt"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.O_RDONLY

// Step 1: 시스템 콜로 직접 파일 읽기
//
// 목표: unix 패키지를 사용하여 /etc/hostname 파일을 읽습니다.
// 이 코드를 완성하면 strace로 실제 시스템 콜을 확인할 수 있습니다.
//
// 실행: go run main.go
// 검증: strace -e openat,read,close go run main.go

func main() {
	fmt.Println("=== Step 1: unix.Open()과 unix.Read()로 파일 읽기 ===")

	// ----------------------------------------
	// TODO 1: unix.Open()으로 /etc/hostname 열기
	// ----------------------------------------
	// 힌트:
	// - unix.Open(path string, mode int, perm uint32) (fd int, err error)
	// - 읽기 전용으로 열려면 mode에 unix.O_RDONLY 사용
	// - perm은 파일 생성 시에만 사용되므로 0으로 설정
	//
	// 예시: fd, err := unix.Open("/some/path", unix.O_RDONLY, 0)

	fd := 0 // <- 이 줄을 수정하세요
	var err error
	_ = err // 컴파일 에러 방지용 (수정 후 삭제)

	// TODO 1 완료 후 아래 주석 해제
	// if err != nil {
	// 	fmt.Printf("파일 열기 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(fd)

	fmt.Printf("파일 디스크립터(fd): %d\n", fd)

	// ----------------------------------------
	// TODO 2: unix.Read()로 데이터 읽기
	// ----------------------------------------
	// 힌트:
	// - unix.Read(fd int, p []byte) (n int, err error)
	// - 버퍼를 미리 만들어서 전달해야 함
	// - 반환값 n은 실제로 읽은 바이트 수
	//
	// 예시:
	// buf := make([]byte, 256)
	// n, err := unix.Read(fd, buf)

	buf := make([]byte, 256)
	n := 0 // <- 이 줄을 수정하세요

	// TODO 2 완료 후 아래 주석 해제
	// if err != nil {
	// 	fmt.Printf("읽기 실패: %v\n", err)
	// 	return
	// }

	fmt.Printf("읽은 바이트 수: %d\n", n)
	fmt.Printf("내용: %s", string(buf[:n]))

	// ----------------------------------------
	// 생각해볼 점
	// ----------------------------------------
	// 1. fd 값이 왜 3인가요? (0, 1, 2는 어디에 쓰이나요?)
	// 2. unix.Open()이 실패하면 fd 값은 어떻게 되나요?
	// 3. buf 크기보다 파일이 크면 어떻게 되나요?
}
