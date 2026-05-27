package main

import (
	"fmt"
	"os"
)

func main() {
	data := []byte(`{"host":"localhost","port":8080}`)

	fmt.Println("=== 안전한 파일 쓰기 ===")
	err := safeWriteFile("config.json", data, 0644)
	if err != nil {
		fmt.Println("에러:", err)
		return
	}

	// 확인
	content, _ := os.ReadFile("config.json")
	fmt.Println("저장된 내용:", string(content))

	// 정리
	os.Remove("config.json")
}

func safeWriteFile(path string, data []byte, perm os.FileMode) error {
	// TODO: 원자적 쓰기 구현
	// 1. 임시 파일 생성 (같은 디렉토리에)
	temp, err := os.CreateTemp(path, "config-*.json")
	if err != nil {
		return err
	}
	tmpPath := temp.Name()
	defer temp.Close()
	defer os.Remove(tmpPath)

	// 2. 데이터 쓰기
	_, err = temp.Write(data)
	if err != nil {
		return err
	}

	// 3. Sync() 호출
	err = temp.Sync()
	if err != nil {
		return err
	}

	// 4. 권한 설정
	if err := os.Chmod(tmpPath, perm); err != nil {
		return err
	}

	// 5. os.Rename
	if err := os.Rename(tmpPath, path); err != nil {
		return err
	}

	return nil
}
