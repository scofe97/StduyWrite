package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strings"
)

func main() {
	// 1. 테스트용 대용량 파일 생성
	createTestFile("large.txt", 10000) // 10000줄

	// 2. ERROR 포함된 줄만 출력
	count := 0
	err := processLargeFile("large.txt", func(line string) error {
		if strings.Contains(line, "ERROR") {
			count++
			fmt.Println(line)
		}
		return nil
	})

	if err != nil {
		fmt.Println("에러:", err)
		return
	}

	fmt.Printf("총 %d개의 ERROR 발견\n", count)

	// 3. 정리
	os.Remove("large.txt")
}

func createTestFile(path string, lines int) error {
	// TODO: 테스트 파일 생성
	// 랜덤하게 INFO, WARN, ERROR 로그 생성
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	levels := []string{"INFO", "WARN", "ERROR"}

	for i := 0; i < lines; i++ {
		level := levels[rand.Intn(len(levels))]
		fmt.Fprintf(file, "%v Line: %d 메시지\n", level, i)
	}
	return nil
}

func processLargeFile(path string, callback func(line string) error) error {
	// TODO: bufio.Scanner로 줄 단위 처리
	// 1. 파일 열기
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()

	// 2. Scanner 생성
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// 3. 줄마다 callback 호출
		line := scanner.Text()
		if err := callback(line); err != nil {
			return err
		}
	}
	// 4. scanner.Err() 반환
	return scanner.Err()
}
