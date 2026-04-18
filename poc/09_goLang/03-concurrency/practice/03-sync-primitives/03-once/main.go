package main

import (
	"fmt"
	"sync"
)

// 과제: sync.Once로 싱글톤 구현
//
// 목표:
// 1. 여러 goroutine이 동시에 호출해도 초기화는 한 번만
// 2. 싱글톤 패턴 이해
//
// TODO: 아래 코드를 완성하세요

type Database struct {
	connection string
}

var (
	instance *Database
	// TODO: once sync.Once 추가
)

func GetDatabase() *Database {
	// TODO: once.Do로 초기화 (한 번만 실행)
	// once.Do(func() {
	//     fmt.Println("데이터베이스 연결 중... (이 메시지는 한 번만 출력)")
	//     instance = &Database{
	//         connection: "postgres://localhost:5432/mydb",
	//     }
	// })

	return instance
}

func main() {
	var wg sync.WaitGroup

	// 10개의 goroutine이 동시에 GetDatabase 호출
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			db := GetDatabase()
			fmt.Printf("Goroutine %d: DB 주소 = %p\n", id, db)
		}(i)
	}

	wg.Wait()
	fmt.Println("\n모든 goroutine이 같은 인스턴스를 받았는지 확인하세요!")
}

// 예상 출력:
// 데이터베이스 연결 중... (이 메시지는 한 번만 출력)
// Goroutine 0: DB 주소 = 0xc0000a6020
// Goroutine 1: DB 주소 = 0xc0000a6020
// ...
// (모든 주소가 동일해야 함)
