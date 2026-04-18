package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"
)

// 과제 4: 요청 추적 미들웨어
// 요청 ID를 생성하여 Context에 저장하고, 모든 로그에 요청 ID가 포함되도록 미들웨어를 구현하세요.

// TODO: Context 키 타입 정의 (타입 안전성)
type contextKey string

const (
	requestIDKey contextKey = "requestID"
	userIDKey    contextKey = "userID"
)

// TODO: 요청 ID 저장 헬퍼
func WithRequestID(ctx context.Context, requestID string) context.Context {
	// TODO: context.WithValue 사용
	return ctx
}

// TODO: 요청 ID 조회 헬퍼
func GetRequestID(ctx context.Context) string {
	// TODO: ctx.Value로 조회, 타입 단언
	return ""
}

// TODO: 사용자 ID 저장 헬퍼
func WithUserID(ctx context.Context, userID string) context.Context {
	return ctx
}

// TODO: 사용자 ID 조회 헬퍼
func GetUserID(ctx context.Context) string {
	return ""
}

// TODO: Context 정보를 포함한 로깅 함수
func LogWithContext(ctx context.Context, msg string) {
	// TODO:
	// requestID와 userID를 추출하여 로그에 포함
	// 형식: [req-xxx] [user-yyy] 메시지
	log.Println(msg)
}

// TODO: 요청 ID 생성 미들웨어
// - 고유한 요청 ID 생성 (UUID 또는 타임스탬프 기반)
// - Context에 요청 ID 저장
// - 응답 헤더에 요청 ID 추가
func RequestIDMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// TODO:
		// 1. 요청 ID 생성 (간단히 타임스탬프 사용)
		// 2. context.WithValue로 저장
		// 3. 응답 헤더에 X-Request-ID 추가
		// 4. r.WithContext(ctx)로 새 context 전달
		// 5. next.ServeHTTP(w, r.WithContext(ctx))

		next.ServeHTTP(w, r)
	})
}

// TODO: 인증 미들웨어 (시뮬레이션)
// - Authorization 헤더에서 사용자 ID 추출 (간단히 헤더 값 사용)
// - Context에 사용자 ID 저장
func AuthMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// TODO:
		// 1. Authorization 헤더 확인
		// 2. 사용자 ID를 context에 저장
		// 3. next.ServeHTTP 호출

		next.ServeHTTP(w, r)
	})
}

// 핸들러 예제
func homeHandler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	LogWithContext(ctx, "홈 페이지 요청")

	// 하위 함수에서도 동일한 context 사용
	processRequest(ctx)

	fmt.Fprintf(w, "Hello! Request ID: %s\n", GetRequestID(ctx))
}

func processRequest(ctx context.Context) {
	LogWithContext(ctx, "요청 처리 시작")

	// 데이터베이스 조회 시뮬레이션
	fetchData(ctx)

	LogWithContext(ctx, "요청 처리 완료")
}

func fetchData(ctx context.Context) {
	LogWithContext(ctx, "데이터 조회 중...")
	time.Sleep(100 * time.Millisecond)
	LogWithContext(ctx, "데이터 조회 완료")
}

func userHandler(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	LogWithContext(ctx, "사용자 정보 요청")

	userID := GetUserID(ctx)
	if userID == "" {
		http.Error(w, "인증 필요", http.StatusUnauthorized)
		return
	}

	fmt.Fprintf(w, "User ID: %s, Request ID: %s\n", userID, GetRequestID(ctx))
}

func main() {
	fmt.Println("=== 요청 추적 미들웨어 테스트 ===\n")

	// TODO: 미들웨어 체인 구성
	mux := http.NewServeMux()
	mux.HandleFunc("/", homeHandler)
	mux.HandleFunc("/user", userHandler)

	// TODO: 미들웨어 적용
	// handler := RequestIDMiddleware(AuthMiddleware(mux))

	// 미들웨어 없는 버전 (TODO 완료 후 위 라인으로 교체)
	handler := http.Handler(mux)

	server := &http.Server{
		Addr:    ":8080",
		Handler: handler,
	}

	fmt.Println("서버 시작: http://localhost:8080")
	fmt.Println("\n테스트 방법:")
	fmt.Println("  curl http://localhost:8080/")
	fmt.Println("  curl -H 'Authorization: user-123' http://localhost:8080/user")
	fmt.Println("\n서버 로그에서 요청 ID가 모든 로그에 포함되는지 확인")

	// TODO: 서버 시작 (주석 해제)
	// log.Fatal(server.ListenAndServe())

	_ = server
	fmt.Println("\nTODO: 요청 추적 미들웨어 구현")
}

// 힌트:
// 1. 요청 ID 생성: fmt.Sprintf("req-%d", time.Now().UnixNano())
// 2. UUID 사용: github.com/google/uuid 패키지
// 3. 미들웨어 체인: RequestIDMiddleware(AuthMiddleware(handler))
// 4. 응답 헤더 추가: w.Header().Set("X-Request-ID", requestID)
