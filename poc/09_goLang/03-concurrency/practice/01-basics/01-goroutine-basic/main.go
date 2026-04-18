package main

import (
	"fmt"
	"time"
)

// 과제: Goroutine 기초
//
// 목표:
// 1. goroutine을 생성하고 실행하기
// 2. main 함수가 먼저 종료되면 goroutine도 종료됨을 이해하기
//
// TODO: 아래 코드를 완성하세요

func sayHello(name string) {
	// TODO: "Hello, {name}!" 출력
}

func main() {
	// TODO 1: sayHello를 goroutine으로 실행 (go 키워드 사용)
	// sayHello("Go")

	// TODO 2: main이 먼저 끝나지 않도록 대기
	// 힌트: time.Sleep 사용

	fmt.Println("main 함수 종료")
}

// 예상 출력:
// Hello, Go!
// main 함수 종료

// 참고: time.Sleep은 임시 해결책입니다.
// 다음 과제에서 WaitGroup을 사용한 적절한 동기화를 배웁니다.
