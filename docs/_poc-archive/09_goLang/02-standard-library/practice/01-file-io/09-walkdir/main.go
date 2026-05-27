package main

import (
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
)

func main() {
	// 테스트 디렉토리 구조 생성
	os.MkdirAll("testdir/src", 0755)
	os.WriteFile("testdir/main.go", []byte("package main"), 0644)
	os.WriteFile("testdir/src/app.go", []byte("package src"), 0644)
	os.WriteFile("testdir/src/util.go", []byte("package src"), 0644)
	os.WriteFile("testdir/readme.txt", []byte("readme"), 0644)
	defer os.RemoveAll("testdir")

	fmt.Println("=== .go 파일 찾기 ===")

	filepath.WalkDir("testdir/src", func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if !d.IsDir() && filepath.Ext(path) == ".go" {
			fmt.Println("Go 파일:", path)
		}

		return nil
	})
}
