package main

import (
	"fmt"
	"os"
	"time"

	"golang.org/x/sys/unix"
)

// 빌드용 blank identifier (TODO 완료 후 제거)
var _ = unix.O_CREAT

// Step 3: 공유 메모리 - 프로세스 간 통신
//
// 목표: 두 프로세스가 같은 메모리 영역을 공유하는 방법을 배웁니다.
// /dev/shm/을 사용한 공유 메모리 IPC를 구현합니다.
//
// 실행:
//   터미널 1: go run main.go write
//   터미널 2: go run main.go read
//
// 검증: ls -la /dev/shm/

const (
	shmPath = "/dev/shm/go-ipc-example"
	shmSize = 4096
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("사용법: go run main.go [write|read]")
		fmt.Println("  write: 공유 메모리에 데이터 쓰기")
		fmt.Println("  read:  공유 메모리에서 데이터 읽기")
		return
	}

	mode := os.Args[1]

	switch mode {
	case "write":
		runWriter()
	case "read":
		runReader()
	default:
		fmt.Println("알 수 없는 모드:", mode)
	}
}

// runWriter는 공유 메모리에 데이터를 씁니다.
func runWriter() {
	fmt.Println("=== 공유 메모리 Writer ===")

	// ----------------------------------------
	// TODO 1: 공유 메모리 파일 생성/열기
	// ----------------------------------------
	// 힌트:
	// - /dev/shm/은 tmpfs로 마운트된 공유 메모리 파일시스템
	// - O_CREAT|O_RDWR로 열어야 함
	// - O_TRUNC로 기존 내용 삭제 (선택)

	// fd, err := unix.Open(shmPath, unix.O_CREAT|unix.O_RDWR|unix.O_TRUNC, 0666)
	// if err != nil {
	// 	fmt.Printf("공유 메모리 열기 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Close(fd)

	fmt.Println("(TODO: 공유 메모리 파일 열기 구현)")
	fd := 3 // 임시값

	// ----------------------------------------
	// TODO 2: 파일 크기 설정
	// ----------------------------------------
	// 힌트: unix.Ftruncate(fd, size)

	// err = unix.Ftruncate(fd, shmSize)
	// if err != nil {
	// 	fmt.Printf("크기 설정 실패: %v\n", err)
	// 	return
	// }

	fmt.Println("(TODO: 파일 크기 설정 구현)")

	// ----------------------------------------
	// TODO 3: mmap으로 공유 메모리 매핑
	// ----------------------------------------
	// 힌트:
	// - MAP_SHARED 필수 (다른 프로세스와 공유하려면)
	// - PROT_READ|PROT_WRITE

	// data, err := unix.Mmap(fd, 0, shmSize, unix.PROT_READ|unix.PROT_WRITE, unix.MAP_SHARED)
	// if err != nil {
	// 	fmt.Printf("mmap 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Munmap(data)

	fmt.Println("(TODO: mmap 구현)")
	data := make([]byte, shmSize) // 임시
	_ = fd

	// ----------------------------------------
	// TODO 4: 데이터 쓰기
	// ----------------------------------------
	fmt.Println("\n데이터 쓰기 시작...")

	for i := 0; i < 10; i++ {
		message := fmt.Sprintf("Message #%d from writer (time: %s)", i, time.Now().Format("15:04:05"))

		// 공유 메모리 클리어 후 새 메시지 쓰기
		for j := range data {
			data[j] = 0
		}
		copy(data, message)

		fmt.Printf("쓰기: %s\n", message)
		time.Sleep(time.Second)
	}

	fmt.Println("\n쓰기 완료")
}

// runReader는 공유 메모리에서 데이터를 읽습니다.
func runReader() {
	fmt.Println("=== 공유 메모리 Reader ===")

	// ----------------------------------------
	// TODO 5: 공유 메모리 파일 열기
	// ----------------------------------------
	// 힌트:
	// - O_RDWR로 열기 (O_CREAT 없이 - 이미 존재해야 함)

	// fd, err := unix.Open(shmPath, unix.O_RDWR, 0)
	// if err != nil {
	// 	fmt.Printf("공유 메모리 열기 실패: %v\n", err)
	// 	fmt.Println("먼저 writer를 실행하세요: go run main.go write")
	// 	return
	// }
	// defer unix.Close(fd)

	fmt.Println("(TODO: 공유 메모리 파일 열기 구현)")
	fd := 3 // 임시값

	// ----------------------------------------
	// TODO 6: mmap으로 공유 메모리 매핑
	// ----------------------------------------
	// 힌트: writer와 동일하게 MAP_SHARED

	// data, err := unix.Mmap(fd, 0, shmSize, unix.PROT_READ|unix.PROT_WRITE, unix.MAP_SHARED)
	// if err != nil {
	// 	fmt.Printf("mmap 실패: %v\n", err)
	// 	return
	// }
	// defer unix.Munmap(data)

	fmt.Println("(TODO: mmap 구현)")
	data := make([]byte, shmSize) // 임시
	_ = fd

	// ----------------------------------------
	// TODO 7: 데이터 읽기 (폴링)
	// ----------------------------------------
	fmt.Println("\n데이터 읽기 시작 (Ctrl+C로 종료)...")

	lastMessage := ""
	for {
		// 널 문자까지 읽기
		end := 0
		for end < len(data) && data[end] != 0 {
			end++
		}

		if end > 0 {
			currentMessage := string(data[:end])
			if currentMessage != lastMessage {
				fmt.Printf("읽기: %s\n", currentMessage)
				lastMessage = currentMessage
			}
		}

		time.Sleep(100 * time.Millisecond)
	}
}

// ----------------------------------------
// 생각해볼 점
// ----------------------------------------
// 1. 공유 메모리의 동기화 문제
//    - 두 프로세스가 동시에 쓰면?
//    - 해결책: 세마포어, 뮤텍스, 또는 원자적 연산
//
// 2. /dev/shm/ vs 일반 mmap 파일
//    - /dev/shm/은 tmpfs (메모리 기반)
//    - 재부팅하면 사라짐
//    - 일반 파일 mmap은 디스크 백업됨
//
// 3. 성능 특성
//    - 파이프, 소켓보다 빠름 (메모리 복사 없음)
//    - 하지만 동기화 오버헤드 존재
//
// 4. 사용 사례
//    - 고성능 IPC가 필요한 경우
//    - 대용량 데이터 공유
//    - 데이터베이스 공유 버퍼
