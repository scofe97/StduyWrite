package main

import (
	"fmt"
	"os"
)

func main() {
	os.WriteFile("test.txt", []byte("test"), 0644)

	fmt.Println("=== 문제 코드 ===")
	badDefer()

	fmt.Println("\n=== 해결 코드 ===")
	goodDefer()
}

// 문제: defer가 함수 종료 시 실행 (역순)
func badDefer() {
	for i := 1; i <= 3; i++ {
		f, _ := os.Open("test.txt")
		fmt.Printf("파일 열림 %d\n", i)
		defer func(n int) {
			f.Close()
			fmt.Printf("파일 닫힘 %d\n", n)
		}(i)
	}
}

// 해결: 별도 함수로 분리
func goodDefer() {
	for i := 1; i <= 3; i++ {
		processFile(i)
	}
}

func processFile(n int) {
	f, _ := os.Open("test.txt")
	fmt.Printf("파일 열림 %d\n", n)
	defer func() {
		f.Close()
		fmt.Printf("파일 닫힘 %d\n", n)
	}()
}
