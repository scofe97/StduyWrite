package main

import (
	"fmt"
	"time"
)

// 과제: 타임아웃 처리
//
// 목표:
// 1. select와 time.After로 타임아웃 구현
// 2. 느린 작업에 제한 시간 적용
//
// TODO: 아래 코드를 완성하세요

// slowAPI는 느린 API 호출을 시뮬레이션합니다
func slowAPI(result chan<- string) {
	time.Sleep(2 * time.Second) // 2초 걸리는 작업
	result <- "API 응답 데이터"
}

func main() {
	result := make(chan string)

	go slowAPI(result)

	// TODO: 1초 타임아웃 적용
	// select {
	// case data := <-result:
	//     fmt.Println("성공:", data)
	// case <-time.After(1 * time.Second):
	//     fmt.Println("타임아웃! 1초 초과")
	// }

	// 보너스: 3초 타임아웃으로 변경하면 성공해야 함
}

// 예상 출력 (1초 타임아웃):
// 타임아웃! 1초 초과
//
// 예상 출력 (3초 타임아웃):
// 성공: API 응답 데이터
