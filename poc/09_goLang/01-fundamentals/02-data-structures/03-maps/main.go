package main

import "fmt"

func main() {
	// === 맵 (Map) ===
	// 키-값 저장소 (해시 테이블)

	// 1. 맵 생성
	// make 사용
	scores := make(map[string]int)
	scores["Alice"] = 95
	scores["Bob"] = 87
	fmt.Println("scores:", scores)

	// 리터럴
	ages := map[string]int{
		"Kim":  25,
		"Lee":  30,
		"Park": 28,
	}
	fmt.Println("ages:", ages)

	// 2. 값 조회
	fmt.Println("Kim의 나이:", ages["Kim"])

	// 3. 키 존재 확인 (comma ok idiom)
	if val, ok := ages["Choi"]; ok {
		fmt.Println("Choi의 나이:", val)
	} else {
		fmt.Println("Choi는 존재하지 않음")
	}

	// 존재하지 않는 키 → 제로 값 반환
	fmt.Println("없는 키 조회:", ages["없음"]) // 0

	// 4. 키 삭제
	delete(ages, "Park")
	fmt.Println("Park 삭제 후:", ages)

	// 5. 맵 순회 (순서 무작위)
	fmt.Print("순회: ")
	for k, v := range ages {
		fmt.Printf("%s=%d ", k, v)
	}
	fmt.Println()

	// 6. 맵 길이
	fmt.Println("맵 크기:", len(ages))

	// 7. nil 맵 주의
	var nilMap map[string]int
	fmt.Println("nil 맵 읽기:", nilMap["key"]) // 0 (안전)
	// nilMap["key"] = 1  // panic: assignment to entry in nil map

	// 8. 맵의 값으로 구조체 사용
	type Person struct {
		Name string
		Age  int
	}
	people := map[int]Person{
		1: {Name: "Kim", Age: 25},
		2: {Name: "Lee", Age: 30},
	}
	fmt.Println("people[1]:", people[1])

	// 9. 맵의 값으로 슬라이스 사용
	graph := make(map[string][]string)
	graph["A"] = append(graph["A"], "B", "C")
	graph["B"] = append(graph["B"], "A", "D")
	fmt.Println("그래프:", graph)

	// 10. 단어 빈도수 세기 예제
	words := []string{"go", "is", "great", "go", "is", "fun", "go"}
	freq := make(map[string]int)
	for _, w := range words {
		freq[w]++
	}
	fmt.Println("단어 빈도:", freq)
}
