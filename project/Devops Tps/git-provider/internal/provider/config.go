package provider

import "errors"

// ProviderType은 Git 프로바이더 종류를 나타냅니다.
type ProviderType string

const (
	GitHub    ProviderType = "github"
	GitLab    ProviderType = "gitlab"
	Bitbucket ProviderType = "bitbucket"
)

// 검증 에러들
var (
	ErrEmptyToken    = errors.New("token is required")
	ErrEmptyUsername = errors.New("username is required")
	ErrInvalidType   = errors.New("invalid provider type")
)

// ProviderConfig는 모든 프로바이더 설정이 구현해야 하는 인터페이스입니다.
//
// Go 인터페이스의 특징:
// - Java처럼 "implements" 키워드가 없음
// - 이 메서드들을 모두 구현하면 자동으로 ProviderConfig가 됨
// - "덕 타이핑": 오리처럼 걷고 꽥꽥거리면 오리다
type ProviderConfig interface {
	// GetType은 프로바이더 종류를 반환합니다.
	GetType() ProviderType

	// GetCredentials는 인증 정보를 반환합니다.
	// 각 프로바이더가 자신만의 방식으로 구현합니다.
	GetCredentials() Credentials

	// GetBaseURL은 API 기본 URL을 반환합니다.
	// - 공개 서비스: 빈 문자열 (기본값 사용)
	// - Self-hosted: 회사 서버 URL
	GetBaseURL() string

	// Validate는 설정이 유효한지 검증합니다.
	// 필수 값이 없으면 에러를 반환합니다.
	Validate() error
}
