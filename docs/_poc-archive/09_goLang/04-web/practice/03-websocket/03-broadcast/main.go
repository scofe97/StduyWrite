// Practice 03: 브로드캐스트
// 목표: 모든 연결된 클라이언트에게 메시지 전송

package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin:     func(r *http.Request) bool { return true },
}

// 연결된 클라이언트 관리
type Hub struct {
	clients map[*websocket.Conn]bool
	mu      sync.RWMutex
}

func NewHub() *Hub {
	return &Hub{
		clients: make(map[*websocket.Conn]bool),
	}
}

func (h *Hub) AddClient(conn *websocket.Conn) {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.clients[conn] = true
	log.Printf("Client added. Total: %d", len(h.clients))
}

func (h *Hub) RemoveClient(conn *websocket.Conn) {
	h.mu.Lock()
	defer h.mu.Unlock()
	delete(h.clients, conn)
	log.Printf("Client removed. Total: %d", len(h.clients))
}

func (h *Hub) Broadcast(message []byte) {
	h.mu.RLock()
	defer h.mu.RUnlock()
	for conn := range h.clients {
		err := conn.WriteMessage(websocket.TextMessage, message)
		if err != nil {
			log.Printf("Broadcast error: %v", err)
		}
	}
}

var hub = NewHub()

func wsHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	hub.AddClient(conn)
	defer hub.RemoveClient(conn)

	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			break
		}

		// 모든 클라이언트에게 브로드캐스트
		log.Printf("Broadcasting: %s", message)
		hub.Broadcast(message)
	}
}

func main() {
	http.HandleFunc("/ws", wsHandler)

	fmt.Println("Broadcast server starting on :8080")
	fmt.Println("WebSocket endpoint: ws://localhost:8080/ws")
	fmt.Println("Open multiple clients to test broadcasting")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// 테스트: 여러 터미널에서 연결
// Terminal 1: wscat -c ws://localhost:8080/ws
// Terminal 2: wscat -c ws://localhost:8080/ws
// Terminal 1> Hello  → 모든 터미널에서 수신
