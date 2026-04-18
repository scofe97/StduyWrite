package main

import (
	"fmt"
	"sync"
	"time"
)

// 과제: sync.Cond로 생산자-소비자 구현
//
// 목표:
// 1. 조건 변수로 goroutine 간 신호 전달
// 2. Wait/Signal/Broadcast 이해
//
// TODO: 아래 코드를 완성하세요

type Queue struct {
	items []int
	cond  *sync.Cond
}

func NewQueue() *Queue {
	return &Queue{
		items: make([]int, 0),
		cond:  sync.NewCond(&sync.Mutex{}),
	}
}

// Produce는 아이템을 큐에 추가합니다
func (q *Queue) Produce(item int) {
	// TODO: Lock → append → Signal → Unlock
	// q.cond.L.Lock()
	// q.items = append(q.items, item)
	// fmt.Printf("생산: %d (큐 크기: %d)\n", item, len(q.items))
	// q.cond.Signal()  // 대기 중인 소비자 깨움
	// q.cond.L.Unlock()
}

// Consume은 큐에서 아이템을 가져옵니다
func (q *Queue) Consume() int {
	// TODO: Lock → Wait (큐가 비어있으면) → pop → Unlock
	// q.cond.L.Lock()
	// for len(q.items) == 0 {
	//     q.cond.Wait()  // 아이템이 생길 때까지 대기
	// }
	// item := q.items[0]
	// q.items = q.items[1:]
	// q.cond.L.Unlock()
	// return item

	return 0 // 임시 반환
}

func main() {
	queue := NewQueue()
	var wg sync.WaitGroup

	// 소비자 3개
	for i := 1; i <= 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for j := 0; j < 2; j++ {
				item := queue.Consume()
				fmt.Printf("소비자 %d: %d 소비\n", id, item)
			}
		}(i)
	}

	// 잠시 대기 후 생산 시작
	time.Sleep(100 * time.Millisecond)

	// 생산자 (6개 아이템 생산)
	for i := 1; i <= 6; i++ {
		queue.Produce(i)
		time.Sleep(50 * time.Millisecond)
	}

	wg.Wait()
	fmt.Println("완료!")
}

// 예상 출력:
// 생산: 1 (큐 크기: 1)
// 소비자 1: 1 소비
// 생산: 2 (큐 크기: 1)
// 소비자 2: 2 소비
// ...
