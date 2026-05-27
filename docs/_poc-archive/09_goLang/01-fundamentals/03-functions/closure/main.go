package main

import "fmt"

func makeCounter() func() int {
	count := 0

	return func() int {
		count++
		return count
	}
}

func main() {
	counter := makeCounter()

	fmt.Println(counter())
	fmt.Println(counter())
	fmt.Println(counter())
}
