package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"
)

// ============================================
// 이벤트 타입 정의
// ============================================

type NotificationEvent struct {
	Message string `json:"message"`
	Level   string `json:"level"`
	Time    string `json:"time"`
}

type UpdateEvent struct {
	Type string      `json:"type"`
	Data interface{} `json:"data"`
	Time string      `json:"time"`
}

type AlertEvent struct {
	Title   string `json:"title"`
	Message string `json:"message"`
	Urgency string `json:"urgency"`
	Time    string `json:"time"`
}

// ch04: 이벤트 스토어 (Last-Event-ID 지원)
type StoredEvent struct {
	ID       int    `json:"id"`
	Data     string `json:"data"`
	Time     string `json:"timestamp"`
	Sequence int    `json:"sequence"`
}

var (
	eventStore   []StoredEvent
	eventStoreMu sync.RWMutex
	eventSeq     int
)

func main() {
	// ch02 엔드포인트
	http.HandleFunc("/events/basic", handleBasicEvents)
	http.HandleFunc("/events/auth", handleAuthEvents)
	http.HandleFunc("/events/multi", handleMultiTypeEvents)

	// ch03 엔드포인트
	http.HandleFunc("/events/custom", handleCustomEvents)
	http.HandleFunc("/events/custom-auth", handleCustomEventsWithAuth)

	// ch04 엔드포인트
	http.HandleFunc("/events/reconnect", handleReconnectEvents)

	// ch05 엔드포인트
	http.HandleFunc("/events/unreliable", handleUnreliableEvents)
	http.HandleFunc("/events/heartbeat", handleHeartbeatEvents)
	http.HandleFunc("/api/polling", handlePolling)

	// ch06 엔드포인트
	http.HandleFunc("/events/cleanup-test", handleCleanupTest)

	// ch08 엔드포인트
	http.HandleFunc("/api/queue", handleQueuePolling)

	fmt.Println("============================================")
	fmt.Println("SSE 통합 서버 시작: http://localhost:3001")
	fmt.Println("============================================")
	fmt.Println("")
	fmt.Println("ch02 엔드포인트:")
	fmt.Println("  /events/basic      - 기본 SSE")
	fmt.Println("  /events/auth       - 인증 SSE")
	fmt.Println("  /events/multi      - 멀티 타입 이벤트")
	fmt.Println("")
	fmt.Println("ch03 엔드포인트:")
	fmt.Println("  /events/custom     - 커스텀 이벤트")
	fmt.Println("  /events/custom-auth - 인증 커스텀 이벤트")
	fmt.Println("")
	fmt.Println("ch04 엔드포인트:")
	fmt.Println("  /events/reconnect  - Last-Event-ID + retry")
	fmt.Println("")
	fmt.Println("ch05 엔드포인트:")
	fmt.Println("  /events/unreliable - 간헐적 에러 서버")
	fmt.Println("  /events/heartbeat  - heartbeat 서버")
	fmt.Println("  /api/polling       - fallback polling")
	fmt.Println("")
	fmt.Println("ch06 엔드포인트:")
	fmt.Println("  /events/cleanup-test - cleanup 테스트")
	fmt.Println("")
	fmt.Println("ch08 엔드포인트:")
	fmt.Println("  /api/queue           - 어댑티브 폴링 대기열")
	fmt.Println("============================================")

	log.Fatal(http.ListenAndServe(":3001", nil))
}

// ============================================
// 공통
// ============================================

func setupSSEHeaders(w http.ResponseWriter) {
	w.Header().Set("Content-Type", "text/event-stream")
	w.Header().Set("Cache-Control", "no-cache")
	w.Header().Set("Connection", "keep-alive")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Access-Control-Allow-Headers", "Authorization, Content-Type, Last-Event-ID")
}

func sendSSEEvent(w http.ResponseWriter, flusher http.Flusher, eventType string, data interface{}) {
	jsonData, _ := json.Marshal(data)
	if eventType != "" {
		fmt.Fprintf(w, "event: %s\n", eventType)
	}
	fmt.Fprintf(w, "data: %s\n\n", jsonData)
	flusher.Flush()
}

func sendSSEEventWithID(w http.ResponseWriter, flusher http.Flusher, id int, eventType string, data interface{}) {
	jsonData, _ := json.Marshal(data)
	fmt.Fprintf(w, "id: %d\n", id)
	if eventType != "" {
		fmt.Fprintf(w, "event: %s\n", eventType)
	}
	fmt.Fprintf(w, "data: %s\n\n", jsonData)
	flusher.Flush()
}

// ============================================
// Ch02: 기본 SSE
// ============================================

func handleBasicEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/basic] 클라이언트 연결")
	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/basic] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			data := map[string]interface{}{
				"count": count,
				"time":  t.Format("15:04:05"),
				"type":  "basic",
			}
			sendSSEEvent(w, flusher, "", data)
		}
	}
}

