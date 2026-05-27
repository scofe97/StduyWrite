package tabledriven

import "errors"

// 과제 1: Table-Driven Tests
// Calculator의 모든 메서드에 대해 Table-Driven Tests를 작성하세요.

// ErrDivideByZero 0으로 나눌 때 반환
var ErrDivideByZero = errors.New("cannot divide by zero")

// ErrNegativeFactorial 음수 팩토리얼 시 반환
var ErrNegativeFactorial = errors.New("factorial of negative number")

// Calculator 기본 산술 연산 수행
type Calculator struct{}

// NewCalculator 새 Calculator 인스턴스 생성
func NewCalculator() *Calculator {
	return &Calculator{}
}

// TODO: 아래 메서드들을 구현하세요

// Add 두 정수의 합 반환
func (c *Calculator) Add(a, b int) int {
	// TODO: 구현
	return 0
}

// Subtract 두 정수의 차 반환
func (c *Calculator) Subtract(a, b int) int {
	// TODO: 구현
	return 0
}

// Multiply 두 정수의 곱 반환
func (c *Calculator) Multiply(a, b int) int {
	// TODO: 구현
	return 0
}

// Divide 두 정수의 몫 반환, 0으로 나누면 에러
func (c *Calculator) Divide(a, b int) (int, error) {
	// TODO: 구현
	// b가 0이면 ErrDivideByZero 반환
	return 0, nil
}

// Power a의 b제곱 반환 (b >= 0 가정)
func (c *Calculator) Power(a, b int) int {
	// TODO: 구현
	// x^0 = 1, x^1 = x
	return 0
}

// Factorial n! 반환, n < 0이면 에러
func (c *Calculator) Factorial(n int) (int, error) {
	// TODO: 구현
	// 0! = 1, n! = n * (n-1)!
	return 0, nil
}

// IsEven n이 짝수이면 true
func (c *Calculator) IsEven(n int) bool {
	// TODO: 구현
	return false
}

// Max 두 정수 중 큰 값 반환
func (c *Calculator) Max(a, b int) int {
	// TODO: 구현
	return 0
}

// Min 두 정수 중 작은 값 반환
func (c *Calculator) Min(a, b int) int {
	// TODO: 구현
	return 0
}

// Abs 절댓값 반환
func (c *Calculator) Abs(n int) int {
	// TODO: 구현
	return 0
}
