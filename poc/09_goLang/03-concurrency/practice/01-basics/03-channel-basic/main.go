package main

import "fmt"

// 과제: Channel 기초
//
// 목표:
// 1. 채널 생성 및 데이터 송수신
// 2. 버퍼 없는 채널과 버퍼 있는 채널 차이 이해
//
// TODO: 아래 코드를 완성하세요

func main() {
	// Part 1: 버퍼 없는 채널
	// TODO 1: string 타입 채널 생성
	// ch := make(chan string)

	// TODO 2: goroutine에서 채널로 데이터 전송
	// go func() {
	//     ch <- "Hello from goroutine!"
	// }()

	// TODO 3: 채널에서 데이터 수신 및 출력
	// msg := <-ch
	// fmt.Println(msg)

	// Part 2: 버퍼 있는 채널
	// TODO 4: 버퍼 크기 2인 int 채널 생성
	// buffered := make(chan int, 2)

	// TODO 5: 버퍼에 데이터 2개 전송 (블로킹 없이)
	// buffered <- 1
	// buffered <- 2

	// TODO 6: 데이터 수신 및 출력
	// fmt.Println(<-buffered)
	// fmt.Println(<-buffered)
}

// 예상 출력:
// Hello from goroutine!
// 1
// 2
