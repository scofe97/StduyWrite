package main

import (
	"fmt"
)

func PrintAuthInfo(c Credentials) {
	fmt.Println(c.GetAuthType())
}

func main() {

	// 실험 1, 2
	var creds []Credentials = []Credentials{
		&TokenCredentials{Token: "token"},
		&BasicCredentials{
			Username: "user",
			Password: "pass",
		},
	}

	for _, c := range creds {
		PrintAuthInfo(c)
	}

	// 실험 3
	var anything interface{}
	anything = 42
	fmt.Printf("%T\n", anything)
	anything = "hello"
	fmt.Printf("%T\n", anything)
	anything = TokenCredentials{Token: "abc"}
	fmt.Printf("%T\n", anything)

	// 실험 4
	// var _ Credentials = (*IncompleteAuth)(nil)

	// 과제
	configs := []ProviderConfig{
		&GitHubConfig{Token: "ghp_xxx"},
		&AzureDevOpsConfig{Organization: "org", Project: "prj", PAT: "pat"},
	}

	for _, cfg := range configs {
		fmt.Printf("Provider: %s, Auth: %s\n",
			cfg.GetType(),
			cfg.GetCredentials().GetAuthType())
	}
}
