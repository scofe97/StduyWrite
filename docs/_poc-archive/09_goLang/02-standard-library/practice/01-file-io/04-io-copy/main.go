package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {

	// 1. 기본
	fmt.Println("=== 기본 io.Copy ===")
	src := strings.NewReader("Hello io.Copy!")
	dst := &bytes.Buffer{}
	n, _ := io.Copy(dst, src)
	fmt.Printf("복사된 바이트: %d, 내용: %s\n", n, dst.String())

	// 2. 파일 간 복사 (ReaderFrom 최적화 발생)
	fmt.Println("\n=== 파일 복사 ===")
	src = strings.NewReader("Hello io.Copy!")
	dst = &bytes.Buffer{}
	n, _ = dst.ReadFrom(src)
	fmt.Printf("복사된 바이트: %d, 내용: %s\n", n, dst.String())

	// TODO: source.txt 생성 → dest.txt로 복사
	srcName := "source.txt"
	dstName := "dest.txt"
	os.WriteFile(srcName, []byte("Hello from source file!"), 0644)
	srcFile, _ := os.Open(srcName)
	dstFile, _ := os.Create(dstName)
	defer srcFile.Close()
	defer dstFile.Close()

	n, _ = dstFile.ReadFrom(srcFile)
	copied, _ := os.ReadFile(dstName)
	fmt.Printf("복사된 바이트: %d, 내용: %s\n", n, string(copied))

	// 3. io.CopyN: 제한된 바이트만 복사
	fmt.Println("\n=== io.CopyN (5바이트만) ===")
	src = strings.NewReader("Hello io.Copy!")
	dst = &bytes.Buffer{}
	n, _ = io.CopyN(dst, src, 5)
	fmt.Printf("복사된 바이트: %d, 내용: %s\n", n, dst.String())

	// 4. io.MultiWriter: 여러 Writer에 동시 쓰기
	fmt.Println("\n=== io.MultiWriter ===")
	srcName2 := "source2.txt"
	dstName2 := "dest2.txt"
	os.WriteFile(srcName2, make([]byte, 100), 0644)
	os.WriteFile(dstName2, make([]byte, 100), 0644)
	srcFile2, _ := os.Create(srcName2)
	dstFile2, _ := os.Create(dstName2)
	defer srcFile2.Close()
	defer dstFile2.Close()

	multi := io.MultiWriter(os.Stdout, srcFile2, dstFile2)
	fmt.Fprintln(multi, "이 메시지는 화면과 파일 모두에!")

	// 5. io.MultiReader: 여러 Reader를 하나로 연결
	fmt.Println("\n=== io.MultiReader ===")
	r1 := strings.NewReader("First ")
	r2 := strings.NewReader("Second ")
	r3 := strings.NewReader("Third")
	multiReader := io.MultiReader(r1, r2, r3)

	result, _ := io.ReadAll(multiReader)
	fmt.Printf("연결된 내용: %s\n", string(result))
}
