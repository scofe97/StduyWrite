package main

import (
	"encoding/json"
	"fmt"
)

// 과제 4: 다형성 메시지 처리
// `type` 필드에 따라 다른 구조체로 파싱하는 메시지 시스템을 구현하세요.

// 테스트용 샘플 메시지들
var sampleMessages = []string{
	`{"type": "text", "payload": {"content": "안녕하세요!"}}`,
	`{"type": "image", "payload": {"url": "https://example.com/image.png", "width": 800, "height": 600}}`,
	`{"type": "file", "payload": {"filename": "document.pdf", "size": 1024000, "mime_type": "application/pdf"}}`,
	`{"type": "location", "payload": {"latitude": 37.5665, "longitude": 126.9780, "address": "서울특별시"}}`,
}

// 기본 메시지 구조체
// json.RawMessage를 사용하여 payload를 나중에 파싱
type Message struct {
	Type    string          `json:"type"`
	Payload json.RawMessage `json:"payload"` // 파싱 지연
}

// TODO: 각 메시지 타입별 Payload 구조체 정의

type TextPayload struct {
	// TODO: 필드 정의
}

type ImagePayload struct {
	// TODO: 필드 정의
}

type FilePayload struct {
	// TODO: 필드 정의
}

type LocationPayload struct {
	// TODO: 필드 정의
}

// TODO: 메시지 파싱 함수 구현
// - JSON 바이트를 받아서 적절한 타입의 Payload를 반환
// - 반환 타입: (interface{}, error)
func ParseMessage(data []byte) (interface{}, error) {
	// TODO:
	// 1. 먼저 Message 구조체로 파싱 (Type과 RawMessage만)
	// 2. msg.Type에 따라 switch-case로 분기
	// 3. 각 case에서 msg.Payload를 해당 타입으로 2차 파싱
	// 4. 알 수 없는 type이면 에러 반환

	return nil, fmt.Errorf("not implemented")
}

// TODO: 메시지 처리 함수 구현
// - 파싱된 메시지를 타입에 따라 다르게 처리
func HandleMessage(payload interface{}) {
	// TODO:
	// type switch 사용
	// switch p := payload.(type) {
	// case TextPayload:
	//     fmt.Printf("텍스트 메시지: %s\n", p.Content)
	// case ImagePayload:
	//     ...
	// }
}

func main() {
	fmt.Println("=== 다형성 메시지 처리 테스트 ===\n")

	for i, msgJSON := range sampleMessages {
		fmt.Printf("메시지 %d: %s\n", i+1, msgJSON)

		// TODO 1: ParseMessage로 파싱
		// payload, err := ParseMessage([]byte(msgJSON))

		// TODO 2: HandleMessage로 처리
		// HandleMessage(payload)

		fmt.Println()
	}

	// TODO 3: (선택) 메시지 생성 (역방향)
	// - TextPayload를 Message로 감싸서 JSON 생성
	// textPayload := TextPayload{Content: "반갑습니다!"}
	// payloadBytes, _ := json.Marshal(textPayload)
	// msg := Message{Type: "text", Payload: payloadBytes}
	// msgBytes, _ := json.Marshal(msg)

	// TODO 4: (선택) 알 수 없는 타입 처리
	// unknownMsg := `{"type": "unknown", "payload": {"data": "test"}}`

	fmt.Println("TODO: 다형성 메시지 처리 구현")
}
