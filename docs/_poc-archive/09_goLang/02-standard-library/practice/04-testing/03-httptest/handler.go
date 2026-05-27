package httptest_practice

import (
	"encoding/json"
	"net/http"
)

// 과제 3: HTTP 테스트
// UserHandler의 GetUser, CreateUser를 httptest로 테스트하세요.

// User 도메인 모델
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// CreateUserRequest 사용자 생성 요청
type CreateUserRequest struct {
	Name  string `json:"name"`
	Email string `json:"email"`
}

// ErrorResponse 에러 응답
type ErrorResponse struct {
	Error string `json:"error"`
}

// 인메모리 저장소 (테스트용)
var users = map[string]*User{
	"user-1": {ID: "user-1", Name: "John", Email: "john@example.com"},
	"user-2": {ID: "user-2", Name: "Jane", Email: "jane@example.com"},
}

// TODO: HealthHandler GET /health
// 응답: {"status": "healthy"}
func HealthHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: 구현
	// w.Header().Set("Content-Type", "application/json")
	// w.WriteHeader(http.StatusOK)
	// json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})

	w.WriteHeader(http.StatusNotImplemented)
}

// TODO: GetUserHandler GET /users/{id}
// 성공: 200 + User JSON
// 실패: 404 + ErrorResponse
func GetUserHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: 구현
	// 1. URL에서 id 추출 (r.PathValue("id") 또는 경로 파싱)
	// 2. users 맵에서 조회
	// 3. 없으면 404, 있으면 200 + JSON

	w.WriteHeader(http.StatusNotImplemented)
}

// TODO: CreateUserHandler POST /users
// 성공: 201 + User JSON
// 실패: 400 (잘못된 JSON 또는 필수 필드 누락)
func CreateUserHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: 구현
	// 1. 요청 본문 JSON 파싱
	// 2. 유효성 검증 (Name, Email 필수)
	// 3. ID 생성 및 저장
	// 4. 201 Created + 생성된 User 반환

	w.WriteHeader(http.StatusNotImplemented)
}

// 헬퍼: JSON 응답
func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// 헬퍼: 에러 응답
func respondError(w http.ResponseWriter, status int, message string) {
	respondJSON(w, status, ErrorResponse{Error: message})
}
