package main

import "fmt"

// 과제: 논블로킹 채널 연산
//
// 목표:
// 1. default 케이스로 블로킹 방지
// 2. 채널이 비어있을 때 대체 동작 수행
//
// TODO: 아래 코드를 완성하세요

func main() {
	messages := make(chan string, 2)

	// 채널에 데이터 추가
	messages <- "첫 번째"
	messages <- "두 번째"
	// 버퍼가 가득 참!

	// TODO 1: 논블로킹 전송 - 버퍼가 가득 차면 default 실행
	// select {
	// case messages <- "세 번째":
	//     fmt.Println("세 번째 메시지 전송 성공")
	// default:
	//     fmt.Println("채널이 가득 참, 전송 실패")
	// }

	// 데이터 하나 빼기
	fmt.Println("수신:", <-messages)

	// TODO 2: 논블로킹 수신 - 여러 번 시도
	// for i := 0; i < 3; i++ {
	//     select {
	//     case msg := <-messages:
	//         fmt.Println("수신:", msg)
	//     default:
	//         fmt.Println("더 이상 데이터 없음")
	//     }
	// }
}

// 예상 출력:
// 채널이 가득 참, 전송 실패
// 수신: 첫 번째
// 수신: 두 번째
// 더 이상 데이터 없음
// 더 이상 데이터 없음
