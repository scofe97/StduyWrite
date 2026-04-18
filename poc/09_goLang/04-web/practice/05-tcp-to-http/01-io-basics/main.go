package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	// TODO: messages.txt 파일을 8바이트씩 읽기

	// 1. 파일 열기
	f, err := os.Open("messages.txt")
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer f.Close()

	// 2. 8바이트 버퍼 생성
	buf := make([]byte, 8)

	// 3. 파일 끝까지 읽기
	for {
		n, err := f.Read(buf)
		if err == io.EOF {
			fmt.Println("EOF reached")
			break
		}
		if err != nil {
			fmt.Println("Error reading:", err)
			break
		}

		// 4. 읽은 내용 출력
		fmt.Printf("Read %d bytes: %s\n", n, buf[:n])
	}
}
