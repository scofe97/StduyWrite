package main

import (
	"fmt"
	"os"
)

func ReadFile(path string) (string, error) {
	// 1. path가 빈 문자열이면 ErrEmptyPath 반환
	if len(path) == 0 {
		return "", ErrEmptyPath
	}

	// 2. 파일 읽기 시도 (os.ReadFile 사용)
	var file, err = os.ReadFile(path)
	if err != nil {
		// 3. 에러 발생 시 래핑해서 반환: fmt.Errorf("ReadFile failed: %w", err)
		return "", fmt.Errorf("Readfile failed: %w", err)
	}

	// 4. 성공 시 내용 반환
	return string(file), nil

}
