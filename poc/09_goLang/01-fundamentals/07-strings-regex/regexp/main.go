package main

import (
	"fmt"
	"regexp"
)

func main() {
	input := "[workflow-api][TPS-1234] #time 2h feat: 기능"

	pattern := regexp.MustCompile(`(TPS|TQ|IGMU)-\d+`)

	result := pattern.FindString(input)

	fmt.Println(result) // TPS-1234 출력되어야 함
}
