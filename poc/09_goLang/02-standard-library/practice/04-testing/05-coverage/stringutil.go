package coverage

import (
	"strings"
	"unicode"
)

// 과제 5: 커버리지 80%
// 이 패키지의 테스트 커버리지를 80% 이상 달성하세요.

// Reverse 문자열 뒤집기
func Reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// IsPalindrome 회문 여부 확인
func IsPalindrome(s string) bool {
	s = strings.ToLower(s)
	// 알파벳과 숫자만 남기기
	var filtered []rune
	for _, r := range s {
		if unicode.IsLetter(r) || unicode.IsDigit(r) {
			filtered = append(filtered, r)
		}
	}

	for i, j := 0, len(filtered)-1; i < j; i, j = i+1, j-1 {
		if filtered[i] != filtered[j] {
			return false
		}
	}
	return true
}

// CountWords 단어 수 세기
func CountWords(s string) int {
	if strings.TrimSpace(s) == "" {
		return 0
	}
	words := strings.Fields(s)
	return len(words)
}

// Truncate 문자열 자르기
func Truncate(s string, maxLen int) string {
	if maxLen <= 0 {
		return ""
	}
	if len(s) <= maxLen {
		return s
	}
	if maxLen <= 3 {
		return s[:maxLen]
	}
	return s[:maxLen-3] + "..."
}

// Capitalize 첫 글자를 대문자로
func Capitalize(s string) string {
	if s == "" {
		return ""
	}
	runes := []rune(s)
	runes[0] = unicode.ToUpper(runes[0])
	return string(runes)
}

// Contains 대소문자 구분 없이 포함 여부
func ContainsIgnoreCase(s, substr string) bool {
	return strings.Contains(
		strings.ToLower(s),
		strings.ToLower(substr),
	)
}

// RemoveSpaces 모든 공백 제거
func RemoveSpaces(s string) string {
	return strings.ReplaceAll(s, " ", "")
}

// IsEmpty 빈 문자열 또는 공백만 있는지 확인
func IsEmpty(s string) bool {
	return strings.TrimSpace(s) == ""
}

// Repeat 문자열 반복
func Repeat(s string, count int) string {
	if count <= 0 {
		return ""
	}
	return strings.Repeat(s, count)
}

// SplitAndTrim 구분자로 나누고 각 요소 트림
func SplitAndTrim(s, sep string) []string {
	parts := strings.Split(s, sep)
	result := make([]string, 0, len(parts))
	for _, p := range parts {
		trimmed := strings.TrimSpace(p)
		if trimmed != "" {
			result = append(result, trimmed)
		}
	}
	return result
}
