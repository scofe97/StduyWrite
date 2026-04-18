package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
)

func main() {
	// 플래그 정의
	pattern := flag.String("pattern", "", "검색할 패턴")
	showLineNum := flag.Bool("n", false, "줄 번호 표시")
	ignoreCase := flag.Bool("i", false, "대소문자 무시")
	invert := flag.Bool("v", false, "매칭되지 않는 줄 출력")

	// 플래그 파싱
	flag.Parse()

	args := flag.Args()
	if len(args) == 0 {
		fmt.Fprintln(os.Stderr, "오류: 파일명을 지정하세요")
		os.Exit(1)
	}
	filename := args[0]

	file, err := os.Open(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "파일 열기 실패: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	searchPattern := *pattern
	if *ignoreCase {
		searchPattern = strings.ToLower(searchPattern)
	}

	scanner := bufio.NewScanner(file)
	lineNum := 0
	matchCount := 0

	for scanner.Scan() {
		lineNum++
		line := scanner.Text()

		compareLine := line
		if *ignoreCase {
			compareLine = strings.ToLower(line)
		}

		matched := strings.Contains(compareLine, searchPattern)

		// -v: 매칭 반전
		if *invert {
			matched = !matched
		}

		if matched {
			matchCount++
			if *showLineNum {
				fmt.Printf("%d: %s\n", lineNum, line)
			} else {
				fmt.Println(line)
			}
		}
	}
	fmt.Printf("검색 패턴: %s\n", *pattern)
	fmt.Printf("나머지 인자: %v\n", flag.Args())
}
