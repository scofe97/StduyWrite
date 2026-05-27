package main

import (
	"flag"
	"fmt"
	"os"
	"sort"
	"strings"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
	}

	switch os.Args[1] {
	case "list":
		cmdList(os.Args[2:])
	case "get":
		cmdGet(os.Args[2:])
	case "check":
		cmdCheck(os.Args[2:])
	default:
		fmt.Fprintf(os.Stderr, "알 수 없는 명령: %s\n", os.Args[1])
		printUsage()
		os.Exit(1)
	}
}

func cmdList(args []string) {

	fs := flag.NewFlagSet("list", flag.ExitOnError)
	filter := fs.String("filter", "", "필터 문자열")
	fs.Parse(args)

	envs := os.Environ()
	sort.Strings(envs)

	count := 0
	for _, env := range envs {
		if *filter != "" && !strings.Contains(env, *filter) {
			continue
		}
		count++
		fmt.Println(env)
	}

	fmt.Fprintf(os.Stderr, "\n총 %d개 환경 변수\n", len(envs))
}

func cmdGet(args []string) {
	fs := flag.NewFlagSet("get", flag.ExitOnError)
	defaultVal := fs.String("default", "", "기본값")
	fs.Parse(args)

	remaining := fs.Args()
	if len(remaining) == 0 {
		fmt.Fprintf(os.Stderr, "오류: 환경 변수 이름을 지정하세요")
		os.Exit(1)
	}

	key := remaining[0]
	value, exists := os.LookupEnv(key)

	if !exists {
		if *defaultVal != "" {
			fmt.Println(*defaultVal)
			return
		}

		fmt.Fprintf(os.Stderr, "환경 변수 '%s'가 존재하지 않습니다.\n", key)
		os.Exit(1)
	}

	fmt.Println(value)
}

func cmdCheck(args []string) {
	if len(args) == 0 {
		fmt.Fprintf(os.Stderr, "오류: 확인할 환경 변수를 지정하세요")
		os.Exit(1)
	}

	allExist := true

	for _, key := range args {
		_, exists := os.LookupEnv(key)
		if exists {
			fmt.Printf("존재 %s\n", key)
		} else {
			fmt.Printf("미존재 %s\n", key)
			allExist = false
		}
	}

	if !allExist {
		os.Exit(1)
	}

}

func printUsage() {
	fmt.Println(`사용법: envtool <command>

  명령:
    list   환경 변수 목록
    get    특정 변수 조회
    check  변수 존재 확인`)
}
