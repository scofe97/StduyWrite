package main

import "fmt"

func main() {
	// === 슬라이스 (Slice) ===
	// 동적 크기, 배열의 "뷰"

	// 1. 슬라이스 생성 방법들
	// 리터럴
	nums := []int{1, 2, 3, 4, 5}
	fmt.Println("리터럴:", nums)

	// make 사용 (길이, 용량)
	s1 := make([]int, 3)     // len=3, cap=3
	s2 := make([]int, 3, 10) // len=3, cap=10
	fmt.Printf("make(3): len=%d cap=%d\n", len(s1), cap(s1))
	fmt.Printf("make(3,10): len=%d cap=%d\n", len(s2), cap(s2))

	// 2. 슬라이스는 배열의 뷰
	arr := [5]int{10, 20, 30, 40, 50}
	slice := arr[1:4] // [20, 30, 40]
	fmt.Println("원본 배열:", arr)
	fmt.Println("슬라이스 [1:4]:", slice)

	slice[0] = 200 // 원본도 변경됨!
	fmt.Println("슬라이스 수정 후 원본:", arr)

	// 3. 슬라이싱 문법
	data := []int{0, 1, 2, 3, 4, 5}
	fmt.Println("data[2:]:", data[2:])   // [2, 3, 4, 5]
	fmt.Println("data[:3]:", data[:3])   // [0, 1, 2]
	fmt.Println("data[1:4]:", data[1:4]) // [1, 2, 3]
	fmt.Println("data[:]:", data[:])     // 전체 복사

	// 4. append - 요소 추가
	items := []string{"a", "b"}
	items = append(items, "c")
	items = append(items, "d", "e")
	fmt.Println("append 후:", items)

	// 5. append로 용량 확장 확인
	grow := make([]int, 0, 2)
	fmt.Printf("초기: len=%d cap=%d\n", len(grow), cap(grow))
	grow = append(grow, 1, 2)
	fmt.Printf("2개 추가: len=%d cap=%d\n", len(grow), cap(grow))
	grow = append(grow, 3) // 용량 초과 → 재할당
	fmt.Printf("3개째 추가: len=%d cap=%d\n", len(grow), cap(grow))

	// 6. 슬라이스 복사
	src := []int{1, 2, 3}
	dst := make([]int, len(src))
	copy(dst, src)
	dst[0] = 100
	fmt.Println("원본:", src, "복사본:", dst)

	// 7. 슬라이스에서 요소 삭제
	del := []int{0, 1, 2, 3, 4}
	idx := 2 // 인덱스 2 삭제
	del = append(del[:idx], del[idx+1:]...)
	fmt.Println("인덱스 2 삭제:", del)

	// 8. nil 슬라이스 vs 빈 슬라이스
	var nilSlice []int
	emptySlice := []int{}
	fmt.Printf("nil 슬라이스: %v, nil=%v\n", nilSlice, nilSlice == nil)
	fmt.Printf("빈 슬라이스: %v, nil=%v\n", emptySlice, emptySlice == nil)
}
