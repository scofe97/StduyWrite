// Practice 02: 에코 서버
// 목표: 메시지 수신 후 그대로 반환

package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin:     func(r *http.Request) bool { return true },
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	log.Println("New client connected")

	for {
		// 메시지 읽기
		messageType, message, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Printf("Error: %v", err)
			}
			break
		}

		log.Printf("Received: %s", message)

		// 에코: 받은 메시지 그대로 반환
		echoMessage := fmt.Sprintf("Echo: %s", message)
		err = conn.WriteMessage(messageType, []byte(echoMessage))
		if err != nil {
			log.Println("Write error:", err)
			break
		}
	}

	log.Println("Client disconnected")
}

func main() {
	http.HandleFunc("/ws", echoHandler)

	fmt.Println("Echo server starting on :8080")
	fmt.Println("WebSocket endpoint: ws://localhost:8080/ws")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// 테스트:
// wscat -c ws://localhost:8080/ws
// > Hello
// < Echo: Hello
