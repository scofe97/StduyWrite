// Practice 01: 기본 WebSocket 연결
// 목표: HTTP → WebSocket 업그레이드 이해

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
	// 개발용: CORS 허용
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
	// HTTP → WebSocket 업그레이드
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	log.Println("Client connected")

	// 연결 환영 메시지
	err = conn.WriteMessage(websocket.TextMessage, []byte("Welcome to WebSocket!"))
	if err != nil {
		log.Println("Write error:", err)
		return
	}

	// 메시지 수신 대기
	for {
		messageType, p, err := conn.ReadMessage()
		if err != nil {
			log.Println("Read error:", err)
			return
		}
		log.Printf("Received: %s (type: %d)", p, messageType)
	}
}

func main() {
	http.HandleFunc("/ws", wsHandler)
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.ServeFile(w, r, "index.html")
	})

	fmt.Println("Server starting on :8080")
	fmt.Println("WebSocket endpoint: ws://localhost:8080/ws")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// go mod init ws-practice
// go get github.com/gorilla/websocket
// go run main.go
//
// 테스트 (JavaScript):
// const ws = new WebSocket('ws://localhost:8080/ws');
// ws.onmessage = (e) => console.log(e.data);
// ws.send('Hello');