func handleAuthEvents(w http.ResponseWriter, r *http.Request) {
	authHeader := r.Header.Get("Authorization")
	if authHeader != "" {
		log.Printf("[/events/auth] Authorization: %s\n", authHeader)
	}

	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/auth] 클라이언트 연결")
	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/auth] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			data := map[string]interface{}{
				"count":         count,
				"time":          t.Format("15:04:05"),
				"authenticated": authHeader != "",
			}
			sendSSEEvent(w, flusher, "", data)
		}
	}
}

func handleMultiTypeEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/multi] 클라이언트 연결")
	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/multi] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			timeStr := t.Format("15:04:05")
			switch count % 4 {
			case 1:
				sendSSEEvent(w, flusher, "", map[string]string{"msg": "기본 메시지", "time": timeStr})
			case 2:
				sendSSEEvent(w, flusher, "notification", map[string]string{"title": "알림!", "body": "새 메시지 도착", "time": timeStr})
			case 3:
				sendSSEEvent(w, flusher, "heartbeat", map[string]string{"status": "alive", "time": timeStr})
			case 0:
				sendSSEEvent(w, flusher, "user-action", map[string]string{"action": "login", "userId": "user123", "time": timeStr})
			}
		}
	}
}

// ============================================
// Ch03: 커스텀 이벤트
// ============================================

func handleCustomEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/custom] 클라이언트 연결")
	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/custom] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			sendRandomCustomEvent(w, flusher, t, count, "")
		}
	}
}

func handleCustomEventsWithAuth(w http.ResponseWriter, r *http.Request) {
	authHeader := r.Header.Get("Authorization")
	if authHeader == "" {
		http.Error(w, "Authorization header required", http.StatusUnauthorized)
		return
	}
	if !strings.HasPrefix(authHeader, "Bearer ") {
		http.Error(w, "Bearer token required", http.StatusUnauthorized)
		return
	}

	token := strings.TrimPrefix(authHeader, "Bearer ")
	log.Printf("[/events/custom-auth] 토큰: %s\n", token)

	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/custom-auth] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			sendRandomCustomEvent(w, flusher, t, count, token)
		}
	}
}

func sendRandomCustomEvent(w http.ResponseWriter, flusher http.Flusher, t time.Time, count int, token string) {
	timeStr := t.Format("15:04:05")
	switch count % 4 {
	case 0:
		sendSSEEvent(w, flusher, "notification", NotificationEvent{
			Message: fmt.Sprintf("알림 #%d: 새로운 메시지가 도착했습니다", count),
			Level:   []string{"info", "warning", "success"}[rand.Intn(3)],
			Time:    timeStr,
		})
	case 1:
		sendSSEEvent(w, flusher, "update", UpdateEvent{
			Type: "metrics",
			Data: map[string]interface{}{
				"cpu":    30 + rand.Intn(50),
				"memory": 40 + rand.Intn(40),
				"disk":   20 + rand.Intn(60),
			},
			Time: timeStr,
		})
	case 2:
		sendSSEEvent(w, flusher, "alert", AlertEvent{
			Title:   fmt.Sprintf("경고 #%d", count),
			Message: "시스템 리소스 사용량이 높습니다",
			Urgency: []string{"low", "medium", "high"}[rand.Intn(3)],
			Time:    timeStr,
		})
	case 3:
		data := map[string]interface{}{
			"text": fmt.Sprintf("일반 메시지 #%d", count),
			"time": timeStr,
		}
		if token != "" {
			data["authenticated"] = true
		}
		sendSSEEvent(w, flusher, "", data)
	}
}

// ============================================
// Ch04: Reconnection + Last-Event-ID
// ============================================

func handleReconnectEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	// retry 간격 설정 (3초)
	fmt.Fprintf(w, "retry: 3000\n\n")
	flusher.Flush()

	// Last-Event-ID 확인
	lastID := r.Header.Get("Last-Event-ID")
	startFrom := 0
	if lastID != "" {
		if id, err := strconv.Atoi(lastID); err == nil {
			startFrom = id
			log.Printf("[/events/reconnect] 재연결! Last-Event-ID: %d\n", id)

			// 놓친 이벤트 전송
			eventStoreMu.RLock()
			for _, event := range eventStore {
				if event.ID > id {
					sendSSEEventWithID(w, flusher, event.ID, "update", event)
				}
			}
			eventStoreMu.RUnlock()
		}
	}

	log.Printf("[/events/reconnect] 클라이언트 연결 (startFrom=%d)\n", startFrom)

	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/reconnect] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			eventStoreMu.Lock()
			eventSeq++
			event := StoredEvent{
				ID:       eventSeq,
				Data:     fmt.Sprintf("이벤트 데이터 #%d", eventSeq),
				Time:     t.Format("15:04:05"),
				Sequence: eventSeq,
			}
			eventStore = append(eventStore, event)
			// 최대 100개만 유지
			if len(eventStore) > 100 {
				eventStore = eventStore[len(eventStore)-100:]
			}
			eventStoreMu.Unlock()

			sendSSEEventWithID(w, flusher, event.ID, "update", event)
		}
	}
}

