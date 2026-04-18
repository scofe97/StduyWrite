package main

import (
	"fmt"
	"os"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.PROT_READ

// Step 2: 파일 mmap - 파일을 메모리처럼 접근
//
// 목표: 파일을 메모리에 매핑하여 배열처럼 접근하는 방법을 배웁니다.
// 이 방식은 대용량 파일 처리에 매우 유용합니다.
//
// 준비:
//   echo "Hello, memory-mapped file!" > /tmp/testfile.txt
//
// 실행: go run main.go
// 검증: strace -e mmap,read,write go run main.go

func main() {
	fmt.Println("=== Step 2: 파일 mmap ===")

	testFile := "/tmp/testfile.txt"

	// ----------------------------------------
	// Part 0: 테스트 파일 준비
	// ----------------------------------------
	fmt.Println("\n--- Part 0: 테스트 파일 준비 ---")

	// 테스트 파일이 없으면 생성
	if _, err := os.Stat(testFile); os.IsNotExist(err) {
		os.WriteFile(testFile, []byte("Hello, memory-mapped file!\n"), 0644)
		fmt.Println("테스트 파일 생성됨")
	}

	// ----------------------------------------
	// Part 1: 파일 열기
	// ----------------------------------------
	fmt.Println("\n--- Part 1: 파일 열기 ---")

	// TODO 1: unix.Open()으로 파일 열기
	// 힌트: 읽기+쓰기로 열어야 매핑도 읽기+쓰기 가능

	// fd, err := unix.Open(testFile, unix.O_RDWR, 0)
	// if err != nil {
	// 	fmt.Printf("파일 열기 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(fd)
	// fmt.Printf("fd: %d\n", fd)

	// 파일 크기 확인
	// var stat unix.Stat_t
	// unix.Fstat(fd, &stat)
	// fileSize := int(stat.Size)
	// fmt.Printf("파일 크기: %d bytes\n", fileSize)

	fmt.Println("(TODO: 파일 열기 구현)")
	fileSize := 27 // 임시값 (위 코드 완성 후 삭제)
	fd := 3        // 임시값 (위 코드 완성 후 삭제)
	_ = fd

	// ----------------------------------------
	// Part 2: 파일을 메모리에 매핑
	// ----------------------------------------
	fmt.Println("\n--- Part 2: 파일 mmap ---")

	// TODO 2: mmap으로 파일 매핑
	// 힌트:
	// - fd에 실제 파일 디스크립터 전달
	// - length는 파일 크기 이상이어야 함
	// - MAP_SHARED로 매핑하면 변경이 파일에 반영됨

	// data, err := unix.Mmap(
	//     fd,                              // 파일 디스크립터
	//     0,                               // 파일 시작 위치
	//     fileSize,                        // 매핑 크기
	//     unix.PROT_READ|unix.PROT_WRITE, // 읽기+쓰기
	//     unix.MAP_SHARED,                 // 변경 공유
	// )
	// if err != nil {
	// 	fmt.Printf("mmap 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Munmap(data)

	fmt.Println("(TODO: 파일 mmap 구현)")
	data := make([]byte, fileSize) // 임시 (위 코드 완성 후 삭제)

	// ----------------------------------------
	// Part 3: 메모리로 파일 읽기
	// ----------------------------------------
	fmt.Println("\n--- Part 3: 메모리로 파일 읽기 ---")

	// TODO 3: 매핑된 메모리에서 데이터 읽기
	// 힌트: data는 파일 내용이 그대로 들어있는 []byte

	fmt.Printf("파일 내용: %s", string(data))

	// 특정 바이트 접근 (read() 시스템 콜 없이!)
	// fmt.Printf("첫 번째 문자: %c (0x%02x)\n", data[0], data[0])

	// ----------------------------------------
	// Part 4: 메모리로 파일 수정
	// ----------------------------------------
	fmt.Println("\n--- Part 4: 메모리로 파일 수정 ---")

	// TODO 4: 매핑된 메모리를 수정하여 파일 변경
	// 주의: MAP_SHARED이면 실제 파일이 변경됩니다!

	// 첫 글자를 대문자로 변경
	// if data[0] >= 'a' && data[0] <= 'z' {
	//     data[0] = data[0] - 32  // 소문자 → 대문자
	//     fmt.Println("첫 글자를 대문자로 변경")
	// }

	fmt.Println("(TODO: 메모리로 파일 수정 구현)")

	// ----------------------------------------
	// Part 5: msync로 동기화
	// ----------------------------------------
	fmt.Println("\n--- Part 5: msync ---")

	// TODO 5: 메모리 변경을 디스크에 동기화
	// 힌트: unix.Msync(data, flags)
	// MS_SYNC: 동기적으로 (완료될 때까지 대기)
	// MS_ASYNC: 비동기적으로 (바로 반환)

	// err = unix.Msync(data, unix.MS_SYNC)
	// if err != nil {
	//     fmt.Printf("msync 실패: %v\n", err)
	// }
	// fmt.Println("변경 사항을 디스크에 동기화했습니다")

	fmt.Println("(TODO: msync 구현)")

	// ----------------------------------------
	// Part 6: 변경 확인
	// ----------------------------------------
	fmt.Println("\n--- Part 6: 변경 확인 ---")

	// cat 명령어로 파일 내용 확인
	fmt.Println("변경된 파일 확인: cat", testFile)

	// ----------------------------------------
	// 생각해볼 점
	// ----------------------------------------
	fmt.Println("\n--- 생각해볼 점 ---")
	fmt.Println(`
1. mmap + 메모리 접근 vs read() 시스템 콜
   어느 쪽이 더 빠를까요?
   - 힌트: 시스템 콜 오버헤드 vs 페이지 폴트

2. MAP_SHARED vs MAP_PRIVATE
   - SHARED: 변경이 파일에 반영
   - PRIVATE: Copy-on-Write, 변경이 프로세스 내에서만 유효

3. 대용량 파일 mmap의 장점
   - 100GB 파일을 16GB RAM에서 처리 가능
   - 필요한 부분만 메모리에 로드 (Demand Paging)

4. msync를 호출하지 않으면?
   - OS가 적절한 시점에 자동으로 동기화
   - 하지만 크래시 시 데이터 손실 가능
`)
}
