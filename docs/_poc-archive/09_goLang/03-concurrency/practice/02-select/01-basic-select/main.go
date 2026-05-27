package main

import (
	"fmt"
	"time"
)

// 과제: 기본 Select
//
// 목표:
// 1. select 문으로 여러 채널 동시 대기
// 2. 먼저 준비된 채널의 데이터 처리
//
// TODO: 아래 코드를 완성하세요

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	// 서로 다른 시간에 데이터 전송
	go func() {
		time.Sleep(200 * time.Millisecond)
		ch1 <- "채널 1에서 온 메시지"
	}()

	go func() {
		time.Sleep(100 * time.Millisecond)
		ch2 <- "채널 2에서 온 메시지"
	}()

	// TODO: select로 먼저 도착한 메시지 2개 받기
	// for i := 0; i < 2; i++ {
	//     select {
	//     case msg := <-ch1:
	//         fmt.Println("ch1:", msg)
	//     case msg := <-ch2:
	//         fmt.Println("ch2:", msg)
	//     }
	// }

	fmt.Println("완료!")
}

// 예상 출력:
// ch2: 채널 2에서 온 메시지
// ch1: 채널 1에서 온 메시지
// 완료!