// ============================================
// Ch05: Error Handling (Unreliable Server)
// ============================================

func handleUnreliableEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/unreliable] 클라이언트 연결")

	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/unreliable] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++

			// 10번째 이벤트마다 강제 연결 종료 (에러 시뮬레이션)
			if count%10 == 0 {
				log.Printf("[/events/unreliable] 의도적 연결 종료 (count=%d)\n", count)
				return
			}

			data := map[string]interface{}{
				"id":        count,
				"data":      fmt.Sprintf("메시지 #%d", count),
				"timestamp": t.Format("15:04:05"),
			}
			sendSSEEvent(w, flusher, "update", data)
		}
	}
}

func handleHeartbeatEvents(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/heartbeat] 클라이언트 연결")

	ctx := r.Context()
	dataTicker := time.NewTicker(3 * time.Second)
	heartbeatTicker := time.NewTicker(10 * time.Second)
	defer dataTicker.Stop()
	defer heartbeatTicker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/heartbeat] 클라이언트 연결 종료")
			return
		case t := <-dataTicker.C:
			count++
			data := map[string]interface{}{
				"id":        count,
				"data":      fmt.Sprintf("데이터 #%d", count),
				"timestamp": t.Format("15:04:05"),
			}
			sendSSEEvent(w, flusher, "update", data)
		case t := <-heartbeatTicker.C:
			sendSSEEvent(w, flusher, "heartbeat", map[string]string{
				"status": "alive",
				"time":   t.Format("15:04:05"),
			})
		}
	}
}

func handlePolling(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	data := map[string]interface{}{
		"id":        rand.Intn(1000),
		"data":      "Polling fallback 데이터",
		"timestamp": time.Now().Format("15:04:05"),
		"source":    "polling",
	}
	json.NewEncoder(w).Encode(data)
}

// ============================================
// Ch08: Adaptive Polling (대기열 시뮬레이션)
// ============================================

type QueueResponse struct {
	Position int    `json:"position"`
	Total    int    `json:"total"`
	TTL      int    `json:"ttl"`
	Redirect string `json:"redirect,omitempty"`
}

var (
	queuePositions   = make(map[string]int)
	queuePositionsMu sync.Mutex
	queueTotal       = 5000
)

func handleQueuePolling(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	token := r.URL.Query().Get("token")
	if token == "" {
		http.Error(w, `{"error":"token required"}`, http.StatusBadRequest)
		return
	}

	queuePositionsMu.Lock()
	pos, exists := queuePositions[token]
	if !exists {
		// 새 토큰: 랜덤 위치 배정
		pos = 100 + rand.Intn(4900)
		queuePositions[token] = pos
		log.Printf("[/api/queue] 새 토큰 %s → 위치 %d\n", token, pos)
	} else {
		// 기존 토큰: 위치 감소 (입장 시뮬레이션)
		decrease := 10 + rand.Intn(40) // 10~50명씩 줄어듦
		pos -= decrease
		if pos < 0 {
			pos = 0
		}
		queuePositions[token] = pos
	}
	queuePositionsMu.Unlock()

	// 입장 가능
	if pos == 0 {
		log.Printf("[/api/queue] 토큰 %s 입장!\n", token)
		json.NewEncoder(w).Encode(QueueResponse{
			Position: 0,
			Total:    queueTotal,
			TTL:      0,
			Redirect: "/booking",
		})
		return
	}

	// 위치에 따라 TTL 동적 조절
	ttl := calculateQueueTTL(pos)

	json.NewEncoder(w).Encode(QueueResponse{
		Position: pos,
		Total:    queueTotal,
		TTL:      ttl,
	})
}

func calculateQueueTTL(position int) int {
	switch {
	case position <= 10:
		return 500 // 0.5초 (곧 입장)
	case position <= 100:
		return 2000 // 2초
	case position <= 1000:
		return 5000 // 5초
	case position <= 3000:
		return 10000 // 10초
	default:
		return 15000 // 15초
	}
}

// ============================================
// Ch06: Cleanup Test
// ============================================

func handleCleanupTest(w http.ResponseWriter, r *http.Request) {
	setupSSEHeaders(w)
	flusher, ok := w.(http.Flusher)
	if !ok {
		http.Error(w, "Streaming not supported", http.StatusInternalServerError)
		return
	}

	log.Println("[/events/cleanup-test] 클라이언트 연결")

	ctx := r.Context()
	ticker := time.NewTicker(2 * time.Second)
	defer ticker.Stop()

	count := 0
	for {
		select {
		case <-ctx.Done():
			log.Println("[/events/cleanup-test] 클라이언트 연결 종료")
			return
		case t := <-ticker.C:
			count++
			data := map[string]interface{}{
				"id":        count,
				"data":      fmt.Sprintf("cleanup 테스트 메시지 #%d", count),
				"timestamp": t.Format("15:04:05"),
			}
			sendSSEEvent(w, flusher, "update", data)
		}
	}
}
