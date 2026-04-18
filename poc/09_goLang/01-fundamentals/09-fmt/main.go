package main

import (
	"errors"
	"fmt"
)

func main() {

	name := "Alice"
	age := 25
	key := 165.29
	isStudent := true

	fmt.Printf("이름: %v, 나이: %v세, 키: %.2fcm, 학생: %v", name, age, key, isStudent)

	data := [][]any{
		{1, "김철수", 5000},
		{2, "이영희", 4500},
		{3, "박민수", 4200},
	}

	fmt.Println()
	fmt.Printf("| %-4v | %-8v | %6v |\n", "ID", "이름", "급여")
	for _, row := range data {
		fmt.Printf("| %-4v | %-8v | %6v |\n", row[0], row[1], row[2])
	}

	origianlErr := errors.New("connection refused")
	errV := fmt.Errorf("DB 실패: %v", origianlErr)
	errW := fmt.Errorf("DB 실패: %w", origianlErr)

	fmt.Println("errV:", errV)
	fmt.Println("errW:", errW)

	fmt.Println("errors.Is(errV, originErr)", errors.Is(errV, origianlErr))
	fmt.Println("errors.Is(errW, originErr)", errors.Is(errW, origianlErr))

}
