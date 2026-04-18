package main

import (
	"encoding/csv"
	"fmt"
	"os"
)

func main() {
	records := [][]string{
		{"이름", "나이", "도시"},
		{"김철수", "25", "서울"},
		{"이영희", "30", "부산"},
	}

	// 1. CSV 쓰기
	err := writeCSV("users.csv", records)
	if err != nil {
		fmt.Println("쓰기 에러:", err)
		return
	}

	// 2. CSV 읽기
	data, err := readCSV("users.csv")
	if err != nil {
		fmt.Println("읽기 에러:", err)
		return
	}

	// 3. 출력
	for _, row := range data {
		fmt.Println(row)
	}

	// 4. 정리
	os.Remove("users.csv")
}

func readCSV(path string) ([][]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	return reader.ReadAll()
}

func writeCSV(path string, records [][]string) error {
	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, record := range records {
		if err := writer.Write(record); err != nil {
			return err
		}
	}

	return writer.Error()
}
