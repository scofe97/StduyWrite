package coverage

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// 과제 5: 커버리지 80%
// 모든 함수에 대한 테스트 케이스 작성

func TestReverse(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		// TODO: 테스트 케이스 추가
		// {"empty", "", ""},
		// {"single char", "a", "a"},
		// {"hello", "hello", "olleh"},
		// {"unicode", "한글", "글한"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Reverse(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestIsPalindrome(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected bool
	}{
		// TODO: 테스트 케이스 추가
		// {"empty", "", true},
		// {"single", "a", true},
		// {"palindrome", "racecar", true},
		// {"not palindrome", "hello", false},
		// {"with spaces", "A man a plan a canal Panama", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := IsPalindrome(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCountWords(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected int
	}{
		// TODO: 테스트 케이스 추가
		// {"empty", "", 0},
		// {"whitespace only", "   ", 0},
		// {"one word", "hello", 1},
		// {"multiple words", "hello world foo", 3},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := CountWords(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestTruncate(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		maxLen   int
		expected string
	}{
		// TODO: 테스트 케이스 추가
		// 모든 분기 커버:
		// - maxLen <= 0
		// - len(s) <= maxLen
		// - maxLen <= 3
		// - 일반 케이스
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Truncate(tt.input, tt.maxLen)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestCapitalize(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		// TODO: 테스트 케이스 추가
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Capitalize(tt.input)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestContainsIgnoreCase(t *testing.T) {
	tests := []struct {
		name     string
		s        string
		substr   string
		expected bool
	}{
		// TODO: 테스트 케이스 추가
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := ContainsIgnoreCase(tt.s, tt.substr)
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestRemoveSpaces(t *testing.T) {
	// TODO: 테스트 구현
}

func TestIsEmpty(t *testing.T) {
	// TODO: 테스트 구현
}

func TestRepeat(t *testing.T) {
	// TODO: 테스트 구현
}

func TestSplitAndTrim(t *testing.T) {
	// TODO: 테스트 구현
}

// 실행 방법:
// go test -cover ./practices/05-coverage/
// go test -coverprofile=coverage.out ./practices/05-coverage/
// go tool cover -html=coverage.out -o coverage.html
// go tool cover -func=coverage.out
