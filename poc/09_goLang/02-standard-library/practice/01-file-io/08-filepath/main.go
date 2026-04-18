package main

import (
	"fmt"
	"path/filepath"
)

func main() {

	// 1. 경로 조합
	fmt.Println("=== filepath.Join ===")
	// TODO: "dir", "subdir", "file.txt" 조합
	join := filepath.Join("dir", "subdir", "file.txt")
	fmt.Println(join)

	// 2. 경로 분리
	fmt.Println("\n=== 경로 분리 ===")
	path := "/home/user/docs/report.pdf"
	// TODO: Dir, Base, Ext 출력
	dir := filepath.Dir(path)
	base := filepath.Base(path)
	ext := filepath.Ext(path)
	fmt.Println(dir)
	fmt.Println(base)
	fmt.Println(ext)

	// 3. 절대 경로 변환
	fmt.Println("\n=== 절대 경로 ===")
	abs, _ := filepath.Abs(".")
	fmt.Println(abs)
	// TODO: 상대 경로 "." 를 절대 경로로 변환

	// 4. 경로 정리
	fmt.Println("\n=== Clean ===")
	clean := filepath.Clean("dir/../other/./file.txt")
	fmt.Println(clean)
	// TODO: "dir/../other/./file.txt" 정리

}
