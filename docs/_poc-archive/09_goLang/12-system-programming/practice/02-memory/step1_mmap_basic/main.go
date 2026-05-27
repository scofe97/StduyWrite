package main

import (
	"fmt"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.PROT_READ

// Step 1: mmap 기초 - 익명 메모리 할당
//
// 목표: mmap으로 메모리를 할당하고 사용하는 방법을 배웁니다.
// Go의 make()나 new()와 달리, mmap은 OS 커널에 직접 메모리를 요청합니다.
//
// 실행: go run main.go
// 검증: strace -e mmap,munmap,mprotect go run main.go

func main() {
	fmt.Println("=== Step 1: mmap 기초 ===")

	// ----------------------------------------
	// Part 1: 익명 메모리 매핑 (Anonymous Mapping)
	// ----------------------------------------
	fmt.Println("\n--- Part 1: 익명 메모리 매핑 ---")

	// TODO 1: mmap으로 4KB 메모리 할당
	// ----------------------------------------
	// 힌트:
	// unix.Mmap(fd int, offset int64, length int, prot int, flags int) ([]byte, error)
	//
	// 파라미터:
	//   fd: 파일 디스크립터 (익명 매핑이면 -1)
	//   offset: 파일 내 시작 위치 (익명 매핑이면 0)
	//   length: 매핑할 크기 (바이트)
	//   prot: 보호 플래그 (PROT_READ, PROT_WRITE, PROT_EXEC)
	//   flags: 매핑 플래그 (MAP_SHARED, MAP_PRIVATE, MAP_ANONYMOUS)
	//
	// 예시:
	// data, err := unix.Mmap(
	//     -1,                                    // fd: 파일 없음
	//     0,                                     // offset: 시작점
	//     4096,                                  // length: 4KB
	//     unix.PROT_READ|unix.PROT_WRITE,       // 읽기+쓰기 가능
	//     unix.MAP_PRIVATE|unix.MAP_ANONYMOUS,  // 프라이빗 + 익명
	// )

	pageSize := 4096 // 일반적인 페이지 크기

	var data []byte
	var err error
	_ = pageSize // 컴파일 에러 방지용 (수정 후 삭제)
	_ = err

	// TODO: 위 예시를 참고하여 mmap 호출
	// data, err = unix.Mmap(...)

	// TODO 완료 후 아래 주석 해제
	// if err != nil {
	// 	fmt.Printf("mmap 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Munmap(data)

	fmt.Printf("할당된 메모리 크기: %d bytes\n", len(data))
	// fmt.Printf("메모리 주소: %p\n", &data[0])

	// ----------------------------------------
	// Part 2: 메모리에 데이터 쓰기
	// ----------------------------------------
	fmt.Println("\n--- Part 2: 메모리 쓰기 ---")

	// TODO 2: 할당된 메모리에 데이터 쓰기
	// 힌트: data는 []byte이므로 일반 슬라이스처럼 사용

	// message := []byte("Hello, mmap!")
	// copy(data, message)
	// fmt.Printf("쓴 데이터: %s\n", string(data[:len(message)]))

	fmt.Println("(TODO: 메모리에 데이터 쓰기 구현)")

	// ----------------------------------------
	// Part 3: 메모리 보호 플래그 실험
	// ----------------------------------------
	fmt.Println("\n--- Part 3: 메모리 보호 플래그 ---")

	// TODO 3: 읽기 전용으로 매핑하고 쓰기 시도하면?
	// 힌트: PROT_READ만 설정하고 쓰기 시도 → SIGSEGV

	// readOnly, _ := unix.Mmap(-1, 0, 4096, unix.PROT_READ, unix.MAP_PRIVATE|unix.MAP_ANONYMOUS)
	// defer unix.Munmap(readOnly)
	//
	// 주의: 아래 코드는 프로그램을 크래시시킵니다!
	// readOnly[0] = 'X'  // SIGSEGV!

	fmt.Println("읽기 전용 메모리에 쓰면 SIGSEGV 발생 (주석 해제하여 테스트)")

	// ----------------------------------------
	// Part 4: mprotect로 보호 플래그 변경
	// ----------------------------------------
	fmt.Println("\n--- Part 4: mprotect ---")

	// TODO 4: 런타임에 메모리 보호 플래그 변경
	// 힌트: unix.Mprotect(data, prot)

	// err = unix.Mprotect(data, unix.PROT_READ)
	// if err != nil {
	//     fmt.Printf("mprotect 실패: %v\n", err)
	// }
	// fmt.Println("메모리를 읽기 전용으로 변경했습니다")

	fmt.Println("(TODO: mprotect로 보호 플래그 변경)")

	// ----------------------------------------
	// 생각해볼 점
	// ----------------------------------------
	fmt.Println("\n--- 생각해볼 점 ---")
	fmt.Println(`
1. mmap과 make([]byte, n)의 차이는 무엇인가요?
   - 힌트: make는 Go 힙에, mmap은 커널이 직접 관리

2. MAP_PRIVATE vs MAP_SHARED의 차이는?
   - 힌트: 변경 사항의 가시성

3. 왜 4096바이트(페이지 크기)로 할당하나요?
   - 힌트: 페이지 단위 관리
`)
}
