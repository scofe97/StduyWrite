package main

import (
	"fmt"
	"net/http"

	"github.com/runners-high/git-provider/internal/provider"
)

func main() {
	fmt.Println("=== Git Provider 테스트 ===")
	fmt.Println()

	// 1. GitHub 설정 테스트
	testGitHub()

	// 2. GitLab 설정 테스트
	testGitLab()

	// 3. Bitbucket 설정 테스트
	testBitbucket()

	// 4. 인터페이스 다형성 테스트
	testPolymorphism()
}

func testGitHub() {
	fmt.Println("--- GitHub 테스트 ---")

	config := &provider.GitHubConfig{
		Token:   "ghp_test_token_12345",
		BaseURL: "", // 공개 GitHub
	}

	// Validate 테스트
	if err := config.Validate(); err != nil {
		fmt.Printf("❌ Validate 실패: %v\n", err)
		return
	}
	fmt.Println("✅ Validate 성공")

	// GetType 테스트
	fmt.Printf("✅ Type: %s\n", config.GetType())

	// GetCredentials 테스트
	creds := config.GetCredentials()
	fmt.Printf("✅ Auth Type: %s\n", creds.GetAuthType())

	// ApplyAuth 테스트
	req, _ := http.NewRequest("GET", "https://api.github.com/user", nil)
	creds.ApplyAuth(req)
	fmt.Printf("✅ Authorization Header: %s\n", req.Header.Get("Authorization"))

	fmt.Println()
}

func testGitLab() {
	fmt.Println("--- GitLab 테스트 ---")

	config := &provider.GitLabConfig{
		Token:   "glpat_test_token_67890",
		BaseURL: "https://gitlab.mycompany.com", // Self-hosted
	}

	if err := config.Validate(); err != nil {
		fmt.Printf("❌ Validate 실패: %v\n", err)
		return
	}
	fmt.Println("✅ Validate 성공")

	fmt.Printf("✅ Type: %s\n", config.GetType())
	fmt.Printf("✅ BaseURL: %s\n", config.GetBaseURL())

	creds := config.GetCredentials()
	req, _ := http.NewRequest("GET", "https://gitlab.mycompany.com/api/v4/user", nil)
	creds.ApplyAuth(req)
	fmt.Printf("✅ Authorization Header: %s\n", req.Header.Get("Authorization"))

	fmt.Println()
}

func testBitbucket() {
	fmt.Println("--- Bitbucket 테스트 ---")

	config := &provider.BitbucketConfig{
		Username:    "my_username",
		AppPassword: "my_app_password",
		Workspace:   "my_workspace",
	}

	if err := config.Validate(); err != nil {
		fmt.Printf("❌ Validate 실패: %v\n", err)
		return
	}
	fmt.Println("✅ Validate 성공")

	fmt.Printf("✅ Type: %s\n", config.GetType())
	fmt.Printf("✅ Workspace: %s\n", config.GetWorkspace())

	creds := config.GetCredentials()
	fmt.Printf("✅ Auth Type: %s\n", creds.GetAuthType())

	req, _ := http.NewRequest("GET", "https://api.bitbucket.org/2.0/user", nil)
	creds.ApplyAuth(req)
	fmt.Printf("✅ Authorization Header: %s\n", req.Header.Get("Authorization"))
	// Basic Auth는 base64 인코딩된 값이 나옴

	fmt.Println()
}

func testPolymorphism() {
	fmt.Println("--- 다형성 테스트 (인터페이스) ---")

	// 서로 다른 프로바이더를 같은 인터페이스로 처리
	configs := []provider.ProviderConfig{
		&provider.GitHubConfig{Token: "github_token"},
		&provider.GitLabConfig{Token: "gitlab_token"},
		&provider.BitbucketConfig{Username: "user", AppPassword: "pass"},
	}

	for _, cfg := range configs {
		// 모든 프로바이더를 동일한 방식으로 처리!
		fmt.Printf("Provider: %-10s | ", cfg.GetType())

		if err := cfg.Validate(); err != nil {
			fmt.Printf("❌ Invalid\n")
			continue
		}

		creds := cfg.GetCredentials()
		fmt.Printf("Auth: %-12s | ✅ Valid\n", creds.GetAuthType())
	}

	fmt.Println()
	fmt.Println("=== 테스트 완료 ===")
}
