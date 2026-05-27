package main

import "fmt"

func main() {
	// 등록된 프로바이더 목록 확인
	fmt.Println("=== 등록된 프로바이더 ===")
	for _, t := range ListProviders() {
		fmt.Printf("- %s\n", t)
	}

	fmt.Println()

	// 팩토리로 프로바이더 생성
	fmt.Println("=== 프로바이더 생성 테스트 ===")

	// GitHub 프로바이더 생성
	github := NewProvider(GitHub, map[string]string{
		"Token":   "token",
		"BaseURL": "https://github.enterprise.com/api",
	})
	if github != nil {
		fmt.Printf("GitHub Type: %s\n", github.GetType())
		fmt.Printf("GitHub URL: %s\n", github.GetBaseURL())
	} else {
		fmt.Println("GitHub: NewProvider 구현 필요!")
	}

	fmt.Println()

	// Azure 프로바이더 생성
	azure := NewProvider(Azure, map[string]string{
		"Organization": "myorg",
		"Project":      "myproject",
		"PAT":          "pat_xxx",
	})
	if azure != nil {
		fmt.Printf("Azure Type: %s\n", azure.GetType())
		fmt.Printf("Azure URL: %s\n", azure.GetBaseURL())
	} else {
		fmt.Println("Azure: 등록되지 않음 (azure.go 구현 필요)")
	}

	fmt.Println()

	// 존재하지 않는 프로바이더
	fmt.Println("=== 미등록 프로바이더 테스트 ===")
	unknown := NewProvider(Bitbucket, map[string]string{})
	if unknown == nil {
		fmt.Println("Bitbucket: 등록되지 않음 (예상대로)")
	}
}
