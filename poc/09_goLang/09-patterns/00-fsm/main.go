package main

import (
	"fmt"

	"fsm-learning/workflow"
)

func main() {
	// TODO: 게시글 상태 기계 생성
	// post := workflow.NewPost(1, "Hello World")

	// TODO: 상태 확인
	// fmt.Printf("Initial state: %s\n", post.State())

	// TODO: 상태 전이 테스트
	// fmt.Println("\n--- Publishing post ---")
	// err := post.Publish()
	// if err != nil {
	//     fmt.Printf("Error: %v\n", err)
	// }
	// fmt.Printf("Current state: %s\n", post.State())

	// TODO: 잘못된 전이 테스트
	// fmt.Println("\n--- Trying invalid transition ---")
	// err = post.Publish() // 이미 published
	// if err != nil {
	//     fmt.Printf("Expected error: %v\n", err)
	// }

	// TODO: 보관 처리
	// fmt.Println("\n--- Archiving post ---")
	// err = post.Archive()
	// fmt.Printf("Current state: %s\n", post.State())

	// TODO: 재발행
	// fmt.Println("\n--- Republishing post ---")
	// err = post.Republish()
	// fmt.Printf("Current state: %s\n", post.State())

	// TODO: 가능한 전이 확인
	// fmt.Println("\n--- Available transitions ---")
	// fmt.Printf("Can archive? %v\n", post.Can("archive"))
	// fmt.Printf("Can publish? %v\n", post.Can("publish"))

	fmt.Println("FSM learning module")
	_ = workflow.NewPost
}
