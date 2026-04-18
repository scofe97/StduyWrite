package main

import (
	"errors"
	"fmt"
)

func UpdateToken(config GitHubConfig, newToken string) {
	config.Token = newToken
}

func UpdateTokenPtr(config *GitHubConfig, newToken string) {
	config.Token = newToken
}

func main() {
	fmt.Println("Hello go")

	// 질문 1 서로 다른타입변환 안됨
	var str1 Status = "string"
	var str2 string = "string"
	var str3 = Status(str2)
	var str4 = string(str1)
	fmt.Println(str3)
	fmt.Println(str4)

	// 질문 2
	var err1 = errors.New("same message")
	var err2 = errors.New("same message")
	fmt.Println("질문2")
	fmt.Println(err1 == err2)

	// 질문 3
	var config GitHubConfig
	fmt.Println("질문3")
	fmt.Println(config.Token) // 아무것도 안뜸

	// 질문 4
	cfg1 := GitHubConfig{Token: "old"}
	UpdateToken(cfg1, "new")
	fmt.Println(cfg1.Token) // 무엇이 출력될까요? (old)

	cfg2 := GitHubConfig{Token: "old"}
	UpdateTokenPtr(&cfg2, "new")
	fmt.Println(cfg2.Token) // 무엇이 출력될까요? (new)

	// 질문 4
	// var m map[string]string
	// m["key"] = "value"

	m2 := make(map[string]string)
	m2["key"] = "value"

	// 질문 5
	var s []string
	fmt.Printf("전: s=%v, len=%d, cap=%d\n", s, len(s), cap(s))

	s = append(s, "hello")
	fmt.Printf("후: s=%v, len=%d, cap=%d\n", s, len(s), cap(s))

	// 질문 6
	az1 := AzureDevopsConfig{}
	azErr1 := az1.Validate()

	az2 := AzureDevopsConfig{Organization: "my-org"}
	azErr2 := az2.Validate()

	az3 := AzureDevopsConfig{Organization: "my-org", Project: "prj", PAT: "pat"}
	azErr3 := az3.Validate()

	fmt.Println(azErr1)
	fmt.Println(azErr2)
	fmt.Println(azErr3)
}
