package main

import (
	"fmt"
	"sync"
	"time"
)

// 과제: RWMutex로 캐시 구현
//
// 목표:
// 1. 읽기 작업은 동시 허용
// 2. 쓰기 작업은 단독 실행
//
// TODO: 아래 코드를 완성하세요

type Cache struct {
	data map[string]string
	// TODO: mu sync.RWMutex 추가
}

func NewCache() *Cache {
	return &Cache{
		data: make(map[string]string),
	}
}

// Get은 캐시에서 값을 읽습니다 (여러 goroutine 동시 가능)
func (c *Cache) Get(key string) (string, bool) {
	// TODO: RLock/RUnlock 추가
	value, ok := c.data[key]
	return value, ok
}

// Set은 캐시에 값을 씁니다 (단독 실행)
func (c *Cache) Set(key, value string) {
	// TODO: Lock/Unlock 추가
	c.data[key] = value
}

func main() {
	cache := NewCache()
	var wg sync.WaitGroup

	// 쓰기 goroutine (5개)
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			key := fmt.Sprintf("key%d", id)
			cache.Set(key, fmt.Sprintf("value%d", id))
			fmt.Printf("Writer %d: %s 저장\n", id, key)
		}(i)
	}

	time.Sleep(100 * time.Millisecond) // 쓰기 먼저 완료 대기

	// 읽기 goroutine (10개)
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			key := fmt.Sprintf("key%d", id%5)
			if value, ok := cache.Get(key); ok {
				fmt.Printf("Reader %d: %s = %s\n", id, key, value)
			}
		}(i)
	}

	wg.Wait()
	fmt.Println("완료!")
}

// RWMutex를 사용하면 여러 Reader가 동시에 읽을 수 있어
// 읽기가 많은 워크로드에서 성능이 향상됩니다.
