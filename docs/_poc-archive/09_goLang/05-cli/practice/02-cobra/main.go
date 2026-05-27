package main

import (
	"fmt"
	"github.com/spf13/cobra"
	"strings"
)

var name string
var loud bool
var formal bool
var timeSpent string
var message string
var verbose bool

func init() {
	helloCmd.Flags().StringVarP(&name, "name", "n", "World", "인사할 이름")
	helloCmd.Flags().BoolVarP(&loud, "loud", "l", false, "대문자로 출력")

	byeCmd.Flags().BoolVarP(&formal, "formal", "f", false, "특수 문구 출력")

	logCmd.Flags().StringVarP(&timeSpent, "time", "t", "", "작업 시간")
	logCmd.Flags().StringVarP(&message, "message", "m", "", "작업 로그")

	// 이건 모든 서브커맨드에도 적용
	err := logCmd.MarkFlagRequired("time")
	if err != nil {
		return
	}

	rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "상세 출력")
	rootCmd.AddCommand(helloCmd)
	rootCmd.AddCommand(byeCmd)
	rootCmd.AddCommand(logCmd)
}

var rootCmd = &cobra.Command{
	Use: "mycli",
	PersistentPreRun: func(cmd *cobra.Command, args []string) {
		// 모든 서브커맨드 실행 전에 자동 호출됨
		if verbose {
			fmt.Println("[설정 로드 중...]")
		}
	},
	Short: "나의 CLI 도구",
}

var helloCmd = &cobra.Command{
	Use:   "hello",
	Short: "인사하기",
	Run: func(cmd *cobra.Command, args []string) {
		if loud {
			fmt.Printf("HELLO, %s!\n", strings.ToUpper(name))
		} else {
			fmt.Printf("Hello, %s!\n", name)
		}
	},
}

var byeCmd = &cobra.Command{
	Use:   "bye",
	Short: "작별 인사",
	Run: func(cmd *cobra.Command, args []string) {
		// ...
		if formal {
			fmt.Println("It was a pleasure. Farewell.")
		} else {
			fmt.Println("GoodBye")
		}
	},
}

var logCmd = &cobra.Command{
	Use:   "log [이슈키]",
	Short: "작업 로그 등록",
	Args:  cobra.MinimumNArgs(1),
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Printf("이슈 키: %s 시간: %s 메세지: %s\n", args[0], timeSpent, message)
	},
}

func main() {
	rootCmd.Execute()
}
