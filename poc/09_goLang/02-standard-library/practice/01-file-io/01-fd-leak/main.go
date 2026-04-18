package main

import (
	"fmt"
	"os"
)

func main() {

	data := make([]byte, 100)
	err := os.WriteFile("test.txt", data, 0644)
	if err != nil {
		return
	}

	fileOpen()

}

func fileOpen() {
	for range 10000 {
		_, err := os.Open("test.txt")
		if err != nil {
			fmt.Println("에러 발생:", err)
			return
		}
	}
}
