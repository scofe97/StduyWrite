package tabledriven

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// 과제 1: Table-Driven Tests
// 각 메서드당 최소 5개의 테스트 케이스 작성
// 경계값, 음수, 0 케이스 포함

func TestCalculator_Add(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		// TODO: 테스트 케이스 추가
		// 예시:
		// {"positive numbers", 2, 3, 5},
		// {"negative numbers", -1, -2, -3},
		// {"zero", 0, 0, 0},
		// {"mixed", -5, 10, 5},
		// {"large numbers", 1000000, 2000000, 3000000},
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Add(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Subtract(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		// TODO: 테스트 케이스 추가
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Subtract(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Multiply(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		// TODO: 테스트 케이스 추가
		// 0 곱하기, 음수 곱하기 포함
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Multiply(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Divide(t *testing.T) {
	tests := []struct {
		name        string
		a, b        int
		expected    int
		expectError bool
	}{
		// TODO: 테스트 케이스 추가
		// 0으로 나누기 에러 케이스 포함
		// 예시:
		// {"normal division", 10, 2, 5, false},
		// {"divide by zero", 10, 0, 0, true},
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := calc.Divide(tt.a, tt.b)

			if tt.expectError {
				assert.Error(t, err)
				assert.ErrorIs(t, err, ErrDivideByZero)
			} else {
				require.NoError(t, err)
				assert.Equal(t, tt.expected, result)
			}
		})
	}
}

func TestCalculator_Power(t *testing.T) {
	tests := []struct {
		name     string
		base     int
		exponent int
		expected int
	}{
		// TODO: 테스트 케이스 추가
		// x^0 = 1, x^1 = x 포함
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Power(tt.base, tt.exponent)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Factorial(t *testing.T) {
	tests := []struct {
		name        string
		n           int
		expected    int
		expectError bool
	}{
		// TODO: 테스트 케이스 추가
		// 0! = 1, 음수는 에러
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := calc.Factorial(tt.n)

			if tt.expectError {
				assert.Error(t, err)
			} else {
				require.NoError(t, err)
				assert.Equal(t, tt.expected, result)
			}
		})
	}
}

func TestCalculator_IsEven(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected bool
	}{
		// TODO: 테스트 케이스 추가
		// 0, 양수 짝수, 양수 홀수, 음수 짝수, 음수 홀수
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.IsEven(tt.n)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Max(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		// TODO: 테스트 케이스 추가
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Max(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Min(t *testing.T) {
	tests := []struct {
		name     string
		a, b     int
		expected int
	}{
		// TODO: 테스트 케이스 추가
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Min(tt.a, tt.b)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCalculator_Abs(t *testing.T) {
	tests := []struct {
		name     string
		n        int
		expected int
	}{
		// TODO: 테스트 케이스 추가
		// 0, 양수, 음수
	}

	calc := NewCalculator()

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := calc.Abs(tt.n)
			assert.Equal(t, tt.expected, result)
		})
	}
}

// 실행: go test -v ./practices/01-table-driven/
