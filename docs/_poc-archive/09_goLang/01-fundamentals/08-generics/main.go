package main

import (
	"fmt"

	"github.com/samber/lo"
	"golang.org/x/exp/constraints"
)

func main() {
	fmt.Println("=== 제네릭 및 samber/lo 학습 ===\n")

	// TODO: 제네릭 함수 예제
	demonstrateGenericFunctions()

	// TODO: samber/lo Map 예제
	demonstrateMap()

	// TODO: samber/lo Filter 예제
	demonstrateFilter()

	// TODO: samber/lo Reduce 예제
	demonstrateReduce()

	// TODO: 복합 파이프라인 예제
	demonstratePipeline()
}

// demonstrateGenericFunctions 제네릭 함수 데모
func demonstrateGenericFunctions() {
	fmt.Println("--- 제네릭 함수 ---")

	// TODO: Min/Max 사용
	// fmt.Printf("Max(10, 20) = %d\n", Max(10, 20))
	// fmt.Printf("Min(10, 20) = %d\n", Min(10, 20))

	// TODO: Contains 사용
	// numbers := []int{1, 2, 3, 4, 5}
	// fmt.Printf("Contains(numbers, 3) = %v\n", Contains(numbers, 3))
	// fmt.Printf("Contains(numbers, 10) = %v\n", Contains(numbers, 10))

	fmt.Println()
}

// demonstrateMap samber/lo Map 데모
func demonstrateMap() {
	fmt.Println("--- samber/lo Map ---")

	// TODO: 숫자 변환
	numbers := []int{1, 2, 3, 4, 5}
	doubled := lo.Map(numbers, func(n int, _ int) int {
		return n * 2
	})
	fmt.Printf("Original: %v\n", numbers)
	fmt.Printf("Doubled: %v\n", doubled)

	// TODO: 타입 변환
	// strings := lo.Map(numbers, func(n int, _ int) string {
	//     return fmt.Sprintf("number-%d", n)
	// })
	// fmt.Printf("Strings: %v\n", strings)

	fmt.Println()
}

// demonstrateFilter samber/lo Filter 데모
func demonstrateFilter() {
	fmt.Println("--- samber/lo Filter ---")

	numbers := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	// TODO: 짝수 필터링
	evens := lo.Filter(numbers, func(n int, _ int) bool {
		return n%2 == 0
	})
	fmt.Printf("Evens: %v\n", evens)

	// TODO: 5보다 큰 수 필터링
	// greaterThan5 := lo.Filter(numbers, func(n int, _ int) bool {
	//     return n > 5
	// })
	// fmt.Printf("Greater than 5: %v\n", greaterThan5)

	fmt.Println()
}

// demonstrateReduce samber/lo Reduce 데모
func demonstrateReduce() {
	fmt.Println("--- samber/lo Reduce ---")

	numbers := []int{1, 2, 3, 4, 5}

	// TODO: 합계
	sum := lo.Reduce(numbers, func(acc int, n int, _ int) int {
		return acc + n
	}, 0)
	fmt.Printf("Sum: %d\n", sum)

	// TODO: 곱
	// product := lo.Reduce(numbers, func(acc int, n int, _ int) int {
	//     return acc * n
	// }, 1)
	// fmt.Printf("Product: %d\n", product)

	fmt.Println()
}

// demonstratePipeline 복합 파이프라인 데모
func demonstratePipeline() {
	fmt.Println("--- 복합 파이프라인 ---")

	type Product struct {
		Name    string
		Price   float64
		InStock bool
	}

	products := []Product{
		{"A", 100, true},
		{"B", 200, false},
		{"C", 150, true},
		{"D", 50, true},
	}

	// TODO: 재고 있는 제품만 → 세금 추가 → 총합 계산
	// inStock := lo.Filter(products, func(p Product) bool {
	//     return p.InStock
	// })
	//
	// withTax := lo.Map(inStock, func(p Product, _ int) float64 {
	//     return p.Price * 1.1 // 10% 세금
	// })
	//
	// total := lo.Reduce(withTax, func(acc float64, price float64, _ int) float64 {
	//     return acc + price
	// }, 0.0)
	//
	// fmt.Printf("Total (with tax): %.2f\n", total)

	_ = products
	fmt.Println()
}

// === 제네릭 유틸리티 함수들 ===

// Min 두 값 중 작은 값을 반환합니다
func Min[T constraints.Ordered](a, b T) T {
	// TODO: 구현
	if a < b {
		return a
	}
	return b
}

// Max 두 값 중 큰 값을 반환합니다
func Max[T constraints.Ordered](a, b T) T {
	// TODO: 구현
	var zero T
	return zero
}

// Contains 슬라이스에 요소가 포함되어 있는지 확인합니다
func Contains[T comparable](slice []T, item T) bool {
	// TODO: 구현
	// for _, v := range slice {
	//     if v == item {
	//         return true
	//     }
	// }
	return false
}

// Keys 맵의 모든 키를 반환합니다
func Keys[K comparable, V any](m map[K]V) []K {
	// TODO: 구현
	// keys := make([]K, 0, len(m))
	// for k := range m {
	//     keys = append(keys, k)
	// }
	// return keys
	return nil
}

// Values 맵의 모든 값을 반환합니다
func Values[K comparable, V any](m map[K]V) []V {
	// TODO: 구현
	return nil
}

// Clamp 값을 min과 max 사이로 제한합니다
func Clamp[T constraints.Ordered](value, min, max T) T {
	// TODO: 구현
	var zero T
	return zero
}
