package main

import (
	"encoding/json"
	"fmt"
	"time"
)

// 과제 3: 커스텀 시간 포맷
// MarshalJSON/UnmarshalJSON을 구현하여 "2024년 01월 15일" 형식의 날짜를 처리하는 타입을 만드세요.

// 한국어 날짜 포맷: "2024년 01월 15일"
const KoreanDateFormat = "2006년 01월 02일"

// TODO: 커스텀 시간 타입 정의
type KoreanDate struct {
	time.Time
}

// TODO: MarshalJSON 구현
// - time.Time을 "2024년 01월 15일" 형식의 JSON 문자열로 변환
// - 반환: []byte, error
func (kd KoreanDate) MarshalJSON() ([]byte, error) {
	// TODO:
	// 1. kd.Time을 KoreanDateFormat으로 포맷팅
	// 2. JSON 문자열 형태로 반환 (따옴표 포함: "2024년 01월 15일")
	// 힌트: fmt.Sprintf("\"%s\"", formatted) 또는 json.Marshal(formatted)
	return nil, fmt.Errorf("not implemented")
}

// TODO: UnmarshalJSON 구현
// - "2024년 01월 15일" 형식의 JSON 문자열을 time.Time으로 파싱
// - 입력: []byte (JSON 데이터)
// - 반환: error
func (kd *KoreanDate) UnmarshalJSON(data []byte) error {
	// TODO:
	// 1. data에서 따옴표 제거 (JSON 문자열이므로 따옴표 포함)
	// 2. time.Parse로 KoreanDateFormat 파싱
	// 3. kd.Time에 파싱된 시간 저장
	// 힌트: strings.Trim(string(data), "\"") 또는 json.Unmarshal
	return fmt.Errorf("not implemented")
}

// 이벤트 구조체 (KoreanDate 사용)
type Event struct {
	Name      string     `json:"name"`
	Date      KoreanDate `json:"date"`
	CreatedAt KoreanDate `json:"created_at"`
}

func main() {
	// TODO 1: 구조체 → JSON (Marshal 테스트)
	event := Event{
		Name:      "새해 첫 회의",
		Date:      KoreanDate{time.Date(2024, 1, 15, 0, 0, 0, 0, time.Local)},
		CreatedAt: KoreanDate{time.Now()},
	}

	// jsonBytes, err := json.MarshalIndent(event, "", "  ")
	// 예상 출력:
	// {
	//   "name": "새해 첫 회의",
	//   "date": "2024년 01월 15일",
	//   "created_at": "2024년 01월 26일"
	// }

	// TODO 2: JSON → 구조체 (Unmarshal 테스트)
	jsonStr := `{
		"name": "봄 세미나",
		"date": "2024년 03월 20일",
		"created_at": "2024년 01월 10일"
	}`
	_ = jsonStr

	// var parsedEvent Event
	// json.Unmarshal([]byte(jsonStr), &parsedEvent)
	// fmt.Printf("이벤트: %s, 날짜: %v\n", parsedEvent.Name, parsedEvent.Date.Format("2006-01-02"))

	// TODO 3: (선택) 여러 포맷 지원
	// UnmarshalJSON에서 여러 날짜 포맷을 시도하도록 확장
	// - "2024년 01월 15일"
	// - "2024-01-15"
	// - "2024/01/15"

	fmt.Println("TODO: 커스텀 시간 포맷 구현")
}
