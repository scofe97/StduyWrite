package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
)

// Response는 JSON 응답 구조체입니다.
type Response struct {
	Success bool        `json:"success"`
	Data    interface{} `json:"data,omitempty"`
	Error   string      `json:"error,omitempty"`
}

// User는 사용자 모델입니다.
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// 임시 데이터 저장소
var users = map[string]User{
	"1": {ID: "1", Name: "John Doe", Email: "john@example.com"},
	"2": {ID: "2", Name: "Jane Doe", Email: "jane@example.com"},
}

// Home은 홈 페이지 핸들러입니다.
// TODO: 간단한 응답 반환
func Home(w http.ResponseWriter, r *http.Request) {
	// 힌트: JSON 응답 또는 텍스트 응답
	// w.Header().Set("Content-Type", "application/json")
	// json.NewEncoder(w).Encode(Response{Success: true, Data: "Welcome!"})
}

// Health는 헬스 체크 핸들러입니다.
// TODO: 서버 상태 반환
func Health(w http.ResponseWriter, r *http.Request) {
	// 힌트: status, timestamp 포함
}

// ListUsers는 사용자 목록을 반환합니다.
// TODO: 모든 사용자 반환
func ListUsers(w http.ResponseWriter, r *http.Request) {
	// 힌트: users map을 slice로 변환 후 반환
}

// GetUser는 특정 사용자를 반환합니다.
// TODO: URL 파라미터에서 ID 추출하여 사용자 반환
func GetUser(w http.ResponseWriter, r *http.Request) {
	// 힌트: id := chi.URLParam(r, "id")
	// 힌트: 사용자가 없으면 404 반환
}

// CreateUser는 새 사용자를 생성합니다.
// TODO: 요청 본문에서 사용자 정보 읽어 생성
func CreateUser(w http.ResponseWriter, r *http.Request) {
	// 힌트: json.NewDecoder(r.Body).Decode(&user)
	// 힌트: 생성 후 201 상태 코드 반환
}

// UpdateUser는 사용자 정보를 업데이트합니다.
// TODO: URL 파라미터와 요청 본문으로 사용자 업데이트
func UpdateUser(w http.ResponseWriter, r *http.Request) {
	// 힌트: ID는 URL에서, 데이터는 Body에서
}

// DeleteUser는 사용자를 삭제합니다.
// TODO: URL 파라미터에서 ID 추출하여 삭제
func DeleteUser(w http.ResponseWriter, r *http.Request) {
	// 힌트: delete(users, id)
	// 힌트: 삭제 후 204 No Content 반환
}

// GetPost는 slug로 게시글을 조회합니다.
// TODO: URL 파라미터에서 slug 추출
func GetPost(w http.ResponseWriter, r *http.Request) {
	// 힌트: slug := chi.URLParam(r, "slug")
}

// --- 유틸리티 함수 ---

// respondJSON은 JSON 응답을 보냅니다.
func respondJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(Response{Success: true, Data: data})
}

// respondError는 에러 응답을 보냅니다.
func respondError(w http.ResponseWriter, status int, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(Response{Success: false, Error: message})
}

// 임시: import 에러 방지
var _ = chi.URLParam
