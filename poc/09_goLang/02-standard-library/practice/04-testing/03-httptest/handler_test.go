package httptest_practice

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// 과제 3: HTTP 테스트
// httptest 패키지로 HTTP 핸들러 테스트

func TestHealthHandler(t *testing.T) {
	// TODO: 헬스 체크 테스트
	// 1. 요청 생성
	// req := httptest.NewRequest("GET", "/health", nil)

	// 2. ResponseRecorder 생성
	// rec := httptest.NewRecorder()

	// 3. 핸들러 호출
	// HealthHandler(rec, req)

	// 4. 검증
	// assert.Equal(t, http.StatusOK, rec.Code)
	// assert.Contains(t, rec.Body.String(), "healthy")
	// assert.Equal(t, "application/json", rec.Header().Get("Content-Type"))

	t.Skip("TODO: 구현 필요")
}

func TestGetUserHandler_Success(t *testing.T) {
	// TODO: 사용자 조회 성공 테스트
	// 존재하는 사용자 ID로 요청

	t.Skip("TODO: 구현 필요")
}

func TestGetUserHandler_NotFound(t *testing.T) {
	// TODO: 사용자 없음 테스트
	// 존재하지 않는 ID로 요청 → 404

	t.Skip("TODO: 구현 필요")
}

func TestCreateUserHandler_Success(t *testing.T) {
	// TODO: 사용자 생성 성공 테스트
	// body := `{"name": "Alice", "email": "alice@example.com"}`
	// req := httptest.NewRequest("POST", "/users", strings.NewReader(body))
	// req.Header.Set("Content-Type", "application/json")
	// rec := httptest.NewRecorder()
	// CreateUserHandler(rec, req)
	// assert.Equal(t, http.StatusCreated, rec.Code)

	t.Skip("TODO: 구현 필요")
}

func TestCreateUserHandler_InvalidJSON(t *testing.T) {
	// TODO: 잘못된 JSON 테스트 → 400
	// body := `{invalid json}`

	t.Skip("TODO: 구현 필요")
}

func TestCreateUserHandler_MissingFields(t *testing.T) {
	// TODO: 필수 필드 누락 테스트 → 400
	// body := `{"name": ""}` // email 누락

	t.Skip("TODO: 구현 필요")
}

// 테스트 서버를 사용한 클라이언트 테스트 예제
func TestWithTestServer(t *testing.T) {
	// TODO: httptest.NewServer 사용
	// server := httptest.NewServer(http.HandlerFunc(HealthHandler))
	// defer server.Close()

	// resp, err := http.Get(server.URL)
	// require.NoError(t, err)
	// assert.Equal(t, http.StatusOK, resp.StatusCode)

	t.Skip("TODO: 구현 필요")
}

// 힌트:
// - httptest.NewRequest(method, url, body)
// - httptest.NewRecorder()
// - httptest.NewServer(handler)
// - rec.Code, rec.Body.String(), rec.Header()

// 실행: go test -v ./practices/03-httptest/

// import 확인용
var _ = strings.NewReader
var _ = http.StatusOK
var _ = httptest.NewRequest
var _ = assert.Equal
var _ = require.NoError
