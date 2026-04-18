package main

import (
	"fmt"
	"sync"
	"time"
)

func WaitGroup() {
	var wg sync.WaitGroup

	wg.Add(1) // 기다릴 goroutine 수 추가
	go func() {
		defer wg.Done() // 완료 신호
		fmt.Println("goroutine 실행됨")
	}()

	wg.Wait() // 모든 goroutine 완료까지 대기
	fmt.Println("main 종료")
}

func Channel() {
	ch := make(chan string) // 채널 생성

	go func() {
		ch <- "hello" // 채널에 전송
	}()

	msg := <-ch // 채널에서 수신 (블로킹)
	fmt.Println(msg)
}

func worker(id int, ch chan string) {
	time.Sleep(time.Second)
	ch <- fmt.Sprintf("worker %d 완료", id)
}

func MultiGoroutine() {
	ch := make(chan string)

	for i := 1; i <= 3; i++ {
		go worker(i, ch)
	}

	// 3개 결과 수신
	for i := 0; i < 3; i++ {
		fmt.Println(<-ch)
	}
}

func BufferedChannel() {
	// ch1 := make(chan int)

	// 버퍼 있는 채널 - 버퍼 크기만큼 전송 가능
	ch2 := make(chan int, 3)

	ch2 <- 1 // OK
	ch2 <- 2 // OK
	ch2 <- 3 // OK
	ch2 <- 4 // 블로킹! (버퍼 가득 참)
}
