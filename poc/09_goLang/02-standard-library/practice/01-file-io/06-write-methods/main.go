package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

func main() {
	count := 10000

	// 1. 직접 쓰기 (시스템 콜 많음)
	fmt.Println("=== 직접 쓰기 ===")
	start := time.Now()
	directWrite(count)
	fmt.Printf("소요 시간: %v\n", time.Since(start))

	// 2. bufio.Writer (버퍼링)
	fmt.Println("\n=== bufio.Writer ===")
	start = time.Now()
	bufferedWrite(count)
	fmt.Printf("소요 시간: %v\n", time.Since(start))
}

func directWrite(count int) {
	// TODO: os.Create로 파일 열고 WriteString으로 count번 쓰기
	file, _ := os.Create("testDirect.log")
	defer file.Close()

	for i := range count {
		io.WriteString(file, "Line "+strconv.Itoa(i)+"\n")
	}
}

func bufferedWrite(count int) {
	// TODO: bufio.NewWriter 사용, 마지막에 Flush 호출
	file, _ := os.Create("testDirect.log")
	defer file.Close()

	writer := bufio.NewWriter(file)
	defer writer.Flush()

	for i := range count {
		fmt.Fprintf(writer, "Line %d\n", i)
	}
}
