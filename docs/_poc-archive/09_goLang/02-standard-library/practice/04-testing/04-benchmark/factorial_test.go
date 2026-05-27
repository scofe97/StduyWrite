package benchmark

import (
	"fmt"
	"testing"
)

// 과제 4: 벤치마크 비교
// 반복 vs 재귀 성능 비교

// 기본 벤치마크
func BenchmarkFactorialIterative(b *testing.B) {
	for i := 0; i < b.N; i++ {
		FactorialIterative(20)
	}
}

func BenchmarkFactorialRecursive(b *testing.B) {
	for i := 0; i < b.N; i++ {
		FactorialRecursive(20)
	}
}

func BenchmarkFactorialMemoized(b *testing.B) {
	for i := 0; i < b.N; i++ {
		FactorialMemoized(20)
	}
}

// TODO: 다양한 입력 크기로 벤치마크
func BenchmarkFactorialBySize(b *testing.B) {
	sizes := []int{5, 10, 15, 20}

	for _, size := range sizes {
		b.Run(fmt.Sprintf("Iterative-%d", size), func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				FactorialIterative(size)
			}
		})

		b.Run(fmt.Sprintf("Recursive-%d", size), func(b *testing.B) {
			for i := 0; i < b.N; i++ {
				FactorialRecursive(size)
			}
		})
	}
}

// TODO: 문자열 연결 벤치마크
func BenchmarkStringConcat(b *testing.B) {
	strs := make([]string, 1000)
	for i := range strs {
		strs[i] = "hello"
	}

	b.Run("Plus", func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			StringConcatPlus(strs)
		}
	})

	b.Run("Builder", func(b *testing.B) {
		for i := 0; i < b.N; i++ {
			StringConcatBuilder(strs)
		}
	})
}

// TODO: 메모리 할당 측정 벤치마크
func BenchmarkWithAllocs(b *testing.B) {
	b.ReportAllocs() // 메모리 할당 보고

	for i := 0; i < b.N; i++ {
		// 슬라이스 생성 (할당 발생)
		_ = make([]int, 100)
	}
}

// TODO: ResetTimer 사용 예제
func BenchmarkWithSetup(b *testing.B) {
	// 셋업 (측정에서 제외)
	data := make([]int, 10000)
	for i := range data {
		data[i] = i
	}

	b.ResetTimer() // 타이머 리셋

	for i := 0; i < b.N; i++ {
		sum := 0
		for _, v := range data {
			sum += v
		}
	}
}

// 실행 방법:
// go test -bench=. ./practices/04-benchmark/
// go test -bench=. -benchmem ./practices/04-benchmark/
// go test -bench=BenchmarkFactorial -benchtime=5s ./practices/04-benchmark/

// 벤치마크 비교 (benchstat):
// go test -bench=. -count=5 > old.txt
// # 코드 수정 후
// go test -bench=. -count=5 > new.txt
// benchstat old.txt new.txt
