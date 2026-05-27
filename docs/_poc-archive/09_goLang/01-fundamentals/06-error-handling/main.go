package main

import (
	"errors"
	"fmt"
)

func getLength(s string) (int, error) {
	if len(s) == 0 {
		return 0, errors.New("error")
	}

	return len(s), nil
}

func main() {
	// 실험 1
	len1, err1 := getLength("hello")
	fmt.Println(len1, err1) // 예상 출력?

	len2, err2 := getLength("")
	fmt.Println(len2, err2) // 예상 출력?
	fmt.Println()

	// 실험 2-1
	err21 := errors.New("error")
	err22 := errors.New("error")

	fmt.Println(err21 == err22)                 // 출력 결과는?
	fmt.Println(err21.Error() == err22.Error()) // 출력 결과는?
	fmt.Println()

	// 실험 2-2
	original := errors.New("원본 에러")

	wrapped1 := fmt.Errorf("래핑: %w", original)
	wrapped2 := fmt.Errorf("래핑: %v", original)

	fmt.Println("실험 2-2")
	fmt.Println(wrapped1)
	fmt.Println(wrapped2)
	fmt.Println(errors.Is(wrapped1, original))
	fmt.Println(errors.Is(wrapped2, original))
	fmt.Println()

	// 실험3
	var err error
	fmt.Println(err)
	fmt.Println(err == nil)
	fmt.Println()

	// 테스트 1: 빈 경로
	_, err5 := ReadFile("")
	if errors.Is(err5, ErrEmptyPath) {
		fmt.Println("빈 경로 에러 감지!")
	}

	// 테스트 2: 없는 파일
	_, err5 = ReadFile("nonexistent.txt")
	fmt.Println(err5) // 래핑된 에러 메시지 출력

	// 테스트 3: 실제 파일 (go.mod 읽어보기)
	content, err5 := ReadFile("../go.mod")
	if err5 == nil {
		fmt.Println("파일 내용:", content[:30]) // 앞 50자만
	}
}
