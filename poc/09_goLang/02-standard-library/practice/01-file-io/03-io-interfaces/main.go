package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {

	// 1. 파일에서 읽기
	os.WriteFile("test.txt", []byte("Hello from file"), 0644)
	f, _ := os.Open("test.txt")
	defer f.Close()

	// 2. 문자열에서 읽기
	reader := strings.NewReader("Hello from String")

	// 3. 버퍼에서 읽기
	bufferString := bytes.NewBufferString("Hello from String")

	// 동일 함수 처리
	printContent(reader)
	printContent(bufferString)

}

func printContent(r io.Reader) {

	buffer := make([]byte, 100)
	n, _ := r.Read(buffer)
	fmt.Println(string(buffer[:n]))
}
