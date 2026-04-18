package main

import (
	"fmt"
	"os"
)

func main() {
	// stdout (fd 1)으로 출력
	fmt.Fprintln(os.Stdout, "[STDOUT] 정상 메시지 1")
	fmt.Fprintln(os.Stdout, "[STDOUT] 정상 메시지 2")

	// stderr (fd 2)로 출력
	fmt.Fprintln(os.Stderr, "[STDERR] 에러 메시지 1")
	fmt.Fprintln(os.Stderr, "[STDERR] 에러 메시지 2")

	// 다시 stdout
	fmt.Fprintln(os.Stdout, "[STDOUT] 정상 메시지 3")
}
