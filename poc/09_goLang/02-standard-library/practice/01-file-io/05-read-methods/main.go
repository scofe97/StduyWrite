package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

func main() {
	// 테스트 파일 생성 (여러 줄)
	content := "Line 1: Hello\nLine 2: ERROR found\nLine 3: World\nLine 4: ERROR again\n"
	os.WriteFile("test.log", []byte(content), 0644)

	// 1. os.ReadFile - 전체 읽기
	fmt.Println("=== os.ReadFile ===")
	file, _ := os.ReadFile("test.log")
	fmt.Println(string(file))

	// 2. bufio.Scanner - 줄 단위 읽기 (ERROR 포함 줄만)
	fmt.Println("\n=== bufio.Scanner (ERROR 줄만) ===")
	open, _ := os.Open("test.log")
	defer open.Close()
	scanners := bufio.NewScanner(open)
	for scanners.Scan() {
		text := scanners.Text()
		if strings.Contains(text, "ERROR") {
			fmt.Println(text)
		}
	}

	// 3. 청크 단위 읽기
	fmt.Println("\n=== 청크 읽기 (10바이트씩) ===")
	open, _ = os.Open("test.log")
	defer open.Close()

	bytes := make([]byte, 10)

	for {
		n, err := open.Read(bytes)
		if err == io.EOF {
			log.Println(err)
			break
		}

		if err != nil {
			log.Fatal(err)
		}
		fmt.Printf("%s", bytes[:n])
	}

}
