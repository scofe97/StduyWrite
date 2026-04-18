package provider

import (
	"encoding/base64"
	"net/http"
)

// Credentials는 인증 정보 인터페이스입니다.
//
// 왜 인터페이스로 바꿨나요?
// - 각 프로바이더마다 인증 방식이 다름
// - GitHub: Bearer Token
// - Bitbucket: Basic Auth (username:password)
// - 새 프로바이더가 다른 방식을 쓴다면? 구현만 추가하면 됨
type Credentials interface {
	// ApplyAuth는 HTTP 요청에 인증 정보를 적용합니다.
	// 각 프로바이더가 자신만의 방식으로 구현합니다.
	ApplyAuth(req *http.Request)

	// GetAuthType은 인증 방식을 반환합니다. (디버깅/로깅용)
	GetAuthType() string
}

// -----------------------------------------------------------
// TokenCredentials: Token 기반 인증 (GitHub, GitLab 등)
// -----------------------------------------------------------

// TokenCredentials는 Bearer Token 인증을 구현합니다.
type TokenCredentials struct {
	Token string
}

// ApplyAuth는 Bearer Token을 요청 헤더에 추가합니다.
// Authorization: Bearer <token>
func (c *TokenCredentials) ApplyAuth(req *http.Request) {
	req.Header.Set("Authorization", "Bearer "+c.Token)
}

func (c *TokenCredentials) GetAuthType() string {
	return "bearer_token"
}

// 컴파일 타임 인터페이스 확인
var _ Credentials = (*TokenCredentials)(nil)

// -----------------------------------------------------------
// BasicCredentials: Basic Auth 인증 (Bitbucket)
// -----------------------------------------------------------

// BasicCredentials는 Basic Auth 인증을 구현합니다.
// username:password를 Base64로 인코딩합니다.
type BasicCredentials struct {
	Username string
	Password string // Bitbucket의 경우 App Password
}

// ApplyAuth는 Basic Auth를 요청 헤더에 추가합니다.
// Authorization: Basic base64(username:password)
func (c *BasicCredentials) ApplyAuth(req *http.Request) {
	auth := c.Username + ":" + c.Password
	encoded := base64.StdEncoding.EncodeToString([]byte(auth))
	req.Header.Set("Authorization", "Basic "+encoded)
}

func (c *BasicCredentials) GetAuthType() string {
	return "basic_auth"
}

// 컴파일 타임 인터페이스 확인
var _ Credentials = (*BasicCredentials)(nil)
