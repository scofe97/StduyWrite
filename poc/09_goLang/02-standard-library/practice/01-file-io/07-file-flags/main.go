package main

import (
	"fmt"
	"os"
)

func main() {
	filename := "app.log"

	// 1. os.Create로 첫 번째 쓰기
	fmt.Println("=== os.Create (첫 번째) ===")
	file, _ := os.Create("app.log")
	file.WriteString("Log 1\n")

	// 2. os.Create로 두 번째 쓰기 (덮어쓰기 문제!)
	fmt.Println("=== os.Create (두 번째) ===")
	file, _ = os.Create("app.log")
	file.WriteString("Log 2\n")

	// 3. O_APPEND로 추가 쓰기
	fmt.Println("\n=== O_APPEND 모드 ===")
	openFile, _ := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	openFile.WriteString("Log 3\n")

	// 최종 파일 내용 출력
	data, _ := os.ReadFile(filename)
	fmt.Printf("최종 파일 내용:\n%s", data)

}
