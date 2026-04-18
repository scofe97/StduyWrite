// Practice 04: 채팅방 구현
// 목표: 이름 기반 메시지 전송 및 입장/퇴장 알림

package main

import (
	"encoding/json"
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

type Message struct {
	Type    string `json:"type"` // "join", "leave", "message"
	Name    string `json:"name"`
	Content string `json:"content,omitempty"`
}

type Client struct {
	conn *websocket.Conn
	name string
}

type ChatRoom struct {
	clients map[*websocket.Conn]*Client
	mu      sync.RWMutex
}

func NewChatRoom() *ChatRoom {
	return &ChatRoom{
		clients: make(map[*websocket.Conn]*Client),
	}
}

func (r *ChatRoom) Join(conn *websocket.Conn, name string) {
	r.mu.Lock()
	r.clients[conn] = &Client{conn: conn, name: name}
	r.mu.Unlock()

	r.Broadcast(Message{Type: "join", Name: name, Content: "joined the chat"})
}

func (r *ChatRoom) Leave(conn *websocket.Conn) {
	r.mu.Lock()
	client, ok := r.clients[conn]
	if ok {
		delete(r.clients, conn)
	}
	r.mu.Unlock()

	if ok {
		r.Broadcast(Message{Type: "leave", Name: client.name, Content: "left the chat"})
	}
}

func (r *ChatRoom) Broadcast(msg Message) {
	data, _ := json.Marshal(msg)
	r.mu.RLock()
	defer r.mu.RUnlock()

	for _, client := range r.clients {
		client.conn.WriteMessage(websocket.TextMessage, data)
	}
}

var chatRoom = NewChatRoom()

func wsHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("Upgrade error:", err)
		return
	}
	defer conn.Close()

	// 첫 메시지로 이름 수신
	var joinMsg Message
	if err := conn.ReadJSON(&joinMsg); err != nil || joinMsg.Type != "join" {
		log.Println("Expected join message")
		return
	}

	chatRoom.Join(conn, joinMsg.Name)
	defer chatRoom.Leave(conn)

	// 메시지 수신 루프
	for {
		var msg Message
		if err := conn.ReadJSON(&msg); err != nil {
			break
		}

		if msg.Type == "message" {
			msg.Name = joinMsg.Name
			chatRoom.Broadcast(msg)
		}
	}
}

func main() {
	http.HandleFunc("/ws", wsHandler)

	fmt.Println("Chat server starting on :8080")
	fmt.Println("WebSocket endpoint: ws://localhost:8080/ws")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

// 테스트 (JavaScript):
// const ws = new WebSocket('ws://localhost:8080/ws');
// ws.onmessage = (e) => console.log(JSON.parse(e.data));
// ws.onopen = () => ws.send(JSON.stringify({type: 'join', name: 'Alice'}));
// ws.send(JSON.stringify({type: 'message', content: 'Hello!'}));
