package main

import "fmt"

func main() {
	// === 배열 (Array) ===
	// 고정 크기, 타입의 일부

	// 1. 배열 선언
	var nums [5]int // 제로 값으로 초기화
	fmt.Println("제로 값 배열:", nums)

	// 2. 배열 초기화
	colors := [3]string{"red", "green", "blue"}
	fmt.Println("초기화된 배열:", colors)

	// 3. 크기 자동 계산
	primes := [...]int{2, 3, 5, 7, 11}
	fmt.Println("크기 자동 계산:", primes, "길이:", len(primes))

	// 4. 인덱스 지정 초기화
	indexed := [5]int{1: 10, 3: 30}
	fmt.Println("인덱스 지정:", indexed)

	// 5. 배열은 값 타입 (복사됨)
	original := [3]int{1, 2, 3}
	copied := original
	copied[0] = 100
	fmt.Println("원본:", original, "복사본:", copied)

	// 6. 배열 비교
	a := [3]int{1, 2, 3}
	b := [3]int{1, 2, 3}
	fmt.Println("a == b:", a == b)

	// 7. 다차원 배열
	matrix := [2][3]int{
		{1, 2, 3},
		{4, 5, 6},
	}
	fmt.Println("2x3 행렬:", matrix)

	// 8. 배열 순회
	fmt.Print("순회: ")
	for i, v := range colors {
		fmt.Printf("[%d]=%s ", i, v)
	}
	fmt.Println()
}
