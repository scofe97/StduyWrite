package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

// TODO: 필요한 패키지 import
// - fmt: 에러 출력용
// - os: 프로그램 종료용
// - mycli/cmd: 커맨드 패키지

func main() {

	if len(os.Args) < 2 {
		fmt.Println("사용법: mycli <command>")
		return
	}

	cmd1 := os.Args[1]

	switch cmd1 {
	case "hello":
		fmt.Println("Hello")
	case "bye":
		fmt.Println("GoodBye")
	default:
		fmt.Println("알 수 없는 명령")
	}

	cmdHello(os.Args[2:])
}

func cmdHello(args []string) {
	fs := flag.NewFlagSet("hello", flag.ExitOnError)

	name := fs.String("name", "World", "인사할 이름")
	loud := fs.Bool("loud", false, "대문자로 출력")

	err := fs.Parse(args)
	if err != nil {
		return
	}

	if *loud {
		fmt.Printf("Hello %s!\n", strings.ToUpper(*name))
	} else {
		fmt.Printf("Hello, %s!\n", *name)
	}

}
