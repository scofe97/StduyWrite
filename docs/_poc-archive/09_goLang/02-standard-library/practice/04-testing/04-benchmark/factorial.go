package benchmark

// 과제 4: 벤치마크 비교
// Factorial의 반복/재귀 구현을 벤치마크로 비교하세요.

// FactorialIterative 반복문으로 팩토리얼 계산
func FactorialIterative(n int) int {
	// TODO: 구현
	// 반복문 사용
	if n < 0 {
		return 0
	}
	result := 1
	for i := 2; i <= n; i++ {
		result *= i
	}
	return result
}

// FactorialRecursive 재귀로 팩토리얼 계산
func FactorialRecursive(n int) int {
	// TODO: 구현
	// 재귀 사용
	if n < 0 {
		return 0
	}
	if n <= 1 {
		return 1
	}
	return n * FactorialRecursive(n-1)
}

// FactorialMemoized 메모이제이션을 사용한 팩토리얼
var memo = make(map[int]int)

func FactorialMemoized(n int) int {
	// TODO: 구현
	// 이미 계산된 값은 캐시에서 반환
	if n < 0 {
		return 0
	}
	if n <= 1 {
		return 1
	}
	if val, ok := memo[n]; ok {
		return val
	}
	memo[n] = n * FactorialMemoized(n-1)
	return memo[n]
}

// StringConcat 문자열 연결 (+ 연산자)
func StringConcatPlus(strs []string) string {
	result := ""
	for _, s := range strs {
		result += s
	}
	return result
}

// StringConcatBuilder strings.Builder 사용
func StringConcatBuilder(strs []string) string {
	// TODO: 구현
	// strings.Builder 사용
	return ""
}
