package main

import "fmt"

// 1. 구조체 정의
type Person struct {
	Name string
	Age  int
}

// 2. 메서드 정의
func (p Person) Greet() string {
	return fmt.Sprintf("안녕하세요, 저는 %s입니다.", p.Name)
}

// 포인터 리시버 - 값 수정 가능
func (p *Person) Birthday() {
	p.Age++
}

// 3. 구조체 임베딩 (상속 대신 조합)
type Employee struct {
	Person  // 임베딩
	Company string
	Salary  int
}

// 4. 인터페이스 정의
type Greeter interface {
	Greet() string
}

func main() {
	// === 구조체 (Struct) ===

	// 5. 구조체 생성
	// 필드 순서대로
	p1 := Person{"Kim", 25}
	fmt.Println("p1:", p1)

	// 필드명 지정 (권장)
	p2 := Person{Name: "Lee", Age: 30}
	fmt.Println("p2:", p2)

	// 포인터로 생성
	p3 := &Person{Name: "Park", Age: 28}
	fmt.Println("p3:", p3)

	// new 사용 (제로 값)
	p4 := new(Person)
	p4.Name = "Choi"
	p4.Age = 35
	fmt.Println("p4:", p4)

	// 6. 필드 접근
	fmt.Println("이름:", p2.Name, "나이:", p2.Age)

	// 7. 메서드 호출
	fmt.Println(p2.Greet())

	// 포인터 리시버 메서드
	fmt.Println("생일 전:", p2.Age)
	p2.Birthday()
	fmt.Println("생일 후:", p2.Age)

	// 8. 구조체 임베딩
	emp := Employee{
		Person:  Person{Name: "Jung", Age: 32},
		Company: "ABC Corp",
		Salary:  50000,
	}
	// 임베딩된 필드 직접 접근
	fmt.Println("직원 이름:", emp.Name) // emp.Person.Name과 동일
	fmt.Println("회사:", emp.Company)
	// 임베딩된 메서드도 직접 호출
	fmt.Println(emp.Greet())

	// 9. 인터페이스 구현 (암시적)
	var g Greeter = p2
	fmt.Println("인터페이스 통해:", g.Greet())

	// 10. 익명 구조체
	point := struct {
		X, Y int
	}{X: 10, Y: 20}
	fmt.Println("익명 구조체:", point)

	// 11. 구조체 비교
	a := Person{Name: "Kim", Age: 25}
	b := Person{Name: "Kim", Age: 25}
	fmt.Println("a == b:", a == b)

	// 12. 구조체 복사 (값 타입)
	original := Person{Name: "Original", Age: 20}
	copied := original
	copied.Name = "Copied"
	fmt.Println("원본:", original.Name, "복사본:", copied.Name)

	// 13. 태그 (JSON 등에서 사용)
	type User struct {
		ID       int    `json:"id"`
		Username string `json:"username"`
		Password string `json:"-"` // JSON 제외
	}
	u := User{ID: 1, Username: "gopher", Password: "secret"}
	fmt.Printf("User: %+v\n", u)
}
